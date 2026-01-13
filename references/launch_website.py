#!/usr/bin/env python3
"""
AI Alchemy Website Launcher
Launch the business website with minimal black and red theme
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

def launch_website():
    """Launch the AI Alchemy business website"""
    
    # Get the directory containing this script
    script_dir = Path(__file__).parent
    website_dir = script_dir / "03_business_website"
    
    # Check if website files exist
    if not (website_dir / "index.html").exists():
        print("❌ Website files not found!")
        print(f"Expected: {website_dir / 'index.html'}")
        return False
    
    # Change to website directory
    os.chdir(website_dir)
    
    # Set up the server
    PORT = 8080
    
    # Try different ports if 8080 is occupied
    for port in range(8080, 8090):
        try:
            handler = http.server.SimpleHTTPRequestHandler
            with socketserver.TCPServer(("", port), handler) as httpd:
                print(f"🚀 AI Alchemy website launched!")
                print(f"📍 Local URL: http://localhost:{port}")
                print(f"📁 Serving from: {website_dir}")
                print(f"🎨 Theme: Minimal Black & Red")
                print(f"🌐 Your sites: avatararts.org | GPTJunkie.com | QuantumforgeLabs.org")
                print("\n" + "="*60)
                print("🎯 BUSINESS EMPIRE LAUNCHED!")
                print("="*60)
                print("📊 Revenue Streams:")
                print("   • Freelance Services: $2,500-15,000")
                print("   • Digital Products: $49-999")
                print("   • SaaS Subscriptions: $29-199/month")
                print("   • Course Sales: $497-4,997")
                print("   • Content Monetization: YouTube, affiliates")
                print("="*60)
                print("\nPress Ctrl+C to stop the server")
                print("="*60)
                
                # Open browser
                webbrowser.open(f"http://localhost:{port}")
                
                # Start serving
                httpd.serve_forever()
                
        except OSError:
            continue
    
    print("❌ Could not find an available port (8080-8089)")
    return False

if __name__ == "__main__":
    try:
        launch_website()
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        print("✅ AI Alchemy website session ended")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error launching website: {e}")
        sys.exit(1)