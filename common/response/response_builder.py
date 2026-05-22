from datetime import datetime, timezone
from typing import Any, Optional, Dict

class ResponseBuilder:
    """Helper class to construct standardized, consistent JSON response bodies."""
    
    @staticmethod
    def success(data: Any = None) -> Dict[str, Any]:
        """Wraps standard result data in a successful response envelope."""
        return {
            "success": True,
            "data": data,
            "error": None,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    @staticmethod
    def error(message: str, code: str = "ERROR", details: Optional[Any] = None) -> Dict[str, Any]:
        """Wraps details in an error envelope for standard exception mapping."""
        return {
            "success": False,
            "data": None,
            "error": {
                "message": message,
                "code": code,
                "details": details
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    @staticmethod
    def paginate(items: list, page: int, limit: int, total: int) -> Dict[str, Any]:
        """Utility for creating structured, paginated records with page meta details."""
        return ResponseBuilder.success({
            "items": items,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "pages": (total + limit - 1) // limit if limit > 0 else 0
            }
        })
