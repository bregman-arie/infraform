# Copyright 2020 Arie Bregman
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
from fabric import Connection
import invoke
import logging
import sys

LOG = logging.getLogger(__name__)


class Executor(object):

    def __init__(self, commands, hosts=[], working_dir=None,
                 warn_on_fail=False, hide_output=False):
        self.commands = commands
        self.hosts = hosts
        self.working_dir = working_dir
        self.results = []
        self.warn_on_fail = warn_on_fail
        self.hide_output = hide_output

    def run(self):
        if self.hosts:
            results = self.execute_on_remote_host()
        else:
            results = self.execute_on_local_host()
        return results

    def execute_on_remote_host(self):
        """Execute commands remotely."""
        for host in self.hosts:
            c = Connection(host)
            for cmd in self.commands:
                try:
                    if self.working_dir:
                        with c.cd(self.working_dir):
                            LOG.debug(crayons.green(
                                "Executing: {} in {}".format(
                                    cmd, self.working_dir)))
                            res = c.run(cmd, warn=self.warn_on_fail,
                                        hide=self.hide_output)
                    else:
                        LOG.debug(crayons.red("Executing: {}".format(cmd)))
                        res = c.run(cmd, warn=self.warn_on_fail,
                                    hide=self.hide_output)
                    self.results.append(res)
                except invoke.exceptions.UnexpectedExit:
                    LOG.error("Failed to execute: {}. Exiting now...".format(
                        cmd))
                    sys.exit(2)
        return self.results

    def execute_on_local_host():
        """Execute given commands on local host."""
        pass

    def execute_cmd(commands, hosts=None, warn_on_fail=False, cwd=None,
                    hide_output=False):
        """Execute given commands on remote hosts or locally."""
        if hosts:
            res = execute_on_remote_host(commands, hosts, warn_on_fail, cwd,
                                         hide_output=hide_output)
        else:
            res = execute_on_local_host(commands, warn_on_fail, cwd,
                                        hide_output=hide_output)
        return res
