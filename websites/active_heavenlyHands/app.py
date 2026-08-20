#!/usr/bin/env python3
"""
Heavenly Hands Call Tracking System
Main application for heavenlyhands.avatararts.org
"""

import os
import sys
from flask import Flask, render_template, request, jsonify, redirect, url_for
from twilio.rest import Client
from twilio.twiml import VoiceResponse
import sqlite3
import json
from datetime import datetime, timedelta
import logging
from twilio_config import *

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = SECRET_KEY

# Initialize Twilio client
try:
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    logger.info("Twilio client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Twilio client: {e}")
    twilio_client = None

def init_database():
    """Initialize the SQLite database"""
    conn = sqlite3.connect('heavenly_hands.db')
    cursor = conn.cursor()
    
    # Create calls table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            call_sid TEXT UNIQUE,
            from_number TEXT,
            to_number TEXT,
            status TEXT,
            duration INTEGER,
            start_time DATETIME,
            end_time DATETIME,
            recording_url TEXT,
            transcription TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create leads table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT,
            name TEXT,
            email TEXT,
            service_type TEXT,
            call_sid TEXT,
            status TEXT DEFAULT 'new',
            notes TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully")

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('heavenly_hands_dashboard.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming calls from Twilio"""
    try:
        call_sid = request.form.get('CallSid')
        from_number = request.form.get('From')
        to_number = request.form.get('To')
        
        logger.info(f"Incoming call: {call_sid} from {from_number} to {to_number}")
        
        # Store call in database
        conn = sqlite3.connect('heavenly_hands.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO calls (call_sid, from_number, to_number, status, start_time)
            VALUES (?, ?, ?, ?, ?)
        ''', (call_sid, from_number, to_number, 'in-progress', datetime.now()))
        conn.commit()
        conn.close()
        
        # Create TwiML response
        response = VoiceResponse()
        
        # Greeting
        response.say("Thank you for calling Heavenly Hands Cleaning Services. How can we help you today?")
        
        # Gather input
        gather = response.gather(
            num_digits=1,
            action='/handle-input',
            method='POST',
            timeout=10
        )
        gather.say("Press 1 for residential cleaning, 2 for commercial cleaning, or 3 to speak with a representative.")
        
        # Fallback if no input
        response.say("We didn't receive your selection. Please call back and try again.")
        response.hangup()
        
        return str(response)
        
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        response = VoiceResponse()
        response.say("Sorry, we're experiencing technical difficulties. Please try again later.")
        response.hangup()
        return str(response)

@app.route('/handle-input', methods=['POST'])
def handle_input():
    """Handle user input from call"""
    try:
        digits = request.form.get('Digits')
        call_sid = request.form.get('CallSid')
        
        response = VoiceResponse()
        
        if digits == '1':
            response.say("You selected residential cleaning. Please hold while we connect you to our residential cleaning specialist.")
            # Here you would transfer to a specific number or queue
        elif digits == '2':
            response.say("You selected commercial cleaning. Please hold while we connect you to our commercial cleaning specialist.")
            # Here you would transfer to a specific number or queue
        elif digits == '3':
            response.say("Please hold while we connect you to a representative.")
            # Here you would transfer to a general number
        else:
            response.say("Invalid selection. Please call back and try again.")
            response.hangup()
        
        return str(response)
        
    except Exception as e:
        logger.error(f"Handle input error: {e}")
        response = VoiceResponse()
        response.say("Sorry, we're experiencing technical difficulties. Please try again later.")
        response.hangup()
        return str(response)

@app.route('/api/calls')
def get_calls():
    """API endpoint to get call data"""
    try:
        conn = sqlite3.connect('heavenly_hands.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT call_sid, from_number, to_number, status, duration, start_time, end_time
            FROM calls
            ORDER BY created_at DESC
            LIMIT 50
        ''')
        calls = cursor.fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'calls': [
                {
                    'call_sid': call[0],
                    'from_number': call[1],
                    'to_number': call[2],
                    'status': call[3],
                    'duration': call[4],
                    'start_time': call[5],
                    'end_time': call[6]
                }
                for call in calls
            ]
        })
    except Exception as e:
        logger.error(f"Get calls error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/leads')
def get_leads():
    """API endpoint to get lead data"""
    try:
        conn = sqlite3.connect('heavenly_hands.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, phone_number, name, email, service_type, status, created_at
            FROM leads
            ORDER BY created_at DESC
            LIMIT 50
        ''')
        leads = cursor.fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'leads': [
                {
                    'id': lead[0],
                    'phone_number': lead[1],
                    'name': lead[2],
                    'email': lead[3],
                    'service_type': lead[4],
                    'status': lead[5],
                    'created_at': lead[6]
                }
                for lead in leads
            ]
        })
    except Exception as e:
        logger.error(f"Get leads error: {e}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    # Initialize database
    init_database()
    
    # Start the application
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=DEBUG)