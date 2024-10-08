"""

Sample bot that shows how to access the HTTP request.

"""

from __future__ import annotations

import re
from typing import AsyncIterable

import fastapi_poe as fp
from devtools import PrettyFormat
from modal import App, Image, asgi_app

pformat = PrettyFormat(width=85)


class HttpRequestBot(fp.PoeBot):
    async def get_response_with_context(
        self, request: fp.QueryRequest, context: fp.RequestContext
    ) -> AsyncIterable[fp.PartialResponse]:

        context_string = pformat(context)
        context_string = re.sub(r"Bearer \w+", "Bearer [REDACTED]", context_string)
        context_string = re.sub(
            r"b'host',\s*b'([^']*)'", r"b'host', b'[REDACTED_HOST]'", context_string
        )

        yield fp.PartialResponse(text="```python\n" + context_string + "\n```")


REQUIREMENTS = ["fastapi-poe==0.0.46", "devtools==0.12.2"]
image = Image.debian_slim().pip_install(*REQUIREMENTS)
app = App("http-request")


@app.function(image=image)
@asgi_app()
def fastapi_app():
    bot = HttpRequestBot()
    # Optionally, provide your Poe access key here:
    # 1. You can go to https://poe.com/create_bot?server=1 to generate an access key.
    # 2. We strongly recommend using a key for a production bot to prevent abuse,
    # but the starter examples disable the key check for convenience.
    # 3. You can also store your access key on modal.com and retrieve it in this function
    # by following the instructions at: https://modal.com/docs/guide/secrets
    # POE_ACCESS_KEY = ""
    # app = make_app(bot, access_key=POE_ACCESS_KEY)
    app = fp.make_app(bot, allow_without_key=True)
    return app
