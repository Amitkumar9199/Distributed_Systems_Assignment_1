from flask import Flask, jsonify
import os

def spawn_container():
    res=os.popen(f'sudo docker run --name server1 --network net1 --network-alias hostserver1 -e SERVER_ID=1 -d server:latest').read()
    if len(res)==0:
        print("Unable to start server1")
    else:
        print("successfully started server1")

if __name__ == "__main__":
    spawn_container()