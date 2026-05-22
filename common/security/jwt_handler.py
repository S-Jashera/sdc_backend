import jwt
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any
from django.conf import settings
from ninja.security import HttpBearer

class JWTHandler:
    """Utility class to encode and decode JSON Web Tokens using PyJWT."""
    
    @staticmethod
    def create_token(user_id: str, additional_claims: Optional[Dict[str, Any]] = None) -> str:
        """Generates a secure JWT token signed with JWT_SECRET and standard claims."""
        payload = {
            "sub": str(user_id),
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(hours=getattr(settings, "JWT_EXPIRATION_HOURS", 24))
        }
        if additional_claims:
            payload.update(additional_claims)
            
        return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> Optional[Dict[str, Any]]:
        """Safely decodes and validates the signature/expiration of a JWT token."""
        try:
            return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        except jwt.PyJWTError:
            return None


class JWTAuthBearer(HttpBearer):
    """
    Standard HTTP Bearer security handler for Django Ninja.
    Attaches decoded token payload directly to `request.auth` on validation.
    """
    def authenticate(self, request, token: str) -> Optional[Dict[str, Any]]:
        payload = JWTHandler.decode_token(token)
        if payload:
            return payload
        return None
