#!/usr/bin/env python3
"""
Knowledge Base Quality Analysis Script
Analyzes all YAML files in domains/ for quality, schema compliance, and optimization opportunities.
"""

import yaml
import os
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any

# Quality scoring rubric
SCORING_RUBRIC = {
    'problem_description': 20,  # Clear, specific, detailed
    'solution': 30,  # Code examples, explained, tested
    'prevention': 20,  # Best practices included
    'metadata': 15,  # Tags, severity, scope
    'formatting': 15  # Consistent structure
}

def get_file_size(filepath: str) -> int:
    """Get line count of file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    except:
        return 0

def parse_yaml(filepath: str) -> Tuple[bool, Any]:
    """Parse YAML file, return (success, content)"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = yaml.safe_load(f)
            return True, content
    except Exception as e:
        return False, str(e)

def check_schema_compliance(content: Any, filepath: str) -> Dict[str, Any]:
    """Check YAML file against schema requirements"""
    issues = []
    score = 100

    # Check for required fields
    if not isinstance(content, dict):
        return {'compliant': False, 'score': 0, 'issues': ['Not a valid YAML dict']}

    # Version check
    if 'version' not in content:
        issues.append('Missing version field')
        score -= 10
    else:
        version = content.get('version', '')
        if version not in ['1.0', '4.0', '5.0', '5.1']:
            issues.append(f'Unusual version: {version}')
            score -= 5

    # Category check
    if 'category' not in content:
        issues.append('Missing category field')
        score -= 10

    # last_updated check
    if 'last_updated' not in content:
        issues.append('Missing last_updated field')
        score -= 5
    else:
        # Check if stale (>6 months)
        try:
            last_updated = datetime.strptime(content['last_updated'], '%Y-%m-%d')
            if datetime.now() - last_updated > timedelta(days=180):
                issues.append(f'Stale last_updated: {content["last_updated"]} (>6 months)')
                score -= 5
        except:
            issues.append(f'Invalid last_updated format: {content["last_updated"]}')
            score -= 5

    # Check for errors or patterns
    has_errors = 'errors' in content and isinstance(content['errors'], list)
    has_patterns = 'patterns' in content and isinstance(content['patterns'], list)

    if not has_errors and not has_patterns:
        issues.append('Missing both errors and patterns sections')
        score -= 15
    elif has_errors:
        # Validate error entries
        for i, error in enumerate(content['errors']):
            if not isinstance(error, dict):
                issues.append(f'Error {i}: Not a dict')
                score -= 10
                continue

            # Check required error fields
            if 'id' not in error:
                issues.append(f'Error {i}: Missing id')
                score -= 10
            else:
                # Check ID format (CATEGORY-NNN)
                error_id = error['id']
                if not re.match(r'^[A-Z]+-\d{3,4}$', error_id):
                    issues.append(f'Error {i}: Invalid ID format {error_id} (expected CATEGORY-NNN)')
                    score -= 5

            if 'title' not in error:
                issues.append(f'Error {i}: Missing title')
                score -= 5

            if 'severity' not in error:
                issues.append(f'Error {i}: Missing severity')
                score -= 3
            else:
                if error['severity'] not in ['critical', 'high', 'medium', 'low']:
                    issues.append(f'Error {i}: Invalid severity {error["severity"]}')
                    score -= 2

            if 'scope' not in error:
                issues.append(f'Error {i}: Missing scope')
                score -= 5
            else:
                valid_scopes = ['universal', 'python', 'javascript', 'docker', 'postgresql', 'vps', 'framework']
                if error['scope'] not in valid_scopes:
                    issues.append(f'Error {i}: Invalid scope {error["scope"]}')
                    score -= 3

            if 'problem' not in error:
                issues.append(f'Error {i}: Missing problem description')
                score -= 15

            if 'solution' not in error:
                issues.append(f'Error {i}: Missing solution')
                score -= 20

    return {
        'compliant': score >= 75,
        'score': max(0, score),
        'issues': issues
    }

def assess_quality(content: Any, filepath: str, line_count: int) -> Dict[str, Any]:
    """Assess overall quality of knowledge entry"""
    scores = {
        'problem_description': 0,
        'solution': 0,
        'prevention': 0,
        'metadata': 0,
        'formatting': 0
    }

    issues = []

    # Check if errors or patterns
    has_errors = 'errors' in content and isinstance(content['errors'], list)
    entries = content.get('errors', []) if has_errors else content.get('patterns', [])

    if not entries:
        return {
            'total_score': 0,
            'breakdown': scores,
            'issues': ['No entries found']
        }

    # Analyze first entry (most files have 1-2 entries)
    entry = entries[0]

    # Problem Description (20 pts)
    if 'problem' in entry:
        problem = entry['problem']
        if len(problem) > 200:
            scores['problem_description'] = 20  # Detailed
        elif len(problem) > 100:
            scores['problem_description'] = 15  # Moderate
        elif len(problem) > 50:
            scores['problem_description'] = 10  # Brief
        else:
            scores['problem_description'] = 5  # Too brief
            issues.append('Problem description too brief')
    else:
        issues.append('Missing problem description')

    # Solution (30 pts)
    if 'solution' in entry:
        solution = entry['solution']
        if isinstance(solution, dict):
            if 'code' in solution:
                code = solution['code']
                if code and len(str(code)) > 100:
                    scores['solution'] += 15  # Has code example
                else:
                    issues.append('Code example missing or too short')

            if 'explanation' in solution:
                if len(solution['explanation']) > 100:
                    scores['solution'] += 15  # Well explained
                else:
                    scores['solution'] += 10  # Brief explanation
            else:
                issues.append('Missing solution explanation')
                scores['solution'] += 5
        else:
            scores['solution'] = 5
            issues.append('Solution not structured as dict with code/explanation')
    else:
        issues.append('Missing solution entirely')

    # Prevention (20 pts)
    if 'prevention' in entry:
        prevention = entry['prevention']
        if prevention and len(str(prevention)) > 100:
            scores['prevention'] = 20  # Comprehensive
        else:
            scores['prevention'] = 10  # Brief but present
    else:
        issues.append('Missing prevention section')

    # Metadata (15 pts)
    metadata_score = 0
    if 'tags' in entry and entry['tags']:
        metadata_score += 5
    else:
        issues.append('Missing tags')

    if 'severity' in entry:
        metadata_score += 5
    else:
        issues.append('Missing severity')

    if 'scope' in entry:
        metadata_score += 5
    else:
        issues.append('Missing scope')

    scores['metadata'] = metadata_score

    # Formatting (15 pts)
    formatting_score = 15
    if line_count < 20:
        formatting_score -= 5
        issues.append('File very short - may be incomplete')

    # Check for consistent structure
    if 'version' not in content:
        formatting_score -= 5

    scores['formatting'] = max(0, formatting_score)

    total_score = sum(scores.values())

    return {
        'total_score': total_score,
        'breakdown': scores,
        'issues': issues
    }

def get_recommendations(quality_score: int, schema_score: int, issues: List[str], filepath: str) -> Tuple[str, str, str]:
    """Determine action, priority, and effort based on analysis"""

    overall_score = min(quality_score, schema_score)

    # Determine action
    if overall_score < 40:
        action = 'DELETE'
        priority = 'High'
        effort = '5 min'
    elif overall_score < 60:
        action = 'MERGE'
        priority = 'High'
        effort = '30 min'
    elif overall_score < 75:
        action = 'UPDATE'
        priority = 'Medium'
        effort = '20 min'
    elif overall_score < 90:
        if 'prevention' in str(issues):
            action = 'EXPAND'
            priority = 'Medium'
            effort = '30 min'
        else:
            action = 'STANDARDIZE'
            priority = 'Low'
            effort = '15 min'
    else:
        action = 'KEEP'
        priority = 'Low'
        effort = '5 min'

    # Adjust priority based on critical issues
    if any('Missing' in issue for issue in issues):
        if action == 'KEEP':
            action = 'UPDATE'
            priority = 'Medium'
            effort = '15 min'

    # Check for stale content
    if 'Stale' in str(issues):
        if action == 'KEEP':
            action = 'UPDATE'
            priority = 'Medium'

    return action, priority, effort

def analyze_file(filepath: str) -> Dict[str, Any]:
    """Analyze a single YAML file"""
    rel_path = os.path.relpath(filepath, 'T:\\Code\\shared-knowledge-base')

    # Basic info
    file_type = 'YAML'
    line_count = get_file_size(filepath)

    # Parse YAML
    success, content = parse_yaml(filepath)

    if not success:
        return {
            'file_path': rel_path,
            'file_type': file_type,
            'size': line_count,
            'quality_score': 0,
            'schema_score': 0,
            'issues': [f'Parse error: {content}'],
            'recommendations': 'Fix YAML syntax',
            'priority': 'Critical',
            'effort': '30 min',
            'action': 'DELETE'
        }

    # Schema compliance
    schema_check = check_schema_compliance(content, filepath)

    # Quality assessment
    quality_assessment = assess_quality(content, filepath, line_count)

    # Get recommendations
    action, priority, effort = get_recommendations(
        quality_assessment['total_score'],
        schema_check['score'],
        schema_check['issues'] + quality_assessment['issues'],
        filepath
    )

    # Combine issues
    all_issues = schema_check['issues'] + quality_assessment['issues']

    return {
        'file_path': rel_path,
        'file_type': file_type,
        'size': line_count,
        'quality_score': quality_assessment['total_score'],
        'schema_score': schema_check['score'],
        'issues': '; '.join(all_issues) if all_issues else 'No issues found',
        'recommendations': f'Quality: {quality_assessment["total_score"]}/100, Schema: {schema_check["score"]}/100',
        'priority': priority,
        'effort': effort,
        'action': action
    }

def main():
    """Main analysis function"""
    print("Starting Knowledge Base Quality Analysis...")
    print("=" * 80)

    # Find all YAML files
    domains_dir = Path('T:\\Code\\shared-knowledge-base\\domains')
    yaml_files = list(domains_dir.rglob('*.yaml'))

    print(f"Found {len(yaml_files)} YAML files to analyze\n")

    # Analyze each file
    results = []
    for i, filepath in enumerate(yaml_files, 1):
        print(f"[{i}/{len(yaml_files)}] Analyzing {filepath.name}...", end=' ')
        try:
            result = analyze_file(str(filepath))
            results.append(result)
            print(f"✓ (Q:{result['quality_score']}/100 S:{result['schema_score']}/100)")
        except Exception as e:
            print(f"✗ Error: {e}")
            results.append({
                'file_path': str(filepath),
                'file_type': 'YAML',
                'size': 0,
                'quality_score': 0,
                'schema_score': 0,
                'issues': f'Analysis error: {str(e)}',
                'recommendations': 'Review file manually',
                'priority': 'Critical',
                'effort': 'Unknown',
                'action': 'DELETE'
            })

    # Write CSV output
    output_file = 'T:\\Code\\shared-knowledge-base\\analysis_agent2_domains.csv'

    print(f"\nWriting results to {output_file}...")

    with open(output_file, 'w', encoding='utf-8') as f:
        # Header
        f.write('File Path,Type,Size,Quality Score,Schema Score,Issues,Recommendations,Priority,Effort,Action\n')

        # Data rows
        for result in results:
            f.write(f"{result['file_path']},")
            f.write(f"{result['file_type']},")
            f.write(f"{result['size']},")
            f.write(f"{result['quality_score']},")
            f.write(f"{result['schema_score']},")
            f.write(f"\"{result['issues']}\",")
            f.write(f"\"{result['recommendations']}\",")
            f.write(f"{result['priority']},")
            f.write(f"{result['effort']},")
            f.write(f"{result['action']}\n")

    # Print summary statistics
    print("\n" + "=" * 80)
    print("ANALYSIS SUMMARY")
    print("=" * 80)

    total_files = len(results)
    avg_quality = sum(r['quality_score'] for r in results) / total_files if total_files > 0 else 0
    avg_schema = sum(r['schema_score'] for r in results) / total_files if total_files > 0 else 0

    action_counts = {}
    for r in results:
        action = r['action']
        action_counts[action] = action_counts.get(action, 0) + 1

    priority_counts = {}
    for r in results:
        priority = r['priority']
        priority_counts[priority] = priority_counts.get(priority, 0) + 1

    print(f"Total files analyzed: {total_files}")
    print(f"Average quality score: {avg_quality:.1f}/100")
    print(f"Average schema score: {avg_schema:.1f}/100")

    print("\nAction Distribution:")
    for action, count in sorted(action_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_files) * 100
        print(f"  {action:12} {count:3} files ({percentage:5.1f}%)")

    print("\nPriority Distribution:")
    for priority, count in sorted(priority_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_files) * 100
        print(f"  {priority:12} {count:3} files ({percentage:5.1f}%)")

    print("\n" + "=" * 80)
    print(f"Results saved to: {output_file}")
    print("=" * 80)

if __name__ == '__main__':
    main()
