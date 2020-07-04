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
import logging
import os
import shutil
import subprocess

from infraform.platforms.platform import Platform
from infraform.exceptions.utils import success_or_exit
from infraform import process

LOG = logging.getLogger(__name__)


class Docker_compose(Platform):

    PACKAGE = 'docker'
    BINARY = '/usr/local/bin/docker-compose'
    INSTALLATION = ["curl -L $(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep browser_download_url | cut -d '\"' -f 4 | grep Linux | grep x86_64$) -o docker-compose", "sudo mv docker-compose /usr/local/bin && sudo chmod +x /usr/local/bin/docker-compose"]

    def __init__(self, args):
        self.binary = self.BINARY
        self.package = self.PACKAGE
        self.installation = self.INSTALLATION

        super(Docker_compose, self).__init__(args)

    def prepare(self):
        """Prepare environment for docker-compose execution."""
        # .../scenarios/docker-compose/elk -> elk
        new_dir = os.path.dirname(self.scenario_fpath).split('/')[-1]
        # $HOME/.infraform
        infraform_dir = os.path.expanduser('~') + '/.infraform/'
        self.execution_dir = infraform_dir + new_dir
        if os.path.isdir(self.execution_dir):
            shutil.rmtree(self.execution_dir)
        subprocess.call(['cp', '-r', os.path.dirname(self.scenario_fpath),
                         infraform_dir])

    def run(self):
        """Execution docker-compose."""
        try:
            cmd = self.vars['execute']
        except KeyError:
            cmd = "docker-compose up -d"
        if "hosts" in self.args:
            process.execute_cmd([cmd], self.args['hosts'])
            res = "x"
        else:
            res = subprocess.run(cmd, shell=True, cwd=self.execution_dir)
        success_or_exit(res.returncode)
        return res

    def rm(self):
        LOG.info("Removing")
        cmd = self.vars['remove']
        res = subprocess.run(cmd, shell=True, cwd=self.execution_dir)
        success_or_exit(res.returncode)
        return res
