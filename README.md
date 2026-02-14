# Workday Commits Generator

Generate realistic Git commit history for workdays only (Monday-Friday).

## Quick Start

```bash
# Generate commits for current year
python3 generate_workday_commits.py

# Generate commits for specific year
python3 generate_workday_commits.py --year 2024

# Generate 6 months with custom file
python3 generate_workday_commits.py --year 2024 --months 6 --file progress.txt
```

## Usage

```
python3 generate_workday_commits.py [OPTIONS]

Options:
  -y, --year YEAR          Starting year (default: current year)
  -m, --months MONTHS      Number of months to generate (default: 12)
  --min-commits N          Minimum commits per workday (default: 3)
  --max-commits N          Maximum commits per workday (default: 5)
  -f, --file FILE          File to modify (default: work.log)
  -o, --output SCRIPT      Output shell script (default: create_commits.sh)
  --vacation-days N        Random vacation days to simulate (default: 20)
```

## Example Workflow

```bash
# 1. Generate the commit script
python3 generate_workday_commits.py --year 2024 --months 12

# 2. Go to your git repository
cd ~/my-project

# 3. Copy and run the script
cp /path/to/create_commits.sh .
./create_commits.sh

# 4. Verify commits
git log --oneline --graph --all
```

## Features

- **Weekdays only**: No commits on Saturday or Sunday
- **Business hours**: Commits between 9:00 AM - 6:00 PM
- **Realistic patterns**: Morning standups, development work, code reviews, EOD commits
- **Vacation simulation**: Random days off for realism
- **Variable intensity**: 3-5 commits per workday

## Commit Message Types

- Morning standups and planning
- Feature development
- Bug fixes
- Code reviews
- Documentation updates
- End-of-day progress commits

## Requirements

- Python 3.6+
- Git repository (to run the generated script)
