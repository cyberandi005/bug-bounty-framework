"""
Report generation utility
"""

import json
from pathlib import Path
from datetime import datetime


class ReportGenerator:
    """Generate scan reports"""
    
    def __init__(self):
        Path('output/reports').mkdir(parents=True, exist_ok=True)
    
    def generate_json(self, findings: list, filename: str = None) -> str:
        """Generate JSON report"""
        if not filename:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = f"output/reports/{filename}"
        
        with open(filepath, 'w') as f:
            json.dump(findings, f, indent=2)
        
        return filepath
    
    def generate_html(self, findings: list, filename: str = None) -> str:
        """Generate HTML report"""
        if not filename:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        filepath = f"output/reports/{filename}"
        
        # Count by severity
        critical = len([f for f in findings if f.get('severity') == 'CRITICAL'])
        high = len([f for f in findings if f.get('severity') == 'HIGH'])
        medium = len([f for f in findings if f.get('severity') == 'MEDIUM'])
        low = len([f for f in findings if f.get('severity') == 'LOW'])
        
        html_content = f"""
        <html>
        <head>
            <title>Bug Bounty Report</title>
            <style>
                body {{ font-family: Arial; margin: 20px; }}
                h1 {{ color: #333; }}
                .critical {{ color: red; }}
                .high {{ color: orange; }}
                .medium {{ color: yellow; }}
                .low {{ color: green; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            </style>
        </head>
        <body>
            <h1>Bug Bounty Scan Report</h1>
            <p>Generated: {datetime.now()}</p>
            <h2>Summary</h2>
            <p>Critical: <span class="critical">{critical}</span></p>
            <p>High: <span class="high">{high}</span></p>
            <p>Medium: <span class="medium">{medium}</span></p>
            <p>Low: <span class="low">{low}</span></p>
            <h2>Findings</h2>
            <table>
                <tr><th>Vulnerability</th><th>Severity</th><th>URL</th></tr>
        """
        
        for finding in findings:
            severity_class = finding.get('severity', 'LOW').lower()
            html_content += f"""
                <tr>
                    <td>{finding.get('vulnerability')}</td>
                    <td class="{severity_class}">{finding.get('severity')}</td>
                    <td>{finding.get('url')}</td>
                </tr>
            """
        
        html_content += """
            </table>
        </body>
        </html>
        """
        
        with open(filepath, 'w') as f:
            f.write(html_content)
        
        return filepath