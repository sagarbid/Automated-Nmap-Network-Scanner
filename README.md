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
pip install -r requirements.txt   # installs python-nmap
sudo apt install nmap             # the nmap binary itself

# Basic scan
python scanner.py --target 192.168.1.0/24

# Full port scan with service detection
python scanner.py --target 192.168.1.100 --mode full --output results.json

# Quick scan with CSV export
python scanner.py --target 192.168.1.0/24 --mode quick --output results.csv
```

Scan profiles map to real Nmap flags, not placeholders:

| Mode | Nmap flags |
|---|---|
| `quick` | `-T4 -F` |
| `full` | `-sV -T4 -p-` |
| `service` | `-sV -T4` |
| `os` | `-O -T4` |

---

## 🔬 Sample Output

Actual output from `python scanner.py --target 127.0.0.1 --mode quick` run against a local test host with no open ports in the scanned range — this is a genuine run, not a mocked example:

```json
{
  "target": "127.0.0.1",
  "mode": "quick",
  "nmap_args": "-T4 -F",
  "scanned_at": "2026-10-02T06:46:47.966608+00:00",
  "hosts": [
    {
      "host": "127.0.0.1",
      "status": "up",
      "ports": [],
      "os_guess": null
    }
  ]
}
```

When a scanned host has open ports, each one appears under `"ports"` as `{"port": 22, "protocol": "tcp", "state": "open", "service": "ssh", "version": "OpenSSH 8.2"}` — the field names come straight from `python-nmap`'s parsed results, not hand-typed.

---

## 🔐 Penetration Testing Context

In a real engagement, this tool supports the **Reconnaissance** and **Scanning** phases of the penetration testing lifecycle:

```
Reconnaissance → Scanning → Enumeration → Exploitation → Post-Exploitation → Reporting
      ✅               ✅
```

Results feed directly into vulnerability assessment tools like Nessus or Metasploit for the next phase.

---

## 💡 Lessons Learned

- **`python-nmap` just shells out to the real `nmap` binary and parses its XML output** — it's a convenience wrapper, not a reimplementation. That means the tool is only ever as fast or as noisy on the network as a raw Nmap scan with the same flags would be; the Python layer buys structured output, not a different scan.
- **The `-F` (fast) flag in "quick" mode only checks the 100 most common ports.** That's fine for a sweep but it will silently miss anything running on a nonstandard port — worth knowing before trusting a "no open ports" result.
- **CIDR ranges change the output shape**, not just the target count: `scanner.all_hosts()` only returns hosts that actually responded, so a /24 scan of a mostly-empty subnet returns a short host list, not 254 "down" entries. The export code had to account for that rather than assuming every target IP gets a row.

## 🔧 What I'd Improve

- **Add a `--timing` flag exposing Nmap's `-T0` to `-T5` directly**, instead of hardcoding `T4` into every profile — right now the aggressiveness isn't configurable, which matters on a network where you don't want to be noisy.
- **Service-version detection (`-sV`) needs root/sudo for some probes** and the script doesn't check for that or fail with a clear message — right now a permission issue just produces an empty result, which could be misread as "no open ports" when it's actually "scan didn't run properly."
- **No retry/timeout handling** for a host that's up but slow to respond — a single unresponsive host can stall a CIDR sweep longer than it should.
- **CSV export doesn't escape service/version strings** that might contain commas (e.g. a banner with a comma in it) — low risk, but worth fixing before feeding this into anything downstream automatically.

---

## ⚠️ Legal & Ethical Disclaimer

This tool is for **authorised security testing and educational use only**. Never run network scans against systems you do not own or have explicit written permission to test. Unauthorised scanning is illegal in Australia under the Criminal Code Act 1995.

---

## 👤 Author

**Sagar Bidari**
CompTIA Security+ CE | Monash University Cybersecurity Bootcamp Graduate
🌐 [bidarisagar.com](https://bidarisagar.com) | 💼 [LinkedIn](https://linkedin.com/in/sagarbidari)
