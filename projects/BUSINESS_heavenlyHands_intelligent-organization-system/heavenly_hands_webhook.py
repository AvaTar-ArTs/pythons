from flask import Flask, request
from twilio.twiml import VoiceResponse
import json

app = Flask(__name__)

@app.route('/handle_gather', methods=['POST'])
def handle_gather():
    """Handle phone keypad input"""
    response = VoiceResponse()
    digits = request.form.get('Digits', '')
    
    if digits == '1':
        response.say("Great! For residential cleaning, we offer weekly, bi-weekly, or monthly services. Our rates start at $120 for a 3-bedroom home.")
        response.say("Press 1 to schedule a free consultation, or 2 to speak with our team.")
    elif digits == '2':
        response.say("For commercial cleaning, we provide customized solutions for offices, retail spaces, and more. Our commercial rates are competitive and flexible.")
        response.say("Press 1 to schedule a free consultation, or 2 to speak with our team.")
    elif digits == '3':
        response.say("Move-in and move-out cleaning is our specialty! We ensure your new home is spotless or help you get your deposit back.")
        response.say("Press 1 to schedule a free consultation, or 2 to speak with our team.")
    elif digits == '4':
        response.say("Connecting you to our team now. Please hold while we transfer your call.")
        response.dial("+1234567890")  # Replace with actual number
    else:
        response.say("I didn't understand your selection. Please call us back at your convenience.")
    
    response.hangup()
    return str(response)

@app.route('/handle_lead_gather', methods=['POST'])
def handle_lead_gather():
    """Handle lead generation call input"""
    response = VoiceResponse()
    digits = request.form.get('Digits', '')
    
    if digits == '1':
        response.say("Perfect! We'll schedule your free consultation. Our team will call you within 24 hours to set up a convenient time.")
        response.say("Thank you for choosing Heavenly Hands Cleaning Service!")
    elif digits == '2':
        response.say("Our residential cleaning starts at $120 for a 3-bedroom home. Commercial rates vary based on size and frequency.")
        response.say("Press 1 to schedule a free consultation for a personalized quote.")
    elif digits == '3':
        response.say("Connecting you to our team now. Please hold while we transfer your call.")
        response.dial("+1234567890")  # Replace with actual number
    elif digits == '0':
        response.say("We'll remove you from our call list. Thank you for your time.")
    else:
        response.say("I didn't understand your selection. Please call us back at your convenience.")
    
    response.hangup()
    return str(response)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
