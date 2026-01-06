# Shared KB Setup Scripts

This directory contains scripts to help set up the Shared Knowledge Base in your project.

## Available Scripts

### setup-shared-kb-sparse.sh / setup-shared-kb-sparse.ps1

**Purpose:** Setup Shared KB as a git submodule with sparse checkout

**What it does:**
- Adds shared-knowledge-base as a git submodule
- Configures sparse checkout to load only Project Agent content
- Excludes Curator-specific files (curator/, analysis files, reports)
- Reduces repository size and context pollution

**Usage:**

Linux/Mac:
```bash
cd /path/to/your/project
bash /path/to/shared-knowledge-base/scripts/setup-shared-kb-sparse.sh
```

Windows (PowerShell):
```powershell
cd C:\path\to\your\project
powershell -ExecutionPolicy Bypass -File C:\path\to\shared-knowledge-base\scripts\setup-shared-kb-sparse.ps1
```

**What gets loaded:**
- ✅ Patterns (universal/, python/, postgresql/, docker/, javascript/)
- ✅ Documentation (README.md, GUIDE.md, agent guides)
- ✅ Tools (tools/kb.py, scripts/)

**What gets excluded:**
- ❌ curator/ (Curator instructions, workflows, prompts)
- ❌ *_ANALYSIS.md (analysis documents)
- ❌ *_REPORT.md (Curator reports)
- ❌ CHAT_*.md (chat analysis)
- ❌ Generated files (.agent-config.local, _index*.yaml)

**Manual Setup (Alternative):**

If you prefer to set up manually:

```bash
# 1. Add submodule
git submodule add https://github.com/ozand/shared-knowledge-base.git \
  docs/knowledge-base/shared

# 2. Enable sparse checkout
cd docs/knowledge-base/shared
git config core.sparseCheckout true

# 3. Create sparse-checkout file
cat > .git/info/sparse-checkout <<'EOF'
# Core documentation
README.md
GUIDE.md
QUICKSTART.md
README_INTEGRATION.md

# Agent guides
AGENT_INTEGRATION_GUIDE.md
AGENT_AUTOCONFIG_GUIDE.md
ROLE_SEPARATION_GUIDE.md
GITHUB_ATTRIBUTION_GUIDE.md

# Patterns (MAIN CONTENT)
universal/
python/
postgresql/
docker/
javascript/
vps/

# Tools
tools/
scripts/

# Base configuration
.kb-config.yaml
.gitignore.agents
EOF

# 4. Pull only specified content
git pull origin main
```

## Updating Shared KB

After setup, update to latest version:

```bash
# Submodule approach
git submodule update --remote --merge docs/knowledge-base/shared

# Check for updates first
python docs/knowledge-base/shared/tools/kb.py check-updates
```

## Why Sparse Checkout?

**Problem:**
- Git submodule loads ENTIRE repository
- Includes Curator-specific files (~377K)
- Agents see irrelevant documentation
- Context pollution

**Solution:**
- Sparse checkout loads only specified paths
- Excludes Curator content
- Clean context for Project Agents
- ~22% size reduction

**See also:** `SUBMODULE_CONTEXT_CONTAMINATION_ANALYSIS.md`

## Other Scripts

- `daily_freshness.py` - Check entry freshness daily
- `weekly_usage.py` - Analyze usage patterns weekly
- `monthly_community.py` - Community contributions monthly
- `init_metadata.py` - Initialize metadata for KB entries
- `migrate_to_clean_structure.sh` - Migrate to new structure

## Troubleshooting

**Issue:** "Submodule already exists"

**Solution:**
```bash
git submodule deinit -f docs/knowledge-base/shared
rm -rf docs/knowledge-base/shared
git rm -f docs/knowledge-base/shared
```

Then run setup script again.

**Issue:** "Permission denied" on Linux/Mac

**Solution:**
```bash
chmod +x scripts/setup-shared-kb-sparse.sh
```

**Issue:** PowerShell execution policy

**Solution:**
```powershell
powershell -ExecutionPolicy Bypass -File scripts/setup-shared-kb-sparse.ps1
```

## Related Documentation

- `SUBMODULE_CONTEXT_CONTAMINATION_ANALYSIS.md` - Detailed analysis
- `SUBMODULE_VS_CLONE.md` - Submodule vs clone comparison
- `README.md` - Main Shared KB README
- `AGENT_INTEGRATION_GUIDE.md` - Agent integration guide
