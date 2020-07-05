## Scenarios

Scenario is a predefined instructions file or template. It can be anything - creating a VM, run tests, set up ELK, ... you choose (or write your own)

## Supported Scenarios

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

## Create your own Scenario

Add new scenarios in `infraform/scenarios`.
Scenario format depends on the platform. Any Scenario can be jinja2 template in order to get certain input from the user and not use fixed values.

