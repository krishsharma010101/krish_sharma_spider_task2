Domain Recon Tool – Setup & Usage Instructions
==============================================

Overview:
---------
This is a Python-based tool that automates fundamental recon tasks on a given domain. It fetches:

- Subdomains
- DNS Records (A, NS, MX)
- WHOIS Information
- HTTP Response Headers
- robots.txt & sitemap.xml
- GeoIP Information

Step-by-Step Setup Guide:
--------------------------
1. Install Python (if not already installed):
   Ensure Python 3.6+ is installed. You can check by running:
   python --version

2. Clone or Download the Tool Files:
   Download or copy the Python script (e.g., recon.py) into a folder on your system.

3. Install Required Python Libraries:
   Open terminal or command prompt in that folder and run:
   pip install requests dnspython python-whois

4. Install CLI whois (Optional but Recommended):
   If python-whois fails, fallback uses the system’s whois command:
   - On Ubuntu/Debian:
     sudo apt install whois
   - On macOS:
     brew install whois

How to Use the Tool:
---------------------
You can run it two ways:

1. Command Line Input:
   python recon.py example.com

2. Manual Prompt (if no domain is passed):
   python recon.py
   # Then when prompted, type: example.com

Output:
-------
- Results will display in the terminal.
- A text file will be created in the current directory with the format:
  basic_example_com.txt

Optional: Creating requirements.txt for Reuse:
----------------------------------------------
If you're sharing the tool, create a requirements.txt file with:

requests
dnspython
python-whois

Then users can run:
pip install -r requirements.txt

That's it! Your domain recon tool is ready to go.
