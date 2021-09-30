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
import importlib
import logging

from infraform.workspace import Workspace
from infraform.exceptions import usage as usage_exc
from infraform.utils import file as file_utils
from infraform.scenario import Scenario

LOG = logging.getLogger(__name__)


class Orchestrator(object):

    def __init__(self, platform_name=None, scenario=[],
                 commands=None, scenario_vars=None,
                 skip_check=False, hosts=[], scenarios_dir=None):
        self.platform_name = platform_name
        self.scenario_name = scenario[0]
        self.commands = commands
        self.scenarios_dir = scenarios_dir
        self.scenario_vars = scenario_vars

    def prepare(self):
        self.validate_input()
        self.prepare_workspace()
        scenario = Scenario(self.scenario_path, self.workspace,
                            scenario_vars=self.scenario_vars)
        scenario.validate()
        scenario.prepare()
        self.platform = self.create_platform(scenario.platform)
        self.platform.prepare()

    def run(self):
        self.platform.run()

    def prepare_workspace(self):
        self.workspace = Workspace(subdir=self.scenario_name)

    def validate_input(self):
        # Check a scenario was provided
        if not self.scenario_name:
            raise usage_exc.RunUsageError
        # Validate it actually exists
        else:
            self.scenario_path = file_utils.get_file_path(
                self.scenarios_dir, self.scenario_name, exact_match=False)
            if not self.scenario_path:
                raise usage_exc.ScenarioNotFoundError(self.scenario_name)
        LOG.info("{}: {}".format(crayons.green("Found scenario"),
                                 self.scenario_path))

    def create_platform(self, platform):
        """Returns platform instance based on the given platform argument."""
        Platform = getattr(importlib.import_module(
            "infraform.platforms.{}".format(platform)),
            platform.capitalize())
        LOG.info("{}: {}".format(crayons.green("Using the platform"),
                                 platform))
        platform_instance = Platform()
        return platform_instance
