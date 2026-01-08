#!/usr/bin/env python
"""
Analyze all documentation and configuration files
Generate quality assessment report
"""

import os
import re
from pathlib import Path
from datetime import datetime

def count_lines(filepath):
    """Count lines in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except:
        return 0

def assess_markdown_quality(filepath, line_count):
    """Assess markdown file quality (0-100)"""
    issues = []
    recommendations = []
    score = 50  # Base score

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except:
        return 0, "Cannot read file", "DELETE", "Critical", "5 min"

    # Check for title (# header)
    if re.search(r'^#\s+', content, re.MULTILINE):
        score += 10
    else:
        issues.append("Missing title header")

    # Check for last_updated date
    if re.search(r'last_updated|updated|Last Updated', content, re.IGNORECASE):
        score += 5
    else:
        issues.append("Missing last_updated date")
        recommendations.append("Add last_updated date")

    # Check for code examples
    if re.search(r'```', content):
        score += 10
    else:
        if line_count > 200:
            issues.append("No code examples")
            recommendations.append("Add code examples")

    # Check for table of contents (if >500 lines)
    if line_count > 500:
        if re.search(r'##.*Contents|Table of Contents|TOC', content, re.IGNORECASE):
            score += 10
        else:
            issues.append("File >500 lines but no TOC")
            recommendations.append("Add table of contents")

    # Check for version references
    versions = re.findall(r'v\d+\.\d+', content)
    if versions:
        # Check if version is consistent
        score += 5
        if 'v3.' in content and 'v5.1' in content:
            issues.append("Mixed version references (v3.x and v5.1)")
            score -= 5

    # Check for @references (progressive disclosure)
    if '@' in content:
        score += 5

    # Check for broken internal links
    internal_links = re.findall(r'\[([^\]]+)\]\((?!http)([^)]+)\)', content)
    if internal_links and not any('README' in content.upper() for _ in internal_links):
        score += 5

    # Cross-reference quality
    if '@references' in content or '@for-claude-code' in content or '@docs' in content:
        score += 10
    else:
        if line_count > 300:
            issues.append("No cross-references to related docs")
            recommendations.append("Add @references for progressive disclosure")

    # File size assessment
    if line_count > 1000:
        issues.append(f"Very long file ({line_count} lines)")
        recommendations.append("Consider splitting into multiple files")
        score -= 10
    elif line_count > 500:
        issues.append(f"Long file ({line_count} lines)")
        score -= 5

    # Quality cap
    score = max(0, min(100, score))

    # Determine action based on score and issues
    if score < 40:
        action = "DELETE"
        priority = "High"
    elif score < 60:
        action = "ARCHIVE"
        priority = "Medium"
    elif score < 75:
        if "Mixed version references" in issues or "Missing last_updated date" in issues:
            action = "UPDATE"
            priority = "High"
        else:
            action = "EXPAND"
            priority = "Medium"
    elif score < 90:
        action = "OPTIMIZE"
        priority = "Low"
    else:
        action = "KEEP"
        priority = "Low"

    # Estimate effort
    if action == "DELETE":
        effort = "5 min"
    elif action in ["ARCHIVE", "UPDATE"]:
        effort = "15 min"
    elif action == "EXPAND":
        effort = "30 min"
    elif "Very long file" in issues:
        effort = "1 hr"
    else:
        effort = "15 min"

    issues_str = "; ".join(issues) if issues else "No major issues"
    recs_str = "; ".join(recommendations) if recommendations else "Good structure"

    return score, issues_str, action, priority, effort

def assess_config_quality(filepath, ext):
    """Assess configuration file quality (0-100)"""
    issues = []
    score = 50

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except:
        return 0, "Cannot read file", "DELETE", "Critical", "5 min"

    # Check for comments/documentation
    if ext in ['.yaml', '.yml']:
        if re.search(r'#', content):
            score += 20
        else:
            issues.append("No comments")
    elif ext == '.json':
        # JSON doesn't support comments
        score += 20

    # Check structure
    if ext in ['.yaml', '.yml']:
        try:
            import yaml
            yaml.safe_load(content)
            score += 30
        except:
            issues.append("Invalid YAML syntax")
            score = 0
    elif ext == '.json':
        try:
            import json
            json.loads(content)
            score += 30
        except:
            issues.append("Invalid JSON syntax")
            score = 0

    # Check for purpose/examples
    line_count = len(content.split('\n'))
    if line_count > 10:
        score += 20
    else:
        issues.append("Very minimal")

    # Quality cap
    score = max(0, min(100, score))

    if score < 60:
        action = "UPDATE"
        priority = "Medium"
    else:
        action = "KEEP"
        priority = "Low"

    issues_str = "; ".join(issues) if issues else "Good structure"

    return score, issues_str, action, priority, "15 min"

def analyze_files():
    """Analyze all target files"""
    base_path = Path("T:/Code/shared-knowledge-base")

    # Target directories
    targets = [
        base_path / ".claude",
        base_path / "docs",
        base_path / "agents",
    ]

    results = []

    for target_dir in targets:
        if not target_dir.exists():
            continue

        for filepath in target_dir.rglob("*"):
            if filepath.is_file():
                ext = filepath.suffix.lower()

                # Only analyze certain file types
                if ext not in ['.md', '.yaml', '.yml', '.json', '.sh']:
                    continue

                # Skip cache and binary files
                if any(skip in str(filepath) for skip in ['.cache', '.db', '__pycache__', '.git']):
                    continue

                rel_path = str(filepath.relative_to(base_path)).replace('\\', '/')

                line_count = count_lines(filepath)

                if ext == '.md':
                    score, issues, action, priority, effort = assess_markdown_quality(filepath, line_count)
                    file_type = "MD"
                elif ext in ['.yaml', '.yml']:
                    score, issues, action, priority, effort = assess_config_quality(filepath, ext)
                    file_type = "YAML"
                elif ext == '.json':
                    score, issues, action, priority, effort = assess_config_quality(filepath, ext)
                    file_type = "JSON"
                elif ext == '.sh':
                    score, issues, action, priority, effort = assess_config_quality(filepath, ext)
                    file_type = "SH"
                else:
                    continue

                recommendations = "See issues" if "No major issues" not in issues else "No changes needed"

                results.append({
                    'file_path': rel_path,
                    'type': file_type,
                    'size': line_count,
                    'quality_score': f"{score}/100",
                    'issues': issues,
                    'recommendations': recommendations,
                    'priority': priority,
                    'effort': effort,
                    'action': action
                })

    return results

def main():
    """Generate CSV report"""
    print("Analyzing files...")

    results = analyze_files()

    # Sort by priority and quality score
    priority_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    results.sort(key=lambda x: (priority_order.get(x['priority'], 4), -int(x['quality_score'].split('/')[0])))

    # Write CSV
    output_path = Path("T:/Code/shared-knowledge-base/analysis_agent1_docs.csv")

    with open(output_path, 'w', encoding='utf-8') as f:
        # Write header
        f.write("File Path,Type,Size,Quality Score,Issues,Recommendations,Priority,Effort,Action\n")

        # Write data
        for r in results:
            # Escape quotes and commas
            issues = r['issues'].replace('"', '""').replace('\n', ' ')
            recs = r['recommendations'].replace('"', '""').replace('\n', ' ')

            f.write(f'"{r["file_path"]}","{r["type"]}",{r["size"]},"{r["quality_score"]}","{issues}","{recs}","{r["priority"]}","{r["effort"]}","{r["action"]}"\n')

    print(f"\n✅ Analysis complete!")
    print(f"📊 Total files analyzed: {len(results)}")
    print(f"📄 Report saved to: {output_path}")

    # Summary statistics
    actions = {}
    priorities = {}
    for r in results:
        actions[r['action']] = actions.get(r['action'], 0) + 1
        priorities[r['priority']] = priorities.get(r['priority'], 0) + 1

    print(f"\n📈 Actions Breakdown:")
    for action, count in sorted(actions.items()):
        print(f"  {action}: {count}")

    print(f"\n🎯 Priority Breakdown:")
    for priority, count in sorted(priorities.items(), key=lambda x: priority_order.get(x[0], 4)):
        print(f"  {priority}: {count}")

if __name__ == "__main__":
    main()
