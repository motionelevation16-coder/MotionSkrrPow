# IT & DevOps Automation 🖥️

**Automation Level:** 🟡 MEDIUM (50-70% of tasks automatable)

---

## Jobs Being Replaced

| Role | Current Salary | Automation % | Monthly Savings |
|------|---------------|--------------|-----------------|
| Junior Sysadmin | $4,000-6,000 | 60% | $2,400-3,600 |
| Deployment Engineer | $5,000-7,000 | 70% | $3,500-4,900 |
| Monitoring Analyst | $4,000-5,500 | 75% | $3,000-4,125 |
| Help Desk Tier 1 | $3,000-4,000 | 80% | $2,400-3,200 |
| Code Reviewer | $5,000-8,000 | 50% | $2,500-4,000 |

---

## Key Automations

### 1. Server Management
**Replaces:** Manual server updates, maintenance

```
Flow: Webhook Trigger → SSH to Server → Run Commands → Report Status
```

**n8n Templates:**
- `Linux System Update via Webhook` (SSH-based)
- `Docker Compose Controller via Webhook`

### 2. Code Review Automation
**Replaces:** Initial code review pass

```
Flow: New PR → AI Analyze Code → Comment Issues → Flag for Human Review
```

**n8n Templates:**
- `ChatGPT Automatic Code Review in Gitlab MR`

### 3. Alert Routing & Response
**Replaces:** Manual alert triage

```
Flow: Alert → AI Classify Severity → Route to Team → Auto-remediate if possible
```

### 4. Documentation Generation
**Replaces:** Manual documentation writing

```
Flow: Code/API → AI Generate Docs → Format → Publish
```

**n8n Templates:**
- `API Schema Extractor`

### 5. Help Desk Automation
**Replaces:** Tier 1 IT support

```
Flow: Ticket → AI Diagnose → Provide Solution → Escalate if needed
```

**n8n Templates:**
- `IT Ops AI SlackBot Workflow - Chat with your knowledge base`

---

## Server Automation Script (Python)

```python
import paramiko
from typing import List

class ServerAutomation:
    def __init__(self, hosts: List[dict]):
        """
        hosts = [
            {"host": "192.168.1.100", "user": "admin", "key_file": "~/.ssh/id_rsa"},
            ...
        ]
        """
        self.hosts = hosts
    
    def execute_on_all(self, command: str) -> dict:
        """Execute command on all servers"""
        results = {}
        
        for server in self.hosts:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            try:
                ssh.connect(
                    server['host'],
                    username=server['user'],
                    key_filename=server['key_file']
                )
                
                stdin, stdout, stderr = ssh.exec_command(command)
                results[server['host']] = {
                    "success": True,
                    "output": stdout.read().decode(),
                    "error": stderr.read().decode()
                }
            except Exception as e:
                results[server['host']] = {
                    "success": False,
                    "error": str(e)
                }
            finally:
                ssh.close()
        
        return results
    
    def update_all(self) -> dict:
        """Update all servers"""
        return self.execute_on_all("sudo apt update && sudo apt upgrade -y")
    
    def restart_service(self, service: str) -> dict:
        """Restart a service on all servers"""
        return self.execute_on_all(f"sudo systemctl restart {service}")
    
    def check_disk_space(self) -> dict:
        """Check disk space on all servers"""
        return self.execute_on_all("df -h")

# Example usage
servers = [
    {"host": "server1.example.com", "user": "admin", "key_file": "~/.ssh/id_rsa"},
    {"host": "server2.example.com", "user": "admin", "key_file": "~/.ssh/id_rsa"},
]

automation = ServerAutomation(servers)
results = automation.check_disk_space()
for host, result in results.items():
    print(f"{host}: {result['output']}")
```

---

## Docker Automation Script

```python
import docker
import openai

def ai_debug_container(container_name: str) -> str:
    """Use AI to diagnose container issues"""
    
    client = docker.from_env()
    container = client.containers.get(container_name)
    
    # Get logs
    logs = container.logs(tail=100).decode()
    
    # Get container info
    info = container.attrs
    
    prompt = f"""
    Debug this Docker container issue:
    
    Container: {container_name}
    Status: {info['State']['Status']}
    Exit Code: {info['State'].get('ExitCode', 'N/A')}
    
    Recent Logs:
    {logs}
    
    Provide:
    1. Root cause analysis
    2. Recommended fix
    3. Commands to run
    """
    
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

# Example
diagnosis = ai_debug_container("web-app")
print(diagnosis)
```

---

## Automation Stack

```
Monitoring (Grafana/Datadog)
    ↓
Alert Triggered
    ↓
n8n Webhook Receives Alert
    ↓
AI Classifies Severity
    ↓
Switch:
  - Critical → Page on-call + auto-remediate
  - High → Slack alert + create ticket
  - Medium → Create ticket
  - Low → Log and ignore
    ↓
Auto-remediation (if possible):
  - Restart service
  - Scale up
  - Clear cache
    ↓
Report status
```

---

## Selling Points for Clients

**Pain Points:**
- "Our sysadmin is overwhelmed"
- "Deployments are manual and error-prone"
- "We miss critical alerts"
- "Documentation is always outdated"

**Your Pitch:**
> "We automate your infrastructure management. Servers update automatically, alerts route intelligently, and deployments happen with one click. $800/month vs $5,000 for a junior sysadmin."

---

## Cost Analysis

| Item | Monthly Cost |
|------|-------------|
| n8n (self-hosted) | $20 |
| OpenAI API | $30-80 |
| Monitoring (Grafana) | $0 (self-hosted) |
| **Total** | $50-100 |
| **Savings** | $3,000-5,000+ |
| **ROI** | **30-100x** |

---

## Security Note

⚠️ IT automation requires:
- Secure credential storage (not in code)
- SSH key rotation
- Audit logging
- Principle of least privilege
- Human approval for production changes
