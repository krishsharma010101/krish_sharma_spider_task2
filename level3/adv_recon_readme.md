
Advanced Recon Tool - Setup and Usage Guide
===========================================

This tool performs deep reconnaissance on a target domain and generates an HTML report.

Requirements
------------
- Python 3.8+
- Install the following Python libraries:
  pip install -r requirements.txt

Manual Installations Required
-----------------------------
- GoWitness (used for screenshots)
  Install GoWitness and place gowitness.exe at:
  C:\Users\Krish Sharma\go\bin\gowitness.exe

- theHarvester (used for email harvesting)
  Clone from: https://github.com/laramies/theHarvester

- whatweb (for technology detection)
  Install via: `pip install whatweb` or follow setup at https://github.com/urbanadventurer/WhatWeb

- wafw00f (for WAF detection)
  pip install wafw00f

- nmap (ensure it’s installed and added to PATH)

Folder Structure
----------------
project/

── adv_recon.py               # Main recon script
── flask_app.py               # Flask UI
── templates/
   ── report.html            # Jinja2 HTML template for report
── static/
   ── screenshots/           # Screenshots saved here by GoWitness
── requirements.txt           # Python dependencies

Setup Instructions
------------------
1. Install Python dependencies:
   pip install -r requirements.txt

2. Download or install the following CLI tools and make sure they are in your PATH:
   - gowitness.exe
   - nmap
   - wafw00f
   - theHarvester
   - whatweb

3. Ensure `gowitness.exe` path is defined in `adv_recon.py`.

Usage
-----
Command-line:
    python adv_recon.py example.com

Flask UI:
    python flask_app.py
    Visit: http://127.0.0.1:5000

Generated Output
----------------
- HTML Report: example.com_report.html
- Screenshots saved in: static/screenshots/
