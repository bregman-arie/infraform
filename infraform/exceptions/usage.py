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
Usage Examples:

    Run pep8 tests for neutron project from git:
    $ {0}

    Run unit tests for nova project:
    $ {1}

    Remove a container called my_container:
    $ {2}
""".format(crayons.yellow("ifr run --tester pep8 --project neutron --git x.com"),
           crayons.yellow("ifr run --tester unit --project nova --gerrit y.com"),
           crayons.yellow("ifr rm --name my_container"),)
    return message


def missing_arg(arg):
    """Missing arg message format."""
    message = """
Please specify the argument: {0}""".format(crayons.red(arg))
    return message


def run_usage():
    """Returns run subcommand usage string."""
    message = """
Usage Examples:

    Run pep8 tests for neutron project from git:
    $ {0}

    Run unit tests for nova project:
    $ {1}
""".format(crayons.yellow("ifr run --tester pep8 --project neutron --git x.com"),
           crayons.yellow("ifr run --tester unit --project nova --gerrit y.com"))
    return message
