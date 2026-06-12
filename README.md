# 🔐 Bug Bounty Framework

**Comprehensive Automated Security Testing & Vulnerability Detection Framework**

A powerful, modular Python framework untuk bug bounty hunters, penetration testers, dan security researchers. Framework ini mencakup automated scanning, vulnerability detection, OSINT, dan exploitation capabilities.

---

## 🚀 Features

### Core Scanning Modules
- ✅ **SQL Injection Detector** - Detect SQL injection vulnerabilities with multiple payloads
- ✅ **XSS Scanner** - Comprehensive cross-site scripting detection
- ✅ **CSRF Checker** - CSRF token validation and bypassing techniques
- ✅ **Directory Enumeration** - Fuzzing and directory discovery
- ✅ **API Testing** - Automated API endpoint testing and vulnerability detection
- ✅ **Authentication Bypass** - Test default credentials, brute force, and bypass techniques
- ✅ **OSINT Module** - Information gathering (subdomain enumeration, WHOIS, DNS, etc)

### Framework Features
- 🔄 Automated scanning pipeline
- 📊 Detailed vulnerability reporting (JSON, HTML, CSV)
- 📋 SQLite database untuk track findings
- 🎯 Multi-target support
- ⚙️ Configurable payloads dan detection rules
- 🧩 Modular & extensible architecture
- 💻 CLI interface dengan progress tracking

---

## 📦 Installation

```bash
# Clone repository
git clone https://github.com/cyberandi005/bug-bounty-framework.git
cd bug-bounty-framework

# Install dependencies
pip install -r requirements.txt

# Verify installation
python bbf.py --help
```

---

## 🎯 Quick Start

### Basic Scan
```bash
python bbf.py -u https://target.com --scan all
```

### Specific Vulnerability Scan
```bash
# SQL Injection
python bbf.py -u https://target.com/search.php?q= --sqli

# XSS
python bbf.py -u https://target.com --xss

# CSRF
python bbf.py -u https://target.com/form --csrf

# Directory Enumeration
python bbf.py -u https://target.com --dir-enum

# API Testing
python bbf.py -u https://api.target.com/v1/ --api-test

# Authentication Bypass
python bbf.py -u https://target.com/login --auth-bypass

# OSINT
python bbf.py -d target.com --osint
```

### Advanced Scanning
```bash
# Full automated scan dengan custom wordlist
python bbf.py -u https://target.com \
  --scan all \
  --wordlist custom-wordlist.txt \
  --threads 10 \
  --output report.json

# Scan multiple targets
python bbf.py -f targets.txt --scan all --output batch-report.html

# Resume previous scan
python bbf.py --resume session-id
```

---

## 📝 Usage Examples

### Example 1: Full Vulnerability Scan
```bash
python bbf.py -u https://vulnerable-app.com \
  --scan all \
  --threads 15 \
  --timeout 30 \
  --output full-report.json
```

### Example 2: API Security Testing
```bash
python bbf.py -u https://api.target.com/v1/ \
  --api-test \
  --api-key YOUR_API_KEY \
  --test-auth \
  --test-injection
```

### Example 3: OSINT Intelligence Gathering
```bash
python bbf.py -d target.com \
  --osint \
  --subdomains \
  --whois \
  --dns-records \
  --tech-stack
```

### Example 4: Authentication Security
```bash
python bbf.py -u https://target.com/login \
  --auth-bypass \
  --brute-force users.txt passwords.txt \
  --test-default-creds
```

---

## 🔧 Configuration

Edit `config/settings.json` untuk customize:

```json
{
  "scanning": {
    "threads": 10,
    "timeout": 30,
    "retry_count": 3
  },
  "payloads": {
    "sqli_payload_count": 50,
    "xss_payload_count": 100,
    "directory_wordlist": "wordlists/common.txt"
  },
  "detection": {
    "sensitive_patterns": true,
    "response_analysis": true
  },
  "output": {
    "formats": ["json", "html", "csv"],
    "detailed_report": true
  }
}
```

---

## 📚 Module Details

### 🔍 SQL Injection Detector
- Detection techniques: Time-based, Error-based, Boolean-based
- Multi-parameter testing
- DBMS identification
- Data extraction capabilities

### 🎨 XSS Scanner
- DOM-based XSS detection
- Reflected XSS testing
- Stored XSS vulnerability finding
- Payload encoding detection bypass

### 🛡️ CSRF Checker
- Token validation analysis
- Referer header checking
- SameSite cookie detection
- Exploit generation

### 📂 Directory Enumeration
- Multi-threaded fuzzing
- Custom wordlist support
- Status code filtering
- Recursive directory discovery

### 🔌 API Testing
- Endpoint discovery
- Method enumeration (GET, POST, PUT, DELETE)
- Authentication testing
- Rate limit detection
- Injection point identification

### 🔑 Authentication Bypass
- Default credential testing
- Brute force capabilities
- Session manipulation
- Cookie/Token analysis

### 🕵️ OSINT Module
- Subdomain enumeration
- WHOIS information
- DNS records lookup
- Technology stack detection
- Port scanning
- Email discovery

---

## 📁 Project Structure

```
bug-bounty-framework/
├── bbf.py                  # Main entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── config/
│   ├── settings.json      # Framework configuration
│   └── payloads/          # Vulnerability payloads
├── modules/
│   ├── __init__.py
│   ├── sqli_detector.py   # SQL Injection module
│   ├── xss_scanner.py     # XSS detection module
│   ├── csrf_checker.py    # CSRF vulnerability module
│   ├── dir_enum.py        # Directory enumeration
│   ├── api_tester.py      # API security testing
│   ├── auth_bypass.py     # Authentication bypass
│   └── osint.py           # OSINT information gathering
├── utils/
│   ├── __init__.py
│   ├── http_client.py     # HTTP request handler
│   ├── payloads.py        # Payload management
│   ├── logger.py          # Logging system
│   ���── database.py        # Database operations
│   ├── reporter.py        # Report generation
│   └── config.py          # Configuration management
├── wordlists/
│   ├── common.txt         # Common directories
│   ├── sqli-payloads.txt  # SQL injection payloads
│   └── xss-payloads.txt   # XSS payloads
├── db/
│   └── findings.db        # SQLite database
└── output/
    └── reports/           # Generated reports
```

---

## ⚠️ Disclaimer

⚠️ **IMPORTANT**: 
- Hanya gunakan framework ini untuk authorized security testing
- Dapatkan written permission sebelum testing target yang bukan milik lo
- Penulis tidak bertanggung jawab untuk misuse atau illegal activities
- Patuhi semua hukum dan regulasi yang berlaku

---

## 📖 Documentation

Lihat `/docs` untuk:
- Detailed module documentation
- Advanced usage scenarios
- Payload customization guide
- Integration with other tools
- Troubleshooting guide

---

## 🤝 Contributing

Contributions are welcome! Silakan:
- Fork repository
- Create feature branch
- Submit pull requests
- Report bugs dan suggest improvements

---

## 📄 License

MIT License - Gunakan dengan bertanggung jawab

---

## 📞 Contact & Support

- 📧 Email: puangandi.006@gmail.com
- 🐙 GitHub: [@cyberandi005](https://github.com/cyberandi005)
- 💬 Issues: Report bugs dan feature requests di GitHub Issues

---

**Happy Bug Hunting! 🎯🔐**

*Keep learning, stay ethical, and help make the internet safer!*