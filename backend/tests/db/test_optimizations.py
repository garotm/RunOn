"""Tests for database optimizations."""

from unittest.mock import MagicMock, patch

from db.optimizations import batch_get, bulk_write, paginated_query


@patch("db.optimizations.firestore.Client")
def test_batch_get(mock_client):
    """Test batch document retrieval."""
    # Setup mock documents
    mock_docs = [
        MagicMock(exists=True, to_dict=lambda: {"id": "1", "data": "test1"}),
        MagicMock(exists=True, to_dict=lambda: {"id": "2", "data": "test2"}),
        MagicMock(exists=False),
    ]

    # Create a collection reference mock
    mock_collection = MagicMock()
    mock_client.return_value.collection.return_value = mock_collection

    # Setup document references
    mock_collection.document.side_effect = [
        MagicMock(get=MagicMock(return_value=doc)) for doc in mock_docs
    ]

    # Test basic retrieval
    results = batch_get("test_collection", ["1", "2", "3"])
    assert len(results) == 2
    assert results[0]["data"] == "test1"
    assert results[1]["data"] == "test2"


@patch("db.optimizations.firestore.Client")
def test_paginated_query(mock_client):
    """Test paginated query."""
    # Setup mock documents
    mock_docs = [
        MagicMock(id="1", to_dict=lambda: {"id": "1"}),
        MagicMock(id="2", to_dict=lambda: {"id": "2"}),
    ]

    # Create query chain mocks
    mock_collection = MagicMock()
    mock_where = MagicMock()
    mock_order = MagicMock()
    mock_limit = MagicMock()

    mock_client.return_value.collection.return_value = mock_collection
    mock_collection.where.return_value = mock_where
    mock_where.order_by.return_value = mock_order
    mock_order.limit.return_value = mock_limit
    mock_limit.stream.return_value = mock_docs  # Return only first 2 docs

    # Test basic query
    results, cursor = paginated_query(
        "test_collection", filters=[("field", "==", "value")], order_by="created_at", page_size=2
    )

    assert len(results) == 2
    assert results[0]["id"] == "1"
    assert results[1]["id"] == "2"
    assert cursor is None  # No more results, so cursor should be None


@patch("db.optimizations.firestore.Client")
def test_bulk_write(mock_client):
    """Test bulk write operations."""
    # Setup mock batch
    mock_batch = MagicMock()
    mock_client.return_value.batch.return_value = mock_batch

    # Setup mock collection
    mock_collection = MagicMock()
    mock_client.return_value.collection.return_value = mock_collection

    operations = [
        {"id": "1", "data": {"field": "value1"}},
        {"id": "2", "delete": True},
        {"id": "3", "data": {"field": "value3"}},
    ]

    # Test batch processing
    bulk_write("test_collection", operations, batch_size=2)

    # Verify batch operations
    assert mock_batch.set.call_count == 2
    assert mock_batch.delete.call_count == 1
    assert mock_batch.commit.call_count == 2
