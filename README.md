# InfraForm

[![Build Status](https://travis-ci.org/bregman-arie/infraform.svg?branch=master)](https://travis-ci.org/bregman-arie/infraform)

Unified interface for infrastructure related operations using predefined templates

The idea is to quickly run common operations and yet, keep it dynamic enough so it can be done with different properties and on different locations.

<div align="center"><img src="./images/infraform.png"></div><hr/>

## Requirements

* Linux
* Python3

## Installation

    git clone https://github.com/bregman-arie/infraform
    cd infraform
    virtualenv ~/ifr_venv && source ~/ifr_venv/bin/activate
    pipenv install .

## Usage

### Provision OpenStack instance with a floating IP

    infraform run --scenario os-1-vm-fip --vars="network_provider=..."

### Run Python PEP8 test inside a Podman container:

    ifr run --scenario pep8-tests --vars 'project=/my/project'

You can also use more specific approach where you choose exactly what to execute once the container is ready

    ifr run --scenario pep8-tests --vars 'project=/my/project execute="git checkout origin/some-branch; tox -e pep8"

### Regiser host as a Jenkins node

    infraform run --scenario jenkins_node --vars="jenkins_url=https://my.jenkins.com node_name=name-in-jenkins jenkins_user=abregman jenkins_password=my-API-token labels=my-hosts host=my.host.com credsid=xxx-xxx-xxx-xxx"

### Run ELK stack + Jenkins + Filebeat. Once running it will automatically process a build log and will also index it

    ifr run --scenario elk_filebeat_jenkins

### Run ELK stack and process an apache log

    ifr run --scenario elk_apache

## Scenarios

Scenario is a predefined instructions file or template. It can be anything - creating a VM, run tests, set up ELK, ... you choose.
Infraform provides with a couple of built-in scenarios

Name | Platform | Description | Arguments
:------ |:------:|:--------:|:---------:
os-1-vm-fip | Terraform | One OpenStack instance with a floating IP | 
libvirt-1-vm | Terraform | One Libvirt VM | remote_host, user
register-jenkins-node | Shell | Registers host as Jenkins node |
setup-jenkins-node | Shell | Configures clean host as Jenkins node |
pep8-tests | Podman, Docker | Run PEP8 tests in a container | override_image
unit-tests | Podman, Docker | Run unit tests in a container | override_image
functional-tests | Podman, Docker | Run functional tests in a container |
elk_filebeat_jenkins | Docker Compose | Containerized ELK + Filbeat + Jenkins and process Jenkins build log
elk_apache | Docker Compose | Containerized ELK and process Apache log

### List Scenarios

You can list scenarios with `ifr list`

### Show Scenario

You can show scenario content with `ifr show <scenario_name>`

### Scenario Structure

The format of a scenario is as follows:

```
---
execute: <some_command>
```

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

## Create your own Scenario

Add new scenarios in `infraform/scenarios`.
Scenario format depends on the platform. Any Scenario can be jinja2 template in order to get certain input from the user and not use fixed values.

## Development

If you are interested in developing Infraform further, please read [here](docs/developer.md)

## Contributions

To contribute to the project use GitHub pull requests.
