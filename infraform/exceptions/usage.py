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

    Run Python PEP8 tests inside a Podman container:
    $ {}

    List available scenarios:
    $ {}

    Show scenario:
    $ {}

    Run unit tests for nova project from git:
    $ {}

""".format(crayons.red("run, list, show"),
           crayons.yellow("infraform run --scenario \
os-1-vm-fip --vars \"provider_network=...\""),
           crayons.yellow('ifr run --scenario pep8-tests \
--vars "project=/home/user/neutron"'),
           crayons.yellow('ifr list'),
           crayons.yellow('ifr show <scenario_name>'),
           crayons.yellow("ifr run --scenario pep8-tests --vars \
'project=/my/project execute=\"git \
checkout origin/some-branch; tox -e pep8\"'"))
    return message


def missing_arg(arg):
    """Missing arg message format."""
    message = """Please specify the argument {0} this way: infraform \
--vars \"{0}=...\"""".format(crayons.red(arg))
    return message


def missing_scenario(scenario):
    """Missing scenario message format."""
    message = """
Couldn't find the the scenario: {0}

New scenarios should be added here: \
https://github.com/bregman-arie/infraform/tree/master/infraform/scenarios
""".format(crayons.red(scenario))
    return message


def missing_scenario_arg():
    """Missing scenario arg message format."""
    message = "Please specify which scenario to run with \
{}".format(crayons.red("--scenario <SCENARIO_NAME>"))
    return message
