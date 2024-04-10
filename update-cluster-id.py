import argparse
import json
import requests
from urllib3.exceptions import InsecureRequestWarning
# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Set up the common parameters (should be pulled from the CLI options)
parser = argparse.ArgumentParser(
                    prog="update-cluster-id.py",
                    description="Manually update the Swarm ClusterID for stacks in the specified environment. For use when your Swarm has been rebuilt and has a new ClusterID. WARNING: Back up your Portainer database first, and use with caution!")
parser.add_argument("url", help="The URL to your Portainer API, including the port and trailing slash. Should look something like 'https://192.168.1.1:9443/'")
parser.add_argument("apikey", help="Your API key for accessing the Portainer API. Must be for an admin user. Can be created under My Account in the Portainer UI.")
parser.add_argument("endpointid", type=int, help="The numerical ID of your Swarm environment (endpoint).")
parser.add_argument("oldswarmid", help="The old Swarm ClusterID value that you want to replace.")
parser.add_argument("newswarmid", help="The new Swarm ClusterID value. You can find this by running `docker info | grep ClusterId` on a management node in your Swarm cluster.")
args = parser.parse_args()

portainer_url = args.url              # "https://192.168.1.1:9443/"
apikey = args.apikey                  # "ptr_abcdefg"
endpointid = args.endpointid          # 3
oldswarmid = args.oldswarmid          # "abcdefghijklm"
newswarmid = args.newswarmid          # "nopqrstuvwxyz"

headers = {'X-API-Key': apikey}

print("\nPortainer Swarm ClusterID Updater\n")
print("Manually update the Swarm ClusterID for stacks in the specified environment. For use when your Swarm has been rebuilt and has a new ClusterID.")
print("WARNING: Back up your Portainer database first, and use with caution!\n")

# Retrieve the list of stacks with the current Swarm ID
querystring = {'SwarmId': oldswarmid}
payload = {'filters': json.dumps(querystring)}
response = requests.get(portainer_url + "api/stacks", params=payload, headers=headers, verify=False)
stacks = json.loads(response.text)

# Iterate through the stacks and update the Swarm ID
print ("Identified " + str(len(stacks)) + " stacks:")

for stack in stacks:
    # Determine and retain the current stack status (running or inactive)
    if stack["Status"] == 2:
      stackStatus = "Inactive"
    else:
      stackStatus = "Running"
    print("- " + stack["Name"] + " (Stack ID: " + str(stack["Id"]) + ", Cluster ID: " + stack["SwarmId"] + ", Status: " + stackStatus + ")")

user_input = input("\nAre you sure you want to proceed? [y/N] ")
if user_input.lower() == "y":
  print("\nContinuing...\n")
else:
  print("\nAborting.")
  exit()

# Do the thing

for stack in stacks:
    if stack["Status"] == 2:
      orphanedRunning = 'false'
    else:
      orphanedRunning = 'true'

    # Update the stack configuration
    updateparams = {'endpointId': endpointid, 'swarmId': newswarmid, 'orphanedRunning': orphanedRunning}
    updatereq = requests.put(portainer_url + "api/stacks/" + str(stack["Id"]) + "/associate", params=updateparams, headers=headers, verify=False)

# Check your work
newquerystring = {'SwarmId': newswarmid}
newpayload = {'filters': json.dumps(newquerystring)}
newresponse = requests.get(portainer_url + "api/stacks", params=newpayload, headers=headers, verify=False)
newstacks = json.loads(newresponse.text)

print ("Updated " + str(len(stacks)) + " stacks:")

for newstack in newstacks:
    if newstack["Status"] == 2:
      newstackStatus = "Inactive"
    else:
      newstackStatus = "Running"

    print("- " + newstack["Name"] + " (Stack ID: " + str(newstack["Id"]) + ", New Cluster ID: " + newstack["SwarmId"] + ", Status: " + newstackStatus + ")")
