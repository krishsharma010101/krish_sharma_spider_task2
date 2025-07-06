Advanced Recon Tool

A modular and extensible Python-based reconnaissance toolkit for automating information gathering during the initial phases of penetration testing.

Features:
- Port scanning and banner grabbing (Nmap)
- Web technology detection (WhatWeb)
- Email harvesting (theHarvester)
- Shodan IP intelligence (requires API key)
- Save results as JSON or CSV reports
- Modular toggles via command line

Requirements:

Python Libraries (install with pip):
nmap
shodan
requests

External Tools (install separately and add to system PATH):
- Nmap: https://nmap.org/
- WhatWeb: https://github.com/urbanadventurer/WhatWeb
- theHarvester: https://github.com/laramies/theHarvester

Directory Structure:
advanced-recon/
- recon.py
- requirements.txt
- reports/
- README.txt

Setup Instructions:

1. Clone the repository:
git clone https://github.com/yourusername/advanced-recon.git
cd advanced-recon

2. Install Python dependencies:
pip install -r requirements.txt

3. Set SHODAN API key (optional):
Linux/macOS: export SHODAN_API_KEY=your_api_key_here
Windows CMD: set SHODAN_API_KEY=your_api_key_here
PowerShell: $env:SHODAN_API_KEY="your_api_key_here"

4. Install WhatWeb (if not already):
git clone https://github.com/urbanadventurer/WhatWeb
cd WhatWeb
sudo gem install bundler
bundle install

Update the WhatWeb path in recon.py if needed.

Usage Example:
python recon.py --domain example.com --scan --tech --emails --shodan --report json

Available Arguments:
--domain      Target domain (required)
--scan        Enable port scanning and banner grabbing
--tech        Enable technology detection (WhatWeb)
--emails      Enable email harvesting (theHarvester)
--shodan      Enable Shodan lookup
--report      Save report as json or csv

Output:
Reports are saved in the reports/ folder as example_com.json or example_com.csv
If no --report is used, results are printed to the screen.

Example:
python recon.py --domain example.com --scan --emails --report csv

