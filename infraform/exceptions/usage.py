# Copyright 2019 Arie Bregman
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import crayons


def general_usage():
    """Returns general usage string."""
    message = """
Choose one of the following infraform commands: {}
Usage Examples:

    Provision an OpenStack instance with floating IP:
    $ {}

    Run pep8 tests for neutron project from local path:
    $ {}

    Run unit tests for nova project from git:
    $ {}

    Remove a container called my_container:
    $ {}
""".format(crayons.red("provision, deploy, run, destroy"),
           crayons.yellow("infraform provision --scenario os-1-vm-fip --platform terraform --vars 'network_name=...'"),
           crayons.yellow("ifr run --tester pep8 --project /home/user/neutron"),
           crayons.yellow("ifr run --tester py27 --project https://opendev.org/openstack/nova.git"),
           crayons.yellow("ifr destroy --name my_container"),)
    return message


def missing_arg(arg):
    """Missing arg message format."""
    message = """Please specify the argument {0} this way: infraform --vars '{0}=...'""".format(crayons.red(arg))
    return message


def missing_scenario(scenario):
    """Missing scenario message format."""
    message = """
Couldn't find the the scenario: {0}

New scenarios should be added here: https://github.com/bregman-arie/infraform/tree/master/infraform/scenarios
""".format(crayons.red(scenario))
    return message


def run_usage():
    """Returns run subcommand usage string."""
    message = """
Usage Examples:

    Run pep8 tests for neutron project from local path:
    $ {0}

    Run unit tests for nova project from git:
    $ {1}
""".format(crayons.yellow("ifr run --tester pep8 --project /home/user/neutron"),
           crayons.yellow("ifr run --tester py27 --project https://opendev.org/openstack/nova.git"))
    return message
