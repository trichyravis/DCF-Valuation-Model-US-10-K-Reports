#!/usr/bin/env python3
"""
DCF VALUATION MODEL - IMPORT VERIFICATION SCRIPT
Prof. V. Ravichandran | The Mountain Path - World of Finance

Run this script to diagnose import issues before deploying to Streamlit Cloud.

Usage:
    python test_imports.py
"""

import sys
import os
from pathlib import Path

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'

def print_header(text):
    """Print colored section header"""
    print(f"\n{BLUE}{BOLD}{'=' * 70}{RESET}")
    print(f"{BLUE}{BOLD}{text:^70}{RESET}")
    print(f"{BLUE}{BOLD}{'=' * 70}{RESET}\n")

def print_check(name, status, message=""):
    """Print a check result"""
    symbol = f"{GREEN}✓{RESET}" if status else f"{RED}✗{RESET}"
    msg = f" - {message}" if message else ""
    print(f"  {symbol} {name:<40}{msg}")

def print_step(num, text):
    """Print a step header"""
    print(f"\n{BOLD}[{num}]{RESET} {text}")

def main():
    """Run all verification checks"""
    
    print_header("DCF VALUATION MODEL - IMPORT VERIFICATION")
    
    # Track overall status
    all_passed = True
    
    # =========================================================================
    # STEP 1: Environment Check
    # =========================================================================
    print_step(1, "ENVIRONMENT SETUP")
    
    # Check Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print_check("Python Version", sys.version_info >= (3, 7), python_version)
    
    # Check working directory
    cwd = Path.cwd()
    print_check("Working Directory", cwd.exists(), str(cwd))
    
    # Check if modules folder exists
    modules_path = cwd / "modules"
    modules_exist = modules_path.exists()
    print_check("modules/ folder exists", modules_exist, str(modules_path))
    
    if not modules_exist:
        print(f"\n{RED}ERROR: modules/ folder not found!{RESET}")
        print(f"Expected location: {modules_path}")
        print(f"Please ensure you're in the correct directory.")
        all_passed = False
        return all_passed
    
    # List files in modules
    print(f"\n  Files in modules/:")
    for file in sorted(modules_path.glob("*.py")):
        print(f"    - {file.name}")
    
    # =========================================================================
    # STEP 2: File Syntax Check
    # =========================================================================
    print_step(2, "PYTHON SYNTAX VERIFICATION")
    
    files_to_check = [
        modules_path / "__init__.py",
        modules_path / "data_fetcher.py",
        modules_path / "valuation_engine.py"
    ]
    
    for file_path in files_to_check:
        if not file_path.exists():
            print_check(f"{file_path.name}", False, "FILE NOT FOUND")
            all_passed = False
            continue
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                compile(f.read(), str(file_path), 'exec')
            print_check(f"{file_path.name}", True, "Valid Python syntax")
        except SyntaxError as e:
            print_check(f"{file_path.name}", False, f"SyntaxError: {e}")
            all_passed = False
        except Exception as e:
            print_check(f"{file_path.name}", False, f"Error: {e}")
            all_passed = False
    
    # =========================================================================
    # STEP 3: Direct Module Import
    # =========================================================================
    print_step(3, "DIRECT PYTHON IMPORTS")
    
    # Add modules to path
    sys.path.insert(0, str(modules_path.parent))
    
    # Test data_fetcher import
    try:
        from modules.data_fetcher import SECDataFetcher
        print_check("modules.data_fetcher.SECDataFetcher", True)
    except ImportError as e:
        print_check("modules.data_fetcher.SECDataFetcher", False, str(e))
        all_passed = False
    except Exception as e:
        print_check("modules.data_fetcher.SECDataFetcher", False, f"Unexpected error: {e}")
        all_passed = False
    
    # Test valuation_engine imports
    try:
        from modules.valuation_engine import run_multi_valuation
        print_check("modules.valuation_engine.run_multi_valuation", True)
    except ImportError as e:
        print_check("modules.valuation_engine.run_multi_valuation", False, str(e))
        all_passed = False
    except Exception as e:
        print_check("modules.valuation_engine.run_multi_valuation", False, f"Unexpected error: {e}")
        all_passed = False
    
    try:
        from modules.valuation_engine import calculate_sensitivity
        print_check("modules.valuation_engine.calculate_sensitivity", True)
    except ImportError as e:
        print_check("modules.valuation_engine.calculate_sensitivity", False, str(e))
        all_passed = False
    except Exception as e:
        print_check("modules.valuation_engine.calculate_sensitivity", False, f"Unexpected error: {e}")
        all_passed = False
    
    # =========================================================================
    # STEP 4: __init__.py Import Chain
    # =========================================================================
    print_step(4, "MODULES __init__.py IMPORT CHAIN")
    
    try:
        from modules import SECDataFetcher
        print_check("from modules import SECDataFetcher", True)
    except ImportError as e:
        print_check("from modules import SECDataFetcher", False, str(e))
        all_passed = False
    except Exception as e:
        print_check("from modules import SECDataFetcher", False, f"Unexpected error: {e}")
        all_passed = False
    
    try:
        from modules import run_multi_valuation
        print_check("from modules import run_multi_valuation", True)
    except ImportError as e:
        print_check("from modules import run_multi_valuation", False, str(e))
        all_passed = False
    except Exception as e:
        print_check("from modules import run_multi_valuation", False, f"Unexpected error: {e}")
        all_passed = False
    
    try:
        from modules import calculate_sensitivity
        print_check("from modules import calculate_sensitivity", True)
    except ImportError as e:
        print_check("from modules import calculate_sensitivity", False, str(e))
        all_passed = False
    except Exception as e:
        print_check("from modules import calculate_sensitivity", False, f"Unexpected error: {e}")
        all_passed = False
    
    # =========================================================================
    # STEP 5: Required Dependencies
    # =========================================================================
    print_step(5, "PYTHON DEPENDENCIES")
    
    required_packages = [
        'streamlit',
        'pandas',
        'numpy',
        'requests',
        'yfinance',
        'plotly'
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            version = __import__(package).__version__ if hasattr(__import__(package), '__version__') else "installed"
            print_check(package, True, version)
        except ImportError:
            print_check(package, False, "NOT INSTALLED")
            all_passed = False
    
    # =========================================================================
    # FINAL RESULT
    # =========================================================================
    print_header("VERIFICATION COMPLETE")
    
    if all_passed:
        print(f"{GREEN}{BOLD}✓ ALL CHECKS PASSED{RESET}")
        print(f"\n{GREEN}Your application is ready to run!{RESET}")
        print(f"\nRun the app with:")
        print(f"  {BOLD}streamlit run app.py{RESET}\n")
        return 0
    else:
        print(f"{RED}{BOLD}✗ SOME CHECKS FAILED{RESET}")
        print(f"\n{YELLOW}Recommended Actions:{RESET}")
        print(f"  1. Review the failed checks above")
        print(f"  2. Fix the issues or restore files from GitHub")
        print(f"  3. Run this script again to verify")
        print(f"  4. If still failing, see DEPLOYMENT_FIX_GUIDE.md\n")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Interrupted by user{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}Unexpected error: {e}{RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
