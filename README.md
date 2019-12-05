# InfraForm

Unified interface for provisioning infrastructure and deploy apps using different platforms and tools

## Installation

In order to use infraform you need to use Python3 and run the following commands:

    pipenv shell
    pipenv install -e .

## Usage Examples

### Provision OpenStack instance

    infraform run --scenario os-1-vm-fip --vars="network_provider=..."

### Run Python PEP8 inside a Podman container:

    ifr run --scenario pep8-tests --vars 'project=/my/project'

You can also use more specific approach where you choose exactly what to execute once the container is ready

    ifr run --scenario pep8-tests --vars 'project=/my/project execute="git checkout origin/some-branch; tox -e pep8"

### Configure host as Jenkins node

    infraform run --scenario jenkins_node --vars="jenkins_url=https://my.jenkins.com node_name=name-in-jenkins jenkins_user=abregman jenkins_password=my-API-token labels=my-hosts host=my.host.com credsid=xxx-xxx-xxx-xxx"

## Scenarios

Name | Platform | Description | Example
:------ |:------:|:--------:|:---------:
os-1-vm-fip | Terraform | One OpenStack instance with a floating IP | 
register-jenkins-node | Shell | Registers host as Jenkins node |
setup-jenkins-node | Shell | Configures clean host as Jenkins node |
pep8-tests | Podman, Docker | Run PEP8 tests in a container |
unit-tests | Podman, Docker | Run unit tests in a container | 
functional-tests | Podman, Docker | Run functional tests in a container |
elastic_stack_host | shell | Install and run Elastic Stack directly on the host
elastic_stack_container | shell | Install and run Elastic Stack inside a container

## Supported platforms and tools

Name | Comments 
:------ |:------:
Podman | Create container images and run apps/tests inside Podman containers
Docker | Same as Podman but using Docker instead
Terraform | Provision infrastucture using Terraform HCL files
Python | Run Python programs
Shell | Run Bash shell scripts

## Terminology

* Platform - an platform or tool to use for operations like provision, run, etc. See [#Supported platforms](#supported-platforms-and-tools)

* Scenario - a predefined instructions file. This is a platform file (e.g. Terraform file) and not Infraform file. It can be fixed or a Jinja2 template which will be then rendered by Infraform

## Containers - Extra Supported Variables

Name | Description
:------ |:--------:
override_image | If there is an existing image, remove it and build the image from scratch

## Create your own Scenario

Add new scenarios in `infraform/scenarios`.
Scenario format depends on the platform. Any Scenario can be jinja2 template in order to get certain input from the user and not use fixed values.

## Contributions

To contribute to the project use GitHub pull requests.
