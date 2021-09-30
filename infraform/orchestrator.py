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
import sys

from infraform.utils import process
from infraform.utils import file as file_utils
from infraform.scenario import Scenario
from infraform.exceptions import usage as usage_exc
from infraform.workspace import Workspace

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
        self.hosts = hosts

    def prepare(self):
        self.validate_input()
        self.prepare_workspace()
        scenario = Scenario(self.scenario_path, self.workspace,
                            scenario_vars=self.scenario_vars)
        scenario.validate()
        scenario.prepare()
        self.platform = self.create_platform(scenario.platform)
        self.platform.prepare(hosts=self.hosts)

        self.check_host_readiness()

    def check_host_readiness(self):
        print(crayons.yellow("verifying host readiness..."), end="")
        for host in self.hosts:
            results = process.execute_cmd(
                commands=self.platform.readiness_check,
                hosts=self.hosts, hide_output=True, warn_on_fail=True)
            for res in results:
                if res.return_code != 0:
                    print(crayons.red(("FAILED")))
                    sys.exit(2)
        print(crayons.green("PASSED"))

    def run(self):
        LOG.info("{}: {}".format(crayons.yellow("running scenario"),
                                 self.scenario_name))
        self.platform.run(hosts=self.hosts)
        LOG.info("{}: {}".format(crayons.green(
            "Finished executing the scenario"), self.scenario_name))

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
        LOG.info("{}: {}".format(crayons.green("scenario"),
                                 self.scenario_path))

    def create_platform(self, platform):
        """Returns platform instance based on the given platform argument."""
        Platform = getattr(importlib.import_module(
            "infraform.platforms.{}".format(platform)),
            platform.capitalize())
        LOG.info("{}: {}".format(crayons.green("platform"),
                                 platform))
        platform_instance = Platform()
        return platform_instance
