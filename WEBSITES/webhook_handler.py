#!/usr/bin/env python3
"""
Twilio Webhook Handler for Heavenly Hands
=========================================

Handles incoming calls from Twilio and routes them to the AI voice agent.
Deployed at: https://avatararts.org/hh/heavenlyhands/webhook
"""

import logging
import os

from flask import Flask, Response, request
from twilio.rest import Client
from twilio.twiml.voice_response import Gather, VoiceResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load environment variables
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv(
    "TWILIO_ACCOUNT_SID", "AC607a77ee54a4dddf63034fe4b3713fb9"
)
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "yI6ZMK7hHgDZt1UzkZsSpAfD2S10laJB")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "+13525811245")

# Initialize Twilio client
try:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    logger.info("Twilio client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Twilio client: {e}")
    client = None


@app.route("/", methods=["POST"])
def webhook():
    """Handle incoming Twilio webhook calls"""
    try:
        # Get call information from Twilio
        call_sid = request.form.get("CallSid")
        from_number = request.form.get("From")
        to_number = request.form.get("To")

        logger.info(
            f"Incoming call - SID: {call_sid}, From: {from_number}, To: {to_number}"
        )

        # Create TwiML response
        response = VoiceResponse()

        # Welcome message
        response.say(
            "Hello! Thank you for calling Heavenly Hands Cleaning Service. "
            "We're Gainesville's premier cleaning professionals with over 8 years of experience. "
            "How can I help you today?",
            voice="alice",
            language="en-US",
        )

        # Gather user input
        gather = Gather(
            num_digits=1,
            action="/hh/heavenlyhands/webhook/handle-input",
            method="POST",
            timeout=10,
        )
        gather.say(
            "Press 1 for residential cleaning services, "
            "press 2 for commercial cleaning, "
            "press 3 to speak with our owner Kimberly, "
            "or press 0 to hear our business hours and location.",
            voice="alice",
        )

        response.append(gather)

        # Fallback if no input
        response.say(
            "I didn't receive any input. Please call back and we'll be happy to help you. "
            "You can also visit us at heavenlyhands.avatararts.org. Thank you!",
            voice="alice",
        )

        return Response(str(response), mimetype="text/xml")

    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        response = VoiceResponse()
        response.say(
            "I'm sorry, there was a technical issue. Please call back later or visit our website. Thank you.",
            voice="alice",
        )
        return Response(str(response), mimetype="text/xml")


@app.route("/handle-input", methods=["POST"])
def handle_input():
    """Handle user input from the gather"""
    try:
        digits = request.form.get("Digits", "")
        call_sid = request.form.get("CallSid")

        logger.info(f"Received input: {digits} for call {call_sid}")

        response = VoiceResponse()

        if digits == "1":
            # Residential cleaning
            response.say(
                "Great! For residential cleaning services, we offer regular house cleaning, "
                "deep cleaning, move-in and move-out cleaning, and Airbnb turnover services. "
                "Our rates start at $120 for a standard 3-bedroom home. "
                "Would you like to schedule a cleaning? Press 1 for yes, or 2 to speak with Kimberly.",
                voice="alice",
            )

        elif digits == "2":
            # Commercial cleaning
            response.say(
                "For commercial cleaning services, we provide office cleaning, "
                "retail space cleaning, and post-construction cleanup. "
                "We're licensed, bonded, and insured for commercial work. "
                "Press 1 to schedule a consultation, or 2 to speak with Kimberly.",
                voice="alice",
            )

        elif digits == "3":
            # Speak with Kimberly
            response.say(
                "I'll connect you with Kimberly Moeller, our owner. "
                "Please hold while I transfer your call to our main number.",
                voice="alice",
            )
            response.dial("+13525811245")

        elif digits == "0":
            # Business hours and location
            response.say(
                "Heavenly Hands Cleaning Service is located in Gainesville, Florida. "
                "We serve Gainesville, Ocala, Alachua, High Springs, Newberry, and Micanopy. "
                "Our business hours are Monday through Friday, 8 AM to 6 PM, "
                "and Saturday 9 AM to 4 PM. We're closed on Sundays. "
                "For immediate service, press 1 to speak with Kimberly.",
                voice="alice",
            )

        else:
            # Invalid input
            response.say(
                "I didn't understand that option. Let me connect you with Kimberly directly. "
                "Please hold while I transfer your call.",
                voice="alice",
            )
            response.dial("+13525811245")

        return Response(str(response), mimetype="text/xml")

    except Exception as e:
        logger.error(f"Error handling input: {e}")
        response = VoiceResponse()
        response.say(
            "I'm sorry, there was a technical issue. Let me connect you with Kimberly directly.",
            voice="alice",
        )
        response.dial("+13525811245")
        return Response(str(response), mimetype="text/xml")


@app.route("/status", methods=["POST"])
def status_callback():
    """Handle call status updates from Twilio"""
    try:
        call_sid = request.form.get("CallSid")
        call_status = request.form.get("CallStatus")
        duration = request.form.get("CallDuration", "0")

        logger.info(f"Call {call_sid} status: {call_status}, duration: {duration}")

        # Log call completion for analytics
        if call_status == "completed":
            logger.info(
                f"Call completed - SID: {call_sid}, Duration: {duration} seconds"
            )

        return Response("OK", mimetype="text/plain")

    except Exception as e:
        logger.error(f"Error in status callback: {e}")
        return Response("ERROR", mimetype="text/plain")


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Heavenly Hands Twilio Webhook",
        "twilio_configured": client is not None,
    }


if __name__ == "__main__":
    # Production configuration
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "False").lower() == "true"

    logger.info(f"Starting Heavenly Hands webhook server on port {port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
