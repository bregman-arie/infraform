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
import crayons
import fabric
import logging
import os
import patchwork.transfers
import shutil
import subprocess

from infraform.platforms.platform import Platform
from infraform.exceptions.utils import success_or_exit
from infraform import process

LOG = logging.getLogger(__name__)


class Docker_compose(Platform):

    PACKAGE = 'docker'
    BINARY = '/usr/local/bin/docker-compose'
    READINESS_CHECK = ["docker-compose --version", "systemctl status docker"]
    INSTALLATION = ["curl -L $(curl -s https://api.github.com/repos/docker/c\
ompose/releases/latest | grep browser_download_url | cut -d '\"' -f 4 | grep L\
inux | grep x86_64$) -o docker-compose", "sudo mv docker-compose /usr/local/bin\
&& sudo chmod +x /usr/local/bin/docker-compose",
                    "sudo dnf config-manager --add-repo=https://download.dock\
er.com/linux/centos/docker-ce.repo",
                    "sudo dnf install --nobest -y docker-ce",
                    "sudo systemctl start docker"]
    RUN = ["docker-compose up -d"]

    def __init__(self, args):
        self.binary = self.BINARY
        self.package = self.PACKAGE
        self.installation = self.INSTALLATION

        super(Docker_compose, self).__init__(args)

    def prepare_remote_host(self, host, s_dir):
        """Prepares remote environment."""
        c = fabric.Connection(host)
        self.execution_dir = "~/.infraform/{}".format(s_dir)
        LOG.debug(crayons.red(
            "Copying scenario from {} to remote host: {}".format(
                self.scenario_dir_path, host)))
        patchwork.transfers.rsync(c, self.scenario_dir_path,
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
        subprocess.call(['cp', '-r', os.path.dirname(self.scenario_fpath),
                         infraform_dir])

    def prepare(self):
        """Prepare environment for docker-compose execution."""
        # .../scenarios/docker-compose/elk -> elk
        target_dir = os.path.dirname(self.scenario_fpath).split('/')[-1]
        if "hosts" in self.args:
            LOG.debug(crayons.red("Preparing remote environment"))
            for host in self.args['hosts']:
                self.prepare_remote_host(host, target_dir)
        else:
            LOG.debug(crayons.red("Preparing local environment"))
            self.prepare_local_host(target_dir)

    def run(self):
        """Execution docker-compose."""
        try:
            cmds = self.vars['execute']
        except KeyError:
            cmds = self.RUN
        if "hosts" in self.args:
            results = process.execute_cmd(
                commands=cmds, hosts=self.args['hosts'],
                cwd=self.execution_dir)
        else:
            results = process.execute_cmd(commands=cmds,
                                          cwd=self.execution_dir)
        [success_or_exit(res.exited) for res in results]
        return results

    def rm(self):
        LOG.info("Removing")
        cmd = self.vars['remove']
        res = subprocess.run(cmd, shell=True, cwd=self.execution_dir)
        success_or_exit(res.returncode)
        return res
