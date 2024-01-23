from flask import Flask, jsonify, request
import docker
import os
import random
app = Flask(__name__)
#TODO: add consistent hash map
client = docker.from_env()
network = "n1"
image = "server"
server_id_to_host = {}
server_host_to_id = {}
@app.route('/rep', methods=['GET'])
def get_replicas():
    # Get server containers hostnames
    containers = client.containers.list(filters={'network':network})
    response_data = {
            "N": len(containers) - 1,
            "replicas": [container.name for container in containers if container.name != "lb"]
        }
    response = {
            "message": response_data,
            "status": "successful"
        }
    return jsonify(response), 200

@app.route('/add', methods=['POST'])
def add_servers():
    data = request.get_json()
    n = data['n']
    hostnames = data['hostnames']
    # If n is less than length of hostnames supplied return error
    if(len(hostnames) > n):
        response_data = {
        "message" : "<Error> Length of hostname list is more than newly added instances",
        "status" : "failure"
    }
        return jsonify(response_data), 400
    else:
        i = 0
        while(i < n):
            # Get server IDs for server
            server_id = random.randint(0, 1000000)
            server_name = ''
            # If n > len(hostnames) generate hostnames based on server IDs
            if i < len(hostnames):
                server_name = hostnames[i]
            else:
                server_name = "S" + str(server_id)
            # spawn a server container
            try:
                client.containers.run(image=image, name=server_name, network=network, detach=True, environment={'SERVER_ID': server_id})
            except Exception as e:
                print(e)
                response = jsonify({'message': '<Error> Failed to spawn new docker container', 
                        'status': 'failure'})
                response.status_code = 400
                return response
            # store id->hostname and hostname->id mapping
            server_id_to_host[server_id] = server_name
            server_host_to_id[server_name] = server_id
            #TODO: add virtual server replicas to consistent hash table
            i = i + 1
        containers = client.containers.list(filters={'network':network})
         # Get server containers hostnames
        response_data = {
            "N": len(containers) - 1,
            "replicas": [container.name for container in containers if container.name != "lb"]
        }
        response = {
            "message": response_data,
            "status": "successful"
        }
        return jsonify(response), 200
@app.route('/rm', methods=['DELETE'])
def remove_servers():
    data = request.get_json()
    n = data['n']
    hostnames = data['hostnames']
    # If n is less than length of hostnames supplied return error
    if(len(hostnames) > n):
        response_data = {
        "message" : "<Error> Length of hostname list is more than removable instances",
        "status" : "failure"
    }
        return jsonify(response_data), 400
    # Get the list of existing server hostnames
    containers = client.containers.list(filters={'network':network})
    container_names = [container.name for container in containers if container.name != "lb"]
    # If number of servers is less than number of removable instances requested return error
    if(len(container_names) < n):
        response_data = {
        "message" : "<Error> Number of removable instances is more than number of replicas",
        "status" : "failure"
    }
        return jsonify(response_data), 400
    # Get the number of extra servers to be removed
    random_remove = n - len(hostnames)
    extra_servers = list(set(container_names) - set(hostnames))
    servers_rm = hostnames
    # Randomly sample from extra servers
    servers_rm += random.sample(extra_servers, random_remove)
    # Check if servers requested for removal exist or not
    for server in servers_rm:
        if server not in container_names:
            response_data = {
        "message" : "<Error> Server not found",
        "status" : "failure"
    }
            return jsonify(response_data), 400
    # Delete the hash map entry of server id and host names and stop and remove the correpsonding server conatiner
    for server in servers_rm:
        #TODO: remove server entry from consistent hash map
        server_id = server_host_to_id[server]
        server_host_to_id.pop(server)
        server_id_to_host.pop(server_id)
        try:
            container = client.containers.get(server)
            container.stop()
            container.remove()
        except Exception as e:
            print(e)
            response = jsonify({'message': '<Error> Failed to remove docker container', 
                        'status': 'failure'})
            response.status_code = 400
            return response
    # Get server containers hostnames
    containers = client.containers.list(filters={'network':network})
    response_data = {
            "N": len(containers) - 1,
            "replicas": [container.name for container in containers if container.name != "lb"]
        }
    response = {
            "message": response_data,
            "status": "successful"
        }
    return jsonify(response), 200


@app.route('/home', methods=['GET'])
def home():
    # Choose a random server and get its ID
    servers = [container.name for container in client.containers.list(filters={'network': network}) if container.name != "lb"]
    if not servers:
        response_data = {
            "message": "<Error> No servers available",
            "status": "failure"
        }
        return jsonify(response_data), 500

    selected_server = random.choice(servers)
    server_id = server_host_to_id.get(selected_server, "<Unknown ID>")

    response_data = {
        "message": f"Hello from Server: {server_id}",
        "status": "successful"
    }
    return jsonify(response_data), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)