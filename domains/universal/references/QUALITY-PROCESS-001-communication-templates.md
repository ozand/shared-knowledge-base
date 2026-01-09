# Quality Assurance Pattern - Communication Templates

**Extracted from:** quality-assurance.yaml
**Pattern ID:** QUALITY-PROCESS-001

## Closing PR with Bad Process

**Subject:** ⚠️ PR Closed: Role Violation

This PR has been closed per AGENT-ROLE-SEPARATION-001.

**Role Violation:** Project Agent created PR directly to shared-knowledge-base, bypassing Curator review process.

**Content Quality:** ⭐⭐⭐⭐⭐ (Excellent!)

**Process Quality:** ❌ (Wrong Workflow)

The issue is with the PROCESS, not the CONTENT.

**Correct Workflow:**
1. Create GitHub issue with GITHUB-ATTRIB-001 format
2. Apply labels: agent:*, project:*, agent-type:*
3. Wait for Curator review (24h SLA)
4. Curator validates, enhances, commits to KB

**Next Steps:**
- I've created Issue #N with proper attribution
- Your excellent content is preserved
- After [minor fixes applied], will merge to KB

See AGENT-HANDOFF-001 for full workflow details.

## Requesting Changes

Thank you for your contribution to Shared KB!

**Quality Assessment:** ⭐⭐⭐ (3/5) - Good start, needs improvements

**What's Good:**
- ✅ Proper GitHub issue workflow
- ✅ Correct attribution format
- ✅ Clear problem statement

**What Needs Improvement:**
- ⚠️ [Specific issue 1]
- ⚠️ [Specific issue 2]
- ⚠️ [Specific issue 3]

**Please:**
1. Address the issues above
2. Add [missing information]
3. Test in [environment]

**References:**
- See SHARED-KB-FORMAT-001 for YAML structure
- See YAML-001 for common syntax errors
- Use `python tools/kb.py validate <file>` before updating

## Approving and Merging

Excellent contribution! Merged to Shared KB.

**Quality:** ⭐⭐⭐⭐⭐ (5/5)

**Process:** ✅ Correct workflow

**What Made This Excellent:**
- ✅ Proper GitHub issue with GITHUB-ATTRIB-001 format
- ✅ Comprehensive, production-tested content
- ✅ Clear examples and anti-patterns
- ✅ Well-validated YAML

**Integration:**
- Commit: [commit hash]
- Files: [list of files]
- Entries added: [number]
- Categories updated: [list]

**Impact:**
- [Describe impact, e.g., "+37 entries indexed", "Unblocks v5.1 features"]

Thank you for following AGENT-HANDOFF-001 workflow!

Other agents can now learn from this contribution.
