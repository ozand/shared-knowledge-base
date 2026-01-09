# GITHUB-002: Git Tag vs GitHub Release - Understanding the Difference

## Problem

Developers create git tags but don't see releases on GitHub Releases page.

**Common misconception:** "Creating a git tag automatically creates a GitHub Release"

## Explanation

Git tags and GitHub Releases are separate concepts:

### Git Tag (git reference)
- Points to specific commit
- Created with: `git tag v5.1`
- Stored in git history
- Visible in: git log, GitHub commits page

### GitHub Release (release object)
- Has title, description, release notes
- Can have binary attachments
- Visible on: GitHub Releases page
- Created via: `gh release create` OR GitHub web UI
- Links to git tag but is NOT created automatically

## Wrong Approach

Create tag and assume Release is created:

```bash
git tag -a v5.1 -m "Release v5.1"
git push origin v5.1
# ❌ Nothing appears on GitHub Releases page!
```

## Correct Approach

Create tag AND GitHub Release:

```bash
# 1. Update documentation
vim README.md  # Update version to 3.0
git add README.md
git commit -m "Release v5.1: Update docs"

# 2. Push commits
git push origin main

# 3. Create and push tag
git tag -a v5.1 -m "Release v5.1"
git push origin v5.1

# 4. Create GitHub Release
gh release create v5.1 \
  --title "v5.1: Release Title" \
  --notes "Release notes here..."
```

## Automated Workflow

Create release with notes from file:

```bash
#!/bin/bash
VERSION=$1
NOTES_FILE="RELEASE_NOTES.md"

# Update docs
sed -i "s/Version .*/Version $VERSION/" README.md
git add README.md
git commit -m "Release $VERSION: Update docs"
git push

# Create tag
git tag -a $VERSION -m "Release $VERSION"
git push origin $VERSION

# Create GitHub Release
gh release create $VERSION \
  --title "Release $VERSION" \
  --notes-file $NOTES_FILE
```

## GitHub CLI Usage

### Installation

```bash
# Windows
winget install --id GitHub.cli

# Authenticate
gh auth login
```

### Create Basic Release

```bash
gh release create v1.0 \
  --title "Version 1.0" \
  --notes "Release notes here"
```

### Create from File

```bash
gh release create v1.0 \
  --title "Version 1.0" \
  --notes-file RELEASE_NOTES.md
```

### Create with Assets

```bash
gh release create v1.0 \
  --notes "Release" \
  ./build/app.zip \
  ./dist/installer.exe
```

### Create Prerelease

```bash
gh release create v1.0-beta \
  --prerelease \
  --notes "Beta release"
```

## Best Practices

1. Always update README.md before creating release
2. Use semantic versioning (v1.0.0)
3. Include release notes with breaking changes
4. Test release on beta channel first
5. Keep CHANGELOG.md in sync with releases

## Troubleshooting

**Issue:** Need to update release

**Solution:**
```bash
# Delete old release and tag
gh release delete v1.0
git tag -d v1.0
git push origin :refs/tags/v1.0

# Recreate
# [follow correct_approach steps]
```

## References

- [About Git Hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)
- [GitHub Releases API](https://docs.github.com/en/rest/releases/releases)
- [GitHub CLI Manual](https://cli.github.com/manual/)
