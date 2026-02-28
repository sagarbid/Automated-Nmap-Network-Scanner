# 🔍 Automated Nmap Network Scanner

> **Python-based CLI tool to automate network reconnaissance using Nmap — mimicking the initial enumeration phase of a professional penetration test.**

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![Nmap](https://img.shields.io/badge/Tool-Nmap-orange?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Linux-yellow?style=flat-square)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=flat-square)
![Type](https://img.shields.io/badge/Type-Red%2FBlue%20Team-red?style=flat-square)

---

## 📌 Project Overview

Developed as part of the **Monash University Cybersecurity Bootcamp (2024)**, this tool automates network reconnaissance by wrapping Nmap's powerful scanning capabilities in a Python CLI interface. The goal was to reduce manual repetition in the enumeration phase and produce structured output that feeds directly into threat analysis workflows.

This project demonstrates scripting for security automation — a core skill for both Red Team (offensive) and Blue Team (defensive) roles.

---

## 🎯 Objectives

- Automate network host discovery and port scanning
- Identify open ports, running services, and OS fingerprints
- Export scan results in structured format for downstream analysis
- Replicate the initial reconnaissance phase of a penetration testing engagement

---

## 🛠️ Tools & Technologies

| Tool | Purpose |
|------|---------|
| Python 3 | Core scripting language |
| Nmap | Network scanning engine |
| python-nmap | Python wrapper for Nmap |
| argparse | CLI argument parsing |
| JSON/CSV | Structured output formats |

---

## ⚙️ Features

- **Target flexibility** — scan single IPs, CIDR ranges, or hostname lists
- **Scan profiles** — quick scan, full port scan, service version detection, OS detection
- **Structured export** — results saved to JSON or CSV for analysis or SIEM ingestion
- **CLI options** — clean argument parsing for easy integration into larger workflows
- **Verbose logging** — detailed output for audit trails

---

## 🚀 Usage

```bash
# Basic scan
python scanner.py --target 192.168.1.0/24

# Full port scan with service detection
python scanner.py --target 192.168.1.100 --mode full --output results.json

# Quick scan with CSV export
python scanner.py --target 192.168.1.0/24 --mode quick --output results.csv
```

---

## 🔬 Sample Output

```json
{
  "host": "192.168.1.10",
  "status": "up",
  "ports": [
    {"port": 22, "state": "open", "service": "ssh", "version": "OpenSSH 8.2"},
    {"port": 80, "state": "open", "service": "http", "version": "Apache 2.4.41"},
    {"port": 443, "state": "open", "service": "https", "version": "Apache 2.4.41"}
  ],
  "os_guess": "Linux 5.x"
}
```

---

## 🔐 Penetration Testing Context

In a real engagement, this tool supports the **Reconnaissance** and **Scanning** phases of the penetration testing lifecycle:

```
Reconnaissance → Scanning → Enumeration → Exploitation → Post-Exploitation → Reporting
      ✅               ✅
```

Results feed directly into vulnerability assessment tools like Nessus or Metasploit for the next phase.

---

## ⚠️ Legal & Ethical Disclaimer

This tool is for **authorised security testing and educational use only**. Never run network scans against systems you do not own or have explicit written permission to test. Unauthorised scanning is illegal in Australia under the Criminal Code Act 1995.

---

## 👤 Author

**Sagar Bidari**
CompTIA Security+ CE | Monash University Cybersecurity Bootcamp Graduate
🌐 [bidarisagar.com](https://bidarisagar.com) | 💼 [LinkedIn](https://linkedin.com/in/sagarbidari)
