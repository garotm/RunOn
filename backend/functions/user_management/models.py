from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict, Optional

from google.cloud import firestore


@dataclass
class User:
    """User model representing a RunOn user."""

    id: str
    email: str
    name: str
    provider: str
    created_at: datetime
    updated_at: datetime
    preferences: Dict[str, Any]
    profile_picture: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert user object to dictionary."""
        data = asdict(self)
        # Convert datetime objects to ISO format strings
        data["created_at"] = self.created_at.isoformat()
        data["updated_at"] = self.updated_at.isoformat()
        return data

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "User":
        """Create user object from dictionary."""
        # Convert ISO format strings to datetime objects
        data["created_at"] = datetime.fromisoformat(data["created_at"])
        data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        return User(**data)


def get_firestore_client() -> firestore.Client:
    """Get Firestore client instance."""
    return firestore.Client()


def create_user_profile(user_id: str, email: str, name: str, provider: str) -> User:
    """Create a new user profile.

    Args:
        user_id: Unique user identifier
        email: User's email address
        name: User's display name
        provider: Authentication provider (google/apple)

    Returns:
        User: Created user profile
    """
    now = datetime.utcnow()
    user = User(
        id=user_id,
        email=email,
        name=name,
        provider=provider,
        created_at=now,
        updated_at=now,
        preferences={
            "notifications": True,
            "email_updates": True,
            "distance_unit": "km",
            "theme": "light",
        },
    )

    # Save to Firestore
    db = get_firestore_client()
    db.collection("users").document(user_id).set(user.to_dict())

    return user


def get_user_profile(user_id: str) -> Optional[User]:
    """Get user profile by ID.

    Args:
        user_id: User identifier

    Returns:
        User object if found, None otherwise
    """
    db = get_firestore_client()
    doc = db.collection("users").document(user_id).get()

    if doc.exists:
        return User.from_dict(doc.to_dict())
    return None


def update_user_profile(user_id: str, data: Dict[str, Any]) -> User:
    """Update user profile.

    Args:
        user_id: User identifier
        data: Dictionary of fields to update

    Returns:
        Updated user profile

    Raises:
        ValueError: If user not found
    """
    user = get_user_profile(user_id)
    if not user:
        raise ValueError(f"User {user_id} not found")

    # Update allowed fields
    allowed_fields = {"name", "preferences", "profile_picture"}
    update_data = {k: v for k, v in data.items() if k in allowed_fields}

    if not update_data:
        return user

    # Update the user object
    for key, value in update_data.items():
        setattr(user, key, value)
    user.updated_at = datetime.utcnow()

    # Save to Firestore
    db = get_firestore_client()
    db.collection("users").document(user_id).update({**update_data, "updated_at": user.updated_at})

    return user


def delete_user_profile(user_id: str) -> None:
    """Delete user profile.

    Args:
        user_id: User identifier

    Raises:
        ValueError: If user not found
    """
    db = get_firestore_client()
    doc_ref = db.collection("users").document(user_id)

    if not doc_ref.get().exists:
        raise ValueError(f"User {user_id} not found")

    doc_ref.delete()
