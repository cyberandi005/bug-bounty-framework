"""
API Security Testing Module
"""

import requests
from typing import List, Dict
import json


class APITester:
    """API endpoint security testing"""
    
    def __init__(self, target: str):
        self.target = target
        self.findings = []
    
    def test(self) -> List[Dict]:
        """Test API security"""
        self._test_authentication()
        self._test_injection()
        self._test_exposure()
        self._test_rate_limit()
        
        return self.findings
    
    def _test_authentication(self):
        """Test API authentication"""
        try:
            # Test without authentication
            response = requests.get(self.target, timeout=5)
            
            if response.status_code == 200:
                self.findings.append({
                    'vulnerability': 'Unauthenticated API Access',
                    'severity': 'CRITICAL',
                    'url': self.target,
                    'issue': 'API accessible without authentication'
                })
        except:
            pass
    
    def _test_injection(self):
        """Test API injection vulnerabilities"""
        injection_payloads = [
            "' OR '1'='1",
            "<script>alert('XSS')</script>",
            "../../../etc/passwd",
        ]
        
        for payload in injection_payloads:
            try:
                response = requests.get(
                    f"{self.target}?search={payload}",
                    timeout=5
                )
                
                if payload in response.text:
                    self.findings.append({
                        'vulnerability': 'API Injection Vulnerability',
                        'severity': 'HIGH',
                        'url': self.target,
                        'payload': payload
                    })
            except:
                pass
    
    def _test_exposure(self):
        """Test for sensitive data exposure"""
        try:
            response = requests.get(self.target, timeout=5)
            
            sensitive_patterns = [
                'password', 'api_key', 'secret', 'token',
                'credit_card', 'ssn', 'private_key'
            ]
            
            for pattern in sensitive_patterns:
                if pattern in response.text.lower():
                    self.findings.append({
                        'vulnerability': 'Sensitive Data Exposure',
                        'severity': 'HIGH',
                        'url': self.target,
                        'pattern': pattern
                    })
        except:
            pass
    
    def _test_rate_limit(self):
        """Test API rate limiting"""
        try:
            # Make multiple requests
            for i in range(100):
                response = requests.get(self.target, timeout=5)
                
                if 'X-RateLimit' not in response.headers:
                    self.findings.append({
                        'vulnerability': 'Missing Rate Limiting',
                        'severity': 'MEDIUM',
                        'url': self.target,
                        'issue': 'API does not implement rate limiting headers'
                    })
                    break
        except:
            pass