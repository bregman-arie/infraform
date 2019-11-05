# InfraForm

Unified interface for provisioning infrastructure and deploy apps using different platforms and tools

## Usage

### Provision OpenStack instance

    infraform provision --scenario os-1-vm-fip --vars="network_provider=..."

### Create a container and run neutron tests in it

    infraform run --vars "project=/home/user/neutron tester=py27"

You can also use more specific approach where you choose exactly what to execute once the container is ready

    ifr run --vars="project=/neutron execute='cd neutron; git checkout origin/rhos-14.0-patches; tox -e pep8'"

## Scenarios

Name | Platform | Description | Example
:------ |:------:|:--------:|:---------:
os-1-vm-fip | Terraform | One OpenStack instance with a floating IP | `
jenkins_slave | Python | Configures host as a Jenkins slave |
usage_patterns | Shell | Deploys Usage Patterns UI server |

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

## Contributions

To contribute to the project use GitHub pull requests.
