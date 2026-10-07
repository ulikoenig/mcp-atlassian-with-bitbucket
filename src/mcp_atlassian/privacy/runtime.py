"""Request-local helpers for privacy-safe runtime diagnostics."""

from __future__ import annotations

from contextvars import ContextVar, Token

_privacy_runtime_active: ContextVar[bool] = ContextVar(
    "mcp_atlassian_identity_privacy_active",
    default=False,
)


def begin_identity_privacy_runtime() -> Token[bool]:
    """Mark the current tool invocation as privacy protected."""
    return _privacy_runtime_active.set(True)


def reset_identity_privacy_runtime(token: Token[bool]) -> None:
    """Restore the preceding privacy runtime state."""
    _privacy_runtime_active.reset(token)


def is_identity_privacy_runtime_active() -> bool:
    """Return whether the current execution is inside an enabled privacy guard."""
    return _privacy_runtime_active.get()


def privacy_safe_value(value: object) -> str:
    """Return a redacted diagnostic value while privacy mode is active."""
    return "<redacted>" if is_identity_privacy_runtime_active() else str(value)


def privacy_safe_exception_detail(error: BaseException) -> str:
    """Return only the exception type while privacy mode is active."""
    if is_identity_privacy_runtime_active():
        return type(error).__name__
    return str(error).strip() or type(error).__name__
