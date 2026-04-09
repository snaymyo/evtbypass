#!/usr/bin/env python3
# run.py - EVT Bypass V3.0 Launcher (Termux Compatible)

import os
import sys
import subprocess

def main():
    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    so_file = os.path.join(current_dir, "app.so")
    
    # Check if app.so exists
    if not os.path.exists(so_file):
        print(f"[!] Error: app.so not found")
        print("[*] Make sure app.so is in the same directory")
        sys.exit(1)
    
    # Method 1: Try with LD_LIBRARY_PATH
    env = os.environ.copy()
    env['LD_LIBRARY_PATH'] = current_dir + ':' + env.get('LD_LIBRARY_PATH', '')
    
    # Run using python -c
    cmd = [
        'python3', '-c',
        f'''
import sys
sys.path.insert(0, "{current_dir}")
import app
if hasattr(app, 'start_process'):
    app.start_process()
elif hasattr(app, 'main'):
    app.main()
'''
    ]
    
    try:
        subprocess.run(cmd, env=env, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[!] Error running app.so: {e}")
    except KeyboardInterrupt:
        print("\n[!] Stopped by user")

if __name__ == "__main__":
    main()