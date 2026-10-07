"""Tests for privacy-safe runtime diagnostic helpers."""

import asyncio

from mcp_atlassian.privacy import (
    begin_identity_privacy_runtime,
    is_identity_privacy_runtime_active,
    privacy_safe_exception_detail,
    privacy_safe_value,
    reset_identity_privacy_runtime,
)


def test_runtime_scope_redacts_values_and_exception_details() -> None:
    assert is_identity_privacy_runtime_active() is False


def test_runtime_scope_is_isolated_between_concurrent_tasks() -> None:
    async def protected_worker(started: asyncio.Event) -> bool:
        token = begin_identity_privacy_runtime()
        try:
            started.set()
            await asyncio.sleep(0)
            return is_identity_privacy_runtime_active()
        finally:
            reset_identity_privacy_runtime(token)

    async def unprotected_worker(started: asyncio.Event) -> bool:
        await started.wait()
        return is_identity_privacy_runtime_active()

    async def run() -> tuple[bool, bool]:
        started = asyncio.Event()
        protected, unprotected = await asyncio.gather(
            protected_worker(started),
            unprotected_worker(started),
        )
        return protected, unprotected

    assert asyncio.run(run()) == (True, False)
    assert is_identity_privacy_runtime_active() is False
    assert privacy_safe_value("CANARY") == "CANARY"
    assert privacy_safe_exception_detail(ValueError("CANARY")) == "CANARY"

    token = begin_identity_privacy_runtime()
    try:
        assert is_identity_privacy_runtime_active() is True
        assert privacy_safe_value("CANARY") == "<redacted>"
        assert privacy_safe_exception_detail(ValueError("CANARY")) == "ValueError"
    finally:
        reset_identity_privacy_runtime(token)

    assert is_identity_privacy_runtime_active() is False
