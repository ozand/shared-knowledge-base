#!/usr/bin/env python3
"""
test_progressive_loading - Test progressive domain-based loading

Run comprehensive tests for progressive loading functionality:
- Token reduction measurement
- Load time benchmarks
- Index size validation
- Domain discovery tests
"""

import yaml
import json
import time
import subprocess
from pathlib import Path
from typing import Dict, List, Any
import sys

# Colors for output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text: str):
    """Print section header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")


def print_success(text: str):
    """Print success message."""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_warning(text: str):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")


def print_error(text: str):
    """Print error message."""
    print(f"{Colors.RED}✗ {text}{Colors.END}")


def print_info(text: str):
    """Print info message."""
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")


def estimate_tokens(file_path: Path) -> int:
    """Estimate tokens in a YAML file (rough approximation: 1 token ≈ 4 chars)."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Rough estimate: 1 token ≈ 4 characters
        return len(content) // 4
    except Exception:
        return 0


class ProgressiveLoadingTest:
    """Test progressive loading functionality."""

    def __init__(self, kb_dir: Path):
        self.kb_dir = kb_dir
        self.domain_index_path = kb_dir / "_domain_index.yaml"
        self.results = {}

    def run_all_tests(self):
        """Run all tests."""
        print_header("PROGRESSIVE LOADING TEST SUITE")

        # Test 1: Index exists and is valid
        self.test_index_exists()

        # Test 2: Index size
        self.test_index_size()

        # Test 3: Domain coverage
        self.test_domain_coverage()

        # Test 4: Token estimation
        self.test_token_estimation()

        # Test 5: Load time benchmark
        self.test_load_time()

        # Test 6: Domain discovery
        self.test_domain_discovery()

        # Print summary
        self.print_summary()

    def test_index_exists(self):
        """Test 1: Check if _domain_index.yaml exists and is valid."""
        print_header("TEST 1: Index Exists and Valid")

        if not self.domain_index_path.exists():
            print_error("_domain_index.yaml not found")
            print_info("Run: python tools/kb_domains.py index --update")
            self.results['index_exists'] = False
            return

        print_success(f"_domain_index.yaml found")

        # Validate YAML
        try:
            with open(self.domain_index_path, 'r') as f:
                index = yaml.safe_load(f)

            required_fields = ['version', 'last_updated', 'total_entries', 'domains']
            for field in required_fields:
                if field not in index:
                    print_error(f"Missing required field: {field}")
                    self.results['index_exists'] = False
                    return

            print_success(f"All required fields present")
            self.results['index_exists'] = True
            self.index = index

        except Exception as e:
            print_error(f"Failed to parse index: {e}")
            self.results['index_exists'] = False

    def test_index_size(self):
        """Test 2: Check index size (should be <200 tokens)."""
        print_header("TEST 2: Index Size Validation")

        if not self.domain_index_path.exists():
            print_error("Index not found, skipping test")
            self.results['index_size'] = False
            return

        index_tokens = estimate_tokens(self.domain_index_path)
        print_info(f"Index size: {index_tokens} tokens")

        if index_tokens < 200:
            print_success(f"Index size OK ({index_tokens} < 200 tokens)")
            self.results['index_size'] = True
            self.results['index_tokens'] = index_tokens
        else:
            print_warning(f"Index size large ({index_tokens} tokens, target <200)")
            self.results['index_size'] = False
            self.results['index_tokens'] = index_tokens

    def test_domain_coverage(self):
        """Test 3: Check domain coverage."""
        print_header("TEST 3: Domain Coverage")

        if not hasattr(self, 'index'):
            print_error("Index not loaded, skipping test")
            self.results['domain_coverage'] = False
            return

        total = self.index.get('total_entries', 0)
        with_domains = self.index.get('entries_with_domains', 0)
        coverage_pct = self.index.get('coverage_percentage', 0)
        num_domains = len(self.index.get('domains', {}))

        print_info(f"Total entries: {total}")
        print_info(f"With domains: {with_domains} ({coverage_pct}%)")
        print_info(f"Number of domains: {num_domains}")

        # Target: >40% coverage
        if coverage_pct >= 40:
            print_success(f"Domain coverage OK ({coverage_pct}% >= 40%)")
            self.results['domain_coverage'] = True
        else:
            print_warning(f"Domain coverage low ({coverage_pct}%, target >=40%)")
            self.results['domain_coverage'] = False

        self.results['total_entries'] = total
        self.results['with_domains'] = with_domains
        self.results['num_domains'] = num_domains

    def test_token_estimation(self):
        """Test 4: Token reduction calculation."""
        print_header("TEST 4: Token Reduction Analysis")

        if not hasattr(self, 'index'):
            print_error("Index not loaded, skipping test")
            self.results['token_reduction'] = False
            return

        total_tokens = self.index.get('total_tokens_estimate', 0)
        print_info(f"Total tokens (all domains): ~{total_tokens}")

        # Calculate token reduction for 1 domain
        domains = self.index.get('domains', {})
        if not domains:
            print_error("No domains found")
            self.results['token_reduction'] = False
            return

        # Sort domains by size
        sorted_domains = sorted(
            domains.items(),
            key=lambda x: x[1]['token_estimate'],
            reverse=True
        )

        print("\nTop 3 domains by size:")
        for i, (name, data) in enumerate(sorted_domains[:3], 1):
            entries = data['entries']
            tokens = data['token_estimate']
            reduction = ((total_tokens - tokens) / total_tokens * 100) if total_tokens > 0 else 0
            print(f"  {i}. {name:20} {entries:3} entries, ~{tokens:4} tokens ({reduction:.1f}% reduction)")

        # Best case: largest domain
        largest_name, largest_data = sorted_domains[0]
        largest_tokens = largest_data['token_estimate']
        largest_reduction = ((total_tokens - largest_tokens) / total_tokens * 100) if total_tokens > 0 else 0

        print(f"\n{Colors.BOLD}Token Reduction Summary:{Colors.END}")
        print(f"  Full KB: ~{total_tokens} tokens")
        print(f"  Largest domain ({largest_name}): ~{largest_tokens} tokens")
        print(f"  Reduction: {largest_reduction:.1f}%")

        if largest_reduction >= 70:
            print_success(f"Target achieved: {largest_reduction:.1f}% >= 70%")
            self.results['token_reduction'] = True
        else:
            print_warning(f"Below target: {largest_reduction:.1f}% < 70%")
            self.results['token_reduction'] = False

        self.results['total_tokens'] = total_tokens
        self.results['largest_domain_tokens'] = largest_tokens
        self.results['token_reduction_pct'] = largest_reduction

    def test_load_time(self):
        """Test 5: Index load time benchmark."""
        print_header("TEST 5: Load Time Benchmark")

        # Test index load time
        start = time.time()
        try:
            with open(self.domain_index_path, 'r') as f:
                yaml.safe_load(f)
            load_time = time.time() - start

            print_info(f"Index load time: {load_time:.3f} seconds")

            if load_time < 1.0:
                print_success(f"Load time OK ({load_time:.3f}s < 1.0s)")
                self.results['load_time'] = True
            else:
                print_warning(f"Load time slow ({load_time:.3f}s, target <1.0s)")
                self.results['load_time'] = False

            self.results['index_load_time'] = load_time

        except Exception as e:
            print_error(f"Failed to load index: {e}")
            self.results['load_time'] = False

    def test_domain_discovery(self):
        """Test 6: Domain discovery functionality."""
        print_header("TEST 6: Domain Discovery")

        if not hasattr(self, 'index'):
            print_error("Index not loaded, skipping test")
            self.results['domain_discovery'] = False
            return

        domains = self.index.get('domains', {})

        print("Available domains:")
        for name, data in sorted(domains.items(), key=lambda x: x[1]['entries'], reverse=True):
            entries = data['entries']
            tokens = data['token_estimate']
            tags = ', '.join(data['tags'][:3])
            print(f"  • {name:20} {entries:3} entries, ~{tokens:4} tokens [{tags}]")

        if len(domains) >= 10:
            print_success(f"Domain discovery OK ({len(domains)} domains)")
            self.results['domain_discovery'] = True
        else:
            print_warning(f"Few domains ({len(domains)}, target >=10)")
            self.results['domain_discovery'] = False

    def print_summary(self):
        """Print test summary."""
        print_header("TEST SUMMARY")

        total_tests = len(self.results)
        passed_tests = sum(1 for v in self.results.values() if v is True)

        print(f"Tests passed: {passed_tests}/{total_tests}")

        if passed_tests == total_tests:
            print_success(f"{Colors.BOLD}ALL TESTS PASSED!{Colors.END}")
        else:
            print_warning(f"{total_tests - passed_tests} test(s) failed")

        # Metrics
        print(f"\n{Colors.BOLD}Key Metrics:{Colors.END}")

        if 'index_tokens' in self.results:
            print(f"  Index size: {self.results['index_tokens']} tokens")

        if 'token_reduction_pct' in self.results:
            print(f"  Token reduction: {self.results['token_reduction_pct']:.1f}%")

        if 'total_tokens' in self.results:
            print(f"  Full KB tokens: ~{self.results['total_tokens']}")
            print(f"  Single domain: ~{self.results['largest_domain_tokens']}")
            print(f"  Savings: ~{self.results['total_tokens'] - self.results['largest_domain_tokens']} tokens")

        if 'index_load_time' in self.results:
            print(f"  Index load time: {self.results['index_load_time']:.3f}s")

        if 'num_domains' in self.results:
            print(f"  Number of domains: {self.results['num_domains']}")

        # Verdict
        print(f"\n{Colors.BOLD}Verdict:{Colors.END}")

        if self.results.get('token_reduction') and self.results.get('index_size'):
            print_success(f"{Colors.BOLD}Progressive Loading: READY{Colors.END}")
        else:
            print_warning(f"{Colors.BOLD}Progressive Loading: NEEDS IMPROVEMENT{Colors.END}")


def main():
    """Run tests."""
    import argparse

    parser = argparse.ArgumentParser(description='Test progressive loading')
    parser.add_argument('--kb-dir', type=Path, default=Path.cwd(), help='KB directory')
    args = parser.parse_args()

    tester = ProgressiveLoadingTest(args.kb_dir)
    tester.run_all_tests()

    # Exit code based on results
    failed = sum(1 for v in tester.results.values() if v is False)
    return 1 if failed > 0 else 0


if __name__ == '__main__':
    sys.exit(main())
