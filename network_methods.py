from aiohttp import ClientSession


async def request_get(
        url: str, return_text: bool = False, return_json: bool = False
) -> str or list:
    async with ClientSession() as session:
        response = await session.get(url)

        if return_text and return_json:
            raise ValueError
        elif not (return_text or return_json):
            raise ValueError

        if return_text:
            return await response.text()
        else:
            return await response.json()

