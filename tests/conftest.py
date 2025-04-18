from unittest.mock import AsyncMock, MagicMock

import pytest

from src.services.notifications_service import NotificationService


@pytest.fixture
def mock_repo():
    """Мок-репозиторий"""
    repo = MagicMock()
    repo.create = AsyncMock()
    repo.list = AsyncMock()
    repo.get_by_id = AsyncMock()
    repo.update = AsyncMock()
    return repo


@pytest.fixture
def service(mock_repo):
    """Сервис с подменённым репозиторием."""
    return NotificationService(repo=mock_repo)
