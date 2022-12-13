import asyncio

import aiohttp
from core.settings import Server


async def __response__(session: aiohttp.ClientSession, url: str, is_text):
    async with session.get(url, ssl=Server.ssl) as response:
        if is_text:
            return await response.text()
        else:
            return await response.json()


async def __response__all__(urls: list, loop: asyncio.AbstractEventLoop, is_text: bool):
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(*[__response__(session, url, is_text) for url in urls],
                                       return_exceptions=True)
        return results


def request(urls: list, is_text=False):
    loop = asyncio.new_event_loop()
    json = loop.run_until_complete(__response__all__(urls, loop, is_text))
    return json
