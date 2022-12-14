""" Researcher (polling, no websocket and no central container)

Example on how the researcher should initialize a task without using
the central container. This means that the central part of the
algorithm needs to be executed on the machine of the researcher.

For simplicity this example also uses polling to obtain the results.
A more advanced example shows how to obtain the results using websockets

The researcher has to execute the following steps:
1) Authenticate to the central-server
2) Prepare the input for the algorithm
3) Post a new task to a collaboration on the central server
4) Wait for all results to finish (polling)
5) Obtain the results
6) Optionally do some central processing
"""
import time

from vantage6.client import Client

# 1. authenticate to the central server
client = Client(
    host="http://192.168.37.1",
    port=5000,
    path="/api"
)
client.setup_encryption(None)
client.authenticate("root", "admin")

# 2. Prepare input for the dsummary Docker image (algorithm)
input_ = {
    "master": "true",
    "method":"master", 
    "args": [], 
    "kwargs": {
        #"functions": ["min", "max"],
        "columns": [
            {
                "variable": "age",
                "table": "records",
                "functions": ["min", "max"]
            },
            {
                "variable": "weight",
                "table": "records"
            }
        ]
    }
}

# post the task to the server
task = client.post_task(
    name="summary",
    image="pmateus/v6-summary-rdb:1.2.0",
    collaboration_id=3,
    input_=input_
)

# poll for results
task_id = task.get("id")
print(f"task id={task_id}")

# check if the task is finished
task = client.request(f"task/{task_id}")
while not task.get("complete"):
    task = client.request(f"task/{task_id}")
    print("Waiting for results...")
    time.sleep(1)

# obtain the finished results
results = client.get_results(task_id=task.get("id"))

# Do some stuff with the results ...

# e.g. print the results per node
for result in results:
    node_id = result.get("node")
    print("-"*80)
    print(f"Results from node = {node_id}")
    print(result.get("result"))
