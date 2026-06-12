"""
OSINT (Open Source Intelligence) Module
"""

import socket
import requests
from typing import List, Dict


class OSINTModule:
    """OSINT information gathering"""
    
    def __init__(self):
        self.findings = []
    
    def gather(self, domain: str) -> List[Dict]:
        """Gather OSINT information"""
        self._get_dns_records(domain)
        self._get_whois_info(domain)
        self._enumerate_subdomains(domain)
        self._detect_technology(domain)
        
        return self.findings
    
    def _get_dns_records(self, domain: str):
        """Get DNS records"""
        try:
            ip = socket.gethostbyname(domain)
            self.findings.append({
                'information': 'DNS A Record',
                'domain': domain,
                'ip': ip
            })
            
            try:
                mx = socket.getmxrrdata(domain)
                self.findings.append({
                    'information': 'DNS MX Records',
                    'domain': domain,
                    'mx': mx
                })
            except:
                pass
        except:
            pass
    
    def _get_whois_info(self, domain: str):
        """Get WHOIS information"""
        try:
            # This would require whois library
            self.findings.append({
                'information': 'WHOIS Data',
                'domain': domain,
                'note': 'Install whois library for full details'
            })
        except:
            pass
    
    def _enumerate_subdomains(self, domain: str):
        """Enumerate subdomains"""
        common_subdomains = [
            'www', 'mail', 'ftp', 'api', 'admin', 'test',
            'dev', 'staging', 'cdn', 'blog', 'shop',
        ]
        
        for subdomain in common_subdomains:
            try:
                full_domain = f"{subdomain}.{domain}"
                ip = socket.gethostbyname(full_domain)
                
                self.findings.append({
                    'information': 'Subdomain Found',
                    'subdomain': full_domain,
                    'ip': ip
                })
            except:
                pass
    
    def _detect_technology(self, domain: str):
        """Detect web technologies"""
        try:
            response = requests.get(f"https://{domain}", timeout=5)
            
            tech_indicators = {
                'X-Powered-By': 'Server Framework',
                'Server': 'Web Server',
                'X-AspNet-Version': 'ASP.NET Version',
            }
            
            for header, tech_type in tech_indicators.items():
                if header in response.headers:
                    self.findings.append({
                        'information': 'Technology Detection',
                        'domain': domain,
                        'type': tech_type,
                        'value': response.headers[header]
                    })
        except:
            pass