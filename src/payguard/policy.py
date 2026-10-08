"""Versioned demo measurement definitions; not PayPal risk thresholds."""

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation


POLICY_VERSION = "payguard.demo.v1"


@dataclass(frozen=True)
class VelocityPolicy:
    threshold: str = "3.5"
    window_hours: int = 1
    version: str = POLICY_VERSION

    def __post_init__(self):
        if not isinstance(self.threshold, str):
            raise ValueError("invalid_threshold")
        try:
            value = Decimal(self.threshold)
        except InvalidOperation as exc:
            raise ValueError("invalid_threshold") from exc
        if not value.is_finite() or value <= 0:
            raise ValueError("invalid_threshold")
        if type(self.window_hours) is not int or not 1 <= self.window_hours <= 24:
            raise ValueError("invalid_window")
        if self.version != POLICY_VERSION:
            raise ValueError("unknown_policy_version")
