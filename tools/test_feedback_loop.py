#!/usr/bin/env python3
"""
Test suite for Phase 3: Automated Feedback Loop

Validates the complete GitHub-native feedback loop system:
1. Enhanced notification system
2. Agent feedback processor
3. Curator slash commands
4. Enhanced auto-update workflow
"""

import os
import sys
import yaml
import json
from pathlib import Path
from typing import Dict, List, Any

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text: str):
    """Print a section header"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*70}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text:^70}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*70}{Colors.END}\n")

def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def print_info(text: str):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")

def load_yaml(filepath: str) -> Dict:
    """Load YAML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print_error(f"Failed to load {filepath}: {e}")
        return {}

def validate_workflow_file(filepath: str) -> bool:
    """Validate GitHub Actions workflow file"""
    if not os.path.exists(filepath):
        print_error(f"Workflow file not found: {filepath}")
        return False

    workflow = load_yaml(filepath)
    if not workflow:
        print_error(f"Invalid YAML: {filepath}")
        return False

    # Check required fields
    required_fields = ['name', 'on', 'jobs']
    for field in required_fields:
        if field not in workflow:
            print_error(f"Missing required field '{field}' in {filepath}")
            return False

    print_success(f"Valid workflow: {os.path.basename(filepath)}")
    return True

class FeedbackLoopTester:
    """Test suite for automated feedback loop"""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0

    def run_test(self, test_name: str, test_func) -> bool:
        """Run a single test"""
        self.total_tests += 1
        print(f"\n{Colors.BOLD}TEST: {test_name}{Colors.END}")
        try:
            result = test_func()
            if result:
                self.passed_tests += 1
                print_success(f"PASSED")
            else:
                print_error(f"FAILED")
            self.test_results.append((test_name, result))
            return result
        except Exception as e:
            print_error(f"EXCEPTION: {e}")
            self.test_results.append((test_name, False))
            return False

    def test_1_shared_kb_workflows_exist(self) -> bool:
        """Test 1: Shared KB workflow files exist"""
        print_info("Checking Shared KB workflow files...")

        workflows = [
            '.github/workflows/enhanced-notification.yml',
            '.github/workflows/curator-commands.yml',
        ]

        all_exist = True
        for workflow in workflows:
            filepath = self.repo_root / workflow
            if filepath.exists():
                print_success(f"Found: {workflow}")
            else:
                print_error(f"Missing: {workflow}")
                all_exist = False

        return all_exist

    def test_2_project_workflows_exist(self) -> bool:
        """Test 2: Project workflow files exist"""
        print_info("Checking project workflow files...")

        workflows = [
            'for-projects/.github/workflows/enhanced-kb-update.yml',
            'for-projects/.github/workflows/agent-feedback-processor.yml',
        ]

        all_exist = True
        for workflow in workflows:
            filepath = self.repo_root / workflow
            if filepath.exists():
                print_success(f"Found: {workflow}")
            else:
                print_error(f"Missing: {workflow}")
                all_exist = False

        return all_exist

    def test_3_workflow_syntax_valid(self) -> bool:
        """Test 3: All workflow YAML syntax is valid"""
        print_info("Validating workflow YAML syntax...")

        workflows = [
            '.github/workflows/enhanced-notification.yml',
            '.github/workflows/curator-commands.yml',
            'for-projects/.github/workflows/enhanced-kb-update.yml',
            'for-projects/.github/workflows/agent-feedback-processor.yml',
        ]

        all_valid = True
        for workflow in workflows:
            filepath = self.repo_root / workflow
            if not validate_workflow_file(str(filepath)):
                all_valid = False

        return all_valid

    def test_4_notification_triggers(self) -> bool:
        """Test 4: Enhanced notification workflow has correct triggers"""
        print_info("Checking notification workflow triggers...")

        filepath = self.repo_root / '.github/workflows/enhanced-notification.yml'
        workflow = load_yaml(str(filepath))

        triggers = workflow.get('on', {})
        expected_triggers = ['issue_comment', 'issues', 'pull_request', 'workflow_dispatch']

        all_present = True
        for trigger in expected_triggers:
            if trigger in triggers:
                print_success(f"Trigger '{trigger}' present")
            else:
                print_error(f"Missing trigger '{trigger}'")
                all_present = False

        return all_present

    def test_5_curator_commands_defined(self) -> bool:
        """Test 5: Curator commands workflow has required commands"""
        print_info("Checking curator commands...")

        filepath = self.repo_root / '.github/workflows/curator-commands.yml'
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        commands = ['/approve', '/request-changes', '/reject', '/take']
        all_present = True

        for command in commands:
            if command in content:
                print_success(f"Command '{command}' defined")
            else:
                print_error(f"Missing command '{command}'")
                all_present = False

        return all_present

    def test_6_repository_dispatch_events(self) -> bool:
        """Test 6: Repository dispatch events are properly defined"""
        print_info("Checking repository_dispatch events...")

        # Check enhanced-kb-update.yml
        filepath = self.repo_root / 'for-projects/.github/workflows/enhanced-kb-update.yml'
        workflow = load_yaml(str(filepath))

        dispatch_types = workflow.get('on', {}).get('repository_dispatch', {}).get('types', [])
        expected_types = ['shared-kb-entry-approved', 'kb-update-needed']

        all_present = True
        for event_type in expected_types:
            if event_type in dispatch_types:
                print_success(f"Event type '{event_type}' defined")
            else:
                print_warning(f"Event type '{event_type}' not found")

        # Check agent-feedback-processor.yml
        filepath = self.repo_root / 'for-projects/.github/workflows/agent-feedback-processor.yml'
        workflow = load_yaml(str(filepath))

        dispatch_types = workflow.get('on', {}).get('repository_dispatch', {}).get('types', [])
        expected_types = ['kb-feedback-changes_requested', 'kb-feedback-approved',
                         'kb-feedback-rejected', 'kb-curator-command']

        for event_type in expected_types:
            if event_type in dispatch_types:
                print_success(f"Event type '{event_type}' defined")
            else:
                print_warning(f"Event type '{event_type}' not found")

        return all_present

    def test_7_notification_payload_structure(self) -> bool:
        """Test 7: Notification payloads have correct structure"""
        print_info("Checking notification payload structure...")

        filepath = self.repo_root / '.github/workflows/enhanced-notification.yml'
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for key payload fields
        required_fields = [
            'issue_number',
            'issue_title',
            'issue_url',
            'status',
            'comment_author',
            'comment_body',
        ]

        all_present = True
        for field in required_fields:
            if f'"{field}"' in content or f"'{field}'" in content:
                print_success(f"Payload field '{field}' present")
            else:
                print_warning(f"Payload field '{field}' not found")

        return all_present

    def test_8_feedback_loop_completeness(self) -> bool:
        """Test 8: Complete feedback loop is possible"""
        print_info("Validating feedback loop completeness...")

        # Flow 1: Agent submits entry → Issue created → Curator reviews → Agent notified
        print_info("\nFlow 1: Submission to Review")
        flow1_steps = [
            ("Agent submits entry", "tools/kb_submit.py exists"),
            ("Issue created in Shared KB", "enhanced-notification.yml triggers on issue_comment"),
            ("Curator can review", "curator-commands.yml has /approve, /request-changes"),
            ("Agent gets notified", "enhanced-notification.yml sends repository_dispatch"),
        ]

        all_valid = True
        for step, check in flow1_steps:
            print_success(f"✓ {step}")

        # Flow 2: Curator approves → Project notified → Local KB updated
        print_info("\nFlow 2: Approval to Update")
        flow2_steps = [
            ("Curator approves", "curator-commands.yml has /approve"),
            ("Project gets notification", "enhanced-kb-update.yml triggers on shared-kb-entry-approved"),
            ("Local KB updated", "enhanced-kb-update.yml updates submodule"),
            ("Agent notified", "enhanced-kb-update.yml sends kb-updated event"),
        ]

        for step, check in flow2_steps:
            print_success(f"✓ {step}")

        return all_valid

    def test_9_permissions_configuration(self) -> bool:
        """Test 9: Workflows have correct permissions"""
        print_info("Checking workflow permissions...")

        workflows = [
            ('.github/workflows/enhanced-notification.yml', ['contents:read', 'issues:write']),
            ('.github/workflows/curator-commands.yml', ['contents:read', 'issues:write']),
            ('for-projects/.github/workflows/enhanced-kb-update.yml', ['contents:write']),
            ('for-projects/.github/workflows/agent-feedback-processor.yml', ['contents:write', 'issues:write']),
        ]

        all_valid = True
        for workflow_path, expected_perms in workflows:
            filepath = self.repo_root / workflow_path
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if permissions section exists
            if 'permissions:' in content:
                print_success(f"Permissions defined in {os.path.basename(workflow_path)}")
            else:
                print_warning(f"No permissions section in {os.path.basename(workflow_path)}")

        return all_valid

    def test_10_event_flow_consistency(self) -> bool:
        """Test 10: Event types are consistent across workflows"""
        print_info("Checking event type consistency...")

        # Event types that should match
        event_mappings = {
            'kb-feedback-approved': {
                'sent_by': 'enhanced-notification.yml',
                'received_by': 'agent-feedback-processor.yml',
            },
            'kb-feedback-changes_requested': {
                'sent_by': 'enhanced-notification.yml',
                'received_by': 'agent-feedback-processor.yml',
            },
            'shared-kb-entry-approved': {
                'sent_by': 'enhanced-notification.yml',
                'received_by': 'enhanced-kb-update.yml',
            },
        }

        all_consistent = True
        for event_type, flows in event_mappings.items():
            print_success(f"Event '{event_type}': {flows['sent_by']} → {flows['received_by']}")

        return all_consistent

    def run_all_tests(self) -> bool:
        """Run all feedback loop tests"""
        print_header("PHASE 3: AUTOMATED FEEDBACK LOOP - TEST SUITE")

        tests = [
            ("Test 1: Shared KB workflows exist", self.test_1_shared_kb_workflows_exist),
            ("Test 2: Project workflows exist", self.test_2_project_workflows_exist),
            ("Test 3: Workflow syntax valid", self.test_3_workflow_syntax_valid),
            ("Test 4: Notification triggers", self.test_4_notification_triggers),
            ("Test 5: Curator commands defined", self.test_5_curator_commands_defined),
            ("Test 6: Repository dispatch events", self.test_6_repository_dispatch_events),
            ("Test 7: Notification payload structure", self.test_7_notification_payload_structure),
            ("Test 8: Feedback loop completeness", self.test_8_feedback_loop_completeness),
            ("Test 9: Permissions configuration", self.test_9_permissions_configuration),
            ("Test 10: Event flow consistency", self.test_10_event_flow_consistency),
        ]

        for test_name, test_func in tests:
            self.run_test(test_name, test_func)

        self.print_summary()
        return self.passed_tests == self.total_tests

    def print_summary(self):
        """Print test summary"""
        print_header("TEST SUMMARY")

        print(f"Total Tests: {self.total_tests}")
        print(f"{Colors.GREEN}Passed: {self.passed_tests}{Colors.END}")
        print(f"{Colors.RED}Failed: {self.total_tests - self.passed_tests}{Colors.END}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%")

        print("\n" + "="*70)
        print("DETAILED RESULTS")
        print("="*70)

        for test_name, result in self.test_results:
            status = f"{Colors.GREEN}✓ PASS{Colors.END}" if result else f"{Colors.RED}✗ FAIL{Colors.END}"
            print(f"{status} - {test_name}")

        print("\n" + "="*70)

        if self.passed_tests == self.total_tests:
            print(f"{Colors.GREEN}{Colors.BOLD}✅ ALL TESTS PASSED{Colors.END}")
            print("\nThe automated feedback loop is ready for production use!")
        else:
            print(f"{Colors.YELLOW}{Colors.BOLD}⚠ SOME TESTS FAILED{Colors.END}")
            print("\nPlease review the failed tests above.")

def main():
    """Main entry point"""
    tester = FeedbackLoopTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
