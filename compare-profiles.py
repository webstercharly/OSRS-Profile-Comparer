import re, os, json, sys
from datetime import datetime

FILE1_PLACEHOLDER = "{{FIRST}}"
FILE2_PLACEHOLDER = "{{SECOND}}"

def normalize_path(path):
    return os.path.normpath(path)

def compare_json_objects(obj1, obj2, path=""):
    MISSING_KEYS_FIRST = f"Missing Keys in {FILE1_PLACEHOLDER}"
    MISSING_KEYS_SECOND = f"Missing Keys in {FILE2_PLACEHOLDER}"
    DIVERGENT_VALUES = f"Divergent Values {FILE1_PLACEHOLDER} vs {FILE2_PLACEHOLDER}"
    differences = {
      MISSING_KEYS_FIRST: [],
      MISSING_KEYS_SECOND: [],
      DIVERGENT_VALUES: []
    }

    if isinstance(obj1, dict) and isinstance(obj2, dict):
        union_keys = set(obj1).union(obj2)
        for key in union_keys:
            new_path = f"{path}/{key}" if path else key
            if new_path == 'tasks':
              tasks1_list = parse_string_to_list(obj1[new_path])
              tasks2_list = parse_string_to_list(obj2[new_path])
              added = set(tasks2_list) - set(tasks1_list)
              removed = set(tasks1_list) - set(tasks2_list)
              differences[MISSING_KEYS_SECOND].extend(added)
              differences[MISSING_KEYS_FIRST].extend(removed)
            elif key not in obj1:
                differences[MISSING_KEYS_FIRST].append(f"{new_path}: {obj2[new_path]}")
            elif key not in obj2:
                differences[MISSING_KEYS_SECOND].append(f"{new_path}: {obj1[new_path]}")
            else:
                sub_diff = compare_json_objects(obj1[key], obj2[key], new_path)
                differences[MISSING_KEYS_FIRST].extend(sub_diff[MISSING_KEYS_FIRST])
                differences[MISSING_KEYS_SECOND].extend(sub_diff[MISSING_KEYS_SECOND])
                differences[DIVERGENT_VALUES].extend(sub_diff[DIVERGENT_VALUES])
    else:
        if obj1 != obj2:
            differences[DIVERGENT_VALUES].append(f"{path}: {obj1} vs {obj2}")
    return differences

def get_relative_file_paths(folder_path):
    file_paths = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.json'):
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, folder_path)
                file_paths.append(relative_path)
    return file_paths

def get_base_filename(file_path):
    normalized_path = normalize_path(file_path)
    pattern = r'_v\d+' # pattern to find '_vXXX' in the file name
    parts = normalized_path.split('\\')
    if len(parts) > 1:
        parts[-1] = re.sub(pattern, '', parts[-1])
        return '\\'.join(parts)
    return normalized_path

def pair_files_for_comparison(files1, files2):
    relative_file11 = get_relative_file_paths(files1)
    relative_file2 = get_relative_file_paths(files2)
    base_to_file1 = {get_base_filename(f): f for f in relative_file11}
    base_to_file2 = {get_base_filename(f): f for f in relative_file2}

    paired_files = []
    for base_name in set(base_to_file1.keys()).union(base_to_file2.keys()):
        file1 = base_to_file1.get(base_name)
        file2 = base_to_file2.get(base_name)
        if file1 or file2:
            paired_files.append((file1, file2))
    return paired_files

def parse_string_to_list(tasks_string):
    tasks = tasks_string.strip("[]").split(", ")
    tasks = [task.strip(" '\"") for task in tasks]
    return tasks

def format_differences(differences):
    formatted_diffs = []
    for category, diffs in differences.items():
        if diffs:
            formatted_diffs.append(f"{category}:")
            formatted_diffs.extend([f" - {item}" for item in diffs])
    return "\n".join(formatted_diffs)

def generate_report(normalized_folder1, normalized_folder2):
    report_lines = []
    modified, added, deleted = 0, 0, 0

    for file1, file2 in pair_files_for_comparison(normalized_folder1, normalized_folder2):
        if file1 and file2:
            normalized_file1 = normalize_path(file1)
            normalized_file2 = normalize_path(file2)
            full_path1 = os.path.join(normalized_folder1, normalized_file1)
            full_path2 = os.path.join(normalized_folder2, normalized_file2)

            with open(full_path1, 'r') as f1, open(full_path2, 'r') as f2:
                json1, json2 = json.load(f1), json.load(f2)

            differences = compare_json_objects(json1, json2)
            if any(value for value in differences.values()):
                modified += 1
                report_lines.append(f"MODIFIED: {normalized_file1} vs {normalized_file2}\n{format_differences(differences)}")
    summary = f"SUMMARY:\nModified: {modified}, Added: {added}, Deleted: {deleted}"
    report = summary + "\n\n" + "\n\n".join(report_lines)
    return report

def save_report(report, folder1_name, folder2_name):
    reports_folder = 'reports'
    if not os.path.exists(reports_folder):
        os.makedirs(reports_folder)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    report_file = f"{folder1_name}_vs_{folder2_name}_report_{timestamp}.txt"
    report_path = os.path.join(reports_folder, report_file)
    with open(report_path, 'w') as f:
        f.write(report)
    print(f"Report saved to {report_path}")

def print_ascii_art():
    art = """
           ( (
            ) )
        __..---..__
    ,-='  /  |  \  `=-.
   :--..___________..--;
    \.,_____________,./
    """
    print(art)

def main():
    if len(sys.argv) != 3:
        print("Usage: python compare-profiles.py <path_to_folder1> <path_to_folder2>")
        sys.exit(1)

    folder1 = normalize_path(sys.argv[1])
    folder2 = normalize_path(sys.argv[2])
    folder1_name = os.path.basename(folder1)
    folder2_name = os.path.basename(folder2)
    try:
        report = generate_report(folder1, folder2)
        report = report.replace(FILE1_PLACEHOLDER, folder1_name)
        report = report.replace(FILE2_PLACEHOLDER, folder2_name)
        save_report(report, folder1_name, folder2_name)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print_ascii_art()
    main()