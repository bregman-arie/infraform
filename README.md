# InfraForm

Provision infrastructure and deploy apps with one liners

Default platform: Podman

## Usage

To provision an instance with floating IP on OpenStack cloud using Terraform:

    infraform provision --scenario os-1-vm-fip --platform terraform

To create a container with neutron project from a local path and run unit tests, run:

    infraform run --project /home/user/neutron --version 15 --tester py27

To run a container with octavia from git, run:

    ifr run --project https://opendev.org/openstack/octavia.git --tester py27

## Supported platforms

Name | Type | Comments
:------ |:------:|:--------:
Podman | Containers | 
Docker | Containers | 
Terraform | All |

## Contributions

To contribute to the project use GitHub pull requests.
