# Trinity Score: 90.0 (Established by Chancellor)
from __future__ import annotations

import logging


class BaseService:
    """Small shared base for API services (logging, future shared deps)."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
