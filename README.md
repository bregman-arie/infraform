# InfraForm

Provision infrastructure and deploy apps with one liners

Default platform: Podman

## Usage

To run a container with neutron project and run unit tests, run the following command:

    infraform --project neutron --version 15 --tester py27

To run a container with nova from git, run the following command:

    infraform --project nova --tester py27 --git opendev.org/openstack

To run neutron pep8 tests on master using docker, run the following command:

    infraform --project neutron --tester pep8 --platform docker

## Supported platforms

Name | Type | Comments
:------ |:------:|:--------:
Podman | Containers | 
Docker | Containers | 

## Contributions

To contribute to the project use GitHub pull requests.
