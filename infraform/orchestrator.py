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
import os
from ansible.parsing.splitter import split_args, parse_kv
import sys

from infraform.utils import process
from infraform.utils import file as file_utils
from infraform.host import Host
from infraform.platforms.platform import Platform
from infraform.scenario import Scenario
from infraform.exceptions import usage as usage_exc
from infraform.workspace import Workspace

LOG = logging.getLogger(__name__)


class Orchestrator(object):

    def __init__(self, platform_name=None, scenario=[],
                 commands=None, scenario_vars={},
                 skip_check=False, hosts=[], scenarios_dir=None):
        self.platform_name = platform_name
        self.scenario_name = scenario[0]
        self.commands = commands
        self.scenarios_dir = scenarios_dir
        self.scenario_vars = self.parse_vars(scenario_vars)
        self.hosts_names = hosts
        self.hosts = []
        self.skip_check = skip_check

    def parse_vars(self, scenario_vars):
        variables = {}
        if scenario_vars:
            vars_split = split_args(scenario_vars)
            for var in vars_split:
                variables.update(parse_kv(var))
        return variables

    def prepare(self):
        # Get scenario file path and create a Scenario instance
        scenario_fpath = self.get_scenario_file_path()
        self.scenario = Scenario(path=scenario_fpath,
                                 scenario_vars=self.scenario_vars)

        # Create and arrange local workspace
        workspace = Workspace(root_dir_path=os.path.join(
            os.getcwd(), '.infraform'), subdir=self.scenario.name)
        self.scenario.workspace = workspace
        self.scenario.copy(path=workspace.path)
        self.scenario.render(dest=workspace.path)
        self.scenario.load_content()
        self.scenario.copy_data(path=workspace.path)

        # Create a platform instance
        self.platform = Platform.create_platform(
            platform_name=self.scenario.platform, scenario=self.scenario)

        # Create a list of hosts instances
        for host in self.hosts_names:
            host_instance = Host(address=host,
                                 workspace_dir=self.scenario.name,
                                 platform_name=self.platform_name)
            self.scenario.copy(host=host_instance.address,
                               path=host_instance.workspace.path)
            if not self.skip_check:
                host_instance.check_host_platform_readiness(
                    self.platform)
            self.hosts.append(host_instance)

    def run(self):
        for host in self.hosts:
            self.platform.run(host=host.address, cwd=host.workspace.path)
        else:
            LOG.info("Finished executing the scenarios on all hosts")

    def get_scenario_file_path(self):
        # Check a scenario was provided
        if not self.scenario_name:
            raise usage_exc.RunUsageError
        # Validate it actually exists
        else:
            scenario_fpath = file_utils.get_file_path(
                self.scenarios_dir, self.scenario_name, exact_match=False)
            if not scenario_fpath:
                raise usage_exc.ScenarioNotFoundError(scenario_fpath)
            else:
                LOG.info("{}: {}".format(crayons.green("scenario"),
                                         scenario_fpath))
                return scenario_fpath
