import uuid
from unittest.mock import patch

import pytest

from src.models.notification import Notification
from src.schemas.filters import NotificationFilter
from src.tasks.task_analyze import analyze_notification


@pytest.mark.asyncio
async def test_create_notification(service, mock_repo):
    dummy_id = uuid.uuid4()
    user_id = uuid.uuid4()
    text = "Test notification"
    title = "Test"
    created_note = Notification(user_id=user_id, title=title, text=text)
    created_note.id = dummy_id
    mock_repo.create.return_value = created_note

    with patch.object(
        analyze_notification, "delay", autospec=True
    ) as mock_delay:
        result = await service.create_notification(user_id, title, text)

        mock_repo.create.assert_awaited_once()
        mock_delay.assert_called_once_with(dummy_id, text)
        assert result is created_note


@pytest.mark.asyncio
async def test_list_notifications(service, mock_repo):
    filters = NotificationFilter(user_id=uuid.uuid4(), limit=5, offset=2)
    notifications = [
        Notification(user_id=filters.user_id, title="A", text="t1"),
        Notification(user_id=filters.user_id, title="B", text="t2"),
    ]
    mock_repo.list.return_value = notifications

    result = await service.list_notifications(filters)

    mock_repo.list.assert_awaited_once_with(filters)
    assert result == notifications


@pytest.mark.asyncio
async def test_get_notification(service, mock_repo):
    nid = uuid.uuid4()
    notification = Notification(user_id=uuid.uuid4(), title="X", text="t")
    mock_repo.get_by_id.return_value = notification

    result = await service.get_notification(nid)
    mock_repo.get_by_id.assert_awaited_once_with(nid)
    assert result == notification

    mock_repo.get_by_id.return_value = None
    result_none = await service.get_notification(nid)
    assert result_none is None


@pytest.mark.asyncio
async def test_mark_as_read(service, mock_repo):
    nid = uuid.uuid4()
    updated_notification = Notification(
        user_id=uuid.uuid4(), title="C", text="t"
    )
    mock_repo.update.return_value = updated_notification

    result = await service.mark_as_read(nid)
    mock_repo.update.assert_awaited_once()
    assert result == updated_notification

    mock_repo.update.return_value = None
    result_none = await service.mark_as_read(nid)
    assert result_none is None


@pytest.mark.asyncio
async def test_check_notification_status(service, mock_repo):
    nid = uuid.uuid4()
    notification = Notification(user_id=uuid.uuid4(), title="Z", text="t")
    notification.processing_status = "completed"
    notification.category = "info"
    notification.confidence = 0.95
    mock_repo.get_by_id.return_value = notification

    status = await service.check_notification_status(nid)
    mock_repo.get_by_id.assert_awaited_once_with(nid)
    assert status == {
        "processing_status": "completed",
        "category": "info",
        "confidence": 0.95,
    }

    mock_repo.get_by_id.return_value = None
    status_none = await service.check_notification_status(nid)
    assert status_none is None
