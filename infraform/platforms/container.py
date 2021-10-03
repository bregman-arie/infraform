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
import subprocess
import sys

from infraform.exceptions import usage
from infraform.platforms.platform import Platform
from infraform.exceptions.utils import success_or_exit

LOG = logging.getLogger(__name__)


class Container(Platform):

    def __init__(self, scenario, binary, package):
        self.binary = binary
        self.package = package
        self.installation = ["dnf install -y {0}\nsystemctl start {1}".format(
            self.package, self.binary)]

        super(Container, self).__init__(scenario)

    def verify_project_exists(self):
        if not os.path.isdir(self.scenario.vars['project']):
            success_or_exit(2, "Couldn't find project: {}".format(self.scenario.vars[
                'project']))

    def pre(self):
        if self.image_not_exists() or (self.scenario.vars.get('override_image')):
            LOG.warning("Building image: {}".format(self.scenario.vars['image']))
            dockerfile_path = self.write_dockerfile()
            self.build_image(dockerfile_path)
        if 'project' in self.scenario.vars:
            self.verify_project_exists()

    def run(self, host='localhost', cwd='/tmp'):
        """Run the container."""
        self.pre()
        try:
            cmd = "{0} run -v {1}:/{2}:z {3} \
/bin/bash -c 'cd {2}; {4}'".format(
                self.binary,
                self.scenario.vars['project'],
                self.scenario.vars['project_name'],
                self.scenario.vars['image'],
                self.scenario.vars['execute'])
        except KeyError as e:
            LOG.error(usage.missing_arg(e.args[0]))
            sys.exit(2)
        LOG.info("Running: {}".format(cmd))
        res = subprocess.run(cmd, shell=True)
        success_or_exit(res.returncode)
        return res

    def image_not_exists(self):
        """Returns true if image exists."""
        res = subprocess.run(
            "{} inspect {}".format(self.binary, self.scenario.vars['image']),
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        return res.returncode

    def get_template(self, name):
        """Returns jinja2 Dockerfile template."""
        with open(name, 'r+') as open_f:
            template_content = open_f.read()
        return template_content

    def write_dockerfile(self, df_path="Dockerfile"):
        with open(df_path, 'w+') as f:
            f.write(self.scenario.vars['dockerfile'])
        return df_path

    def destroy(self):
        """Removes the container from the system."""
        res = subprocess.run("{} rm {}".format(self.binary,
                                               self.args['name']))
        if res.returncode != 0:
            sys.exit(2)
        return res

    def build_image(self, df_path):
        """Builds image given df path."""
        cmd = "{} build -f {} -t {} .".format(
            self.binary, df_path, self.scenario.vars['image'])
        LOG.info("Running: {}".format(cmd))
        res = subprocess.run(cmd, shell=True)
        if res.returncode != 0:
            sys.exit(2)
        return res
