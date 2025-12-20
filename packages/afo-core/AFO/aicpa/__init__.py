"""
AICPA Module - 에이전트 군단
"""

from .report_generator import (
    generate_email_draft,
    generate_quickbooks_csv,
    generate_strategy_report,
    generate_turbotax_csv,
)
from .service import (
    AICPAService,
    get_aicpa_service,
)
from .tax_engine import (
    FilingStatus,
    TaxInput,
    TaxResult,
    calculate_ca_state_tax,
    calculate_federal_tax,
    calculate_tax,
    check_irmaa_risk,
    simulate_roth_ladder,
)

__all__ = [
    # Tax Engine
    "TaxInput",
    "TaxResult",
    "FilingStatus",
    "calculate_tax",
    "simulate_roth_ladder",
    "calculate_federal_tax",
    "calculate_ca_state_tax",
    "check_irmaa_risk",
    # Report Generator
    "generate_strategy_report",
    "generate_turbotax_csv",
    "generate_quickbooks_csv",
    "generate_email_draft",
    # Service
    "AICPAService",
    "get_aicpa_service",
]
