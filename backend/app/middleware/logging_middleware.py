import time
import uuid
import logging
import json
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("app.request")

class StructuredLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.time()
        
        # Attach request_id to state
        request.state.request_id = request_id

        try:
            response = await call_next(request)
            duration = time.time() - start_time
            
            # Create a structured log dictionary
            log_data = {
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round(duration * 1000, 2),
            }
            
            # In a real app we'd fetch the user ID from request.state if authenticated
            if hasattr(request.state, "user_id"):
                log_data["user_id"] = request.state.user_id

            logger.info(json.dumps(log_data))
            return response
            
        except Exception as exc:
            duration = time.time() - start_time
            log_data = {
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "duration_ms": round(duration * 1000, 2),
                "error": str(exc)
            }
            logger.error(json.dumps(log_data))
            raise
