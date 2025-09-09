#!/usr/bin/env python3
"""
Run this script to start the Streamlit application
"""

import subprocess
import sys
import os

def main():
    print("🚀 Starting Book Master - Red 8-bit AI Assistant...")
    app_file = "app.py"
    print("🎮 Running full version...")
    # Run streamlit app
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", app_file,
            "--server.headless", "true",
            "--server.port", "8501"
        ], cwd=os.path.dirname(__file__))
    except KeyboardInterrupt:
        print("\n👋 Thanks for using Book Master!")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("💡 Make sure Streamlit is installed: pip install streamlit")

if __name__ == "__main__":
    main()
