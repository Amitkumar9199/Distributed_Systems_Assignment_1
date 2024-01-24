# write a python script to launch 1000 async requests to (url):

import asyncio
import aiohttp
import matplotlib.pyplot as plt

# write a function to launch a get request to the url and return the response
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

def extract_server_id(response):
    # Find the index of the colon in the response
    colon_index = response.find(':')

    # Extract the server_id by slicing the string after the colon
    server_id = response[colon_index + 1:].strip()

    return server_id
    
async def main():
    url = 'https://www.google.com'

    # store the count of serverid responses in a dictionary

    freq = {}

    for i in range(10000):
        async with aiohttp.ClientSession() as session:
            response = await fetch(session, url)
            
            serverid = extract_server_id(response)
            freq[serverid] = freq.get(serverid, 0) + 1

    # draw a bar graph of the frequency of each serverid
    plt.bar(freq.keys(), freq.values())



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
