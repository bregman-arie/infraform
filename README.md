# InfraForm

Terraform based project for managing OpenStack related resources

## Usage

To create one instance with reachable floating IP:

    infraform form --scenario one_instance_with_fip --name my_setup

List managed resources:

    infraform list

Remove group of resources:

    infraform delete --name my_setup

Remove all resources:

    infraform delete --all


## Contributions

To contribute, submit patches through review.gerrithub.io
