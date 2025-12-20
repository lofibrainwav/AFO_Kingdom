"""
AICPA Module - 에이전트 군단
"""

from .tax_engine import (
    TaxInput,
    TaxResult,
    FilingStatus,
    calculate_tax,
    simulate_roth_ladder,
    calculate_federal_tax,
    calculate_ca_state_tax,
    check_irmaa_risk,
)

from .report_generator import (
    generate_strategy_report,
    generate_turbotax_csv,
    generate_quickbooks_csv,
    generate_email_draft,
)

from .service import (
    AICPAService,
    get_aicpa_service,
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
