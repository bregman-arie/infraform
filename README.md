# InfraForm

Provision infrastructure and deploy apps with one liners

Default platform: Podman

## Usage

To run a container with neutron project from a local path and run unit tests, run:

    infraform --project /home/user/neutron --version 15 --tester py27

To run a container with octavia from git, run:

    infraform --project https://opendev.org/openstack/octavia.git --tester py27

## Supported platforms

Name | Type | Comments
:------ |:------:|:--------:
Podman | Containers | 
Docker | Containers | 

## Contributions

To contribute to the project use GitHub pull requests.
