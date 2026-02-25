
from datetime import datetime
from typing import List, Dict, Any, Optional
import hashlib
import secrets
import json


class User:
    def __init__(
        self,
        username: str,
        email: str,
        role: str,
        organization: str = "",
        user_id: Optional[str] = None
    ):
        self.user_id = user_id or self._generate_id()
        self.username = username
        self.email = email
        self.password_hash: Optional[str] = None
        self.role = role  # researcher, developer, admin, viewer
        self.organization = organization
        self.created_at = datetime.now()
        self.last_login: Optional[datetime] = None
        self.is_active = True
        self.preferences: Dict[str, Any] = {
            'theme': 'light',
            'notifications': True,
            'default_models': [],
            'export_format': 'json'
        }
        self.session_token: Optional[str] = None

    def _generate_id(self) -> str:
        """Generate a unique user ID"""
        return f"user_{secrets.token_hex(8)}"

    def set_password(self, password: str) -> None:
        """Set password hash"""
        salt = secrets.token_hex(16)
        self.password_hash = self._hash_password(password, salt)

    def authenticate(self, password: str) -> bool:
        """Authenticate user with password"""
        if not self.password_hash:
            return False
        stored_hash, salt = self.password_hash.split(':')
        computed_hash = self._hash_password(password, salt)
        return secrets.compare_digest(stored_hash, computed_hash)

    def _hash_password(self, password: str, salt: str) -> str:
        """Hash password with salt"""
        hash_obj = hashlib.sha256((password + salt).encode())
        return f"{hash_obj.hexdigest()}:{salt}"

    def create_session(self) -> str:
        """Create a new session token"""
        self.session_token = secrets.token_urlsafe(32)
        self.last_login = datetime.now()
        return self.session_token

    def validate_session(self, token: str) -> bool:
        """Validate session token"""
        return self.session_token == token and self.is_active

    def has_permission(self, action: str) -> bool:
        """Check if user has permission for an action"""
        permissions = {
            'admin': ['*'],
            'researcher': [
                'create_evaluation', 'view_results', 'export',
                'compare_models', 'tune_models', 'create_reports'
            ],
            'developer': [
                'create_evaluation', 'view_results', 'export'
            ],
            'viewer': ['view_results']
        }
        
        if self.role == 'admin':
            return True
        
        user_perms = permissions.get(self.role, [])
        return action in user_perms or '*' in user_perms

    def update_profile(self, info: Dict[str, Any]) -> bool:
        """Update user profile information"""
        try:
            allowed_fields = ['email', 'organization', 'preferences']
            for field, value in info.items():
                if field in allowed_fields:
                    setattr(self, field, value)
            return True
        except Exception:
            return False

    def change_password(self, old_password: str, new_password: str) -> bool:
        """Change user password"""
        if not self.authenticate(old_password):
            return False
        self.set_password(new_password)
        return True

    def update_preferences(self, preferences: Dict[str, Any]) -> None:
        """Update user preferences"""
        self.preferences.update(preferences)

    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary (safe version without sensitive data)"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'organization': self.organization,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active,
            'preferences': self.preferences
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """Create user from dictionary"""
        user = cls(
            username=data['username'],
            email=data['email'],
            role=data['role'],
            organization=data.get('organization', ''),
            user_id=data.get('user_id')
        )
        user.password_hash = data.get('password_hash')
        user.created_at = datetime.fromisoformat(data['created_at']) if 'created_at' in data else datetime.now()
        user.last_login = datetime.fromisoformat(data['last_login']) if data.get('last_login') else None
        user.is_active = data.get('is_active', True)
        user.preferences = data.get('preferences', {})
        return user