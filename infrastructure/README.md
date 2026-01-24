# Infrastructure Knowledge Base

This directory contains patterns and lessons learned for infrastructure, DevOps, and system administration.

## Structure

```
infrastructure/
├── patterns/
│   ├── nginx-llm-streaming.yaml    # Nginx config for LLM API streaming
│   └── xray-sni-routing.yaml        # SNI-based routing with Xray/X-ui
└── errors/
    └── (add infrastructure-specific errors here)
```

## Categories

### Nginx LLM Streaming (`nginx-llm-streaming.yaml`)
Optimal reverse proxy configuration for LLM APIs with streaming support.

**Key settings:**
- `proxy_buffering off` for real-time token streaming
- Extended timeouts (300s) for long generations
- Proxy protocol for real client IP

**Use when:** Setting up reverse proxy for OpenAI, Anthropic, or local LLM APIs.

### Xray SNI Routing (`xray-sni-routing.yaml`)
SNI-based routing for multiple services on a single port 443.

**Architecture:**
```
Client → Xray:443 → [SNI match] → Nginx:8443/8444 → Backends:8111/8112
```

**Key points:**
- Update x-ui via SQLite database, not config.json directly
- Order of fallbacks matters (specific before default)
- Use proxy_protocol for real client IPs

**Use when:** Hosting multiple HTTPS services on a single IP.

## Contributing

When adding new infrastructure knowledge:

1. **Categorize correctly:** `patterns/` for solutions, `errors/` for problems
2. **Use YAML format:** Follow existing file structure
3. **Include examples:** Show actual commands/config
4. **Add tags:** For easy searching
5. **Update this README:** Add entry to appropriate section

## Quick Reference

### Common Issues

| Issue | File | ID |
|-------|------|-----|
| SSL certificate permissions | `../universal/errors/nginx-ssl-permissions.yaml` | SSL-001 |
| Disk space (deleted files) | `../universal/errors/disk-space-deleted-files.yaml` | DISK-001 |
| LLM streaming not working | `patterns/nginx-llm-streaming.yaml` | - |
| x-ui SNI routing | `patterns/xray-sni-routing.yaml` | - |

### Essential Commands

```bash
# Find deleted files still using disk space
lsof | grep "(deleted)"

# Truncate open file (free space without restart)
truncate -s 0 /proc/PID/fd/FD

# Fix SSL permissions
chmod 755 /etc/letsencrypt/archive
chmod 644 /etc/letsencrypt/archive/*/privkey*.pem

# Update x-ui fallbacks via database
sqlite3 /etc/x-ui/x-ui.db "SELECT id, stream_settings FROM inbounds WHERE port = 443;"

# Test nginx config
nginx -t
```
