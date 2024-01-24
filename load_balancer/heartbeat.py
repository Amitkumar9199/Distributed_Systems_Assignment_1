import asyncio
import aiohttp
from time import sleep

# write a function to launch a get request to the url and return the response
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()
    
async def main():
    while True:
        sleep(2)
        url = 'http://localhost:5000/heartbeat'
        async with aiohttp.ClientSession() as session:
            response = await fetch(session, url)
            

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
