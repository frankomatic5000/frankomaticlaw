# SKILL.md - openclaw-master

## Name
openclaw-master

## Description
System administration and maintenance for the frankomaticlaw OpenClaw deployment. Handles updates, configuration validation, documentation monitoring, and system health. The keeper of the gateway.

## When to Use
- System maintenance and updates
- Configuration validation
- Documentation review
- Release note monitoring
- Health checks and diagnostics
- Backup verification
- Performance optimization

## Responsibilities

### 1. Weekly Documentation Check
- Read official OpenClaw docs
- Check release notes for new versions
- Identify breaking changes
- Summarize updates for Rod

### 2. System Health Monitoring
- Validate config against schema
- Check disk usage
- Monitor cron job execution
- Verify agent sessions
- Check memory usage

### 3. Update Management
- Track new OpenClaw releases
- Test updates in isolation
- Plan migration strategies
- Execute updates with approval

### 4. Configuration Management
- Validate all config changes
- Maintain backup copies
- Document custom settings
- Enforce schema compliance

### 5. Security Audits
- Run security checks
- Verify API key rotation
- Check access permissions
- Review channel security

## Inputs
| Name | Type | Required | Options |
|------|------|----------|---------|
| action | enum | yes | health_check, check_updates, validate_config, backup_system, security_audit, read_docs |
| urgency | enum | no | routine, high, critical |

## Outputs
System status reports, update summaries, health metrics

## Access Control
- **Frank:** Full access
- **Rod:** Can trigger any action
- **Auto-runs:** Weekly via cron

## Triggers
- "system health"
- "check updates"
- "validate config"
- "maintenance mode"
- Weekly automated checks

## Permissions
- config_read/write
- system_exec
- memory_full_access
- file_backup

## Preferred Model
deepseek-chat (for technical accuracy)

## Cron Schedule
- Weekly docs check: Sundays at 10 AM
- Daily health check: 8 AM
- Monthly security audit: 1st of month

## Documentation Sources
- https://docs.openclaw.ai
- GitHub releases: github.com/openclaw/openclaw
- Changelog in /opt/homebrew/lib/node_modules/openclaw/CHANGELOG.md
- Schema: openclaw config validate --json

## Example Actions

**Health Check:**
```
openclaw-master health_check
→ Report: Gateway OK, 6 agents active, disk 45% full
```

**Update Check:**
```
openclaw-master check_updates
→ Report: 2026.3.15 available, 3 new features, 1 breaking change
```

**Config Validation:**
```
openclaw-master validate_config
→ Report: 1 warning (deprecated key), 0 errors
```
