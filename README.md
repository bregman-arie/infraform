# InfraForm

[![Build Status](https://travis-ci.org/bregman-arie/infraform.svg?branch=master)](https://travis-ci.org/bregman-arie/infraform)

Unified interface for infrastructure related operations. Infraform allows you to:

* Run common built-in operations (aka scenarios) or provide your own and let Infraform handle the execution
* Use templated scenarios - one scenario, many ways to render it
* Execute scenarios locally or on remote hosts
* Make use of different technologies to run the scenarios - Ansible, Python, Terraform, Docker, Docker Compose

Infraform is really all about ease of use. Infraform not only let's you use the same interface to run all these different technologies but it also supports templating which makes the use common technologies like Ansible, Terraform, Containers, ... much easier.

Hope you'll enjoy using it :)

<div align="center"><img src="./images/infraform.png"></div><hr/>

## Requirements

* Linux (Developed and tested on Fedora)
* Python>=3.7

## Installation

    git clone https://github.com/bregman-arie/infraform && cd infraform
    virtualenv ~/ifr_venv && source ~/ifr_venv/bin/activate
    pip install .

## Usage Examples

### List Scenarios

    ifr list

### Setup ELK on a remote host

    ifr run elk --host some.host

### Provision OpenStack instance with a floating IP

    infraform run os-1-vm-fip --vars="network_provider=..."

## Scenarios

Scenario file is one that ends with `.ifr` or `ifr.j2` suffix. It uses the YAML format with the following directives:

```
description: # the description of the scenario
platform:    # the platform or tool to use (e.g. terraform, ansible, shell, python, etc.)
files:       # the files to copy to the workspace to be used during the execution of the scenario
 - file1
 - file2
content: |   # The content of the scenario (shell script, terraform, ansible playbooks, etc.)
    just
    the
    contents
    of the
    scenario
```

Infraform provides you with a couple of built-in scenarios you can list with `ifr list`<br>
To see the content of scenario, run `infraform show <scenario_name>`

In addition to running scenarios you can also run directly files and directories with `ifr run <DIR/FILE name/path>`<br>
As opposed to scenarios, the tool or platform used in this case, is determined by the suffix of the file or the files in the directory.

## Supported platforms and tooling

InfraForm is able to execute using the following technologies

Name | Comments 
:------ |:------:
Podman | Run containers using Podman
Docker | Run containers using Docker
docker-compose | Run containers using Docker
Terraform | Provision infrastucture using Terraform HCL files
Python | Run Python programs
Shell | Run Bash shell scripts

### Too detailed workflow

The following is a description of what InfraForm does when you run a scenario

1. Validates the scenario you've specified exists (the .ifr file)
2. Check if a workspace (~/.infraform/<SCENARIO_NAME>) directory exists already. If it exists, it removes the entire directory
3. Creates a workspace (~/.infraform/<SCENARIO_NAME>) directory
4. Copies the scenario file (.ifr) and all the related content to the directory

## Contributions

To contribute to the project use GitHub pull requests.
