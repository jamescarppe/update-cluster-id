# Portainer Swarm ClusterID Updater

Manually update the Swarm ClusterID for stacks in the specified environment. For use when your Swarm has been rebuilt and has a new ClusterID.

WARNING: Back up your Portainer database first, and use with caution!

## Usage

```
update-cluster-id.py [-h] url apikey endpointid oldswarmid newswarmid

positional arguments:
  url         The URL to your Portainer API, including the port and trailing slash. Should look something like 'https://192.168.1.1:9443/'
  apikey      Your API key for accessing the Portainer API. Must be for an admin user. Can be created under My Account in the Portainer UI.
  endpointid  The numerical ID of your Swarm environment (endpoint).
  oldswarmid  The old Swarm ClusterID value that you want to replace.
  newswarmid  The new Swarm ClusterID value. You can find this by running `docker info | grep ClusterId` on a management node in your Swarm cluster.

options:
  -h, --help  show this help message and exit
```

## Example

```
$ ./update-cluster-id.py https://portainer:9443/ ptr_abcdefg 3 abcdefghijklm nopqrstuvwxyz

Portainer Swarm ClusterID Updater

Manually update the Swarm ClusterID for stacks in the specified environment. For use when your Swarm has been rebuilt and has a new ClusterID.
WARNING: Back up your Portainer database first, and use with caution!

Identified 3 stacks:
- wordpress (Stack ID: 31, Cluster ID: abcdefghijklm, Status: Running)
- nginx-example (Stack ID: 36, Cluster ID: abcdefghijklm, Status: Inactive)
- abc (Stack ID: 84, Cluster ID: abcdefghijklm, Status: Running)

Are you sure you want to proceed? [y/N] y

Continuing...

Updated 3 stacks:
- wordpress (Stack ID: 31, New Cluster ID: nopqrstuvwxyz, Status: Running)
- nginx-example (Stack ID: 36, New Cluster ID: nopqrstuvwxyz, Status: Inactive)
- abc (Stack ID: 84, New Cluster ID: nopqrstuvwxyz, Status: Running)
```