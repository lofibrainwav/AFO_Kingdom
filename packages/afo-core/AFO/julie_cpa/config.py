from pydantic_settings import BaseSettings
from pydantic import Field

class JulieConfig(BaseSettings):
    """
    [The Prince #31: Maintain the State]
    Centralized Configuration for Julie CPA.
    Eliminates Hardcoding (Sun Tzu #1: Laying Plans).
    """
    # Friction Controls (On War)
    MAX_FRICTION_THRESHOLD: float = Field(30.0, description="Max friction before blocking")
    
    # Resilience Controls (Three Kingdoms)
    MAX_RETRIES: int = Field(3, description="Max retry attempts for external APIs")
    RETRY_BACKOFF_FACTOR: float = Field(0.5, description="Exponential backoff multiplier")
    
    # Validation Controls (The Prince)
    MIN_TX_ID_LENGTH: int = Field(10, description="Minimum length for Transaction ID")
    MIN_DESC_LENGTH: int = Field(5, description="Minimum length for Description")

    class Config:
        env_prefix = "JULIE_"

# Singleton Instance
julie_config = JulieConfig()
