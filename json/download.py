"""
Script 200

This module provides functionality for script 200.

Author: Auto-generated
Date: 2025-11-01
"""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/hello", methods=["GET"])
def hello():
    """hello function."""

    return jsonify({"message": "Hello from Scripty's custom action!"})


if __name__ == "__main__":
    app.run(debug=True)
