# GITHUB-006: GitHub API Timeout and Connectivity Handling

## Problem

GitHub CLI (gh) commands fail due to network timeouts, connectivity issues, or API unavailability, causing automated workflows to fail unexpectedly.

**Real example:** When closing Issue #10, connection timeout occurred:

```
Post "https://api.github.com/graphql": dial tcp 140.82.121.6:443: connectex:
A connection attempt failed because the connected party did not properly
respond after a period of time, or established connection failed to respond
```

## Affected Scenarios

- Automated issue closure in CI/CD pipelines
- Bulk PR operations via scripts
- Curator workflows processing multiple issues
- GitHub release automation
- Label management and updates

## Solutions

### Python Retry with Exponential Backoff

```python
import time
import subprocess
from functools import wraps
from typing import Callable, Any

def retry_github_command(max_retries: int = 3, base_delay: float = 1.0):
    """
    Retry decorator for GitHub CLI commands with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds (multiplied by 2^attempt)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None

            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (subprocess.CalledProcessError,
                      OSError,
                      TimeoutError) as e:
                    last_exception = e

                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt)
                        print(f"  ⚠️  GitHub API failed (attempt {attempt + 1}/{max_retries})")
                        print(f"  🔄 Retrying in {delay:.1f}s...")
                        time.sleep(delay)
                    else:
                        print(f"  ❌ All {max_retries} attempts failed")

            raise last_exception
        return wrapper
    return decorator

# Usage:
@retry_github_command(max_retries=3, base_delay=2.0)
def close_issue(issue_number: int, comment: str):
    cmd = [
        'gh', 'issue', 'close', str(issue_number),
        '--comment', comment
    ]
    subprocess.run(cmd, check=True, capture_output=True)

# Try it:
close_issue(10, "Issue resolved")
```

**Pros:** Automatic retry, exponential backoff prevents API overload
**Cons:** Requires Python, adds code complexity

### Bash Retry Wrapper

```bash
#!/bin/bash
# retry_github.sh - Retry GitHub CLI commands with backoff

retry_gh() {
    local max_attempts=$1
    shift
    local command=("$@")

    for ((attempt=1; attempt<=max_attempts; attempt++)); do
        echo "🔄 Attempt $attempt/$max_attempts: ${command[*]}"

        if "${command[@]}"; then
            echo "✅ Success on attempt $attempt"
            return 0
        else
            exit_code=$?
            if [ $attempt -lt $max_attempts ]; then
                delay=$((2 ** (attempt - 1)))
                echo "⚠️  Failed (exit code: $exit_code)"
                echo "⏳ Waiting ${delay}s before retry..."
                sleep $delay
            else
                echo "❌ All $max_attempts attempts failed"
                return $exit_code
            fi
        fi
    done
}

# Usage examples:
retry_gh 3 gh issue close 10 --comment "Resolved"
retry_gh 3 gh pr create --title "Fix bug" --body "Description"
retry_gh 3 gh release create v1.0 --notes "Release notes"
```

**Pros:** Pure bash, works in scripts, simple to understand
**Cons:** No exponential backoff (unless enhanced), bash syntax limitations

### Graceful Degradation

Queue failed operations for manual retry:

```python
import json
from datetime import datetime
from pathlib import Path

class PendingOperations:
    """Queue GitHub operations that failed due to connectivity"""

    def __init__(self, queue_file: Path = Path('.pending_operations.json')):
        self.queue_file = queue_file
        self.queue = self._load_queue()

    def _load_queue(self):
        if self.queue_file.exists():
            with self.queue_file.open() as f:
                return json.load(f)
        return []

    def _save_queue(self):
        with self.queue_file.open('w') as f:
            json.dump(self.queue, f, indent=2)

    def add(self, operation: str, params: dict):
        """Add failed operation to queue"""
        self.queue.append({
            'operation': operation,
            'params': params,
            'timestamp': datetime.now().isoformat(),
            'retries': 0
        })
        self._save_queue()

    def process(self, executor: Callable):
        """
        Process queued operations

        Args:
            executor: Function that takes (operation, params) and executes
        """
        remaining = []

        for item in self.queue:
            try:
                executor(item['operation'], item['params'])
                print(f"✅ Processed: {item['operation']}")
            except Exception as e:
                item['retries'] += 1
                if item['retries'] < 3:
                    print(f"⚠️  Queued for later: {item['operation']}")
                    remaining.append(item)
                else:
                    print(f"❌ Gave up after 3 retries: {item['operation']}")

        self.queue = remaining
        self._save_queue()

# Usage:
pending = PendingOperations()

def close_issue_safe(issue_number: int, comment: str):
    try:
        subprocess.run(['gh', 'issue', 'close', str(issue_number),
                      '--comment', comment], check=True)
    except Exception as e:
        print(f"⚠️  Failed to close issue #{issue_number}: {e}")
        pending.add('close_issue', {
            'issue': issue_number,
            'comment': comment
        })

# Later, when connectivity improves:
pending.process(lambda op, params: subprocess.run(
    ['gh', 'issue', 'close', str(params['issue']),
     '--comment', params['comment']],
    check=True
))
```

**Pros:** No work lost, can retry later, audit trail
**Cons:** Requires manual re-run or scheduled job

### Pre-Flight Check

Check connectivity before attempting operations:

```bash
#!/bin/bash
# check_github_connectivity.sh

check_github() {
    echo "🔍 Checking GitHub connectivity..."

    # Test 1: DNS resolution
    if ! nslookup api.github.com >/dev/null 2>&1; then
        echo "❌ Cannot resolve api.github.com"
        return 1
    fi

    # Test 2: TCP connection
    if ! bash -c 'cat < /dev/null > /dev/tcp/api.github.com/443' 2>/dev/null; then
        echo "❌ Cannot connect to api.github.com:443"
        return 1
    fi

    # Test 3: gh CLI auth
    if ! gh auth status >/dev/null 2>&1; then
        echo "❌ gh auth failed - not authenticated"
        return 1
    fi

    # Test 4: Simple API call
    if ! gh api /user >/dev/null 2>&1; then
        echo "❌ GitHub API not responding"
        return 1
    fi

    echo "✅ GitHub connectivity confirmed"
    return 0
}

# Usage in scripts:
if ! check_github; then
    echo "⚠️  GitHub is not accessible, queuing operations"
    # Queue operations or exit gracefully
    exit 1
fi

# Proceed with GitHub operations
gh issue close 10 --comment "..."
```

**Pros:** Fail fast, clear error messages, prevents partial failures
**Cons:** Adds latency, doesn't handle mid-operation failures

## Best Practices

1. **Use exponential backoff for retries**
   - Reason: Prevents API overload, gives network time to recover

2. **Set maximum retry limit (3-5 attempts)**
   - Reason: Don't retry indefinitely, fail eventually

3. **Log all retries with timestamps**
   - Reason: Debugging, audit trail, capacity planning

4. **Check connectivity before bulk operations**
   - Reason: Fail fast instead of processing half the items

5. **Queue failed operations for retry**
   - Reason: Don't lose work, can recover when connectivity returns

6. **Use timeouts on all gh commands**
   - Example: `gh issue close 10 --comment '...' --timeout 30`

## Anti-Patterns

### Anti-Pattern 1: Infinite retry without backoff

```python
# ❌ WRONG
while ! gh issue close 10; do
    echo "Retrying..."
    # No delay, no limit
done
```

**Why wrong:** Overloads API, never fails, wastes resources
**Correct:** Use retry with exponential backoff and max attempts

### Anti-Pattern 2: Silent failure handling

```python
# ❌ WRONG
try:
    gh issue close 10
except:
    pass  # Ignore all errors
```

**Why wrong:** Loses work, no error visibility, can't debug
**Correct:** Log error, queue operation, raise alert

### Anti-Pattern 3: No timeout on long-running operations

```python
# ❌ WRONG - May hang forever
subprocess.run(['gh', 'pr', 'create', ...])
```

**Why wrong:** Script hangs indefinitely, blocks pipeline

**Correct:**
```python
subprocess.run(['gh', 'pr', 'create', ...], timeout=60)
```

## Implementation Example

**Scenario:** Curator closing multiple issues after review

**Without resilience:**
```python
# ❌ Fails completely on first network issue
issues = [8, 9, 10]
for issue in issues:
    subprocess.run(['gh', 'issue', 'close', str(issue)])
# If issue 8 fails due to timeout, 9 and 10 never closed
```

**With resilience:**
```python
# ✅ Handles failures gracefully
from retry_github import retry_github_command
import json

pending = PendingOperations()

@retry_github_command(max_retries=3, base_delay=2.0)
def close_issue(issue_number: int, comment: str):
    subprocess.run(
        ['gh', 'issue', 'close', str(issue_number),
         '--comment', comment],
        check=True, timeout=30
    )

# Process all issues
issues = {
    8: "Closed: 5 patterns need YAML fixes",
    9: "Closed: kb_config.py module merged",
    10: "Closed: Indexing bug fixed"
}

for issue_number, comment in issues.items():
    try:
        close_issue(issue_number, comment)
        print(f"✅ Closed issue #{issue_number}")
    except Exception as e:
        print(f"⚠️  Failed to close #{issue_number}: {e}")
        pending.add('close_issue', {
            'issue': issue_number,
            'comment': comment
        })

# Report queued operations
if pending.queue:
    print(f"\n⚠️  {len(pending.queue)} operations queued for later:")
    print(f"   Run: python process_pending.py")
```

## Monitoring

### Metrics to Track

1. **GitHub API failure rate**
   - Calculation: `failed_requests / total_requests`
   - Threshold: < 5%

2. **Average retry count**
   - Calculation: `sum(retries) / successful_requests`
   - Threshold: < 1.5

3. **Pending operations queue size**
   - Check: `len(pending.queue)`
   - Alert if: '> 10 operations'

### Logging Example

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('github_operations.log'),
        logging.StreamHandler()
    ]
)

# In retry decorator:
logging.warning(f"GitHub API failed (attempt {attempt + 1}): {e}")
```

## Real-World Examples

### Example 1: Issue #10 closure failure

**Context:** Issue #10 closure failure
**Error:** `Post https://api.github.com/graphql: dial tcp 140.82.121.6:443: connectex`

**Workaround used:**
```bash
# Manually closed when connectivity returned
gh issue close 10 --comment "..."
```

**Better approach:**
```python
# Should have used retry decorator
@retry_github_command(max_retries=3)
def close_issue_with_comment():
    with open('tmp/issue-10-comment.md') as f:
        comment = f.read()
    subprocess.run(['gh', 'issue', 'close', '10',
                  '--comment', comment], check=True)
```

## Troubleshooting

**Issue:** Intermittent GitHub API failures

**Diagnosis:**
1. Check GitHub status: https://www.githubstatus.com/
2. Test connectivity: `check_github()`
3. Review logs: `tail -f github_operations.log`
4. Check rate limits: `gh api /rate_limit`

**Solutions:**
1. Implement retry logic (see solutions above)
2. Check for GitHub API incidents
3. Verify network stability
4. Check gh authentication: `gh auth status`

## Related Patterns

- **GITHUB-001:** Git Hooks with Python Scripts Fail on Windows (related)
- **GITHUB-005:** Git Push Rejected (related)
  - Both cover network-related git operations failures
