from starlette.middleware.base import BaseHTTPMiddleware


class SecurityHeadersMiddleware(
    BaseHTTPMiddleware
):

    async def dispatch(
        self,
        request,
        call_next
    ):

        response = await call_next(
            request
        )

        # Clickjacking Protection
        response.headers[
            "X-Frame-Options"
        ] = "DENY"

        # MIME Sniffing Protection
        response.headers[
            "X-Content-Type-Options"
        ] = "nosniff"

        # XSS Protection
        response.headers[
            "X-XSS-Protection"
        ] = "1; mode=block"

        # HTTPS Enforcement
        response.headers[
            "Strict-Transport-Security"
        ] = (
            "max-age=31536000; "
            "includeSubDomains"
        )

        # Referrer Policy
        response.headers[
            "Referrer-Policy"
        ] = "strict-origin-when-cross-origin"

        # Content Security Policy
        response.headers[
            "Content-Security-Policy"
        ] = (
            "default-src 'self'; "
            "