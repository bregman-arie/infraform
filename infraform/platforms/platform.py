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
import fabric
import os
import patchwork.transfers
import re

import logging
from pathlib import Path
import shutil
import sys
from ansible.parsing.splitter import split_args, parse_kv
import crayons
import yaml

from infraform.executor import Executor
from infraform.scenario import Scenario
from infraform.exceptions import requirements as req_exc
from infraform.exceptions import usage as usage_exc
from infraform.exceptions.utils import success_or_exit

LOG = logging.getLogger(__name__)


class Platform(object):

    def __init__(self, args, installation=None, run_platform=None,
                 readiness_check=None, binary=None, name=None, rm=None):
        self.args = {k: v for k, v in vars(args).items() if v is not None}
        self.installation = installation
        self.run_platform = run_platform
        self.binary = binary
        self.name = name
        self.readiness_check = readiness_check

        # Array of commands to run in order to check the host is ready
        if "hosts" in self.args:
            self.readiness_check.append("rsync --version")
        # vars are used for feeding scenario template
        if 'vars' in self.args:
            self.vars = self.get_vars(self.args['vars'])
        # Create additional vars based on passed ones
        self.create_new_vars()
        # Create a workspace where all the files will be saved
        self.create_workspace_dir()

    def create_workspace_dir(self):
        """Create infraform workspace."""
        ifr_dir = str(Path.home()) + '/.infraform'
        if not os.path.exists(ifr_dir):
            os.mkdir(ifr_dir)

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

    def install_reqs(self):
        ans = input("Do you want me to try and fix that for you with the\
 commands above? [yY/nN]: ")
        if ans.lower() == "y":
            exe = Executor(commands=self.INSTALLATION,
                           hosts=self.args['hosts'])
            exe.run()
        else:
            LOG.info("Fine then, have a nice day :)")
            sys.exit(2)

    def check_host_readiness(self):
        """Validates the platform specified is ready for use."""
        exe = Executor(commands=self.readiness_check,
                       hosts=self.args['hosts'], warn_on_fail=True,
                       hide_output=True)
        results = exe.run()

        if not results or any(res.exited for res in results):
            LOG.error(req_exc.missing_reqs(
                self.installation, hosts=self.args['hosts'],
                failed_cmds=[res.command for res in results if
                             res.exited != 0]))
            self.install_reqs()

    def prepare_remote_host(self, host, s_dir):
        """Prepares remote environment."""
        c = fabric.Connection(host)
        self.execution_dir = "~/.infraform/{}".format(s_dir)
        LOG.debug(crayons.green(
            "Copying scenario from {} to remote host: {}".format(
                self.scenario.dir_path, host)))
        patchwork.transfers.rsync(c, self.scenario.dir_path,
                                  "~/.infraform")

    def prepare_local_host(self, target_dir):
        """Prepares local host environment."""
        # $HOME/.infraform
        infraform_dir = os.path.expanduser('~') + '/.infraform/'
        # $HOME/.infraform/elk
        self.execution_dir = infraform_dir + target_dir
        # Checks if a current directory exists and removes it in case it does
        if os.path.isdir(self.execution_dir):
            shutil.rmtree(self.execution_dir)
        # Copy scenario from infraform to $HOME/.infraform/elk/
        subprocess.call(['cp', '-r', os.path.dirname(self.scenario.file_path),
                         infraform_dir])
        _, suffix = os.path.splitext(self.scenario.file_name)
            # Load YAML based scenario and save in self.vars
        if suffix == ".yml" or suffix == ".yaml" or suffix == ".ifr":
            self.load_yaml_to_vars()

    def prepare(self):
        """Prepare environment for docker-compose execution."""
        # Check the host is available to run the chosen platform/tool
        if not self.args['skip_check'] and self.readiness_check:
            LOG.debug(crayons.blue("# Verifying the host is ready"))
            self.check_host_readiness()
        if 'scenario' in self.args:
            self.scenario = Scenario(name=self.args['scenario'],
                                     variables=self.vars)
            self.scenario.render()
            # Merge the content of the scenario with the variables
            # we got from the user
            self.vars.update(self.scenario.content)

        if "hosts" in self.args:
            LOG.debug(crayons.blue("# Preparing remote environment"))
            for host in self.args['hosts']:
                self.prepare_remote_host(host, self.scenario.dir_name)
        else:
            LOG.debug(crayons.blue("# Preparing local environment"))
            self.prepare_local_host(self.scenario.dir_name)
    
    def run(self):
        """Execute platform commands."""
        try:
            cmds = self.vars['execute'].split("\n")
        except KeyError:
            cmds = self.RUN
        hosts = []
        if "hosts" in self.args:
            hosts = self.args['hosts']
        LOG.info(crayons.blue("# Executing scenario"))
        exe = Executor(commands=cmds, hosts=hosts,
                       working_dir=self.execution_dir)
        results = exe.run()
        [success_or_exit(res.exited) for res in results]
        return results

    def rm(self):
        LOG.info("Removing")
        cmd = self.vars['remove']
        exe = Executor()
        res = exe.run(cmd, shell=True, cwd=self.execution_dir)
        success_or_exit(res.returncode)
        return res
