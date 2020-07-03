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


def service_down(inst, host):
    """Notify user that service is down or the package is not installed."""
    if host:
        loc = "on the host {}".format(host)
    else:
        loc = "on this host"
    message = """
It looks like the service is down or the package is not installed {0}

To fix it, try the following:

{1}
""".format(crayons.red(loc), crayons.red(inst))
    return message
