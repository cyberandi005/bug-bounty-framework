"""
XSS (Cross-Site Scripting) Scanner Module
"""

import requests
from typing import List, Dict
from urllib.parse import urljoin


class XSSScanner:
    """XSS vulnerability scanner"""
    
    def __init__(self, target: str):
        self.target = target
        self.findings = []
        self.payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "javascript:alert('XSS')",
            "<iframe src=javascript:alert('XSS')></iframe>",
            "<body onload=alert('XSS')>",
            "<input onfocus=alert('XSS') autofocus>",
        ]
    
    def scan(self) -> List[Dict]:
        """Scan for XSS vulnerabilities"""
        self._test_reflected_xss()
        self._test_dom_based_xss()
        self._test_stored_xss()
        
        return self.findings
    
    def _test_reflected_xss(self):
        """Test for reflected XSS"""
        for payload in self.payloads:
            try:
                response = requests.get(
                    f"{self.target}?search={payload}",
                    timeout=5
                )
                
                if payload in response.text:
                    self.findings.append({
                        'vulnerability': 'Reflected XSS',
                        'severity': 'HIGH',
                        'url': self.target,
                        'parameter': 'search',
                        'payload': payload,
                        'method': 'GET'
                    })
            except:
                pass
    
    def _test_dom_based_xss(self):
        """Test for DOM-based XSS"""
        try:
            response = requests.get(self.target, timeout=5)
            
            dom_patterns = [
                'innerHTML',
                'outerHTML',
                'eval(',
                'document.write',
            ]
            
            for pattern in dom_patterns:
                if pattern in response.text:
                    self.findings.append({
                        'vulnerability': 'Potential DOM-based XSS',
                        'severity': 'MEDIUM',
                        'url': self.target,
                        'pattern': pattern,
                        'type': 'Code analysis'
                    })
        except:
            pass
    
    def _test_stored_xss(self):
        """Test for stored XSS (comment, profile, etc)"""
        # This would typically involve POST requests and data persistence
        pass