from starlette.responses import HTMLResponse


async def not_found(request, exc):
    return HTMLResponse(content="Page Not Found!", status_code=exc.status_code)

exception_handlers = {
    404: not_found,
}
