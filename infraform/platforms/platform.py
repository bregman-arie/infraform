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
import os

import logging
import sys
from ansible.parsing.splitter import split_args, parse_kv
import crayons

from infraform.executor import Executor
from infraform.scenario import Scenario
from infraform.exceptions.utils import success_or_exit

LOG = logging.getLogger(__name__)


class Platform(object):

    WORKSPACE = "~/.infraform/"

    def __init__(self, args, installation=None, run_platform=None,
                 readiness_check=[], binary=None, platform_name=None, rm=None):
        self.args = {k: v for k, v in vars(args).items() if v is not None}
        self.installation = installation
        self.run_platform = run_platform
        self.binary = binary
        self.platform_name = platform_name
        self.readiness_check = readiness_check
        self.rm = rm

        # Array of commands to run in order to check the host is ready
        if "hosts" in self.args:
            self.readiness_check.append("rsync --version")
        # vars are used for feeding scenario template
        if 'vars' in self.args:
            self.vars = self.get_vars(self.args['vars'])
        # Create additional vars based on passed ones
        self.create_new_vars()

    def create_workspace_dir(self):
        """Create infraform workspace.

        If the scenario is a file (e.g. scenario.yml) then the file is
        copied to the workspace.
        If the scenario is a directory (e.g. scenario/scenario.ifr that
        includes other files as well then the whole directory is copied
        to the workspace.
        """

        if self.scenario.dir_name == self.scenario.name:
            self.scenario_dir = os.path.join(self.WORKSPACE,
                                             self.scenario.dir_name)
            Executor(commands=["mkdir -p {}".format(self.scenario_dir)]).run()
        else:
            self.scenario_dir = self.WORKSPACE

    def create_new_vars(self):
        """Create additional variables out of existing variables."""
        if 'project' in self.vars:
            if '/' in self.vars['project']:
                self.vars['project_name'] = os.path.basename(
                    self.vars['project'])
            else:
                self.vars['project_name'] = self.vars['project']

    def get_vars(self, args):
        """Updates variables based on given arguments from CLI."""
        variables = {}
        args_split = split_args(args)
        for arg in args_split:
            variables.update(parse_kv(arg))
        return variables

    def fix_host(self):
        LOG.info("To fix, run the following:\n{}".format(
            crayons.green("\n".join(self.installation))))
        ans = input("Do you want me to try and fix that for you with the\
 commands above? [yY/nN]: ")
        if ans.lower() == "y":
            exe = Executor(
                commands=self.installation + ['sudo dnf install rsync -y'],
                hosts=self.args['hosts'])
            exe.run()
        else:
            LOG.info("Fine then, have a nice day :)")
            sys.exit(2)

    def check_host_readiness(self):
        """Validates the platform specified is ready for use."""
        exe = Executor(commands=self.readiness_check,
                       hosts=self.args['hosts'], warn_on_fail=True,
                       hide_output=True, keep_files=self.args['keep_files'])
        result = exe.run()

        if result.return_code != 0:
            LOG.info(result)
            LOG.info(crayons.red("\u274c The host is not ready"))
            self.fix_host()
        else:
            LOG.info(crayons.green("\u2714 The host is ready"))

    def prepare(self):
        """Prepare environment for docker-compose execution."""
        # Check the host is available to run the chosen platform/tool
        if not self.args['skip_check'] and self.readiness_check:
            LOG.debug(crayons.blue("\n==== Verifying the host is ready ===="))
            self.check_host_readiness()
        # Create a workspace where all the files will be saved
        self.scenario = Scenario(name=self.args['scenario'],
                                 variables=self.vars)
        LOG.debug(crayons.blue("\n==== Create workspace ===="))
        self.create_workspace_dir()
        self.scenario.render(target_dir=self.scenario_dir)
        # Merge the content of the scenario with the variables
        # we got from the user
        self.vars.update(self.scenario.content)

        if "hosts" in self.args:
            LOG.debug(crayons.blue("\n==== Preparing remote environment ===="))
            for host in self.args['hosts']:
                Executor.transfer(
                    hosts=self.args['hosts'], source=self.WORKSPACE,
                    dest=self.WORKSPACE)

        else:
            LOG.debug(crayons.blue("# Preparing local environment"))
            Executor.transfer(
                hosts=self.args['hosts'], source=self.scenario.source,
                dest=self.WORKSPACE, local=True)

    def run(self):
        """Execute platform commands."""
        self.prepare()
        try:
            cmds = self.vars['execute'].split("\n")
        except KeyError:
            cmds = self.RUN
        hosts = []
        if "hosts" in self.args:
            hosts = self.args['hosts']
        LOG.info(crayons.blue("\n===== Executing scenario ====="))
        exe = Executor(commands=cmds, hosts=hosts,
                       working_dir=self.scenario_dir)
        result = exe.run()
        LOG.info(crayons.blue("===== Done Executing scenario ====="))
        success_or_exit(result.exited)
        return result

    def remove(self):
        LOG.info("Removing")
        try:
            cmds = self.vars['remove'].split("\n")
        except KeyError:
            cmds = self.rm
        hosts = []
        if "hosts" in self.args:
            hosts = self.args['hosts']
        exe = Executor(commands=cmds, hosts=hosts,
                       working_dir=self.scenario_dir)
        result = exe.run()
        success_or_exit(result.exited)
        return result
