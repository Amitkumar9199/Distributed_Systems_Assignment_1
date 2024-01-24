# write a python script to launch 1000 async requests to (url):

import asyncio
import aiohttp
import matplotlib.pyplot as plt
import requests
import json

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

    # launch a GET request to the url
    url = 'http://localhost:5000/home'

    # run curl -X DELETE  -H "Content-Type: application/json" -d '{"n": 1, "hostnames": ["s1"]}' 
    # http://localhost:5000/hosts

    data = {"n": 1, "hostnames": ["s3"]}
    headers = {"Content-Type": "application/json"}

    # we deleted one instance of a server (which was 3 initially)

    response = requests.delete(url, data=json.dumps(data), headers=headers)

    if response.status_code == 200:

        main_data = {}

        for i in range (2, 7):

            freq = {}

            for j in range(10000):
                async with aiohttp.ClientSession() as session:
                    response = await fetch(session, url)
                    
                    serverid = extract_server_id(response)
                    freq[serverid] = freq.get(serverid, 0) + 1
            
            server_count = len(freq.values())

            mean = sum(freq.values()) / server_count

            variance = sum([((x - mean) ** 2) for x in freq.values()]) / server_count

            std_dev = variance ** 0.5

            main_data[i] = std_dev

            data = {"n": 1, "hostnames": ["s" + str(i + 1)]}

            response = requests.post(url, data=json.dumps(data), headers=headers)

        plt.bar(main_data.keys(), main_data.values())
        plt.xlabel('Number of Servers')
        plt.ylabel('Standard Deviation')

        # print the graph
        plt.show()

    else:
        print("Error: " + str(response.status_code))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())