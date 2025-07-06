from flask import Flask, render_template, request
from adv_recon import run_recon
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    domain = request.form["domain"]
    modules = {
        "subdomains": "subdomains" in request.form,
        "dns": "dns" in request.form,
        "whois": "whois" in request.form,
        "headers": "headers" in request.form,
        "robots_sitemap": "robots_sitemap" in request.form,
        "port_scan": "port_scan" in request.form,
        "technologies": "technologies" in request.form,
        "emails": "emails" in request.form,
        "shodan": "shodan" in request.form,
        "waf": "waf" in request.form,
        "screenshots": "screenshots" in request.form
    }

    result = run_recon(domain, modules)
    report_file = f"{domain}_report.html"

    return render_template("result.html", domain=domain, data=result, report_file=report_file)

@app.route("/report/<path:filename>")
def report(filename):
    return app.send_static_file(filename)

if __name__ == "__main__":
    os.makedirs("screenshots", exist_ok=True)
    app.run(debug=True)
