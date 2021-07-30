# Copyright 2021 Arie Bregman
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

LOG = logging.getLogger(__name__)


class Orchestrator(object):

    def __init__(self, platform_name=None, scenario=None, commands=None, vars=None,
                 skip_check=False, hosts=[]):
        self.platform_name = platform_name
        self.scenario = scenario
        self.commands = commands

    def prepare(self):
        self.validate_input()
        self.prepare_workspace()

    def run(self):
        if not self.platform_name:
            self.platform = get_platform()
        self.platform.prepare()
        self.platform.run()

    def validate_input(self):
        if not self.scenario and not self.commands:
            pass
