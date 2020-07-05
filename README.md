# InfraForm

[![Build Status](https://travis-ci.org/bregman-arie/infraform.svg?branch=master)](https://travis-ci.org/bregman-arie/infraform)

Unified interface for infrastructure related operations using dynamic, predefined templates

* Run common operations (aka scenarios) using different tools and platforms like Terraform, Ansible and Docker
* Template scenarios to reuse them in different environments and with different properties - one scenario, many ways to run it
* Execute locally or on remote hosts
* Checks hosts are able to run the scenario and if not, modify the hosts accordingly

Infraform aims to provides users with simple, yet dynamic, way to manage their infra related operations.
Hope you'll enjoy using it :)

<div align="center"><img src="./images/infraform.png"></div><hr/>

## Requirements

* Linux (Developed and tested on Fedora)
* Python>=3.7

## Installation

    git clone https://github.com/bregman-arie/infraform
    cd infraform
    virtualenv ~/ifr_venv && source ~/ifr_venv/bin/activate
    pip install .

## Usage Examples

### Provision OpenStack instance with a floating IP

    infraform run --scenario os-1-vm-fip --vars="network_provider=..."

### Run Python PEP8 test inside a Podman container:

    ifr run --scenario pep8-tests --vars 'project=/my/project'

You can also use more specific approach where you choose exactly what to execute once the container is ready

    ifr run --scenario pep8-tests --vars 'project=/my/project execute="git checkout origin/some-branch; tox -e pep8"

### Regiser host as a Jenkins node

    infraform run --scenario jenkins_node --vars="jenkins_url=https://my.jenkins.com node_name=name-in-jenkins jenkins_user=abregman jenkins_password=my-API-token labels=my-hosts host=my.host.com credsid=xxx-xxx-xxx-xxx"

### Run ELK stack + Jenkins + Filebeat. Once running, it will automatically process a Jenkins build log and will also index it

    ifr run --scenario elk_filebeat_jenkins

### Set up ELK on a remote host

    ifr run --scenario elk --host some.host

## Scenarios

Scenario is a predefined instructions file or template. It can be anything - creating a VM, run tests, set up ELK, ... you choose (or write your own)
Infraform provides you with a couple of built-in scenarios

Name | Platform | Description | Arguments
:------ |:------:|:--------:|:---------:
os-1-vm-fip | Terraform | One OpenStack instance with a floating IP | 
register-jenkins-node | Shell | Registers host as Jenkins node |
pep8-tests | Podman, Docker | Run PEP8 tests in a container | override_image
elk_filebeat_jenkins | Docker Compose | Containerized ELK + Filbeat + Jenkins and process Jenkins build log

To see the full list of scenarios and learn more it, have a look [here](docs/scenarios.md)

## Supported platforms and tools

InfraForm is able to execute the following types of platforms and tools

Name | Comments 
:------ |:------:
Podman | Run containers using Podman
Docker | Run containers using Docker
docker-compose | Run containers using Docker
Terraform | Provision infrastucture using Terraform HCL files
Python | Run Python programs
Shell | Run Bash shell scripts

## Development

If you are interested in developing Infraform further, please read [here](docs/developer.md)

## Contributions

To contribute to the project use GitHub pull requests.
