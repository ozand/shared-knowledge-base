# PostgreSQL Knowledge Base

This section contains PostgreSQL-specific errors, patterns, and tools for database administration, performance tuning, migration, and maintenance.

## 📁 Structure

```
postgresql/
├── errors/          # Common problems and their solutions
│   └── disk-space-issues.yaml
├── patterns/        # Best practices and proven patterns
│   ├── performance-tuning.yaml
│   └── migration-upgrade.yaml
└── tools/           # Automation scripts
    └── analyze-disk-space.ps1
```

## 🎯 Content Overview

### Errors (`errors/`)

**[disk-space-issues.yaml](errors/disk-space-issues.yaml)**
- **Problem:** PostgreSQL data directory consuming excessive disk space
- **Symptoms:** High disk usage (>90%), slow performance, large log files
- **Solution:** Cleanup logs, remove unused indexes, VACUUM, move tablespaces
- **Real-world result:** 105 GB freed (96% → 83% disk usage)

### Patterns (`patterns/`)

**[performance-tuning.yaml](patterns/performance-tuning.yaml)**
- **Context:** PostgreSQL configuration for high-end servers (64GB+ RAM)
- **Problem:** Default configuration uses only 10-20% of system capacity
- **Solution:** Optimized settings for memory, parallelism, WAL, I/O
- **Results:**
  - SELECT performance: +38% faster
  - Memory usage: 4GB → 50GB
  - Parallel workers: 8 → 32
  - Overall improvement: +100-200%

**[migration-upgrade.yaml](patterns/migration-upgrade.yaml)**
- **Context:** Major version migration (e.g., 15→16, 15→17, 15→18)
- **Problem:** Long downtime with traditional pg_dump/pg_restore
- **Solution:** pg_upgrade with --link mode
- **Results:**
  - Downtime: 1-2 hours (vs 20-40 hours)
  - Migration time: 12 minutes for 10TB database
  - Zero data loss

### Tools (`tools/`)

**[analyze-disk-space.ps1](tools/analyze-disk-space.ps1)**
- **Purpose:** PowerShell script for comprehensive disk space analysis
- **Features:**
  - Database size ranking
  - Top 20 largest tables
  - Top 20 largest indexes
  - Unused index detection (> 100MB)
  - Tablespace usage
  - Bloat detection
  - System disk space
  - Automated recommendations

## 🚀 Quick Start

### Using Knowledge Base Entries

Each entry contains:
- `id`: Unique identifier
- `title`: Descriptive title
- `problem`: Detailed problem description
- `symptoms`: Signs of the problem
- `context`: When it applies
- `solution`: Step-by-step solution
- `expected_improvements`: What to expect
- `validation`: How to verify it works
- `rollout_plan`: Implementation phases
- `rollback_plan`: How to undo if needed
- `sources`: References and documentation
- `examples`: Real-world examples
- `tested`: Where it was tested
- `caveats`: Warnings and limitations

### Search with kb.py CLI

```bash
# Search for disk space issues
kb search "disk space"
kb search --category postgresql --severity high

# Search for performance patterns
kb search "performance tuning"
kb search --tags postgresql, memory

# Search for migration help
kb search "migration upgrade"
kb search --tags pg-upgrade, link-mode
```

### Using PowerShell Tool

```powershell
# Run disk space analyzer
cd C:\Users\ozand\shared-knowledge-base\postgresql\tools
.\analyze-disk-space.ps1

# With verbose output
.\analyze-disk-space.ps1 -Verbose

# Connect to remote server
.\analyze-disk-space.ps1 -PGHost "remote-server" -PGPort 5432
```

## 📊 Case Studies

### Case Study 1: PostgreSQL 15 → 18 Migration

**System:** Windows Server, AMD Ryzen 9 5950X, 128GB RAM
**Databases:** postgres (8.7 TB), sw (501 GB), 19 others (<4 GB)
**Tablespaces:** 13 across 9 drives

**Challenge:** Upgrade to PostgreSQL 18 with minimal downtime

**Solution:** pg_upgrade with --link mode

**Results:**
- ✅ Migration completed in 12 minutes
- ✅ Total downtime: 1.5 hours (including ANALYZE)
- ✅ Zero data loss
- ✅ Performance improvement: +38% on SELECT queries

**Files:**
- [migration-upgrade.yaml](patterns/migration-upgrade.yaml)

### Case Study 2: Performance Tuning

**System:** PostgreSQL 18.1 on 128GB RAM server
**Problem:** Default configuration performing poorly

**Solution:** Applied optimized configuration

**Results:**
- shared_buffers: 128MB → 32GB (+25000%)
- effective_cache_size: 4GB → 96GB (+2300%)
- work_mem: 4MB → 256MB (+6300%)
- max_parallel_workers: 8 → 32 (+300%)
- SELECT performance: +38% faster

**Files:**
- [performance-tuning.yaml](patterns/performance-tuning.yaml)

### Case Study 3: Disk Space Cleanup

**System:** PostgreSQL 15.11, Disk C: 96.2% full
**Problem:** Excessive log generation (81 GB in 2-3 days)

**Root Cause:** log_rotation_size = 10MB (default)

**Solution:**
1. Increased log_rotation_size to 1GB
2. Set log_min_duration_statement to 5000ms
3. Cleaned up old logs
4. Dropped 15GB duplicate index
5. Removed 8.1GB old WAL files

**Results:**
- Total freed: 105 GB
- Disk usage: 96.2% → 83.5%
- Log overhead: -95%
- Performance: Improved (less I/O)

**Files:**
- [disk-space-issues.yaml](errors/disk-space-issues.yaml)

## 🛠️ Common Tasks

### Performance Tuning

1. **Analyze current configuration**
   ```sql
   SELECT name, setting, unit, source
   FROM pg_settings
   WHERE name IN ('shared_buffers', 'effective_cache_size', 'work_mem')
   ORDER BY name;
   ```

2. **Check cache hit ratio** (target: > 0.95)
   ```sql
   SELECT sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) as ratio
   FROM pg_statio_user_tables;
   ```

3. **Find slow queries**
   ```sql
   SELECT query, mean_exec_time, calls
   FROM pg_stat_statements
   ORDER BY mean_exec_time DESC
   LIMIT 20;
   ```

### Migration Checklist

- [ ] Install target PostgreSQL version
- [ ] Run pg_upgrade --check
- [ ] Stop all PostgreSQL services
- [ ] Fix compatibility issues (extensions, tablespaces)
- [ ] Run pg_upgrade --link
- [ ] Update configuration files
- [ ] Start new PostgreSQL
- [ ] Run VACUUM ANALYZE
- [ ] Update extensions
- [ ] Verify all databases
- [ ] Test applications

### Disk Space Maintenance

1. **Check what's consuming space**
   ```powershell
   .\analyze-disk-space.ps1
   ```

2. **Clean up logs** (delete older than 7 days)
   ```powershell
   cd $env:PGDATA\log
   forfiles /P . /M *.log /D -7 /C "cmd /c del @path"
   ```

3. **Remove unused indexes**
   ```sql
   -- Check usage first
   SELECT indexname, idx_scan, pg_size_pretty(pg_relation_size(indexrelid))
   FROM pg_stat_user_indexes
   WHERE idx_scan = 0 AND pg_relation_size(indexrelid) > 100 * 1024 * 1024;

   -- Drop if truly unused
   DROP INDEX CONCURRENTLY IF EXISTS unused_index;
   ```

4. **VACUUM large tables**
   ```sql
   VACUUM ANALYZE large_table;
   ```

## 📚 Additional Resources

### Official Documentation
- [PostgreSQL Documentation](https://www.postgresql.org/docs/current/)
- [pg_upgrade Documentation](https://www.postgresql.org/docs/current/pgupgrade.html)
- [Performance Tips](https://www.postgresql.org/docs/current/performance-tips.html)

### Community Resources
- [PostgreSQL Wiki](https://wiki.postgresql.org/)
- [Planet PostgreSQL](https://planet.postgresql.org/)
- [PostgreSQL Performance Mailing List](https://www.postgresql.org/list/pgsql-performance)

### Internal Documentation
- [POSTGRESQL_18_TUNING_ANALYSIS.md](https://github.com/ozand/shared-knowledge-base/blob/master/postgresql/patterns/performance-tuning.md)
- [MIGRATION_PLAN_PG15_TO_PG18_WINDOWS.md](https://github.com/ozand/shared-knowledge-base/blob/master/postgresql/patterns/migration-upgrade.md)
- [DISK_SPACE_ANALYSIS_REPORT.md](https://github.com/ozand/shared-knowledge-base/blob/master/postgresql/errors/disk-space-issues.md)

## 🤝 Contributing

To add new PostgreSQL knowledge:

1. Create YAML file in appropriate directory (errors/, patterns/, tools/)
2. Follow the structure from existing entries
3. Include real-world examples when possible
4. Test your solution before documenting
5. Validate YAML syntax: `kb validate your-file.yaml`
6. Submit Pull Request

See [GUIDE.md](../GUIDE.md) for detailed guidelines.

## 📝 License

MIT License - See [LICENSE](../LICENSE) for details

---

**Last Updated:** January 5, 2026
**PostgreSQL Versions Covered:** 14, 15, 16, 17, 18
**Maintained by:** @ozand
