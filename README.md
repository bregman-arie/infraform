# InfraForm

Provision infrastructure and deploy apps with one liners

## Usage

### Provision OpenStack instance

    infraform provision --scenario os-1-vm-fip --platform terraform --vars "cloud=myCloud"

    OR if you already have set environment variables for authentication then simply run:

    infraform provision --scenario os-1-vm-fip --platform terraform

### Create a container and run neutron tests in it

    infraform run --vars "project=/home/user/neutron tester=py27"

    To run a container with octavia from git, run:

    ifr run --vars "project='https://opendev.org/openstack/octavia.git' tester=py27"

    You can also use the following command to run anything you would like:

    ifr run --vars="project=/neutron execute='cd neutron; git checkout origin/rhos-14.0-patches; tox -e pep8'"

## Supported platforms & tools

Name | Comments | 
:------ |:------:|:--------:
Podman |
Docker |
Terraform |
Python |
Shell |

## Scenarios

Name | Platform | Description | Example
:------ |:------:|:--------:|:---------:
os-1-vm-fip | Terraform | One instance with floating IP | `
jenkins_slave | Python | Configures host as Jenkins slave |
usage_patterns | Shell | Deploys Usage Patterns server |

## Terminology

* Operation - infraform supports several operations when it comes to infra and apps:
    * provision - the creation of infrastructure
    * run - executing instructions, apps and tools on existing infrastructure
    * deploy - install and configure apps on existing infrastructure

* Platform - an platform or tool to use for operations like provision, run, etc. See [#Supported platforms](#supported-platforms)

* Scenario - a predefined instructions file. This is a platform file (e.g. Terraform file) and not Infraform file. It can be fixed or an Jinja2 template which will be then rendered by Infraform

## Containers - Supported Variables

Name | Description
:------ |:--------:
override_image | If there is an existing image, remove it and build the image from scratch

## Contributions

To contribute to the project use GitHub pull requests.
