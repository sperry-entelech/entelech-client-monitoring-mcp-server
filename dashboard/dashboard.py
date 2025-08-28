#!/usr/bin/env python3
"""
Entelech Client Monitoring Dashboard
Web-based unified dashboard for monitoring all client automation systems
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any
from pathlib import Path
import sqlite3

from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
import subprocess
import sys
import os

# Add the src directory to the path to import our MCP server
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

app = Flask(__name__, 
           template_folder='templates',
           static_folder='static')
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("entelech-dashboard")

class DashboardManager:
    """Manages dashboard data and MCP server communication"""
    
    def __init__(self, db_path="../database/client_monitoring.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    
    def get_all_clients_summary(self) -> Dict[str, Any]:
        """Get summary of all clients for dashboard"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Get client counts by status
            clients_query = """
                SELECT 
                    COUNT(*) as total_clients,
                    SUM(CASE WHEN is_active = 1 THEN 1 ELSE 0 END) as active_clients
                FROM clients
            """
            cursor = conn.execute(clients_query)
            client_counts = cursor.fetchone()
            
            # Get recent health status summary
            health_query = """
                SELECT 
                    client_id,
                    system_name,
                    status,
                    response_time_ms,
                    uptime_percentage,
                    check_timestamp
                FROM health_checks 
                WHERE check_timestamp >= datetime('now', '-1 hour')
                ORDER BY check_timestamp DESC
            """
            cursor = conn.execute(health_query)
            recent_health = cursor.fetchall()
            
            # Process health data
            status_summary = {"healthy": 0, "degraded": 0, "down": 0, "unknown": 0}
            client_health = {}
            
            for row in recent_health:
                client_id, system_name, status, response_time, uptime, timestamp = row
                
                if client_id not in client_health:
                    client_health[client_id] = {
                        "systems": [],
                        "overall_status": "healthy",
                        "last_check": timestamp
                    }
                
                client_health[client_id]["systems"].append({
                    "system_name": system_name,
                    "status": status,
                    "response_time_ms": response_time,
                    "uptime_percentage": uptime
                })
                
                # Update overall client status (worst status wins)
                if status == "down":
                    client_health[client_id]["overall_status"] = "down"
                elif status == "degraded" and client_health[client_id]["overall_status"] != "down":
                    client_health[client_id]["overall_status"] = "degraded"
            
            # Count clients by status
            for client_data in client_health.values():
                status = client_data["overall_status"]
                status_summary[status] = status_summary.get(status, 0) + 1
            
            # Get today's automation summary
            automation_query = """
                SELECT 
                    SUM(total_automations) as total_automations,
                    SUM(successful_automations) as successful_automations,
                    SUM(failed_automations) as failed_automations,
                    AVG(success_rate) as avg_success_rate
                FROM performance_metrics 
                WHERE metric_date = date('now')
            """
            cursor = conn.execute(automation_query)
            automation_stats = cursor.fetchone()
            
            conn.close()
            
            return {
                "summary": {
                    "total_clients": client_counts[0] or 0,
                    "active_clients": client_counts[1] or 0,
                    "healthy_systems": status_summary["healthy"],
                    "degraded_systems": status_summary["degraded"],
                    "down_systems": status_summary["down"],
                    "today_automations": automation_stats[0] or 0,
                    "today_success_rate": automation_stats[3] or 0
                },
                "client_health": client_health,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to get dashboard summary: {str(e)}")
            return {"error": str(e)}
    
    def get_client_details(self, client_id: str) -> Dict[str, Any]:
        """Get detailed information for a specific client"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Get client information
            client_query = "SELECT * FROM clients WHERE client_id = ?"
            cursor = conn.execute(client_query, (client_id,))
            client_row = cursor.fetchone()
            
            if not client_row:
                return {"error": "Client not found"}
            
            # Get recent health checks
            health_query = """
                SELECT system_name, status, response_time_ms, uptime_percentage, 
                       error_message, check_timestamp
                FROM health_checks 
                WHERE client_id = ? AND check_timestamp >= datetime('now', '-24 hours')
                ORDER BY check_timestamp DESC
            """
            cursor = conn.execute(health_query, (client_id,))
            health_data = cursor.fetchall()
            
            # Get performance metrics
            metrics_query = """
                SELECT metric_date, total_automations, successful_automations,
                       success_rate, cost_savings
                FROM performance_metrics 
                WHERE client_id = ? AND metric_date >= date('now', '-30 days')
                ORDER BY metric_date DESC
            """
            cursor = conn.execute(metrics_query, (client_id,))
            metrics_data = cursor.fetchall()
            
            # Get recent alerts
            alerts_query = """
                SELECT alert_type, metric_name, actual_value, alert_message,
                       severity, sent_at, acknowledged
                FROM alert_history 
                WHERE client_id = ? AND sent_at >= datetime('now', '-7 days')
                ORDER BY sent_at DESC
                LIMIT 10
            """
            cursor = conn.execute(alerts_query, (client_id,))
            alerts_data = cursor.fetchall()
            
            conn.close()
            
            # Format response
            columns = ['id', 'client_id', 'client_name', 'industry', 'implementation_date',
                      'automation_systems', 'monitoring_endpoints', 'contact_email', 
                      'alert_preferences', 'is_active', 'created_at', 'updated_at']
            client_info = dict(zip(columns, client_row))
            
            return {
                "client_info": client_info,
                "health_data": [
                    {
                        "system_name": row[0],
                        "status": row[1], 
                        "response_time_ms": row[2],
                        "uptime_percentage": row[3],
                        "error_message": row[4],
                        "timestamp": row[5]
                    } for row in health_data
                ],
                "performance_metrics": [
                    {
                        "date": row[0],
                        "total_automations": row[1],
                        "successful_automations": row[2],
                        "success_rate": row[3],
                        "cost_savings": row[4]
                    } for row in metrics_data
                ],
                "recent_alerts": [
                    {
                        "type": row[0],
                        "metric": row[1],
                        "value": row[2],
                        "message": row[3],
                        "severity": row[4],
                        "sent_at": row[5],
                        "acknowledged": row[6]
                    } for row in alerts_data
                ]
            }
            
        except Exception as e:
            logger.error(f"Failed to get client details: {str(e)}")
            return {"error": str(e)}
    
    def get_system_trends(self, days: int = 30) -> Dict[str, Any]:
        """Get system-wide trends for the dashboard"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Get daily automation trends
            trends_query = """
                SELECT 
                    metric_date,
                    SUM(total_automations) as daily_automations,
                    AVG(success_rate) as daily_success_rate,
                    SUM(cost_savings) as daily_savings
                FROM performance_metrics 
                WHERE metric_date >= date('now', '-{} days')
                GROUP BY metric_date
                ORDER BY metric_date
            """.format(days)
            
            cursor = conn.execute(trends_query)
            trends_data = cursor.fetchall()
            
            # Get health trends
            health_trends_query = """
                SELECT 
                    date(check_timestamp) as check_date,
                    AVG(CASE WHEN status = 'healthy' THEN 100 
                             WHEN status = 'degraded' THEN 50 
                             ELSE 0 END) as health_score,
                    AVG(uptime_percentage) as avg_uptime
                FROM health_checks 
                WHERE check_timestamp >= datetime('now', '-{} days')
                GROUP BY date(check_timestamp)
                ORDER BY check_date
            """.format(days)
            
            cursor = conn.execute(health_trends_query)
            health_trends_data = cursor.fetchall()
            
            conn.close()
            
            return {
                "automation_trends": [
                    {
                        "date": row[0],
                        "automations": row[1] or 0,
                        "success_rate": row[2] or 0,
                        "cost_savings": row[3] or 0
                    } for row in trends_data
                ],
                "health_trends": [
                    {
                        "date": row[0],
                        "health_score": row[1] or 0,
                        "avg_uptime": row[2] or 0
                    } for row in health_trends_data
                ]
            }
            
        except Exception as e:
            logger.error(f"Failed to get system trends: {str(e)}")
            return {"error": str(e)}

# Initialize dashboard manager
dashboard_manager = DashboardManager()

# Routes
@app.route('/')
def dashboard_home():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/client/<client_id>')
def client_detail(client_id):
    """Client detail page"""
    return render_template('client_detail.html', client_id=client_id)

@app.route('/api/dashboard/summary')
def api_dashboard_summary():
    """API endpoint for dashboard summary data"""
    summary = dashboard_manager.get_all_clients_summary()
    return jsonify(summary)

@app.route('/api/client/<client_id>/details')
def api_client_details(client_id):
    """API endpoint for client details"""
    details = dashboard_manager.get_client_details(client_id)
    return jsonify(details)

@app.route('/api/system/trends')
def api_system_trends():
    """API endpoint for system trends"""
    days = request.args.get('days', 30, type=int)
    trends = dashboard_manager.get_system_trends(days)
    return jsonify(trends)

@app.route('/api/health-check')
def api_health_check():
    """Health check endpoint for the dashboard itself"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

if __name__ == '__main__':
    # Create necessary directories
    Path('templates').mkdir(exist_ok=True)
    Path('static').mkdir(exist_ok=True)
    Path('static/css').mkdir(exist_ok=True)
    Path('static/js').mkdir(exist_ok=True)
    
    print("🌐 Starting Entelech Client Monitoring Dashboard...")
    print("Dashboard will be available at: http://localhost:5000")
    print("API endpoints:")
    print("  - GET /api/dashboard/summary")
    print("  - GET /api/client/{client_id}/details") 
    print("  - GET /api/system/trends?days=30")
    print("  - GET /api/health-check")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)