"""pytest configuration for nba_service."""

import pytest


@pytest.fixture(autouse=True)
def reset_db_sequences(db):
    """Ensure DB sequences are reset between tests."""
    pass
