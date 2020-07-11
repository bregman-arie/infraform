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


def missing_reqs(inst, hosts, failure):
    """Message on missing requirements"""
    if hosts:
        loc = "on {}".format(' '.join(hosts))
    else:
        loc = "on this host"
    if failure:
        failures = "The following failure happened:\n\n{}".format(
            crayons.red("\n".join(failure)))
    else:
        failures = ""

    message = """
There seems to be a problem {0}
{1}
Perhaps try the following:

{2}
""".format(crayons.red(loc), failures, crayons.cyan("\n".join(inst)))

    return message
