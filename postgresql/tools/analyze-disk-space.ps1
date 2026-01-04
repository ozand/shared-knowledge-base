# PostgreSQL Disk Space Analyzer
# Analyzes and reports on PostgreSQL disk space usage
# Usage: .\analyze-disk-space.ps1

param(
    [string]$PGHost = "localhost",
    [int]$PGPort = 5432,
    [string]$PGUser = "postgres",
    [string]$PGDatabase = "postgres",
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "PostgreSQL Disk Space Analyzer" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check if psql is available
$PG_BIN = "C:\Program Files\PostgreSQL\15\bin\psql.exe"
if (-not (Test-Path $PG_BIN)) {
    $PG_BIN = "C:\Program Files\PostgreSQL\18\bin\psql.exe"
    if (-not (Test-Path $PG_BIN)) {
        Write-Host "ERROR: PostgreSQL not found!" -ForegroundColor Red
        exit 1
    }
}

Write-Host "Using PostgreSQL: $PG_BIN" -ForegroundColor Green
Write-Host ""

# Helper function to run SQL queries
function Invoke-PGQuery {
    param([string]$Query)

    $output = & $PG_BIN -U $PGUser -d $PGDatabase -c $Query 2>&1
    return $output
}

# Helper function to format bytes
function Format-Bytes {
    param([long]$Bytes)

    if ($Bytes -ge 1TB) {
        return "{0:N2} TB" -f ($Bytes / 1TB)
    } elseif ($Bytes -ge 1GB) {
        return "{0:N2} GB" -f ($Bytes / 1GB)
    } elseif ($Bytes -ge 1MB) {
        return "{0:N2} MB" -f ($Bytes / 1MB)
    } elseif ($Bytes -ge 1KB) {
        return "{0:N2} KB" -f ($Bytes / 1KB)
    } else {
        return "$Bytes bytes"
    }
}

# 1. Check overall database sizes
Write-Host "=== 1. Database Sizes ===" -ForegroundColor Yellow
$dbQuery = @"
SELECT datname,
       pg_database_size(datname) as size_bytes,
       pg_size_pretty(pg_database_size(datname)) as size
FROM pg_database
WHERE datname NOT IN ('template0', 'template1')
ORDER BY pg_database_size(datname) DESC;
"@

$dbResults = Invoke-PGQuery -Query $dbQuery
$dbResults | Write-Host

$total_size = 0
foreach ($line in $dbResults) {
    if ($line -match '^\s*(\w+).*\|.*\|.*(\d+)') {
        $total_size += [int]$matches[2]
    }
}
Write-Host "Total database size: $(Format-Bytes $total_size)" -ForegroundColor Green
Write-Host ""

# 2. Check largest tables
Write-Host "=== 2. Top 20 Largest Tables ===" -ForegroundColor Yellow
$tableQuery = @"
SELECT
    n.nspname as schema_name,
    c.relname as table_name,
    pg_total_relation_size(c.oid) as total_bytes,
    pg_size_pretty(pg_total_relation_size(c.oid)) as total_size,
    pg_size_pretty(pg_relation_size(c.oid)) as table_size,
    pg_size_pretty(pg_total_relation_size(c.oid) - pg_relation_size(c.oid)) as index_size
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE c.relkind = 'r' AND n.nspname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(c.oid) DESC
LIMIT 20;
"@

Invoke-PGQuery -Query $tableQuery
Write-Host ""

# 3. Check largest indexes
Write-Host "=== 3. Top 20 Largest Indexes ===" -ForegroundColor Yellow
$indexQuery = @"
SELECT
    n.nspname as schema_name,
    c.relname as table_name,
    i.relname as index_name,
    pg_relation_size(i.oid) as index_bytes,
    pg_size_pretty(pg_relation_size(i.oid)) as index_size,
    s.idx_scan as times_used
FROM pg_class i
JOIN pg_namespace n ON n.oid = i.relnamespace
JOIN pg_class c ON c.oid = i.indrelid
JOIN pg_stat_user_indexes s ON s.indexrelid = i.oid
WHERE n.nspname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_relation_size(i.oid) DESC
LIMIT 20;
"@

Invoke-PGQuery -Query $indexQuery
Write-Host ""

# 4. Check potentially unused indexes (> 100MB)
Write-Host "=== 4. Potentially Unused Large Indexes (> 100MB) ===" -ForegroundColor Yellow
$unusedIndexQuery = @"
SELECT
    n.nspname as schema_name,
    c.relname as table_name,
    i.relname as index_name,
    pg_relation_size(i.oid) as index_bytes,
    pg_size_pretty(pg_relation_size(i.oid)) as index_size,
    s.idx_scan as times_used,
    CASE
        WHEN s.idx_scan = 0 THEN 'NEVER USED'
        WHEN s.idx_scan < 10 THEN 'RARELY USED'
        ELSE 'ACTIVE'
    END as usage_status
FROM pg_class i
JOIN pg_namespace n ON n.oid = i.relnamespace
JOIN pg_class c ON c.oid = i.indrelid
JOIN pg_stat_user_indexes s ON s.indexrelid = i.oid
WHERE n.nspname NOT IN ('pg_catalog', 'information_schema')
  AND pg_relation_size(i.oid) > 100 * 1024 * 1024
ORDER BY pg_relation_size(i.oid) DESC;
"@

Invoke-PGQuery -Query $unusedIndexQuery
Write-Host ""

# 5. Check tablespaces
Write-Host "=== 5. Tablespace Usage ===" -ForegroundColor Yellow
$tablespaceQuery = @"
SELECT
    spcname,
    pg_tablespace_location(oid) as location,
    pg_size_pretty(pg_tablespace_size(spcname)) as size
FROM pg_tablespace
ORDER BY pg_tablespace_size(spcname) DESC;
"@

Invoke-PGQuery -Query $tablespaceQuery
Write-Host ""

# 6. Check for table and index bloat (simplified)
Write-Host "=== 6. Potential Bloat (Top 10 Tables) ===" -ForegroundColor Yellow
$bloatQuery = @"
SELECT
    n.nspname as schema_name,
    c.relname as table_name,
    pg_total_relation_size(c.oid) as total_bytes,
    pg_size_pretty(pg_total_relation_size(c.oid)) as total_size,
    c.relpages as pages
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE c.relkind = 'r'
  AND n.nspname NOT IN ('pg_catalog', 'information_schema')
  AND pg_total_relation_size(c.oid) > 100 * 1024 * 1024  -- > 100MB
ORDER BY pg_total_relation_size(c.oid) DESC
LIMIT 10;
"@

Invoke-PGQuery -Query $bloatQuery
Write-Host ""

# 7. Check disk space on server
Write-Host "=== 7. System Disk Space ===" -ForegroundColor Yellow
try {
    $drives = Get-PSDrive -PSProvider FileSystem
    foreach ($drive in $drives) {
        $used = $drive.Used
        $free = $drive.Free
        $total = $used + $free
        $usedPercent = ($used / $total) * 100

        $color = if ($usedPercent -gt 90) { "Red" }
                 elseif ($usedPercent -gt 75) { "Yellow" }
                 else { "Green" }

        Write-Host "$($drive.Name): " -NoNewline
        Write-Host "Used: $(Format-Bytes $used) " -ForegroundColor $color
        Write-Host "Free: $(Format-Bytes $free) " -ForegroundColor $color
        Write-Host "($(Format-Bytes $total) total - $([math]::Round($usedPercent, 1))% used)"
    }
} catch {
    Write-Host "Could not get disk space information" -ForegroundColor Red
}
Write-Host ""

# 8. Recommendations
Write-Host "=== 8. Recommendations ===" -ForegroundColor Yellow
Write-Host ""
Write-Host "Based on analysis, consider:" -ForegroundColor White
Write-Host "1. Dropping unused indexes (see section 4)" -ForegroundColor Cyan
Write-Host "2. Running VACUUM ANALYZE on large tables" -ForegroundColor Cyan
Write-Host "3. Checking log file size (ls -la \$PGDATA/log)" -ForegroundColor Cyan
Write-Host "4. Moving large tables to different tablespaces" -ForegroundColor Cyan
Write-Host "5. Setting up autovacuum for bloated tables" -ForegroundColor Cyan
Write-Host ""

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Analysis complete!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
