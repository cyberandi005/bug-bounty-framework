"""
Configuration management utility
"""

import json
from pathlib import Path


class ConfigManager:
    """Configuration file manager"""
    
    def __init__(self, config_file='config/settings.json'):
        Path('config').mkdir(exist_ok=True)
        self.config_file = config_file
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        if Path(self.config_file).exists():
            with open(self.config_file) as f:
                self.config = json.load(f)
        else:
            self.config = self.get_default_config()
            self.save_config()
    
    def get_default_config(self) -> dict:
        """Get default configuration"""
        return {
            'scanning': {
                'threads': 10,
                'timeout': 30,
                'retry_count': 3
            },
            'payloads': {
                'sqli_payload_count': 50,
                'xss_payload_count': 100
            },
            'output': {
                'formats': ['json', 'html'],
                'detailed_report': True
            }
        }
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        return self.config.get(key, default)