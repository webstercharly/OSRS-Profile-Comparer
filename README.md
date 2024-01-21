# OSRS-Profile-Comparer
Compare Profiles is a Python utility designed to compare JSON profiles of Old School RuneScape (OSRS) characters, highlighting differences between two versions of profiles. It's perfect for developers managing multiple character configurations or players tracking changes in their game setup.

## Features

- **Deep Comparison**: Recursively compares JSON objects, including nested structures.
- **Task Differences**: Special handling for task lists, identifying added or removed tasks.
- **Report Generation**: Summarizes modifications, additions, and deletions in a readable report.
- **Path Normalization**: Works across different operating systems by normalizing file paths.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

- Python 3.x

### Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/webstercharly/OSRS-Profile-Comparer.git
```

Navigate to the cloned directory:

```bash
cd compare-profiles
```

### Usage

To run the comparison, execute the script with two directories containing JSON profiles as arguments:

```bash
python compare-profiles.py "path/to/old/profiles" "path/to/new/profiles"
```

The script will generate a report in a `reports` directory, detailing the differences between the two sets of profiles.

## Built With

- [Python](https://www.python.org/) - The programming language used.

## Contributing

Please read [CONTRIBUTING.md](https://github.com/webstercharly/OSRS-Profile-Comparer/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.


## Authors

- **Charly Webster** - *Initial work* - [WebsterCharly](https://github.com/webstercharly)

See also the list of [contributors](https://github.com/webstercharly/OSRS-Profile-Comparer/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
