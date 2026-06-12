"""
Directory Enumeration Module
"""

import requests
import threading
from typing import List, Dict
from queue import Queue
from urllib.parse import urljoin


class DirectoryEnumerator:
    """Directory and path enumeration"""
    
    def __init__(self, target: str, threads: int = 10):
        self.target = target
        self.threads = threads
        self.findings = []
        self.queue = Queue()
        
        # Common directories
        self.common_dirs = [
            'admin', 'api', 'config', 'test', 'backup',
            '.git', '.env', 'uploads', 'includes', 'assets',
            'wp-admin', 'phpmyadmin', 'cgi-bin', 'console',
            '.htaccess', 'web.config', 'robots.txt',
        ]
    
    def enumerate(self) -> List[Dict]:
        """Enumerate directories"""
        # Queue all directories
        for directory in self.common_dirs:
            self.queue.put(directory)
        
        # Start worker threads
        workers = []
        for _ in range(min(self.threads, len(self.common_dirs))):
            t = threading.Thread(target=self._worker)
            t.daemon = True
            workers.append(t)
            t.start()
        
        # Wait for completion
        for worker in workers:
            worker.join()
        
        return self.findings
    
    def _worker(self):
        """Worker thread function"""
        while not self.queue.empty():
            try:
                directory = self.queue.get_nowait()
                self._check_path(directory)
                self.queue.task_done()
            except:
                break
    
    def _check_path(self, path: str):
        """Check if directory exists"""
        try:
            url = urljoin(self.target, path)
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                self.findings.append({
                    'vulnerability': 'Directory Found',
                    'severity': 'LOW',
                    'url': url,
                    'status_code': response.status_code,
                    'content_length': len(response.text)
                })
            elif response.status_code in [301, 302, 403]:
                # Interesting responses
                self.findings.append({
                    'vulnerability': 'Interesting Response',
                    'severity': 'LOW',
                    'url': url,
                    'status_code': response.status_code
                })
        except:
            pass