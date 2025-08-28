# Entelech Client Monitoring MCP Server

## 🎯 **Overview**

Comprehensive MCP (Model Context Protocol) server for monitoring client automation systems with unified dashboard. Eliminates manual checking by providing real-time visibility into all client implementations from a single interface.

**Problem Solved:** Instead of manually checking each client's automation system individually, get unified monitoring with proactive alerts and automated reporting across all implementations.

### **Key Features**

✅ **Unified Dashboard** - Monitor all clients from single web interface  
✅ **Real-time Health Checks** - Automated endpoint monitoring with status tracking  
✅ **Performance Metrics** - ROI tracking, success rates, processing times  
✅ **Proactive Alerting** - Configurable thresholds with email/Slack/webhook delivery  
✅ **Automated Reports** - Scheduled client status reports with recommendations  
✅ **Historical Analytics** - Trend analysis and performance insights  

---

## 🚀 **Quick Start**

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Initialize Database**
```bash
python database/init_database.py
```

### **3. Start MCP Server**
```bash
python src/mcp_server.py
```

### **4. Start Dashboard**
```bash
python dashboard/dashboard.py
```

### **5. Access Dashboard**
Open http://localhost:5000 to view unified client monitoring dashboard.

---

## 🔧 **MCP Functions**

### **get_system_health(client_id)**
Checks all automation endpoints for client system health.

```javascript
// Example usage in Claude
await get_system_health("tnt-limousine");
// Returns: health status, response times, uptime percentages
```

### **get_performance_metrics(client_id, timeframe)**
Retrieves ROI tracking and automation performance data.

```javascript
// Get 30-day performance metrics
await get_performance_metrics("tnt-limousine", "30d");
// Returns: success rates, cost savings, efficiency gains
```

### **alert_on_failures(client_id, metric, threshold, comparison, alert_type)**
Configures proactive issue detection with custom thresholds.

```javascript
// Alert when uptime drops below 95%
await alert_on_failures("tnt-limousine", "uptime", 95.0, "less_than", "slack");
```

### **generate_client_reports(client_id, report_type)**
Creates comprehensive automated status reports.

```javascript
// Generate monthly report with recommendations
await generate_client_reports("tnt-limousine", "monthly");
```

### **get_all_clients_status()**
Unified dashboard view of all client systems at once.

```javascript
// Get overview of all clients
await get_all_clients_status();
// Returns: system health summary, performance overview
```

---

## 📊 **Dashboard Features**

### **Main Dashboard**
- **Real-time Overview**: System health across all clients
- **Performance Metrics**: Today's automation counts and success rates
- **Visual Charts**: Status distribution and 30-day trends
- **Client Table**: Quick status with drill-down capabilities
- **Auto-refresh**: Live updates every 30 seconds

### **Client Detail Views**
- **System Breakdown**: Individual system health and performance
- **Historical Metrics**: 30-day automation and success rate trends
- **Alert History**: Recent issues and resolution status
- **Report Downloads**: Automated reports in multiple formats

---

## 🔗 **Client Integration**

### **Required Endpoints**
Each client automation system needs these endpoints:

**Health Check** (`GET /health`)
```json
{
  "status": "healthy|degraded|down",
  "uptime_percentage": 99.8,
  "response_time_ms": 245.3,
  "endpoints_healthy": 5
}
```

**Metrics** (`GET /metrics?start_date=...&end_date=...`)
```json
{
  "total_automations": 450,
  "successful_automations": 428,
  "cost_savings": 2840.75,
  "efficiency_gains": {...}
}
```

### **Register New Client**
```javascript
await register_client({
  client_id: "new-client-001",
  client_name: "ABC Company",
  automation_systems: ["Lead Processing", "Email Automation"],
  monitoring_endpoints: ["https://abc-api.entelech.com"],
  contact_email: "admin@abccompany.com"
});
```

---

## 📈 **Use Cases**

### **For Entelech Operations Team**
- **Daily Monitoring**: Check all client systems from single dashboard
- **Proactive Support**: Get alerts before clients notice issues
- **Performance Reporting**: Generate client reports automatically
- **Trend Analysis**: Identify patterns across implementations

### **For Client Success**
- **Health Validation**: Verify all systems operating optimally
- **Performance Metrics**: Track ROI and efficiency improvements
- **Issue Resolution**: Quick identification and response to problems
- **Status Communication**: Automated client report delivery

### **For Sales & Demos**
- **Social Proof**: Real-time success metrics across client base
- **Performance Data**: Concrete ROI figures for prospect discussions
- **System Reliability**: Uptime and success rate demonstrations
- **Scalability Evidence**: Multi-client monitoring capabilities

---

## ⚠️ **Alert Configuration Examples**

```javascript
// Critical system failures
alert_on_failures("*", "uptime", 95.0, "less_than", "slack");

// Performance degradation
alert_on_failures("tnt-limo", "success_rate", 90.0, "less_than", "email");

// High response times
alert_on_failures("abc-corp", "response_time", 5000, "greater_than", "webhook");

// Low automation volume (system issues)
alert_on_failures("*", "daily_automations", 10, "less_than", "email");
```

---

## 🗄️ **Database Schema**

**Core Tables:**
- `clients` - Client system registry and configuration
- `health_checks` - Historical health status and response times
- `performance_metrics` - Daily automation and ROI tracking
- `alert_thresholds` - Alert configuration and rules
- `alert_history` - Alert delivery and acknowledgment tracking
- `client_reports` - Generated reports and delivery status

---

## 🔐 **Security & Configuration**

### **Environment Variables**
```bash
# Database
DATABASE_URL=sqlite:///database/client_monitoring.db

# MCP Server
MCP_SERVER_PORT=8080

# Dashboard  
DASHBOARD_PORT=5000

# Alerts
SMTP_SERVER=smtp.gmail.com
SLACK_WEBHOOK_URL=https://hooks.slack.com/...
```

### **Production Considerations**
- Use PostgreSQL for production database
- Implement API key authentication
- Enable HTTPS with SSL certificates
- Configure firewall rules for monitoring endpoints
- Set up log rotation and monitoring

---

## 📋 **Project Structure**

```
├── src/mcp_server.py              # Main MCP server implementation
├── dashboard/dashboard.py         # Web dashboard application
├── config/mcp_config.json        # Server configuration
├── database/init_database.py     # Database setup script
├── docs/DEVELOPER_GUIDE.md       # Complete technical documentation
└── requirements.txt               # Python dependencies
```

---

## 🧪 **Testing**

```bash
# Run test suite
pytest tests/

# Test individual components
python -c "from src.mcp_server import EntelechMonitoringServer; print('MCP Server OK')"

# Test dashboard
curl http://localhost:5000/api/health-check
```

---

## 📞 **Support**

**Documentation**: Complete guides in `/docs/` directory  
**Developer Guide**: `docs/DEVELOPER_GUIDE.md`  
**API Reference**: `docs/API_REFERENCE.md`  
**Deployment Guide**: `docs/DEPLOYMENT.md`  

---

## 🎯 **Business Impact**

**Before Monitoring System:**
- ❌ Manual checking of individual client systems
- ❌ Reactive issue response (clients report problems)
- ❌ No centralized performance visibility
- ❌ Time-intensive status report generation

**After Monitoring System:**
- ✅ Unified dashboard for all client systems
- ✅ Proactive issue detection and alerts
- ✅ Real-time performance and ROI tracking  
- ✅ Automated client reporting with recommendations

**ROI for Entelech:**
- **Time Savings**: 2-3 hours daily on manual monitoring tasks
- **Improved Support**: Proactive issue resolution vs. reactive
- **Client Satisfaction**: Transparent performance reporting
- **Sales Enablement**: Real-time success metrics for prospects

---

**System Status**: ✅ **Production Ready**  
**Version**: 1.0.0  
**Created**: January 2025  
**Target Users**: Entelech operations team, client success managers, sales team

Transform manual client system monitoring into automated, unified dashboard with proactive alerting and comprehensive reporting.