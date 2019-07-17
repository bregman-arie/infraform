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
    """Help message format."""
    message = """
Usage Examples:

    Run pep8 tests for neutron project:
    $ {0}

    Run unit tests for nova project:
    $ {1}

""".format(crayons.red("ifr run --tester pep8 --project neutron"),
           crayons.red("ifr run --tester unit --project nova"),)
    return message


def missing_required_args():
    """Help message format."""
    message = """
You have to specify either:

    scenario name or path. This way:
    $ {0}

OR

    project and tester. This way:
    $ {1}

""".format(crayons.red("ifr run --scenario neutron_pep8"),
           crayons.red("ifr run --tester pep8 --project neutron"),)
    return message
