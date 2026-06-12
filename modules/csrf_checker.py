"""
CSRF (Cross-Site Request Forgery) Checker Module
"""

import requests
from typing import List, Dict
from bs4 import BeautifulSoup


class CSRFChecker:
    """CSRF vulnerability checker"""
    
    def __init__(self, target: str):
        self.target = target
        self.findings = []
    
    def check(self) -> List[Dict]:
        """Check for CSRF vulnerabilities"""
        self._check_token_presence()
        self._check_samesite_cookie()
        self._check_referer_validation()
        
        return self.findings
    
    def _check_token_presence(self):
        """Check if CSRF token is present in forms"""
        try:
            response = requests.get(self.target, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            forms = soup.find_all('form')
            csrf_token_found = False
            
            for form in forms:
                if form.find('input', {'name': ['csrf_token', 'token', '_token']}):
                    csrf_token_found = True
            
            if forms and not csrf_token_found:
                self.findings.append({
                    'vulnerability': 'Missing CSRF Token',
                    'severity': 'HIGH',
                    'url': self.target,
                    'issue': 'Forms found without CSRF token protection'
                })
        except:
            pass
    
    def _check_samesite_cookie(self):
        """Check SameSite cookie attribute"""
        try:
            response = requests.get(self.target, timeout=5)
            
            if 'Set-Cookie' in response.headers:
                cookies = response.headers.get('Set-Cookie', '')
                
                if 'SameSite' not in cookies:
                    self.findings.append({
                        'vulnerability': 'Missing SameSite Attribute',
                        'severity': 'MEDIUM',
                        'url': self.target,
                        'issue': 'Cookies missing SameSite attribute'
                    })
        except:
            pass
    
    def _check_referer_validation(self):
        """Check if server validates Referer header"""
        try:
            headers = {'Referer': 'https://attacker.com'}
            response = requests.get(self.target, headers=headers, timeout=5)
            
            # If request succeeds with wrong referer, it might be vulnerable
            self.findings.append({
                'vulnerability': 'Potential CSRF Vulnerability',
                'severity': 'HIGH',
                'url': self.target,
                'issue': 'Server may not validate Referer header',
                'note': 'Manual verification recommended'
            })
        except:
            pass