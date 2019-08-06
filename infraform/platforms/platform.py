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


class Platform(object):

    def __init__(self, args):
        self.args = args
        self.image = "{}-{}-{}".format(self.args.project,
                                       self.args.tester,
                                       self.args.release)

    def raise_service_down(self):
        """Notify user that service is down or package is not installed."""
        message = """
It looks like service is down or package is not installed.

To fix it, run the following commands:

    $ {0}
    $ {1}
""".format(crayons.red("sudo dnf install %s" % self.PACKAGE),
           crayons.red("sudo systemctl install %s" % self.PACKAGE),)
        return message
