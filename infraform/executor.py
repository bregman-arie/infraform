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
import os
from pathlib import Path
import patchwork.transfers
import sys
import uuid

from infraform.context import suppress_output

LOG = logging.getLogger(__name__)


class Executor(object):

    def __init__(self, commands=None, hosts=[], working_dir="/tmp",
                 warn_on_fail=False, hide_output=False):
        self.commands = commands
        self.hosts = hosts
        self.working_dir = working_dir
        self.results = []
        self.warn_on_fail = warn_on_fail
        self.hide_output = hide_output

    @staticmethod
    def transfer(hosts, source, dest):
        for host in hosts:
            with suppress_output():
                c = Connection(host)
                patchwork.transfers.rsync(c, source, dest)
                c.run("chmod +x {}".format(dest, hide=True, warn=True))
            LOG.debug(crayons.green("Transferred {} to {}:{}".format(
                source, host, dest)))

    def write_script(self):
        self.script_name = "infraform-" + str(uuid.uuid4()) + ".sh"
        self.script_path = os.path.join(self.working_dir, self.script_name)
        with open(Path(self.script_path).expanduser(), 'w+') as f:
            f.write("\n".join(self.commands))
            LOG.debug(crayons.green("Created: {}".format(self.script_path)))
        c = Connection("127.0.0.1")
        c.run("chmod +x {}".format(self.script_path, hide=True, warn=True))
        return self.script_path

    def run(self):
        self.script = self.write_script()
        if self.hosts:
            self.transfer(hosts=self.hosts, source=self.script,
                          dest=self.script)
            result = self.execute_on_remote_host()
        else:
            result = self.execute_on_local_host()
        self.cleanup()
        return result
       

    def execute_on_remote_host(self):
        """Execute on remote host(s)."""
        for host in self.hosts:
            c = Connection(host)
            try:
                with c.cd(self.working_dir):
                    LOG.debug("Executing on {}:{}\n-----\n{}\n-----".format(
                        crayons.blue(host), crayons.blue(self.working_dir),
                        crayons.green("\n".join(self.commands))))
                    self.result = c.run(self.script, warn=self.warn_on_fail,
                                         hide=self.hide_output)
            except invoke.exceptions.UnexpectedExit:
                LOG.error("Failed to execute: {}. Exiting now...".format(
                    self.commands))
                sys.exit(2)
        return self.result

    def execute_on_local_host(self):
        """Execute given commands on local host."""
        c = Connection("127.0.0.1")
        with c.cd(self.working_dir):
            c.local(self.script)

    def cleanup(self):
        if self.hosts:
            for host in self.hosts:
                c = Connection(host)
                c.run("rm {}".format(self.script))
        c = Connection('127.0.0.1')
        c.run("rm {}".format(self.script))
