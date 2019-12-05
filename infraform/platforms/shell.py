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
import logging

from infraform.platforms.platform import Platform

LOG = logging.getLogger(__name__)


class Shell(Platform):

    PACKAGE = 'bash'
    BINARY = 'bash'

    def __init__(self, args):
        self.binary = self.BINARY
        self.package = self.PACKAGE
        self.installation = "yum install bash"
        super(Shell, self).__init__(args)

    def prepare(self):
        self.render_scenario()

    def run(self):
        if 'host' in self.vars:
            self.execute_script_remotely()
        else:
            self.execute_cmd("chmod +x {0}; ./{0}".format(self.scenario_f))
