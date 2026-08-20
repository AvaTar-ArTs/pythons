#!/usr/bin/env python3
"""
Heavenly Hands Call Center - Web Interface
Real business integration with web and phone capabilities
"""

from flask import Flask, render_template, request, jsonify
import os
from heavenly_hands_call_center import HeavenlyHandsCallCenterAgent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize the call center agent
call_center_agent = HeavenlyHandsCallCenterAgent()

@app.route('/')
def index():
    """Main web interface"""
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Heavenly Hands Call Center - Gainesville, FL</title>
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                max-width: 1000px; 
                margin: 0 auto; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container { 
                background: white; 
                padding: 30px; 
                border-radius: 15px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            h1 { 
                color: #2c3e50; 
                text-align: center; 
                margin-bottom: 30px;
                font-size: 2.5em;
            }
            .call-box { 
                border: 3px solid #3498db; 
                border-radius: 15px; 
                padding: 25px; 
                margin: 20px 0; 
                background: #f8f9fa;
            }
            .conversation { 
                min-height: 400px; 
                max-height: 500px; 
                overflow-y: auto; 
                border: 2px solid #e9ecef; 
                padding: 20px; 
                background: #ffffff; 
                border-radius: 10px;
                margin: 20px 0;
            }
            .user-message { 
                background: linear-gradient(135deg, #3498db, #2980b9); 
                color: white; 
                padding: 15px; 
                border-radius: 15px; 
                margin: 10px 0; 
                text-align: right; 
                max-width: 80%;
                margin-left: auto;
            }
            .assistant-message { 
                background: linear-gradient(135deg, #27ae60, #2ecc71); 
                color: white; 
                padding: 15px; 
                border-radius: 15px; 
                margin: 10px 0; 
                max-width: 80%;
            }
            .input-area { 
                display: flex; 
                margin-top: 20px; 
                gap: 10px;
            }
            input[type="text"] { 
                flex: 1; 
                padding: 15px; 
                border: 2px solid #ddd; 
                border-radius: 25px; 
                font-size: 16px;
                outline: none;
                transition: border-color 0.3s;
            }
            input[type="text"]:focus {
                border-color: #3498db;
            }
            button { 
                padding: 15px 25px; 
                background: linear-gradient(135deg, #e74c3c, #c0392b); 
                color: white; 
                border: none; 
                border-radius: 25px; 
                cursor: pointer; 
                font-size: 16px;
                font-weight: bold;
                transition: transform 0.2s;
            }
            button:hover {
                transform: translateY(-2px);
            }
            .status { 
                background: #ecf0f1; 
                padding: 10px; 
                border-radius: 10px; 
                margin: 10px 0; 
                text-align: center;
                font-weight: bold;
            }
            .phone-info {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
                border-left: 5px solid #3498db;
            }
            .business-info {
                background: #e8f5e8;
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
                border-left: 5px solid #27ae60;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏠 Heavenly Hands Call Center</h1>
            <p style="text-align: center; color: #7f8c8d; font-size: 1.2em; margin-bottom: 30px;">
                Gainesville's Premier Cleaning Service - Real Business Integration
            </p>
            
            <div class="business-info">
                <h3>🏢 About Heavenly Hands Cleaning Service</h3>
                <p><strong>Owner:</strong> Steven Rodriguez</p>
                <p><strong>Location:</strong> Gainesville, Florida</p>
                <p><strong>Services:</strong> Residential & Commercial Cleaning</p>
                <p><strong>Areas Served:</strong> Gainesville, Alachua, Newberry, High Springs, Micanopy, Archer, Williston, Ocala</p>
                <p><strong>Experience:</strong> 8+ years serving North Central Florida</p>
            </div>
            
            <div class="call-box">
                <h3>📞 Live Call Simulation</h3>
                <div class="status" id="status">Ready to take your call</div>
                <div class="conversation" id="conversation">
                    <div class="assistant-message">
                        <strong>Steven (Owner):</strong> Hello and thank you for calling Heavenly Hands Cleaning Service, Gainesville's premier cleaning professionals. This is Steven, the owner. How may I help you today with your residential or commercial cleaning needs?
                    </div>
                </div>
                <div class="input-area">
                    <input type="text" id="userInput" placeholder="Type your message here..." onkeypress="handleKeyPress(event)">
                    <button onclick="sendMessage()">Send</button>
                    <button onclick="startNewCall()">New Call</button>
                </div>
            </div>
            
            <div class="phone-info">
                <h3>📱 Phone Integration Setup</h3>
                <p>To enable real phone calling:</p>
                <ol>
                    <li>Configure Twilio webhook: <code>https://heavenlyhands.avatararts.org/twilio/webhook</code></li>
                    <li>Set up your Twilio phone number: <strong>(352) 329-6150</strong></li>
                    <li>Test with real calls to your Twilio number</li>
                </ol>
                <p><strong>Current Status:</strong> Web interface ready, phone integration pending Twilio configuration</p>
            </div>
        </div>

        <script>
            let callId = 'CALL_' + Math.random().toString(36).substr(2, 9);
            
            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            }
            
            function startNewCall() {
                callId = 'CALL_' + Math.random().toString(36).substr(2, 9);
                document.getElementById('conversation').innerHTML = '<div class="assistant-message"><strong>Steven (Owner):</strong> Hello and thank you for calling Heavenly Hands Cleaning Service, Gainesville\'s premier cleaning professionals. This is Steven, the owner. How may I help you today with your residential or commercial cleaning needs?</div>';
                document.getElementById('status').textContent = 'New call started';
            }
            
            function sendMessage() {
                const userInput = document.getElementById('userInput');
                const userMessage = userInput.value.trim();
                
                if (!userMessage) return;
                
                // Add user message to conversation
                addMessageToConversation('user', userMessage);
                userInput.value = '';
                
                // Update status
                document.getElementById('status').textContent = 'Processing your request...';
                
                // Send to backend
                fetch('/api/process_message', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        call_id: callId,
                        message: userMessage
                    })
                })
                .then(response => response.json())
                .then(data => {
                    addMessageToConversation('assistant', data.response);
                    document.getElementById('status').textContent = `Intent: ${data.intent} | Confidence: ${(data.confidence || 0).toFixed(2)}`;
                })
                .catch(error => {
                    console.error('Error:', error);
                    addMessageToConversation('assistant', 'Sorry, there was an error processing your request.');
                    document.getElementById('status').textContent = 'Error occurred';
                });
            }
            
            function addMessageToConversation(role, message) {
                const conversation = document.getElementById('conversation');
                const messageDiv = document.createElement('div');
                messageDiv.className = role + '-message';
                
                if (role === 'assistant') {
                    messageDiv.innerHTML = `<strong>Steven (Owner):</strong> ${message}`;
                } else {
                    messageDiv.innerHTML = `<strong>Customer:</strong> ${message}`;
                }
                
                conversation.appendChild(messageDiv);
                conversation.scrollTop = conversation.scrollHeight;
            }
        </script>
    </body>
    </html>
    '''

@app.route('/api/process_message', methods=['POST'])
def process_message():
    """Process customer message"""
    data = request.get_json()
    call_id = data.get('call_id', 'unknown')
    message = data.get('message', '')
    
    # Process message through call center agent
    response = call_center_agent.process_customer_message(call_id, message)
    
    # Get call summary for additional info
    summary = call_center_agent.get_call_summary(call_id)
    
    return {
        'response': response,
        'intent': summary.get('intent_classification', 'unknown'),
        'confidence': summary.get('confidence_score', 0.0),
        'call_id': call_id
    }

@app.route('/api/call_summary/<call_id>')
def get_call_summary(call_id):
    """Get call summary"""
    summary = call_center_agent.get_call_summary(call_id)
    return summary

@app.route('/twilio/webhook', methods=['POST'])
def twilio_webhook():
    """Handle incoming Twilio phone calls"""
    from twilio.twiml import VoiceResponse
    
    response = VoiceResponse()
    
    # Get call details
    call_sid = request.form.get('CallSid', 'unknown')
    caller_id = request.form.get('From', 'unknown')
    
    # Process incoming call
    greeting = call_center_agent.process_incoming_call(call_sid, caller_id)
    
    # Create gather for user input
    gather = response.gather(
        input='speech',
        action='/twilio/process_speech',
        method='POST',
        timeout=3,
        speech_timeout='auto'
    )
    gather.say(greeting)
    
    # If no input, redirect to get input
    response.redirect('/twilio/webhook')
    
    return str(response)

@app.route('/twilio/process_speech', methods=['POST'])
def process_speech():
    """Process speech input from Twilio"""
    from twilio.twiml import VoiceResponse
    
    response = VoiceResponse()
    
    # Get speech result
    speech_result = request.form.get('SpeechResult', '')
    call_sid = request.form.get('CallSid', 'unknown')
    
    if speech_result:
        # Process the speech through call center agent
        agent_response = call_center_agent.process_customer_message(call_sid, speech_result)
        
        # Create gather for next input
        gather = response.gather(
            input='speech',
            action='/twilio/process_speech',
            method='POST',
            timeout=3,
            speech_timeout='auto'
        )
        gather.say(agent_response)
        
        # If no input, redirect to get input
        response.redirect('/twilio/webhook')
    else:
        # No speech detected, ask again
        gather = response.gather(
            input='speech',
            action='/twilio/process_speech',
            method='POST',
            timeout=3,
            speech_timeout='auto'
        )
        gather.say("I'm sorry, I didn't catch that. Could you please repeat?")
        response.redirect('/twilio/webhook')
    
    return str(response)

def main():
    """Main function to run the web server"""
    print("🎙️ Heavenly Hands Call Center - Web & Phone Integration")
    print("=" * 70)
    print("Starting web server for avatar arts.org deployment...")
    
    # Check for required environment variables
    required_vars = ['OPENAI_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"⚠️  Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these in your .env file:")
        for var in missing_vars:
            print(f"  {var}=your_actual_key_here")
        return
    
    print("✅ Environment variables loaded")
    print("🌐 Web interface: http://localhost:5000")
    print("📞 Phone webhook: http://localhost:5000/twilio/webhook")
    print("🚀 Ready for deployment to avatar arts.org!")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    main()