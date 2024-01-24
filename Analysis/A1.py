# write a python script to launch 1000 async requests to (url):

import asyncio
import aiohttp

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()
    
async def main():
    url = 'https://www.google.com'

    for i in range(10000):
        async with aiohttp.ClientSession() as session:
            html = await fetch(session, url)
            print(html.message)
    
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
