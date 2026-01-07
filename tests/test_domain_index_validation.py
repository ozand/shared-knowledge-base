"""
Tests for _domain_index.yaml validation and kb_domains.py compatibility.

This test suite ensures that:
1. _domain_index.yaml follows v4.0.0 specification
2. Tools work correctly with the flat format
3. No regression in domain index handling
"""

import pytest
import yaml
import subprocess
from pathlib import Path


class TestDomainIndexFormat:
    """Test that _domain_index.yaml follows correct v4.0.0 format."""

    @pytest.fixture
    def domain_index_path(self):
        return Path("_domain_index.yaml")

    @pytest.fixture
    def domain_index(self, domain_index_path):
        with open(domain_index_path) as f:
            return yaml.safe_load(f)

    def test_required_fields_present(self, domain_index):
        """Test that all required fields are present."""
        required_fields = [
            'version',
            'last_updated',
            'total_entries',
            'entries_with_domains',
            'coverage_percentage',
            'domains'
        ]

        for field in required_fields:
            assert field in domain_index, f"Missing required field: {field}"

    def test_domains_use_flat_format(self, domain_index):
        """Test that domains use flat format (int values), not nested dict."""
        domains = domain_index.get('domains', {})

        for domain_name, value in domains.items():
            # Must be int (flat format)
            assert isinstance(value, int), \
                f"Domain {domain_name} must be int (flat format), got {type(value).__name__}"

            # Must NOT be dict (nested format - wrong for v4.0.0)
            assert not isinstance(value, dict), \
                f"Domain {domain_name} should NOT be dict in v4.0.0"

    def test_domain_names_are_valid(self, domain_index):
        """Test that all domain names are from the valid set."""
        valid_domains = {
            'api', 'asyncio', 'authentication', 'claude-code',
            'deployment', 'docker', 'fastapi', 'monitoring',
            'performance', 'postgresql', 'security', 'testing', 'websocket'
        }

        domains = domain_index.get('domains', {})

        for domain_name in domains.keys():
            assert domain_name in valid_domains, \
                f"Unknown domain: {domain_name}. Valid domains: {valid_domains}"

    def test_no_extra_fields_in_domains(self, domain_index):
        """Test that domains don't have nested structure with extra fields."""
        domains = domain_index.get('domains', {})

        for domain_name, value in domains.items():
            # In flat format, value is just an int
            if isinstance(value, dict):
                # This is wrong for v4.0.0!
                extra_fields = set(value.keys()) - {'entries', 'token_estimate', 'tags', 'description'}
                if extra_fields:
                    pytest.fail(
                        f"Domain {domain_name} has unexpected nested structure. "
                        f"v4.0.0 uses flat format: {domain_name}: <int>"
                    )

    def test_version_format(self, domain_index):
        """Test that version follows expected format."""
        version = domain_index.get('version')

        assert version is not None
        assert isinstance(version, str)

        # Should be in format "X.Y"
        parts = version.split('.')
        assert len(parts) == 2, f"Version should be 'X.Y', got {version}"

        major, minor = parts
        assert major.isdigit() and minor.isdigit()


class TestKbDomainsCompatibility:
    """Test that kb_domains.py works correctly with flat format."""

    def test_kb_domains_list_command(self):
        """Test that kb_domains.py list works without errors."""
        result = subprocess.run(
            ['python', 'tools/kb_domains.py', 'list'],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Should succeed (exit code 0)
        assert result.returncode == 0, \
            f"kb_domains.py list failed with error:\n{result.stderr}"

        # Should show domain list
        output = result.stdout
        assert "Knowledge Base Domains" in output
        assert "entries" in output

        # Should not show TypeError
        assert "TypeError" not in result.stderr
        assert "'int' object is not subscriptable" not in result.stderr

    def test_kb_domains_handles_flat_format(self):
        """Test that kb_domains.py correctly handles flat domain format."""
        result = subprocess.run(
            ['python', 'tools/kb_domains.py', 'list'],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Should show domains
        output = result.stdout
        assert "docker" in output
        assert "testing" in output
        assert "postgresql" in output

        # Should show entry counts
        assert "entries" in output

    def test_kb_domains_list_sorted_by_entries(self):
        """Test that domains are sorted by entry count (descending)."""
        result = subprocess.run(
            ['python', 'tools/kb_domains.py', 'list'],
            capture_output=True,
            text=True,
            timeout=30
        )

        output = result.stdout
        lines = output.split('\n')

        # Extract entry counts from lines like "docker                11 entries"
        entry_counts = []
        for line in lines:
            if 'entries' in line:
                try:
                    # Extract number before "entries"
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == 'entries' and i > 0:
                            count = int(parts[i-1])
                            entry_counts.append(count)
                            break
                except (ValueError, IndexError):
                    continue

        # Check that counts are in descending order
        assert entry_counts == sorted(entry_counts, reverse=True), \
            "Domains should be sorted by entry count (descending)"


class TestDomainIndexValidation:
    """Test validation functionality for domain index."""

    def test_validate_domain_index_flat_format(self):
        """Validation function for flat format."""
        index_path = Path("_domain_index.yaml")

        with open(index_path) as f:
            index = yaml.safe_load(f)

        domains = index.get('domains', {})

        # All domains should use flat format
        for domain_name, value in domains.items():
            assert isinstance(value, int), \
                f"Domain {domain_name} must use flat format (int), got {type(value)}"

    def test_domain_index_matches_v4_spec(self):
        """Test that domain index matches v4.0.0 specification."""
        index_path = Path("_domain_index.yaml")

        with open(index_path) as f:
            index = yaml.safe_load(f)

        # Version should be 2.0 or higher
        version = index.get('version', '0.0')
        major_version = int(version.split('.')[0])

        assert major_version >= 2, \
            f"Domain index version should be >= 2.0, got {version}"


class TestCommonMistakes:
    """Test detection of common mistakes from tmp/tmp1.txt analysis."""

    def test_no_token_estimate_field(self):
        """Test that token_estimate field is NOT present (not in v4.0.0 spec)."""
        index_path = Path("_domain_index.yaml")

        with open(index_path) as f:
            index = yaml.safe_load(f)

        domains = index.get('domains', {})

        for domain_name, value in domains.items():
            # In v4.0.0, value is int, not dict
            # If it's a dict, someone added token_estimate incorrectly
            if isinstance(value, dict):
                assert 'token_estimate' not in value, \
                    f"Domain {domain_name} has token_estimate field " \
                    f"which is NOT in v4.0.0 specification"

    def test_no_tags_field(self):
        """Test that tags field is NOT present (not in v4.0.0 spec)."""
        index_path = Path("_domain_index.yaml")

        with open(index_path) as f:
            index = yaml.safe_load(f)

        domains = index.get('domains', {})

        for domain_name, value in domains.items():
            if isinstance(value, dict):
                assert 'tags' not in value, \
                    f"Domain {domain_name} has tags field " \
                    f"which is NOT in v4.0.0 specification"

    def test_no_description_field(self):
        """Test that description field is NOT present (not in v4.0.0 spec)."""
        index_path = Path("_domain_index.yaml")

        with open(index_path) as f:
            index = yaml.safe_load(f)

        domains = index.get('domains', {})

        for domain_name, value in domains.items():
            if isinstance(value, dict):
                assert 'description' not in value, \
                    f"Domain {domain_name} has description field " \
                    f"which is NOT in v4.0.0 specification"


if __name__ == '__main__':
    # Run tests
    pytest.main([__file__, '-v'])
