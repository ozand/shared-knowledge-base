# VPS Knowledge Base

This knowledge base contains **VPS-specific administration patterns, errors, and solutions** based on real-world optimization work on a 2GB RAM VPS.

## Quick Start

### Search Knowledge Base
```bash
# Via vps-admin tool (recommended)
vps-admin kb-search "keyword"

# Examples
vps-admin kb-search "port conflict"
vps-admin kb-search "swap"
vps-admin kb-search "scanner"
vps-admin kb-search "log cleanup"
```

### Direct Access
```bash
# Use kb.py tool directly (from shared-knowledge-base root)
python3 tools/kb.py search "keyword"
python3 tools/kb.py stats

# Rebuild index
python3 tools/kb.py index -v
```

## VPS-Specific Content

### Errors Documented (8 entries)

#### Critical (🔴)
- **VPS-LOG-001**: Massive Log File Consuming Disk Space (48GB 3xui.log)
  - Truncation procedure
  - Logrotate configuration
  - Detection and monitoring

#### High Severity (🟠)
- **VPS-NET-001**: Port 8080 Already in Use - Docker Container Fails to Start
  - Port conflict resolution
  - Service inventory script
  - Prevention strategies

- **VPS-MEM-001**: High Swap Usage Causing Performance Degradation
  - Swap clearing procedure
  - Swappiness optimization
  - Memory monitoring

- **VPS-SEC-001**: Malicious Scanner Making 84% of HTTP Requests
  - IP blocking in Nginx
  - Security hardening
  - Fail2ban integration

#### Medium Severity (🟡)
- **VPS-LOG-002**: Systemd Journal Consuming Excessive Disk Space
- **VPS-MEM-002**: High Memory Usage by Unnecessary Services
- **VPS-SEC-002**: Exposing Docker Services Only to Localhost

#### Low Severity (🟢)
- **VPS-MEM-003**: Docker Container Memory Limits Not Configured

### Best Practices (6 patterns)

1. **VPS-BP-001**: Layered Monitoring Strategy
   - Real-time (bpytop)
   - Quick checks (vps-admin)
   - Log analysis (nginx-stats)
   - Automated monitoring

2. **VPS-BP-002**: Incremental Optimization Approach
   - Measure baseline
   - Make single change
   - Compare results
   - Keep or revert

3. **VPS-BP-003**: Documentation-Driven Administration
   - Document before changes
   - Record exact commands
   - Note results
   - Add to knowledge base

4. **VPS-BP-004**: Security in Layers (Defense in Depth)
   - Network level filtering
   - Application authentication
   - Intrusion detection
   - Log monitoring
   - Offsite backups

5. **VPS-BP-005**: Automated Backup Strategy
   - 3-2-1 backup rule
   - Daily automated backups
   - Offsite via Tailscale
   - Regular testing

6. **VPS-BP-006**: Service Management with Systemd
   - Proper lifecycle management
   - Automatic restart
   - Dependency management
   - Centralized logging

## Usage Examples

### Troubleshooting Port Conflicts
```bash
# Search for port conflict solutions
vps-admin kb-search "port 8080"

# Output shows VPS-NET-001 with:
# - Detection commands (ss, lsof, fuser)
# - Solution steps
# - Prevention scripts
```

### Memory Optimization
```bash
# Search swap-related issues
vps-admin kb-search "swap"

# Results include:
# - VPS-MEM-001: Swap clearing procedure
# - VPS-MEM-002: Memory usage by services
# - Prevention strategies
```

### Security Issues
```bash
# Search for scanner blocking
vps-admin kb-search "scanner"

# Shows:
# - Detection methods
# - Nginx blocking configuration
# - Fail2ban setup
# - Monitoring scripts
```

## Directory Structure

```
shared-knowledge-base/
├── domains/
│   └── vps/
│       ├── errors/
│       │   ├── logs.yaml         # Log management issues
│       │   ├── networking.yaml   # Network & security issues
│       │   └── memory.yaml       # Memory & performance issues
│       └── README.md             # This file
├── tools/
│   └── kb.py                    # Knowledge base CLI tool
└── .kb-config.yaml              # KB configuration
```

## Integration with VPS Tools

The knowledge base is integrated with existing VPS administration tools:

```bash
# vps-admin tool includes KB commands
vps-admin help              # See all commands
vps-admin kb-search <kw>    # Search KB
vps-admin kb-index          # Rebuild index
vps-admin kb-stats          # Show statistics
```

## Adding New Entries

When documenting new VPS issues:

1. **Identify scope**: Should this be in VPS KB or shared KB?
   - VPS-specific: Add to `domains/vps/`
   - Universal: Consider contributing to shared KB

2. **Follow YAML structure**:
   ```yaml
   errors:
     - id: "VPS-XXX-001"
       title: "Descriptive Title"
       severity: "critical|high|medium|low"
       scope: "vps"
       problem: |
         Description of the problem
       symptoms:
         - Symptom 1
         - Symptom 2
       solution:
         code: |
           # Actual commands
         explanation: |
           Why this works
       prevention:
         code: |
           # Prevention steps
   ```

3. **Validate and index**:
   ```bash
   # Validate YAML syntax
   python3 tools/kb.py validate domains/vps/errors/new-file.yaml

   # Rebuild index
   python3 tools/kb.py index -v
   ```

## Related Documentation

- **Server Documentation**: Check your VPS config for local documentation
- **Optimization Guide**: See `domains/universal/patterns/` for optimization patterns
- **Admin Tools**: See `tools/` for available CLI tools

## Maintenance

### Regular Tasks

**Daily** (automated via cron):
- Backup VPS configurations: `sudo vps-backup-simple`
- Check for large log files
- Monitor swap usage

**Weekly**:
- Review KB statistics: `vps-admin kb-stats`
- Check for new scanners: `sudo nginx-stats`
- Verify backups are working

**Monthly**:
- Rebuild KB index: `vps-admin kb-index`
- Audit running services
- Test restore procedure
- Review and update KB entries

### Updating KB from Shared Repository

```bash
# From shared-knowledge-base root
git pull origin main
python3 tools/kb.py index -v
```

## Real-World Results

This knowledge base is based on actual optimization work that achieved:

- **48GB log file** → 332KB (99.9% reduction)
- **Swap usage**: 326MB → 0B
- **Load average**: 1.34 → 0.29 (78% improvement)
- **Available RAM**: 185MB → 712MB (285% increase)
- **Malicious scanner**: Blocked (was 84% of traffic)

## Contributing

When you solve new VPS issues:

1. Document the solution in appropriate YAML file
2. Validate with `vps-admin kb-index`
3. Test search with `vps-admin kb-search "keyword"`
4. If solution is universally applicable, consider contributing to shared KB at:
   https://github.com/ozand/shared-knowledge-base

---

**Last Updated**: 2026-01-05
**Maintained By**: VPS Administrator & Claude Code
**Total Entries**: 37 (8 VPS-specific + 29 shared)
