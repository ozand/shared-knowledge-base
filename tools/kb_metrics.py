#!/usr/bin/env python3
"""
Shared Knowledge Base Metrics Dashboard
Generates quality metrics and repository statistics
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
import yaml

class KBMetrics:
    """Calculate and display KB metrics"""

    def __init__(self, repo_path=None):
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
        self.domains_path = self.repo_path / "domains"
        self.metrics = {}

    def calculate_all_metrics(self):
        """Calculate all metrics"""
        print("🔍 Calculating KB metrics...")

        self.metrics['timestamp'] = datetime.now().isoformat()
        self.metrics['repository_stats'] = self.get_repository_stats()
        self.metrics['yaml_files'] = self.analyze_yaml_files()
        self.metrics['quality_scores'] = self.calculate_quality_scores()
        self.metrics['domain_distribution'] = self.get_domain_distribution()
        self.metrics['entry_types'] = self.get_entry_types()
        self.metrics['version_distribution'] = self.get_version_distribution()

        # Calculate validation status after yaml_files is set
        self.metrics['validation_status'] = self.get_validation_status()

        return self.metrics

    def get_repository_stats(self):
        """Get basic repository statistics"""
        stats = {
            'total_files': 0,
            'total_lines': 0,
            'total_size_kb': 0,
            'yaml_files': 0,
            'markdown_files': 0,
            'python_files': 0
        }

        # Count files by type
        for ext in ['*.yaml', '*.yml', '*.md', '*.py']:
            files = list(self.repo_path.rglob(ext))
            for file in files:
                if '.git' in str(file):
                    continue

                stats['total_files'] += 1

                # Get file size
                try:
                    stats['total_size_kb'] += file.stat().st_size / 1024
                except:
                    pass

                # Get line count
                try:
                    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                        stats['total_lines'] += sum(1 for _ in f)
                except:
                    pass

                # Count by type
                if file.suffix in ['.yaml', '.yml']:
                    stats['yaml_files'] += 1
                elif file.suffix == '.md':
                    stats['markdown_files'] += 1
                elif file.suffix == '.py':
                    stats['python_files'] += 1

        return stats

    def analyze_yaml_files(self):
        """Analyze YAML files in domains/"""
        yaml_stats = {
            'total_entries': 0,
            'errors': 0,
            'patterns': 0,
            'avg_entry_size_lines': 0,
            'largest_file': None,
            'domains': {}
        }

        total_lines = 0
        max_lines = 0
        largest_file = None

        for yaml_file in self.domains_path.rglob('*.yaml'):
            if '_meta.yaml' in str(yaml_file):
                continue

            try:
                with open(yaml_file, 'r') as f:
                    content = yaml.safe_load(f)
                    lines = sum(1 for _ in open(yaml_file, 'r'))

                    # Count entries
                    if 'errors' in content:
                        count = len(content['errors'])
                        yaml_stats['errors'] += count
                        yaml_stats['total_entries'] += count
                    elif 'patterns' in content:
                        count = len(content['patterns'])
                        yaml_stats['patterns'] += count
                        yaml_stats['total_entries'] += count

                    total_lines += lines

                    # Track largest file
                    if lines > max_lines:
                        max_lines = lines
                        largest_file = str(yaml_file.relative_to(self.repo_path))

                    # Track by domain
                    domain = yaml_file.parent.parent.name
                    if domain not in yaml_stats['domains']:
                        yaml_stats['domains'][domain] = {
                            'files': 0,
                            'entries': 0,
                            'lines': 0
                        }

                    yaml_stats['domains'][domain]['files'] += 1
                    yaml_stats['domains'][domain]['entries'] += count
                    yaml_stats['domains'][domain]['lines'] += lines

            except Exception as e:
                print(f"  ⚠️  Error reading {yaml_file}: {e}")

        if yaml_stats['total_entries'] > 0:
            yaml_stats['avg_entry_size_lines'] = total_lines / yaml_stats['total_entries']

        yaml_stats['largest_file'] = {
            'path': largest_file,
            'lines': max_lines
        }

        return yaml_stats

    def calculate_quality_scores(self):
        """Calculate quality scores for entries"""
        quality_stats = {
            'total_entries': 0,
            'excellent': 0,  # 90-100
            'good': 0,       # 75-89
            'acceptable': 0, # 60-74
            'poor': 0,       # 40-59
            'critical': 0,   # 0-39
            'avg_score': 0
        }

        total_score = 0

        for yaml_file in self.domains_path.rglob('*.yaml'):
            if '_meta.yaml' in str(yaml_file):
                continue

            try:
                with open(yaml_file, 'r') as f:
                    content = yaml.safe_load(f)

                    entries = content.get('errors', []) + content.get('patterns', [])

                    for entry in entries:
                        score = self.calculate_entry_score(entry)
                        quality_stats['total_entries'] += 1
                        total_score += score

                        if score >= 90:
                            quality_stats['excellent'] += 1
                        elif score >= 75:
                            quality_stats['good'] += 1
                        elif score >= 60:
                            quality_stats['acceptable'] += 1
                        elif score >= 40:
                            quality_stats['poor'] += 1
                        else:
                            quality_stats['critical'] += 1

            except Exception as e:
                pass

        if quality_stats['total_entries'] > 0:
            quality_stats['avg_score'] = total_score / quality_stats['total_entries']

        return quality_stats

    def calculate_entry_score(self, entry):
        """Calculate quality score for a single entry (0-100)"""
        score = 0

        # Required fields (40 points)
        required_fields = ['id', 'title', 'severity', 'scope', 'problem', 'solution']
        for field in required_fields:
            if field in entry:
                score += 40 // len(required_fields)

        # Solution quality (30 points)
        if 'solution' in entry:
            solution = entry['solution']
            if isinstance(solution, dict):
                if 'code' in solution and solution['code']:
                    score += 15
                if 'explanation' in solution and solution['explanation']:
                    score += 15

        # Prevention/best practices (20 points)
        if 'prevention' in entry and entry['prevention']:
            score += 20

        # Additional metadata (10 points)
        if 'tags' in entry and entry['tags']:
            score += 5
        if 'symptoms' in entry or 'root_cause' in entry:
            score += 5

        return min(score, 100)

    def get_domain_distribution(self):
        """Get distribution of entries across domains"""
        distribution = defaultdict(int)

        for yaml_file in self.domains_path.rglob('*.yaml'):
            if '_meta.yaml' in str(yaml_file):
                continue

            try:
                with open(yaml_file, 'r') as f:
                    content = yaml.safe_load(f)

                    domain = yaml_file.parent.parent.name
                    entries = content.get('errors', []) + content.get('patterns', [])
                    distribution[domain] += len(entries)

            except:
                pass

        return dict(sorted(distribution.items(), key=lambda x: x[1], reverse=True))

    def get_entry_types(self):
        """Get distribution of entry types"""
        yaml_stats = self.metrics.get('yaml_files', {})
        return {
            'errors': yaml_stats.get('errors', 0),
            'patterns': yaml_stats.get('patterns', 0)
        }

    def get_version_distribution(self):
        """Get distribution of schema versions"""
        versions = Counter()

        for yaml_file in self.domains_path.rglob('*.yaml'):
            if '_meta.yaml' in str(yaml_file):
                continue

            try:
                with open(yaml_file, 'r') as f:
                    content = yaml.safe_load(f)
                    if 'version' in content:
                        versions[content['version']] += 1
            except:
                pass

        return dict(versions)

    def get_validation_status(self):
        """Get validation status"""
        yaml_stats = self.metrics.get('yaml_files', {})
        total = 0
        for domain in yaml_stats.get('domains', {}).values():
            total += domain.get('files', 0)

        return {
            'total_files': total,
            'validated': total,
            'errors': 0,  # Would be populated by actual validation
            'warnings': 0
        }

    def print_dashboard(self):
        """Print metrics dashboard"""
        print("\n" + "="*60)
        print("📊 SHARED KNOWLEDGE BASE METRICS DASHBOARD")
        print("="*60)

        # Repository Stats
        print("\n📁 Repository Statistics:")
        print(f"  Total Files: {self.metrics['repository_stats']['total_files']:,}")
        print(f"  Total Lines: {self.metrics['repository_stats']['total_lines']:,}")
        print(f"  Total Size: {self.metrics['repository_stats']['total_size_kb']:.1f} KB")
        print(f"  YAML Files: {self.metrics['repository_stats']['yaml_files']}")
        print(f"  Markdown Files: {self.metrics['repository_stats']['markdown_files']}")
        print(f"  Python Files: {self.metrics['repository_stats']['python_files']}")

        # YAML Stats
        yaml = self.metrics['yaml_files']
        print("\n📝 YAML Entry Statistics:")
        print(f"  Total Entries: {yaml['total_entries']}")
        print(f"  Errors: {yaml['errors']}")
        print(f"  Patterns: {yaml['patterns']}")
        print(f"  Avg Entry Size: {yaml['avg_entry_size_lines']:.1f} lines")
        print(f"  Largest File: {yaml['largest_file']['path']} ({yaml['largest_file']['lines']} lines)")

        # Domain Distribution
        print("\n📂 Domain Distribution:")
        for domain, count in list(self.metrics['domain_distribution'].items())[:10]:
            print(f"  {domain}: {count} entries")

        # Quality Scores
        quality = self.metrics['quality_scores']
        print("\n⭐ Quality Scores:")
        print(f"  Total Entries: {quality['total_entries']}")
        print(f"  Average Score: {quality['avg_score']:.1f}/100")
        print(f"  Excellent (90-100): {quality['excellent']} ({quality['excellent']/quality['total_entries']*100:.1f}%)" if quality['total_entries'] > 0 else "")
        print(f"  Good (75-89): {quality['good']} ({quality['good']/quality['total_entries']*100:.1f}%)" if quality['total_entries'] > 0 else "")
        print(f"  Acceptable (60-74): {quality['acceptable']} ({quality['acceptable']/quality['total_entries']*100:.1f}%)" if quality['total_entries'] > 0 else "")
        print(f"  Poor (40-59): {quality['poor']} ({quality['poor']/quality['total_entries']*100:.1f}%)" if quality['total_entries'] > 0 else "")
        print(f"  Critical (0-39): {quality['critical']} ({quality['critical']/quality['total_entries']*100:.1f}%)" if quality['total_entries'] > 0 else "")

        # Version Distribution
        print("\n🔢 Version Distribution:")
        for version, count in self.metrics['version_distribution'].items():
            print(f"  {version}: {count} files")

        # Overall Health
        print("\n🏥 Overall Health:")
        health_score = quality['avg_score']
        if health_score >= 90:
            print(f"  Status: ✅ Excellent ({health_score:.1f}/100)")
        elif health_score >= 75:
            print(f"  Status: ✅ Good ({health_score:.1f}/100)")
        elif health_score >= 60:
            print(f"  Status: ⚠️  Acceptable ({health_score:.1f}/100)")
        else:
            print(f"  Status: ❌ Needs Improvement ({health_score:.1f}/100)")

        print("\n" + "="*60)
        print(f"Generated: {self.metrics['timestamp']}")
        print("="*60 + "\n")

    def export_json(self, output_file):
        """Export metrics to JSON file"""
        with open(output_file, 'w') as f:
            json.dump(self.metrics, f, indent=2)
        print(f"✅ Metrics exported to {output_file}")

def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="KB Metrics Dashboard")
    parser.add_argument('--repo', '-r', help='Repository path', default='.')
    parser.add_argument('--export', '-e', help='Export to JSON file')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    # Calculate metrics
    metrics = KBMetrics(args.repo)
    metrics.calculate_all_metrics()

    # Output
    if args.json:
        print(json.dumps(metrics.metrics, indent=2))
    else:
        metrics.print_dashboard()

    # Export if requested
    if args.export:
        metrics.export_json(args.export)

if __name__ == '__main__':
    main()
