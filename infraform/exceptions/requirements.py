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


def service_down(package):
        """Notify user that service is down or the package is not installed."""
        message = """
It looks like the service is down or the package is not installed.

To fix it, try running the following commands:

    $ {0}
    $ {1}
""".format(crayons.red("sudo dnf install %s" % package),
           crayons.red("sudo systemctl install %s" % package),)
        return message
