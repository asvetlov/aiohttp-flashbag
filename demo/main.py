import aiohttp_flashbag
from aiohttp import web
from aiohttp_session import setup as setup_session
from aiohttp_session import SimpleCookieStorage


async def handler_get(request):
    validation_error = aiohttp_flashbag.flashbag_get(request, 'error')

    error_html = ''

    if validation_error is not None:
        error_html = '<span>{validation_error}</span>'.format(
            validation_error=validation_error,
        )

    body = '''
        <html>
            <head><title>aiohttp_flashbag demo</title></head>
            <body>
                <form method="POST" action="/">
                    <input type="text" name="name" />
                    {error_html}
                    <input type="submit" value="Say hello">
                </form>
            </body>
        </html>
    '''
    body = body.format(error_html=error_html)

    return web.Response(body=body.encode('utf-8'), content_type='text/html')


async def handler_post(request):
    post = await request.post()

    if len(post['name']) == 0:
        aiohttp_flashbag.flashbag_set(request, 'error', 'Name is required')

        return web.HTTPSeeOther('/')

    body = 'Hello, {name}'.format(name=post['name'])

    return web.Response(body=body.encode('utf-8'), content_type='text/html')


def make_app():
    session_storage = SimpleCookieStorage()

    app = web.Application()

    setup_session(app, session_storage)

    app.middlewares.append(aiohttp_flashbag.flashbag_middleware)

    app.router.add_route(
        'GET',
        '/',
        handler_get,
    )

    app.router.add_route(
        'POST',
        '/',
        handler_post,
    )

    return app


web.run_app(make_app())
