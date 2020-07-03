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


def missing_reqs(inst, host):
    """Message on missing requirements"""
    if host:
        loc = "on the host {}".format(host)
    else:
        loc = "on this host"
    message = """
Alfred: Sir, I'm unable to execute what you've requested from me
There seems to be a problem {0}

Perhaps try the following:

{1}
""".format(crayons.red(loc), crayons.cyan(inst))
    return message
