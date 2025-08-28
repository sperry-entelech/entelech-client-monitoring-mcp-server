# Entelech Client Monitoring MCP Server - Developer Guide

## 🎯 **Project Overview**

Complete MCP (Model Context Protocol) server for monitoring client automation systems with unified dashboard. Provides real-time health monitoring, performance metrics tracking, proactive alerting, and automated reporting across all client implementations.

**Key Capabilities:**
- **System Health Monitoring**: Real-time status checks across all client endpoints
- **Performance Metrics**: ROI tracking, automation success rates, processing times
- **Proactive Alerting**: Configurable thresholds with multiple notification methods
- **Unified Dashboard**: Web-based interface showing all clients at once
- **Automated Reporting**: Scheduled client status reports with recommendations

---

## 🏗️ **System Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                    MCP SERVER CORE                              │
├─────────────────────────────────────────────────────────────────┤
│  📊 get_system_health(client_id)                               │
│  📈 get_performance_metrics(client_id, timeframe)              │
│  🚨 alert_on_failures(threshold)                               │
│  📋 generate_client_reports(client_id)                         │
│  👥 get_all_clients_status()                                   │
│  ➕ register_client(client_data)                               │
└─────────────────┬───────────────────────────────────────────────┘
                  │
        ┌─────────┼─────────┐
        │         │         │
┌───────▼───────┐ │ ┌───────▼───────┐
│   DATABASE    │ │ │  WEB DASHBOARD │
│   ┌─────────┐ │ │ │  ┌─────────┐   │
│   │clients  │ │ │ │  │Flask App│   │
│   │health   │ │ │ │  │Real-time│   │
│   │metrics  │ │ │ │  │Charts   │   │
│   │alerts   │ │ │ │  │Tables   │   │
│   │reports  │ │ │ │  │API      │   │
│   └─────────┘ │ │ │  └─────────┘   │
└───────────────┘ │ └───────────────┘
                  │
    ┌─────────────▼─────────────┐
    │     CLIENT SYSTEMS        │
    │  ┌─────────┐ ┌─────────┐  │
    │  │Client A │ │Client B │  │
    │  │/health  │ │/health  │  │
    │  │/metrics │ │/metrics │  │
    │  └─────────┘ └─────────┘  │
    └───────────────────────────┘
```

---

## 📦 **Package Structure**

```
Entelech-Client-Monitoring-MCP-Server/
├── 📄 README.md                          # Project overview
├── 📄 requirements.txt                   # Python dependencies
├── 📄 setup.py                          # Package setup script
├── 📄 .env.example                      # Environment variables template
├── 📁 src/                              # Core MCP server code
│   ├── mcp_server.py                    # Main MCP server implementation
│   ├── client_manager.py               # Client system management
│   ├── alert_manager.py                # Alert processing and delivery
│   ├── report_generator.py             # Automated report generation
│   └── utils/                           # Utility modules
├── 📁 config/                           # Configuration files
│   ├── mcp_config.json                 # Main server configuration
│   ├── client_templates.json           # Client registration templates
│   └── alert_templates.json            # Alert message templates
├── 📁 dashboard/                        # Web dashboard
│   ├── dashboard.py                     # Flask web application
│   ├── templates/                       # HTML templates
│   │   ├── dashboard.html              # Main dashboard page
│   │   ├── client_detail.html          # Client detail view
│   │   └── base.html                   # Base template
│   └── static/                          # CSS, JS, images
├── 📁 database/                         # Database schema and scripts
│   ├── init_database.py                # Database initialization
│   ├── schema.sql                      # Database schema
│   └── migrations/                      # Schema migration scripts
├── 📁 docs/                            # Documentation
│   ├── DEVELOPER_GUIDE.md              # This file
│   ├── API_REFERENCE.md               # MCP functions reference
│   ├── DEPLOYMENT.md                  # Production deployment guide
│   └── TROUBLESHOOTING.md             # Common issues and solutions
├── 📁 tests/                           # Test suite
│   ├── test_mcp_server.py             # MCP server tests
│   ├── test_dashboard.py              # Dashboard tests
│   └── fixtures/                       # Test fixtures
└── 📁 scripts/                         # Utility scripts
    ├── setup_development.py           # Development environment setup
    ├── backup_database.py             # Database backup utility
    └── deploy.sh                      # Deployment script
```

---

## 🔧 **MCP Server Functions**

### **1. get_system_health(client_id)**
Checks health status of all automation endpoints for a client.

**Parameters:**
- `client_id` (string): Client identifier to check

**Returns:**
```json
{
  "client_id": "client-001",
  "client_name": "TNT Limousine",
  "overall_status": "healthy|degraded|down",
  "systems": [
    {
      "system_name": "Lead Processing",
      "status": "healthy",
      "response_time_ms": 245.3,
      "uptime_percentage": 99.8,
      "last_check": "2025-01-15T14:30:00Z"
    }
  ],
  "summary": {
    "total_systems": 3,
    "healthy_systems": 3,
    "degraded_systems": 0,
    "down_systems": 0,
    "avg_response_time": 230.1
  }
}
```

**Implementation Details:**
- Tests multiple endpoints per client system
- Measures response times and uptime percentages
- Stores historical health data for trending
- Supports configurable timeout and retry logic

### **2. get_performance_metrics(client_id, timeframe)**
Retrieves performance metrics and ROI tracking for specified timeframe.

**Parameters:**
- `client_id` (string): Client identifier
- `timeframe` (string): "24h", "7d", "30d", "90d"

**Returns:**
```json
{
  "client_id": "client-001",
  "timeframe": "30d",
  "period": {
    "start": "2024-12-15T00:00:00Z",
    "end": "2025-01-15T00:00:00Z"
  },
  "metrics": {
    "total_automations": 1250,
    "successful_automations": 1187,
    "success_rate": 94.96,
    "avg_processing_time": 2.3,
    "cost_savings": 15420.50,
    "roi_metrics": {
      "time_saved_hours": 312.5,
      "labor_cost_savings": 7812.50,
      "efficiency_improvement": 85.2
    }
  },
  "trends": {
    "automation_volume_trend": 15.2,
    "success_rate_trend": 2.1,
    "performance_direction": "improving"
  }
}
```

### **3. alert_on_failures(client_id, metric_name, threshold, comparison, alert_type)**
Configures proactive issue detection with customizable thresholds.

**Parameters:**
- `client_id` (string): Client to monitor
- `metric_name` (string): Metric to monitor (uptime, success_rate, response_time, etc.)
- `threshold` (number): Threshold value for alerting
- `comparison` (string): "greater_than", "less_than", "equals"
- `alert_type` (string): "email", "slack", "webhook"

**Example Alert Configurations:**
```javascript
// Alert when uptime drops below 95%
alert_on_failures("client-001", "uptime", 95.0, "less_than", "slack")

// Alert when success rate falls below 90%
alert_on_failures("client-001", "success_rate", 90.0, "less_than", "email")

// Alert when response time exceeds 5 seconds
alert_on_failures("client-001", "response_time", 5000, "greater_than", "webhook")
```

### **4. generate_client_reports(client_id, report_type)**
Generates comprehensive automated status reports.

**Parameters:**
- `client_id` (string): Client for report generation
- `report_type` (string): "daily", "weekly", "monthly", "quarterly"
- `include_recommendations` (boolean): Include optimization suggestions

**Report Structure:**
```json
{
  "report_metadata": {
    "client_name": "TNT Limousine",
    "report_type": "monthly",
    "period_label": "Last 30 Days",
    "generated_at": "2025-01-15T09:00:00Z"
  },
  "executive_summary": {
    "overall_health": "healthy",
    "key_achievements": [...],
    "areas_for_improvement": [...]
  },
  "system_health": {
    "uptime_summary": 99.2,
    "critical_issues": [],
    "performance_highlights": [...]
  },
  "performance_metrics": {
    "automation_summary": {...},
    "roi_analysis": {...},
    "efficiency_gains": {...}
  },
  "recommendations": {
    "performance_optimizations": [...],
    "cost_savings_opportunities": [...],
    "strategic_initiatives": [...]
  }
}
```

### **5. get_all_clients_status(include_inactive)**
Unified dashboard view of all client systems.

**Returns:**
```json
{
  "dashboard_updated": "2025-01-15T14:30:00Z",
  "total_clients": 12,
  "active_clients": 11,
  "clients": [
    {
      "client_id": "client-001",
      "client_name": "TNT Limousine",
      "overall_status": "healthy",
      "systems_count": 3,
      "healthy_systems": 3,
      "today_automations": 45,
      "today_success_rate": 97.8
    }
  ],
  "overall_summary": {
    "healthy_clients": 9,
    "degraded_clients": 2,
    "down_clients": 0,
    "total_automations_today": 567,
    "overall_success_rate": 94.2
  }
}
```

---

## 🗄️ **Database Schema**

### **Core Tables**

**clients** - Client system registry
```sql
CREATE TABLE clients (
    id INTEGER PRIMARY KEY,
    client_id TEXT UNIQUE NOT NULL,
    client_name TEXT NOT NULL,
    industry TEXT,
    automation_systems TEXT, -- JSON array
    monitoring_endpoints TEXT, -- JSON array  
    contact_email TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**health_checks** - System health history
```sql
CREATE TABLE health_checks (
    id INTEGER PRIMARY KEY,
    client_id TEXT NOT NULL,
    system_name TEXT NOT NULL,
    status TEXT NOT NULL,
    response_time_ms REAL,
    uptime_percentage REAL,
    error_message TEXT,
    check_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**performance_metrics** - Client performance tracking
```sql  
CREATE TABLE performance_metrics (
    id INTEGER PRIMARY KEY,
    client_id TEXT NOT NULL,
    metric_date DATE NOT NULL,
    total_automations INTEGER,
    successful_automations INTEGER,
    success_rate REAL,
    cost_savings REAL,
    roi_metrics TEXT, -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**alert_thresholds** - Alert configurations
```sql
CREATE TABLE alert_thresholds (
    id INTEGER PRIMARY KEY,
    client_id TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    threshold_value REAL NOT NULL,
    comparison TEXT NOT NULL,
    alert_type TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
);
```

---

## 🌐 **Web Dashboard**

### **Dashboard Features**

**Main Dashboard (`/`)**
- Real-time overview of all client systems
- System health summary with visual indicators
- Performance trends charts (30-day automation volume, success rates)
- Client status table with quick actions
- Auto-refresh every 30 seconds

**Client Detail View (`/client/{client_id}`)**
- Detailed system health breakdown
- Historical performance metrics
- Recent alerts and incident history
- Downloadable reports
- System configuration information

**API Endpoints**
- `GET /api/dashboard/summary` - Dashboard overview data
- `GET /api/client/{client_id}/details` - Client-specific details  
- `GET /api/system/trends?days=30` - System-wide trends
- `GET /api/health-check` - Dashboard health status

### **Dashboard Technologies**
- **Backend**: Flask with SQLite/PostgreSQL
- **Frontend**: HTML5, TailwindCSS, Chart.js
- **Real-time Updates**: AJAX polling (30-second intervals)
- **Responsive Design**: Mobile and desktop optimized

---

## 🚀 **Installation & Setup**

### **Prerequisites**
- Python 3.9+
- SQLite3 (included) or PostgreSQL (production)
- Node.js (for dashboard assets, optional)

### **Development Setup**

1. **Clone and Setup Environment**
```bash
# Navigate to project directory
cd Entelech-Client-Monitoring-MCP-Server

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

2. **Initialize Database**
```bash
python database/init_database.py
```

3. **Configure Environment**
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
nano .env
```

4. **Start MCP Server**
```bash
python src/mcp_server.py
```

5. **Start Dashboard (separate terminal)**
```bash
python dashboard/dashboard.py
```

### **Production Deployment**

**Using Docker (Recommended)**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python database/init_database.py

EXPOSE 5000
CMD ["python", "src/mcp_server.py"]
```

**Manual Deployment**
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 dashboard.dashboard:app

# Run MCP server in background
nohup python src/mcp_server.py > mcp_server.log 2>&1 &
```

---

## 📊 **Client Integration**

### **Required Client Endpoints**

Each client automation system must implement these endpoints:

**Health Check Endpoint** (`GET /health`)
```json
{
  "status": "healthy|degraded|down",
  "timestamp": "2025-01-15T14:30:00Z",
  "uptime_percentage": 99.8,
  "endpoints_checked": 5,
  "endpoints_healthy": 5,
  "response_time_ms": 245.3,
  "system_info": {
    "version": "1.2.0",
    "environment": "production"
  }
}
```

**Metrics Endpoint** (`GET /metrics?start_date=...&end_date=...`)
```json
{
  "period": {
    "start": "2025-01-01T00:00:00Z",
    "end": "2025-01-15T23:59:59Z"
  },
  "total_automations": 450,
  "successful_automations": 428,
  "failed_automations": 22,
  "total_processing_time": 1125.5,
  "cost_savings": 2840.75,
  "efficiency_gains": {
    "time_saved_hours": 112.5,
    "error_reduction_percentage": 87.3,
    "process_improvement": 45.2
  }
}
```

### **Client Registration**

**Register New Client**
```javascript
// Example client registration
await mcp_server.register_client({
  client_id: "tnt-limousine-001",
  client_name: "TNT Limousine",
  industry: "Transportation",
  automation_systems: [
    "Lead Processing System",
    "Booking Management",
    "Customer Communication"
  ],
  monitoring_endpoints: [
    "https://tnt-api.entelech.com",
    "https://tnt-booking.entelech.com",
    "https://tnt-comms.entelech.com"
  ],
  contact_email: "operations@tntlimo.com"
});
```

---

## 🚨 **Alert Configuration**

### **Alert Types**

**Email Alerts**
```json
{
  "enabled": true,
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "from_address": "alerts@entelech.com",
  "default_recipients": ["team@entelech.com"]
}
```

**Slack Alerts**
```json
{
  "enabled": true,
  "webhook_url": "https://hooks.slack.com/services/...",
  "channel": "#monitoring",
  "username": "Entelech Monitor"
}
```

**Webhook Alerts**
```json
{
  "enabled": true,
  "url": "https://your-webhook.com/alerts",
  "headers": {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_TOKEN"
  }
}
```

### **Common Alert Configurations**

```javascript
// Critical system down alerts
alert_on_failures("*", "uptime", 95.0, "less_than", "slack");

// Performance degradation
alert_on_failures("*", "success_rate", 90.0, "less_than", "email");

// High response times
alert_on_failures("*", "response_time", 5000, "greater_than", "webhook");

// Low automation volume (possible system issue)
alert_on_failures("*", "daily_automations", 10, "less_than", "email");
```

---

## 🧪 **Testing**

### **Run Test Suite**
```bash
# Run all tests
pytest tests/

# Run specific test files
pytest tests/test_mcp_server.py -v
pytest tests/test_dashboard.py -v

# Run with coverage
pytest --cov=src tests/
```

### **Manual Testing Checklist**

**MCP Server Functions**
- [ ] `get_system_health()` returns proper status for all clients
- [ ] `get_performance_metrics()` calculates ROI correctly
- [ ] `alert_on_failures()` triggers alerts at configured thresholds
- [ ] `generate_client_reports()` produces complete reports
- [ ] `get_all_clients_status()` shows unified dashboard data

**Dashboard Functionality**
- [ ] Main dashboard loads with real client data
- [ ] Charts update with live performance data
- [ ] Client detail pages show comprehensive information
- [ ] Auto-refresh works correctly (30-second intervals)
- [ ] Mobile responsive design functions properly

**Database Operations**
- [ ] Client registration stores data correctly
- [ ] Health checks are recorded with proper timestamps
- [ ] Performance metrics aggregate accurately
- [ ] Alert history maintains complete records

---

## 📈 **Performance Optimization**

### **Database Optimization**
- Index frequently queried columns (client_id, timestamps)
- Archive old health check data (>90 days) to separate tables
- Use connection pooling for high-traffic scenarios
- Consider PostgreSQL for production deployments

### **MCP Server Optimization**
- Implement connection pooling for client HTTP requests
- Use async/await for concurrent health checks
- Cache frequently accessed client configurations
- Implement rate limiting to prevent API overload

### **Dashboard Optimization**
- Enable gzip compression for API responses
- Implement client-side caching for static chart data
- Use WebSocket connections for real-time updates (future enhancement)
- Optimize SQL queries with proper joins and aggregations

---

## 🔒 **Security Considerations**

### **API Security**
- Implement API key authentication for MCP server access
- Use HTTPS in production environments
- Validate and sanitize all input parameters
- Implement rate limiting to prevent abuse

### **Database Security**
- Use parameterized queries to prevent SQL injection
- Encrypt sensitive configuration data
- Regular backup with secure storage
- Implement access controls and audit logging

### **Dashboard Security**
- Authentication for dashboard access (future enhancement)
- CORS configuration for API endpoints
- Input validation for all form submissions
- Secure session management

---

## 🔧 **Configuration Reference**

### **Environment Variables (.env)**
```bash
# Database Configuration
DATABASE_URL=sqlite:///database/client_monitoring.db

# MCP Server Settings
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=8080

# Dashboard Settings
DASHBOARD_HOST=0.0.0.0
DASHBOARD_PORT=5000
DASHBOARD_DEBUG=false

# Alert Settings
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=alerts@entelech.com
SMTP_PASSWORD=your_app_password

SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...

# Security Settings
API_KEY=your_secure_api_key
SECRET_KEY=your_flask_secret_key

# Monitoring Settings
HEALTH_CHECK_INTERVAL=900  # 15 minutes
METRICS_INTERVAL=3600      # 1 hour
ALERT_CHECK_INTERVAL=300   # 5 minutes
```

### **Main Configuration (config/mcp_config.json)**
- Server settings and connection parameters
- Database configuration and retention policies
- Alert thresholds and notification settings
- Dashboard customization options
- Integration settings for external services

---

## 📋 **Maintenance Tasks**

### **Daily Tasks**
- Review dashboard for any critical alerts
- Check system health across all clients
- Verify automated report generation

### **Weekly Tasks**
- Analyze performance trends for anomalies
- Review and acknowledge alert history
- Update client configurations if needed
- Check database performance and size

### **Monthly Tasks**
- Generate comprehensive client reports
- Review and optimize alert thresholds
- Backup database and configuration files
- Update system documentation
- Performance optimization review

### **Quarterly Tasks**
- Client satisfaction review based on monitoring data
- System architecture assessment
- Security audit and updates
- Disaster recovery testing

---

## 🆘 **Troubleshooting**

### **Common Issues**

**MCP Server Won't Start**
```bash
# Check Python environment
python --version
pip list | grep mcp

# Verify database connection
python -c "import sqlite3; conn = sqlite3.connect('database/client_monitoring.db'); print('DB OK')"

# Check configuration
python -c "import json; print(json.load(open('config/mcp_config.json')))"
```

**Dashboard Shows No Data**
- Verify MCP server is running and accessible
- Check database has client records
- Confirm API endpoints respond correctly
- Review browser console for JavaScript errors

**Health Checks Failing**
- Verify client endpoints are accessible
- Check network connectivity and firewalls
- Validate endpoint URLs and response formats
- Review timeout and retry configurations

**Alerts Not Firing**
- Confirm alert thresholds are properly configured
- Check SMTP/Slack/webhook credentials
- Verify metric calculations are correct
- Review alert history for delivery status

### **Debug Mode**
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python src/mcp_server.py

# Dashboard debug mode
export FLASK_DEBUG=true
python dashboard/dashboard.py
```

---

## 📞 **Support & Contact**

**Development Team**: Entelech Automation Solutions
**Documentation**: Complete guides in `/docs/` directory
**Issue Tracking**: GitHub Issues (if applicable)
**Email**: support@entelech.com

**System Status**: ✅ Production Ready
**Version**: 1.0.0
**Last Updated**: January 15, 2025

The Entelech Client Monitoring MCP Server provides comprehensive automation system monitoring with unified dashboard visibility across all client implementations.