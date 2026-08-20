#!/usr/bin/env python3
"""
AI Receptionist Web Interface - Flask-based web dashboard
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
from ai_receptionist import AIReceptionist, BusinessClient, create_sample_clients
from datetime import datetime, timedelta

app = Flask(__name__)
receptionist = AIReceptionist()

# Initialize with sample data
sample_clients = create_sample_clients()
for client in sample_clients:
    receptionist.add_client(client)

@app.route('/')
def dashboard():
    """Main dashboard"""
    # Get analytics for all clients
    clients_data = []
    for client in sample_clients:
        analytics = receptionist.get_business_analytics(client.id, 30)
        clients_data.append({
            'client': client,
            'analytics': analytics
        })
    
    return render_template('dashboard.html', clients_data=clients_data)

@app.route('/client/<client_id>')
def client_detail(client_id):
    """Client detail page"""
    client = receptionist.get_client(client_id)
    if not client:
        return "Client not found", 404
    
    analytics = receptionist.get_business_analytics(client_id, 30)
    appointments = receptionist.get_appointments(client_id)
    call_logs = receptionist.get_call_logs(client_id, 7)
    
    return render_template('client_detail.html', 
                         client=client, 
                         analytics=analytics,
                         appointments=appointments,
                         call_logs=call_logs)

@app.route('/simulate_call', methods=['POST'])
def simulate_call():
    """Simulate a call"""
    data = request.json
    client_id = data.get('client_id')
    caller_message = data.get('message')
    
    client = receptionist.get_client(client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404
    
    # Generate AI response
    response = receptionist.generate_ai_response(client, caller_message)
    
    # Log the call
    receptionist.log_call(
        client_id=client_id,
        caller_phone="+1-555-0000",
        call_duration=60,
        outcome="simulated_call",
        transcript=f"Caller: {caller_message}\nAI: {response}"
    )
    
    return jsonify({
        'response': response,
        'client_name': client.name
    })

@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    """Book an appointment"""
    data = request.json
    client_id = data.get('client_id')
    customer_name = data.get('customer_name')
    customer_phone = data.get('customer_phone')
    service = data.get('service')
    appointment_date = data.get('appointment_date')
    appointment_time = data.get('appointment_time')
    notes = data.get('notes', '')
    
    success = receptionist.book_appointment(
        client_id, customer_name, customer_phone,
        service, appointment_date, appointment_time, notes
    )
    
    if success:
        return jsonify({'success': True, 'message': 'Appointment booked successfully!'})
    else:
        return jsonify({'success': False, 'message': 'Failed to book appointment'})

@app.route('/api/analytics/<client_id>')
def get_analytics(client_id):
    """Get analytics for a client"""
    analytics = receptionist.get_business_analytics(client_id, 30)
    return jsonify(analytics)

@app.route('/api/appointments/<client_id>')
def get_appointments(client_id):
    """Get appointments for a client"""
    appointments = receptionist.get_appointments(client_id)
    return jsonify([{
        'id': apt.id,
        'customer_name': apt.customer_name,
        'customer_phone': apt.customer_phone,
        'service': apt.service,
        'appointment_date': apt.appointment_date,
        'appointment_time': apt.appointment_time,
        'status': apt.status,
        'notes': apt.notes
    } for apt in appointments])

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Create basic HTML templates
    create_html_templates()
    
    print("🌐 Starting AI Receptionist Web Interface...")
    print("Visit: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

def create_html_templates():
    """Create basic HTML templates"""
    
    # Dashboard template
    dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Receptionist Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .client-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .client-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .client-card h3 { color: #2c3e50; margin-top: 0; }
        .metric { display: flex; justify-content: space-between; margin: 10px 0; }
        .metric-value { font-weight: bold; color: #27ae60; }
        .btn { background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; }
        .btn:hover { background: #2980b9; }
        .simulate-section { background: white; padding: 20px; border-radius: 8px; margin-top: 20px; }
        .form-group { margin: 10px 0; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
        .form-group input, .form-group select, .form-group textarea { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        .response-box { background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 4px; padding: 15px; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI Receptionist Dashboard</h1>
            <p>Manage your AI-powered business receptionist services</p>
        </div>
        
        <div class="client-grid">
            {% for item in clients_data %}
            <div class="client-card">
                <h3>{{ item.client.name }}</h3>
                <p><strong>Industry:</strong> {{ item.client.industry }}</p>
                <p><strong>Monthly Fee:</strong> ${{ item.client.monthly_fee }}</p>
                
                <div class="metric">
                    <span>Total Calls (30d):</span>
                    <span class="metric-value">{{ item.analytics.total_calls }}</span>
                </div>
                <div class="metric">
                    <span>Appointments Booked:</span>
                    <span class="metric-value">{{ item.analytics.appointments_booked }}</span>
                </div>
                <div class="metric">
                    <span>Conversion Rate:</span>
                    <span class="metric-value">{{ item.analytics.conversion_rate }}%</span>
                </div>
                
                <a href="/client/{{ item.client.id }}" class="btn">View Details</a>
            </div>
            {% endfor %}
        </div>
        
        <div class="simulate-section">
            <h2>📞 Simulate a Call</h2>
            <form id="simulateForm">
                <div class="form-group">
                    <label for="client">Select Business:</label>
                    <select id="client" name="client_id" required>
                        <option value="">Choose a business...</option>
                        {% for item in clients_data %}
                        <option value="{{ item.client.id }}">{{ item.client.name }}</option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="message">Caller Message:</label>
                    <textarea id="message" name="message" rows="3" placeholder="What would the caller say?" required></textarea>
                </div>
                
                <button type="submit" class="btn">Simulate Call</button>
            </form>
            
            <div id="response" class="response-box" style="display: none;">
                <h4>🤖 AI Response:</h4>
                <p id="response-text"></p>
            </div>
        </div>
    </div>
    
    <script>
        document.getElementById('simulateForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = {
                client_id: formData.get('client_id'),
                message: formData.get('message')
            };
            
            try {
                const response = await fetch('/simulate_call', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (result.response) {
                    document.getElementById('response-text').textContent = result.response;
                    document.getElementById('response').style.display = 'block';
                } else {
                    alert('Error: ' + (result.error || 'Unknown error'));
                }
            } catch (error) {
                alert('Error: ' + error.message);
            }
        });
    </script>
</body>
</html>
    """
    
    # Client detail template
    client_detail_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ client.name }} - AI Receptionist</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .content { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .section { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .section h3 { color: #2c3e50; margin-top: 0; }
        .metric { display: flex; justify-content: space-between; margin: 10px 0; }
        .metric-value { font-weight: bold; color: #27ae60; }
        .btn { background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; }
        .btn:hover { background: #2980b9; }
        .appointment { border: 1px solid #ddd; padding: 10px; margin: 10px 0; border-radius: 4px; }
        .call-log { border: 1px solid #ddd; padding: 10px; margin: 10px 0; border-radius: 4px; background: #f8f9fa; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏢 {{ client.name }}</h1>
            <p>{{ client.industry }} - ${{ client.monthly_fee }}/month</p>
        </div>
        
        <div class="content">
            <div class="section">
                <h3>📊 Analytics (Last 30 Days)</h3>
                <div class="metric">
                    <span>Total Calls:</span>
                    <span class="metric-value">{{ analytics.total_calls }}</span>
                </div>
                <div class="metric">
                    <span>Appointments Booked:</span>
                    <span class="metric-value">{{ analytics.appointments_booked }}</span>
                </div>
                <div class="metric">
                    <span>Leads Captured:</span>
                    <span class="metric-value">{{ analytics.leads_captured }}</span>
                </div>
                <div class="metric">
                    <span>Conversion Rate:</span>
                    <span class="metric-value">{{ analytics.conversion_rate }}%</span>
                </div>
            </div>
            
            <div class="section">
                <h3>📅 Recent Appointments</h3>
                {% for appointment in appointments[:5] %}
                <div class="appointment">
                    <strong>{{ appointment.customer_name }}</strong><br>
                    {{ appointment.service }} - {{ appointment.appointment_date }} {{ appointment.appointment_time }}<br>
                    <small>Status: {{ appointment.status }}</small>
                </div>
                {% endfor %}
            </div>
            
            <div class="section">
                <h3>📞 Recent Calls</h3>
                {% for call in call_logs[:5] %}
                <div class="call-log">
                    <strong>{{ call.caller_phone }}</strong> - {{ call.outcome }}<br>
                    <small>{{ call.timestamp }}</small>
                </div>
                {% endfor %}
            </div>
            
            <div class="section">
                <h3>🔧 Business Info</h3>
                <p><strong>Services:</strong> {{ client.services | join(', ') }}</p>
                <p><strong>AI Personality:</strong> {{ client.ai_personality }}</p>
                <p><strong>Phone:</strong> {{ client.phone_number }}</p>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 20px;">
            <a href="/" class="btn">← Back to Dashboard</a>
        </div>
    </div>
</body>
</html>
    """
    
    # Write templates
    with open('templates/dashboard.html', 'w') as f:
        f.write(dashboard_html)
    
    with open('templates/client_detail.html', 'w') as f:
        f.write(client_detail_html)