import asyncio
import httpx
from core.settings import Server


class Query(object):

    async def __getresponse__(self, client: httpx.AsyncClient, url, **kwargs):
        response = await client.get(url, **kwargs)
        return response

    async def __get_client_str__(self, url, isText: bool, **kwargs):
        async with httpx.AsyncClient(verify=Server.ssl) as client:
            response = await client.get(url, **kwargs)
            if isText:
                return response.text
            else:
                return response.json()

    async def __get_client_lst__(self, urls, isText: bool, **kwargs):

        async with httpx.AsyncClient(verify=Server.ssl) as client:
            tasks = []
            for i in urls:
                tasks.append(asyncio.ensure_future(
                    self.__getresponse__(client, i, **kwargs)))
            result: httpx.Response = await asyncio.gather(*tasks, return_exceptions=True)

            if isText:
                return [i.text for i in result]
            else:
                return [i.json() for i in result]

    def get(self, url, isText=False, **kwargs):
        loop = asyncio.new_event_loop()
        if isinstance(url, list):
            result = loop.run_until_complete(
                self.__get_client_lst__(url, isText, **kwargs))

        elif isinstance(url, str):
            result = loop.run_until_complete(
                self.__get_client_str__(url, isText, **kwargs)
            )
        return result

    async def __post_client_str__(self, url: str, isText: bool, **kwargs):
        async with httpx.AsyncClient(verify=Server.ssl) as client:
            response = await client.post(url, **kwargs)
            if isText:
                return response.text
            else:
                return response.json()

    def post(self, url, isText=False, **kwargs):
        loop = asyncio.new_event_loop()
        if isinstance(url, str):
            result = loop.run_until_complete(
                self.__post_client_str__(url, isText, **kwargs)
            )
        return result
