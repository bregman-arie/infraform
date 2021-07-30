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

### Set up ELK on a remote host

    ifr run elk --host some.host

### Provision OpenStack instance with a floating IP

    infraform run --scenario os-1-vm-fip --vars="network_provider=..."

## Scenarios

Scenario file is one that ends with `.ifr` or `ifr.j2` suffix. It's YAML with the following directives:

```
description: the description of the scenario
platform: the platform or tool to use (e.g. terraform, ansible, shell, python, etc.)
content: |
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

## Workflow

What happens when you execute a scenario on a remote host(s)?

1. Infraform checks the host is ready to execute the scenario. For example, if it's Docker based scenario then Infraform checks docker is installed and running on the host
2. A workspace is created. Basically the scenario directory (or file) copied recursively to ~/.infraform path
3. Any templates in ~/.infraform/<scenario_dir> are being rendered, including the scenario file itself
4. Remote environment is prepared. Local ~/.infraform/<scenario_dir> is copied to remote hosts to ~/.infraform path.
5. Infraform runs the "run" directive in ~/.infraform/<scenario_dir>/<scenario_file> on the remote hosts

## Contributions

To contribute to the project use GitHub pull requests.
