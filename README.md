# A-1

It is clear from the graph that the load is unevenly distributed amoung the servers.
Which has some known pitfalls.
1. Uneven utilization of resources.
2. Uneven load distribution can result in higher latency for users accessing the overloaded servers, leading to slower response times.
3. Overloaded servers may become prone to failures, leading to potential downtime or service disruptions.
4. Uneven load distribution can make it harder to accurately plan for and allocate resources.

<!-- TODO: Explaination of the uneven distribution -->

## A-2

By looking on the data of standard deviation vs server counts we can say that Linear probing technique is effective on large number of server instances, while on small server instances Quadratic probing is helpful. However in both of these cases the distribution is fairly uneven which may result in scalabily issue and Capacity planning becomes more challenging when the load balancer is not distributing traffic evenly across servers.

<!-- TODO: Explaination of the uneven distribution -->

## A-3

We are creating a new process which regularly sends 'heartbeat in interval of 2 seconds. It helps loadbalancer to check whether servers are alive or not. We are maintaining a circular array of servers and sending heatbeat in a circular way. If status code is 200 then it isonline and we do nohing. Otherwise we cheking if server container has stopped or is removed  . if it is stppoed then we will resume then server container else we will fire up a new server container.
This way we are keeping fixed number if servers. 
In worst case how much time will be required to again make server alive: 
    Assuming there are currently  n live servers , then in worst case it might take 2*n seconds 

