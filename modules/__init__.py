
# modules/__init__.py - FIXED v1.0.1
"""
Modules Package - Core Valuation Engine and Data Fetcher
Mountain Path Valuation Terminal
Prof. V. Ravichandran | Advanced Financial Education

Fixed version with graceful error handling for Streamlit Cloud deployment
"""

import logging
import sys

logger = logging.getLogger(__name__)

# ============================================================================
# IMPORT: Data Fetcher (Required)
# ============================================================================

try:
    from .data_fetcher import SECDataFetcher
    logger.debug("✓ SECDataFetcher imported successfully")
except ImportError as e:
    logger.error(f"Critical: Failed to import SECDataFetcher: {e}")
    raise

# ============================================================================
# IMPORT: Valuation Engine (with fallback)
# ============================================================================

run_multi_valuation = None
calculate_sensitivity = None

try:
    from .valuation_engine import run_multi_valuation, calculate_sensitivity
    logger.debug("✓ run_multi_valuation imported successfully")
    logger.debug("✓ calculate_sensitivity imported successfully")
except ImportError as e:
    logger.warning(f"Could not import from valuation_engine: {e}")
    logger.warning("Attempting alternative import strategy...")
    
    try:
        from . import valuation_engine
        
        if hasattr(valuation_engine, 'run_multi_valuation'):
            run_multi_valuation = valuation_engine.run_multi_valuation
            logger.debug("✓ run_multi_valuation found via module inspection")
        else:
            logger.error("run_multi_valuation not found in valuation_engine module")
        
        if hasattr(valuation_engine, 'calculate_sensitivity'):
            calculate_sensitivity = valuation_engine.calculate_sensitivity
            logger.debug("✓ calculate_sensitivity found via module inspection")
        else:
            logger.error("calculate_sensitivity not found in valuation_engine module")
            
    except ImportError as e2:
        logger.error(f"Failed to import valuation_engine module: {e2}")

# If imports still failed, create error-handling stubs
if run_multi_valuation is None:
    def run_multi_valuation(*args, **kwargs):
        raise RuntimeError(
            "run_multi_valuation is not available. "
            "Check that valuation_engine.py is properly configured."
        )
    logger.warning("Created stub for run_multi_valuation")

if calculate_sensitivity is None:
    def calculate_sensitivity(*args, **kwargs):
        raise RuntimeError(
            "calculate_sensitivity is not available. "
            "Check that valuation_engine.py is properly configured."
        )
    logger.warning("Created stub for calculate_sensitivity")

# ============================================================================
# PACKAGE EXPORTS
# ============================================================================

__all__ = [
    'SECDataFetcher',
    'run_multi_valuation',
    'calculate_sensitivity'
]

__version__ = '1.0.1'
__author__ = 'Prof. V. Ravichandran'
__description__ = 'Mountain Path Valuation Terminal - Core Modules'
