"""Database query optimizations."""

from typing import Any, Dict, List, Optional

from google.cloud import firestore


def batch_get(
    collection: str, ids: List[str], fields: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """Optimized batch document retrieval."""
    db = firestore.Client()
    refs = [db.collection(collection).document(id_) for id_ in ids]

    # Use select() for field filtering if specified
    if fields:
        docs = [ref.get(field_paths=fields) for ref in refs]
    else:
        docs = [ref.get() for ref in refs]

    return [doc.to_dict() for doc in docs if doc.exists]


def paginated_query(
    collection: str,
    filters: Optional[List[tuple]] = None,
    order_by: Optional[str] = None,
    page_size: int = 10,
    cursor: Optional[str] = None,
) -> tuple[List[Dict[str, Any]], Optional[str]]:
    """Optimized paginated query."""
    db = firestore.Client()
    query = db.collection(collection)

    # Apply filters
    if filters:
        for field, op, value in filters:
            query = query.where(field, op, value)

    # Apply ordering
    if order_by:
        query = query.order_by(order_by)

    # Apply pagination
    if cursor:
        query = query.start_after({"id": cursor})

    # Execute query
    docs = query.limit(page_size + 1).stream()

    # Process results
    results = []
    next_cursor = None

    for i, doc in enumerate(docs):
        if i < page_size:
            results.append(doc.to_dict())
        else:
            next_cursor = doc.id
            break

    return results, next_cursor


def bulk_write(collection: str, operations: List[Dict[str, Any]], batch_size: int = 500) -> None:
    """Optimized bulk write operations."""
    db = firestore.Client()

    # Process in batches
    for i in range(0, len(operations), batch_size):
        batch = db.batch()
        batch_ops = operations[i : i + batch_size]

        for op in batch_ops:
            doc_ref = db.collection(collection).document(op.get("id"))
            if op.get("delete"):
                batch.delete(doc_ref)
            else:
                batch.set(doc_ref, op.get("data", {}), merge=True)

        batch.commit()
