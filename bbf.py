#!/usr/bin/env python3
"""
Bug Bounty Framework - Main Entry Point
Comprehensive automated security testing and vulnerability detection
"""

import argparse
import sys
import json
import os
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress

# Import modules
sys.path.insert(0, str(Path(__file__).parent))

try:
    from modules import (
        SQLiDetector,
        XSSScanner,
        CSRFChecker,
        DirectoryEnumerator,
        APITester,
        AuthBypassTester,
        OSINTModule
    )
    from utils import (
        Logger,
        DatabaseManager,
        ReportGenerator,
        ConfigManager
    )
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please ensure all modules are properly installed.")
    sys.exit(1)

console = Console()
logger = Logger()
db = DatabaseManager()


class BugBountyFramework:
    """Main framework class"""
    
    def __init__(self):
        self.version = "1.0.0"
        self.session_id = self.generate_session_id()
        self.findings = []
        self.config = ConfigManager()
        
    def generate_session_id(self):
        """Generate unique session ID"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def display_banner(self):
        """Display framework banner"""
        banner = """
╔═══════════════════════════════════════════════════════════════════════╗
║         🔐 BUG BOUNTY FRAMEWORK v1.0.0 🔐            ║
║     Automated Security Testing & Vulnerability      ║
║              Detection Framework                    ║
║                                                     ║
║              Made by: @cyberandi005                 ║
╚═══════════════════════════════════════════════════════════════════════╝
        """
        console.print(banner, style="bold cyan")
    
    def show_modules_info(self):
        """Display available modules"""
        table = Table(title="Available Scanning Modules", style="cyan")
        table.add_column("Module", style="magenta")
        table.add_column("Description", style="green")
        table.add_column("Status", style="yellow")
        
        modules_info = [
            ("SQL Injection", "Detect SQL injection vulnerabilities", "✓"),
            ("XSS Scanner", "Cross-site scripting detection", "✓"),
            ("CSRF Checker", "CSRF token validation & bypass", "✓"),
            ("Directory Enum", "Directory fuzzing & enumeration", "✓"),
            ("API Testing", "API endpoint vulnerability testing", "✓"),
            ("Auth Bypass", "Authentication bypass detection", "✓"),
            ("OSINT", "Information gathering & reconnaissance", "✓")
        ]
        
        for module, desc, status in modules_info:
            table.add_row(module, desc, status)
        
        console.print(table)
    
    def run_full_scan(self, target, options):
        """Execute full automated scan"""
        console.print(f"\n[cyan]Starting full scan on: {target}[/cyan]")
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Scanning...", total=7)
            
            # SQL Injection
            console.print("[yellow]→[/yellow] Running SQL Injection tests...")
            sqli = SQLiDetector(target)
            sqli_results = sqli.detect()
            self.findings.extend(sqli_results)
            progress.update(task, advance=1)
            
            # XSS
            console.print("[yellow]→[/yellow] Running XSS tests...")
            xss = XSSScanner(target)
            xss_results = xss.scan()
            self.findings.extend(xss_results)
            progress.update(task, advance=1)
            
            # CSRF
            console.print("[yellow]→[/yellow] Running CSRF tests...")
            csrf = CSRFChecker(target)
            csrf_results = csrf.check()
            self.findings.extend(csrf_results)
            progress.update(task, advance=1)
            
            # Directory Enumeration
            console.print("[yellow]→[/yellow] Running directory enumeration...")
            dir_enum = DirectoryEnumerator(target, options.get('threads', 10))
            dir_results = dir_enum.enumerate()
            self.findings.extend(dir_results)
            progress.update(task, advance=1)
            
            # API Testing
            console.print("[yellow]→[/yellow] Running API tests...")
            api = APITester(target)
            api_results = api.test()
            self.findings.extend(api_results)
            progress.update(task, advance=1)
            
            # Authentication
            console.print("[yellow]→[/yellow] Running authentication bypass tests...")
            auth = AuthBypassTester(target)
            auth_results = auth.test()
            self.findings.extend(auth_results)
            progress.update(task, advance=1)
            
            # OSINT
            console.print("[yellow]→[/yellow] Running OSINT gathering...")
            osint = OSINTModule()
            osint_target = options.get('domain') or target.split('/')[2]
            osint_results = osint.gather(osint_target)
            self.findings.extend(osint_results)
            progress.update(task, advance=1)
        
        return self.findings
    
    def save_findings(self, output_format='json'):
        """Save findings to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if output_format == 'json':
            filename = f"output/reports/findings_{timestamp}.json"
            with open(filename, 'w') as f:
                json.dump(self.findings, f, indent=2)
        
        console.print(f"\n[green]✓ Report saved: {filename}[/green]")
        return filename
    
    def display_summary(self):
        """Display findings summary"""
        summary_table = Table(title="Vulnerability Summary", style="cyan")
        summary_table.add_column("Severity", style="magenta")
        summary_table.add_column("Count", style="yellow")
        
        critical = len([f for f in self.findings if f.get('severity') == 'CRITICAL'])
        high = len([f for f in self.findings if f.get('severity') == 'HIGH'])
        medium = len([f for f in self.findings if f.get('severity') == 'MEDIUM'])
        low = len([f for f in self.findings if f.get('severity') == 'LOW'])
        
        summary_table.add_row("🔴 CRITICAL", str(critical))
        summary_table.add_row("🟠 HIGH", str(high))
        summary_table.add_row("🟡 MEDIUM", str(medium))
        summary_table.add_row("🟢 LOW", str(low))
        summary_table.add_row("─" * 20, "─" * 10)
        summary_table.add_row("[bold]TOTAL[/bold]", f"[bold]{len(self.findings)}[/bold]")
        
        console.print(summary_table)


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Bug Bounty Framework - Automated Security Testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full scan
  python bbf.py -u https://target.com --scan all
  
  # SQL Injection test
  python bbf.py -u https://target.com --sqli
  
  # OSINT gathering
  python bbf.py -d target.com --osint
  
  # API testing
  python bbf.py -u https://api.target.com/v1/ --api-test
        """
    )
    
    # Target options
    parser.add_argument('-u', '--url', help='Target URL')
    parser.add_argument('-d', '--domain', help='Target domain for OSINT')
    parser.add_argument('-f', '--file', help='File with multiple targets')
    
    # Scanning options
    parser.add_argument('--scan', choices=['all', 'sqli', 'xss', 'csrf', 'api', 'auth', 'osint', 'dir'],
                       help='Type of scan to perform')
    parser.add_argument('--sqli', action='store_true', help='SQL Injection test')
    parser.add_argument('--xss', action='store_true', help='XSS test')
    parser.add_argument('--csrf', action='store_true', help='CSRF test')
    parser.add_argument('--dir-enum', action='store_true', help='Directory enumeration')
    parser.add_argument('--api-test', action='store_true', help='API testing')
    parser.add_argument('--auth-bypass', action='store_true', help='Authentication bypass test')
    parser.add_argument('--osint', action='store_true', help='OSINT information gathering')
    
    # Options
    parser.add_argument('--threads', type=int, default=10, help='Number of threads (default: 10)')
    parser.add_argument('--timeout', type=int, default=30, help='Request timeout in seconds')
    parser.add_argument('--wordlist', help='Custom wordlist for directory enumeration')
    parser.add_argument('--output', help='Output filename')
    parser.add_argument('--format', choices=['json', 'html', 'csv'], default='json', help='Output format')
    
    # Info options
    parser.add_argument('--list-modules', action='store_true', help='List available modules')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    
    args = parser.parse_args()
    
    # Initialize framework
    framework = BugBountyFramework()
    framework.display_banner()
    
    # Show modules info if requested
    if args.list_modules:
        framework.show_modules_info()
        return
    
    # Validate target
    if not args.url and not args.domain and not args.file:
        console.print("[red]Error: Please provide target URL (-u), domain (-d), or file (-f)[/red]")
        parser.print_help()
        sys.exit(1)
    
    # Prepare options
    options = {
        'threads': args.threads,
        'timeout': args.timeout,
        'wordlist': args.wordlist,
        'domain': args.domain
    }
    
    try:
        # Run scans
        if args.scan == 'all':
            findings = framework.run_full_scan(args.url or args.domain, options)
        elif args.sqli:
            sqli = SQLiDetector(args.url)
            findings = sqli.detect()
        elif args.xss:
            xss = XSSScanner(args.url)
            findings = xss.scan()
        elif args.csrf:
            csrf = CSRFChecker(args.url)
            findings = csrf.check()
        elif args.dir_enum:
            dir_enum = DirectoryEnumerator(args.url, args.threads)
            findings = dir_enum.enumerate()
        elif args.api_test:
            api = APITester(args.url)
            findings = api.test()
        elif args.auth_bypass:
            auth = AuthBypassTester(args.url)
            findings = auth.test()
        elif args.osint:
            osint = OSINTModule()
            findings = osint.gather(args.domain)
        else:
            console.print("[red]Please specify a scan type[/red]")
            sys.exit(1)
        
        # Display results
        framework.findings = findings
        framework.display_summary()
        
        # Save report
        output_file = framework.save_findings(args.format)
        console.print(f"\n[green]✓ Scan completed successfully![/green]")
        console.print(f"[cyan]Session ID: {framework.session_id}[/cyan]")
        
    except KeyboardInterrupt:
        console.print("\n[red]Scan interrupted by user[/red]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        logger.error(f"Scan failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()