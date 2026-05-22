import logging
from ninja import NinjaAPI
from ninja.errors import ValidationError
from django.http import JsonResponse
from django.conf import settings
from common.exception.base_exception import APIException
from common.response.response_builder import ResponseBuilder

logger = logging.getLogger(__name__)

def register_exception_handlers(api: NinjaAPI):
    """
    Registers custom exception handlers globally for a Django Ninja API instance.
    This guarantees that all exceptions are wrapped in a standard JSON envelope.
    """
    
    @api.exception_handler(APIException)
    def api_exception_handler(request, exc: APIException):
        """Catches custom system exceptions (e.g. NotFoundException, BadRequestException)."""
        response_body = ResponseBuilder.error(
            message=exc.message,
            code=exc.error_code,
            details=exc.details
        )
        return JsonResponse(response_body, status=exc.status_code)

    @api.exception_handler(ValidationError)
    def validation_error_handler(request, exc: ValidationError):
        """Catches Pydantic schema validation errors and presents a simplified field-to-message mapping."""
        field_errors = {}
        for error in exc.errors:
            # Format the location path (e.g., body.name -> name)
            loc_list = [str(x) for x in error.get("loc", [])]
            # Exclude standard prefix words like 'body' or 'query' if present for cleaner frontend display
            if loc_list and loc_list[0] in ("body", "query", "path"):
                loc_list = loc_list[1:]
            
            field = ".".join(loc_list) if loc_list else "global"
            field_errors[field] = error.get("msg", "Invalid value")
        
        response_body = ResponseBuilder.error(
            message="Input data validation failed",
            code="VALIDATION_ERROR",
            details={"fields": field_errors}
        )
        return JsonResponse(response_body, status=422)

    @api.exception_handler(Exception)
    def general_exception_handler(request, exc: Exception):
        """Catches uncaught system exceptions, shielding internal structures from clients."""
        logger.error(f"Unhandled Exception in request: {str(exc)}", exc_info=True)
        
        details = {}
        if settings.DEBUG:
            details["system_message"] = str(exc)
            details["error_class"] = exc.__class__.__name__
            
        response_body = ResponseBuilder.error(
            message="An unexpected server error occurred",
            code="INTERNAL_SERVER_ERROR",
            details=details if details else None
        )
        return JsonResponse(response_body, status=500)
