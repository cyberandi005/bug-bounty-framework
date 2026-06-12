"""
Database management utility
"""

import sqlite3
from pathlib import Path
from datetime import datetime


class DatabaseManager:
    """SQLite database manager"""
    
    def __init__(self, db_file='db/findings.db'):
        Path('db').mkdir(exist_ok=True)
        self.db_file = db_file
        self.init_db()
    
    def init_db(self):
        """Initialize database schema"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            
            # Findings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS findings (
                    id INTEGER PRIMARY KEY,
                    vulnerability TEXT,
                    severity TEXT,
                    url TEXT,
                    payload TEXT,
                    timestamp DATETIME,
                    session_id TEXT
                )
            ''')
            
            # Sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    target TEXT,
                    scan_type TEXT,
                    start_time DATETIME,
                    end_time DATETIME,
                    total_findings INTEGER
                )
            ''')
            
            conn.commit()
    
    def save_finding(self, finding: dict, session_id: str):
        """Save finding to database"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO findings 
                (vulnerability, severity, url, payload, timestamp, session_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                finding.get('vulnerability'),
                finding.get('severity'),
                finding.get('url'),
                finding.get('payload'),
                datetime.now(),
                session_id
            ))
            conn.commit()