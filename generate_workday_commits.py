#!/usr/bin/env python3
"""
Generate workday Git commits script.
Creates realistic commit history for workdays (Mon-Fri) only.
"""

import argparse
import random
from datetime import datetime, timedelta
from pathlib import Path

# Realistic commit message templates
COMMIT_MESSAGES = {
    "morning": [
        "Start day: review PR queue and plan tasks",
        "Daily standup notes and sprint planning",
        "Check overnight builds and CI status",
        "Morning sync: align on priorities",
        "Review emails and update task board",
    ],
    "development": [
        "Implement feature: {component}",
        "Refactor {component} for better performance",
        "Add tests for {component}",
        "Update {component} documentation",
        "Fix edge case in {component}",
        "Optimize {component} query performance",
        "Integrate {component} with API",
        "Add validation to {component}",
    ],
    "bugfix": [
        "Fix bug: {issue} causing {symptom}",
        "Hotfix: resolve {issue} in production",
        "Debug and fix {issue}",
        "Address code review feedback on {issue}",
        "Fix regression in {issue}",
    ],
    "review": [
        "Code review: {pr}",
        "Review and approve PR: {pr}",
        "Leave feedback on {pr}",
        "Pair programming session on {feature}",
        "Mentoring session: review {feature}",
    ],
    "planning": [
        "Update sprint backlog",
        "Write technical spec for {feature}",
        "Estimate tasks for next sprint",
        "Document {feature} architecture decision",
        "Update README with {feature} instructions",
    ],
    "endofday": [
        "Wrap up: commit WIP on {feature}",
        "End of day: save progress on {feature}",
        "Checkpoint: {feature} progress",
        "Daily commit: {feature} updates",
        "Push EOD changes for {feature}",
    ],
}

COMPONENTS = [
    "user authentication", "payment gateway", "dashboard API", "data pipeline",
    "notification service", "user profile", "search functionality", "reporting module",
    "cache layer", "database migrations", "API endpoints", "frontend components",
    "background jobs", "webhook handlers", "error logging", "metrics collection",
    "config management", "security middleware", "rate limiting", "audit trail",
]

ISSUES = [
    "memory leak", "race condition", "null pointer", "authentication timeout",
    "database deadlock", "race condition", "validation error", "indexing issue",
    "session handling", "token refresh", "data sync", "cache invalidation",
]

SYMPTOMS = [
    "slow response times", "intermittent failures", "login errors", "data inconsistency",
    "timeout issues", "crashes", "incorrect totals", "missing notifications",
]

PRS = [
    "#1423", "#1425", "#1428", "#1430", "#1432",
    "user-auth-refactor", "payment-fix", "dashboard-v2", "api-cleanup",
]

FEATURES = [
    "new onboarding flow", "analytics dashboard", "bulk export", "real-time updates",
    "mobile optimization", "accessibility improvements", "dark mode", "SSO integration",
    "audit logging", "rate limiting", "caching layer", "API v2",
]


def generate_commit_message(hour: int) -> str:
    """Generate a realistic commit message based on time of day."""
    if hour < 10:
        category = "morning"
    elif hour < 12:
        category = random.choice(["development", "bugfix", "review"])
    elif hour < 14:
        category = random.choice(["planning", "review"])
    elif hour < 17:
        category = random.choice(["development", "bugfix", "review"])
    else:
        category = "endofday"
    
    template = random.choice(COMMIT_MESSAGES[category])
    
    # Fill in placeholders
    message = template.format(
        component=random.choice(COMPONENTS),
        issue=random.choice(ISSUES),
        symptom=random.choice(SYMPTOMS),
        pr=random.choice(PRS),
        feature=random.choice(FEATURES),
    )
    
    return message


def is_workday(date: datetime) -> bool:
    """Check if date is a weekday (Mon-Fri)."""
    return date.weekday() < 5  # Monday=0, Friday=4


def generate_commits_for_day(date: datetime, num_commits: int, filename: str) -> list:
    """Generate commit commands for a single workday."""
    commits = []
    
    # Distribute commits between 9:00 and 18:00
    work_hours = list(range(9, 18))
    selected_hours = sorted(random.sample(work_hours, min(num_commits, len(work_hours))))
    
    # If we need more commits than hours, add some within the same hour
    while len(selected_hours) < num_commits:
        selected_hours.append(random.choice(work_hours))
    selected_hours = sorted(selected_hours[:num_commits])
    
    for i, hour in enumerate(selected_hours):
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        
        commit_time = date.replace(hour=hour, minute=minute, second=second)
        timestamp = commit_time.strftime("%Y-%m-%d %H:%M:%S")
        iso_timestamp = commit_time.strftime("%Y-%m-%dT%H:%M:%S")
        
        message = generate_commit_message(hour)
        
        # Generate content for the file
        content_line = f"[{timestamp}] {message}\n"
        
        commits.append({
            'timestamp': timestamp,
            'iso_timestamp': iso_timestamp,
            'message': message,
            'content': content_line,
        })
    
    return commits


def generate_shell_script(commits: list, filename: str, output_path: str) -> str:
    """Generate a shell script that creates the commits."""
    script_lines = [
        "#!/bin/bash",
        "# Auto-generated commit script",
        "# Run this in your git repository",
        "",
        "set -e",
        "",
        f'FILE="{filename}"',
        "",
        "# Ensure file exists",
        'touch "$FILE"',
        "",
    ]
    
    for commit in commits:
        script_lines.extend([
            f"# Commit: {commit['message']}",
            f"echo '{commit['content'].rstrip()}' >> \"$FILE\"",
            f"export GIT_AUTHOR_DATE='{commit['iso_timestamp']}'",
            f"export GIT_COMMITTER_DATE='{commit['iso_timestamp']}'",
            f"git add \"$FILE\"",
            f"git commit -m '{commit['message']}'",
            "",
        ])
    
    script_lines.extend([
        "echo 'All commits created successfully!'",
        "git log --oneline -10",
    ])
    
    return '\n'.join(script_lines)


def main():
    parser = argparse.ArgumentParser(
        description='Generate realistic workday Git commits'
    )
    parser.add_argument(
        '--year', '-y',
        type=int,
        default=datetime.now().year,
        help='Starting year (default: current year)'
    )
    parser.add_argument(
        '--start-date',
        type=str,
        help='Start date in YYYY-MM-DD format (overrides --year)'
    )
    parser.add_argument(
        '--end-date',
        type=str,
        help='End date in YYYY-MM-DD format (overrides --months)'
    )
    parser.add_argument(
        '--months', '-m',
        type=int,
        default=12,
        help='Number of months to generate (default: 12)'
    )
    parser.add_argument(
        '--min-commits',
        type=int,
        default=3,
        help='Minimum commits per workday (default: 3)'
    )
    parser.add_argument(
        '--max-commits',
        type=int,
        default=5,
        help='Maximum commits per workday (default: 5)'
    )
    parser.add_argument(
        '--file', '-f',
        type=str,
        default='work.log',
        help='File to modify (default: work.log)'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='create_commits.sh',
        help='Output shell script name (default: create_commits.sh)'
    )
    parser.add_argument(
        '--vacation-days',
        type=int,
        default=-1,
        help='Number of vacation days to simulate (default: ~8%% of workdays)'
    )
    
    args = parser.parse_args()
    
    # Generate date range
    if args.start_date:
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    else:
        start_date = datetime(args.year, 1, 1)
    
    if args.end_date:
        end_date = datetime.strptime(args.end_date, "%Y-%m-%d") + timedelta(days=1)
    else:
        end_date = start_date + timedelta(days=30 * args.months)
    
    # Collect all workdays
    workdays = []
    current = start_date
    while current < end_date:
        if is_workday(current):
            workdays.append(current)
        current += timedelta(days=1)
    
    # Simulate vacation days (random workdays off)
    # Default to ~8% of workdays (about 20 days per year)
    vacation_days = args.vacation_days
    if vacation_days < 0:
        vacation_days = max(1, int(len(workdays) * 0.08))
    
    if vacation_days > 0:
        vacation_days = min(vacation_days, len(workdays) - 1)  # Keep at least one workday
        vacation_day_list = random.sample(workdays, vacation_days)
        workdays = [d for d in workdays if d not in vacation_day_list]
    
    print(f"Generating commits from {start_date.date()} to {end_date.date()}")
    total_workdays_before_vacation = len(workdays) + vacation_days
    print(f"Total workdays: {len(workdays)} (excluded {vacation_days} vacation days)")
    
    # Generate commits for each workday
    all_commits = []
    for workday in workdays:
        num_commits = random.randint(args.min_commits, args.max_commits)
        day_commits = generate_commits_for_day(workday, num_commits, args.file)
        all_commits.extend(day_commits)
    
    print(f"Total commits to generate: {len(all_commits)}")
    
    # Generate shell script
    script_content = generate_shell_script(all_commits, args.file, args.output)
    
    output_path = Path(args.output)
    output_path.write_text(script_content)
    output_path.chmod(0o755)
    
    print(f"\nGenerated: {args.output}")
    print(f"\nTo use:")
    print(f"  1. cd /path/to/your/git/repo")
    print(f"  2. cp {args.output} .")
    print(f"  3. ./{args.output}")
    print(f"\nPreview of first 5 commits:")
    for commit in all_commits[:5]:
        print(f"  [{commit['timestamp']}] {commit['message']}")


if __name__ == '__main__':
    main()
