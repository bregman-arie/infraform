# InfraForm

Unified interface for infrastructure related operations using predefined templates

The idea is to quickly run common operations and yet, keep it dynamic enough so it can be done with different properties and on different locations.

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

### Regiser host as a Jenkins node

    infraform run --scenario jenkins_node --vars="jenkins_url=https://my.jenkins.com node_name=name-in-jenkins jenkins_user=abregman jenkins_password=my-API-token labels=my-hosts host=my.host.com credsid=xxx-xxx-xxx-xxx"

### Elasticsearch summary + perform a query

ifr run --scenario elastic_summary --vars "es_server='"http://<es_server>:9200"' index=my_index query='{\"someKey\": \"someValue\"}'"

## Scenarios

Scenario is a predefined instructions file or template. This is a platform dependent file (e.g. Terraform file) and not Infraform file. 

Name | Platform | Description | Arguments
:------ |:------:|:--------:|:---------:
os-1-vm-fip | Terraform | One OpenStack instance with a floating IP | 
libvirt-1-vm | Terraform | One Libvirt VM | remote_host, user
register-jenkins-node | Shell | Registers host as Jenkins node |
setup-jenkins-node | Shell | Configures clean host as Jenkins node |
pep8-tests | Podman, Docker | Run PEP8 tests in a container | override_image
unit-tests | Podman, Docker | Run unit tests in a container | override_image
functional-tests | Podman, Docker | Run functional tests in a container |
elastic_summary | python | Print information on Elasticsearch server and indices and performs query (optional) | es_server

### List Scenarios

You can list scenarios with `ifr list`

## Supported platforms and tools

InfraForm is able to execute the following types of platforms and tools

Name | Comments 
:------ |:------:
Podman | Run containers using Podman
Docker | Run containers using Docker
Terraform | Provision infrastucture using Terraform HCL files
Python | Run Python programs
Shell | Run Bash shell scripts

## Create your own Scenario

Add new scenarios in `infraform/scenarios`.
Scenario format depends on the platform. Any Scenario can be jinja2 template in order to get certain input from the user and not use fixed values.

## Contributions

To contribute to the project use GitHub pull requests.
