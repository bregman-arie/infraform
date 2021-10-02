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
from fabric import Connection
import crayons
import importlib
import jinja2 as j2
import logging
import os
import re
import sys
import shutil
import yaml

from infraform import filters
from infraform.utils.file import transfer
from infraform.exceptions import usage as usage_exc
from infraform.platforms.platform import Platform

LOG = logging.getLogger(__name__)


class Scenario(object):

    def __init__(self, path, platform_name=None, scenario_vars={}):
        self.path = path
        if platform_name:
            self.platform = create_platform(
                platform_name, scenario_vars)
        self.name = os.path.basename(
            self.path).split('.')[0]
        self.file_suffix = os.path.basename(
            self.path).split('.')[-1]
        self.scenario_vars = scenario_vars

    def get_scenario_template(self, name):
        """Returns jinja2 template."""
        with open(name, 'r+') as open_f:
            template_content = open_f.read()
        return template_content

    def render(self, dest):
        if self.file_suffix == "j2":
            LOG.info("{}: {}".format(
                crayons.yellow("rendering the scenario"),
                self.path))
            j2_env = j2.Environment(loader=j2.FunctionLoader(
                self.get_scenario_template), trim_blocks=True,
                undefined=j2.StrictUndefined)
            j2_env.filters['env_override'] = filters.env_override
            template = j2_env.get_template(self.path)
            try:
                rendered_scenario = template.render(vars=self.scenario_vars)
            except j2.exceptions.UndefinedError as e:
                LOG.error(e)
                missing_arg = re.findall(
                    r'no attribute (.*)', e.message)[0].strip("'")
                LOG.error(usage_exc.missing_arg(missing_arg))
                sys.exit(2)
            self.write_rendered_scenario(rendered_scenario, dest)

    def load_content(self, host='localhost'):
        """Returns Scenario content as a dictionary."""
        with Connection(host) as conn:
            with conn.sftp().open(self.path) as stream:
                try:
                    content_yaml = yaml.safe_load(stream)
                    for k, v in content_yaml.items():
                        if k == "platform":
                            self.platform = Platform.create_platform(
                                v, self.scenario_vars)
                        elif k not in self.scenario_vars:
                            if not hasattr(self, k):
                                setattr(self, k, v)
                except yaml.YAMLError as exc:
                    LOG.error(exc)

    def run(self, host, cwd='/tmp/'):
        LOG.info("{}: {}".format(crayons.yellow("running scenario"),
                                 self.name))
        self.platform.run(host=host, cwd=cwd)

    def write_rendered_scenario(self, scenario, dest):
        """Save the rendered scenario."""
        self.path = os.path.join(dest, self.name + '.ifr')
        with open(self.path, 'w+') as f:
            f.write(scenario)

    def copy(self, path, host='localhost'):
        # Copy the scenario to remote or local path
        transfer(host=host, source=self.path, dest=path)
        LOG.info("{} {} to {}".format(crayons.yellow("copied"),
        crayons.cyan(self.path), crayons.cyan(path)))
        if self.file_suffix == 'j2':
            self.path = os.path.join(path, self.name + '.ifr.j2')
        else:
            self.path = os.path.join(path, self.name + '.ifr')
        # Check if additional files specified in the scenario itself
        if hasattr(self, 'files'):
            for file in self.files:
                transfer(host=host, source=os.path.join(
                    os.path.dirname(self.path), file),
                         dest=path)
