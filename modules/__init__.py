
# modules/__init__.py
"""
Modules Package - Core Valuation Engine and Data Fetcher
Mountain Path Valuation Terminal
"""

from .data_fetcher import SECDataFetcher
from .valuation_engine import run_multi_valuation, calculate_sensitivity

__all__ = [
    'SECDataFetcher',
    'run_multi_valuation',
    'calculate_sensitivity'
]

__version__ = '1.0.0'
__author__ = 'Prof. V. Ravichandran'
