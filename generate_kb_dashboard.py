#!/usr/bin/env python3
"""
Knowledge Base Dashboard Generator
Creates visual summaries of KB quality analysis
"""

import csv
from collections import Counter, defaultdict
import json

def generate_dashboard():
    """Generate dashboard from analysis results"""

    # Read CSV
    results = []
    with open('T:\\Code\\shared-knowledge-base\\analysis_agent2_domains.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        results = list(reader)

    # Group by directory
    by_directory = defaultdict(list)
    for r in results:
        path_parts = r['File Path'].split('\\')
        if len(path_parts) >= 2:
            directory = path_parts[1]  # Second level (docker, python, etc.)
            by_directory[directory].append(r)

    # Calculate statistics
    total_files = len(results)
    total_quality = sum(int(r['Quality Score']) for r in results)
    total_schema = sum(int(r['Schema Score']) for r in results)

    # Count actions
    action_counts = Counter(r['Action'] for r in results)
    priority_counts = Counter(r['Priority'] for r in results)

    # Count by quality tier
    quality_tiers = {
        'Excellent (90-100)': 0,
        'Good (75-89)': 0,
        'Acceptable (60-74)': 0,
        'Poor (40-59)': 0,
        'Critical (0-39)': 0
    }

    for r in results:
        score = int(r['Quality Score'])
        if score >= 90:
            quality_tiers['Excellent (90-100)'] += 1
        elif score >= 75:
            quality_tiers['Good (75-89)'] += 1
        elif score >= 60:
            quality_tiers['Acceptable (60-74)'] += 1
        elif score >= 40:
            quality_tiers['Poor (40-59)'] += 1
        else:
            quality_tiers['Critical (0-39)'] += 1

    # Print dashboard
    print("=" * 80)
    print("KNOWLEDGE BASE QUALITY DASHBOARD")
    print("=" * 80)
    print()

    print("OVERALL METRICS")
    print("-" * 80)
    print(f"Total Files:          {total_files}")
    print(f"Average Quality:      {total_quality/total_files:.1f}/100")
    print(f"Average Schema:       {total_schema/total_files:.1f}/100")
    print(f"Target Quality:       75/100 minimum")
    print(f"Quality Gap:          {75 - (total_quality/total_files):.1f} points")
    print()

    print("QUALITY DISTRIBUTION")
    print("-" * 80)
    for tier, count in sorted(quality_tiers.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_files) * 100
        bar = "█" * int(percentage / 2)
        print(f"{tier:20} {count:3} files ({percentage:5.1f}%) {bar}")
    print()

    print("ACTION DISTRIBUTION")
    print("-" * 80)
    for action, count in sorted(action_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_files) * 100
        bar = "█" * int(percentage / 2)
        print(f"{action:15} {count:3} files ({percentage:5.1f}%) {bar}")
    print()

    print("PRIORITY DISTRIBUTION")
    print("-" * 80)
    for priority, count in sorted(priority_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_files) * 100
        bar = "█" * int(percentage / 2)
        print(f"{priority:15} {count:3} files ({percentage:5.1f}%) {bar}")
    print()

    print("BY DIRECTORY")
    print("-" * 80)
    dir_stats = []
    for directory, files in sorted(by_directory.items(), key=lambda x: len(x[1]), reverse=True):
        count = len(files)
        avg_quality = sum(int(f['Quality Score']) for f in files) / count
        avg_schema = sum(int(f['Schema Score']) for f in files) / count
        dir_stats.append({
            'dir': directory,
            'count': count,
            'quality': avg_quality,
            'schema': avg_schema
        })

    for stat in sorted(dir_stats, key=lambda x: x['quality']):
        print(f"{stat['dir']:20} {stat['count']:3} files | Q:{stat['quality']:5.1f}/100 | S:{stat['schema']:5.1f}/100")
    print()

    print("TOP 10 ISSUES")
    print("-" * 80)
    issue_counts = Counter()
    for r in results:
        issues = r['Issues'].split('; ')
        for issue in issues[:3]:  # Count first 3 issues per file
            if issue and issue != 'No issues found':
                # Simplify issue text
                simplified = issue.split('(')[0].strip()
                issue_counts[simplified] += 1

    for issue, count in issue_counts.most_common(10):
        print(f"  {count:3} files - {issue}")
    print()

    print("HIGH PRIORITY FILES (Top 20)")
    print("-" * 80)
    high_priority = [r for r in results if r['Priority'] in ['Critical', 'High']]
    high_priority_sorted = sorted(high_priority, key=lambda x: int(x['Quality Score']))

    for i, r in enumerate(high_priority_sorted[:20], 1):
        print(f"{i:2}. {r['File Path']:60} Q:{r['Quality Score']:3}/100 {r['Action']:12}")
    print()

    print("EXCELLENT QUALITY FILES (90-100/100)")
    print("-" * 80)
    excellent = [r for r in results if int(r['Quality Score']) >= 90]
    for i, r in enumerate(excellent, 1):
        print(f"{i:2}. {r['File Path']:60} Q:{r['Quality Score']:3}/100 {r['Action']:12}")
    print()

    print("=" * 80)
    print("RECOMMENDATION SUMMARY")
    print("=" * 80)
    print()
    print("IMMEDIATE ACTIONS (This Week):")
    print("  1. Delete all _meta.yaml files (28 files)")
    print("  2. Fix broken YAML syntax (6 files)")
    print("  3. Delete empty catalog files (2 files)")
    print("  Estimated effort: 5 hours")
    print()
    print("HIGH PRIORITY (This Month):")
    print("  1. Delete VPS patterns (7 files) - rewrite if needed")
    print("  2. Delete Docker errors (6 files) - rewrite if needed")
    print("  3. Merge duplicate content (38 files)")
    print("  Estimated effort: 12 hours")
    print()
    print("MEDIUM PRIORITY (This Quarter):")
    print("  1. Standardize ID formats (9 files)")
    print("  2. Add missing tags (~60 files)")
    print("  3. Add prevention sections (~40 files)")
    print("  4. Restructure solutions (~40 files)")
    print("  Estimated effort: 15.5 hours")
    print()
    print(f"TOTAL ESTIMATED EFFORT: 32.5 hours (~4 weeks)")
    print("=" * 80)

if __name__ == '__main__':
    generate_dashboard()
