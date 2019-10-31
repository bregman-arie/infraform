# InfraForm

Provision infrastructure and deploy apps with one liners

## Usage

### Provision OpenStack instance

    infraform provision --scenario os-1-vm-fip --platform terraform --vars "cloud=myCloud"

    OR if you already have set environment variables for authentication then simply run:

    infraform provision --scenario os-1-vm-fip --platform terraform

### Create a container and run neutron tests in it

    infraform run --project /home/user/neutron --version 15 --tester py27

    To run a container with octavia from git, run:

    ifr run --project https://opendev.org/openstack/octavia.git --tester py27

## Supported platforms

Name | Type | Comments
:------ |:------:|:--------:
Podman | Containers |
Docker | Containers | 
Terraform | All |

## Scenarios

Name | Platform | Description
:------ |:------:|:--------:
os-1-vm-fip | Terraform | One instance with floating IP
jenkins_slave | - | Configures host as Jenkins slave

## Terminology

* Operation - infraform supports several operations when it comes to infra and apps:
    * provision - the creation of infrastructure
    * run - executing instructions, apps and tools on existing infrastructure
    * deploy - install and configure apps on existing infrastructure

* Platform - an platform or tool to use for operations like provision, run, etc. See [#Supported platforms](#supported-platforms)

* Scenario - a predefined instructions file. This is a platform file (e.g. Terraform file) and not Infraform file. It can be fixed or an Jinja2 template which will be then rendered by Infraform

## Contributions

To contribute to the project use GitHub pull requests.
