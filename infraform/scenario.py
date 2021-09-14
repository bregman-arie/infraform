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
import crayons
import logging
import os

LOG = logging.getLogger(__name__)


class Scenario(object):

    def __init__(self, scenario_path):
        self.scenario_path = scenario_path
        self.scenario_name = os.path.basename(self.scenario_path).split('.')[0]
        self.scenario_suffix = os.path.basename(self.scenario_path).split('.')[-1]

    def validate(self):
        pass

    def render(self):
        LOG.info("{}: {}".format(crayons.yellow("Rendering the scenario"), self.scenario_name))

    def prepare(self):
        # Check if scenario is templated and has to be rendered
        if self.scenario_suffix == ".j2":
            self.render()

    def run(self):
        LOG.info("{}: {}".format(crayons.yellow("Running scenario"), self.scenario_name))
