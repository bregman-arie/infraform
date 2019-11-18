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
from ansible.parsing.splitter import split_args, parse_kv
import jinja2 as j2
import logging
import os
import re
import subprocess
import sys
import yaml

from infraform import filters
from infraform.exceptions import requirements as req_exc
from infraform.exceptions import usage as usage_exc
from infraform.exceptions.utils import success_or_exit

LOG = logging.getLogger(__name__)


class Platform(object):

    SCENARIOS_PATH = os.path.dirname(__file__) + '/../scenarios'

    def __init__(self, args):
        self.args = {k: v for k, v in vars(args).items() if v is not None}
        # vars are used for feeding scenario templates (jinja2)
        if 'vars' in self.args:
            self.vars = self.get_vars(self.args['vars'])
        self.check_platform_avaiable()

        # If user specified scenario, make sure it exists
        if 'scenario' in self.args:
            self.scenario_fpath, self.scenario_f = self.verify_scenario_exists(
                self.SCENARIOS_PATH, self.args['scenario'])
             
            self.render_scenario()

            _, suffix = os.path.splitext(self.scenario_f)
            os.path.splitext('/path/to/somefile.ext')
            if suffix == ".yml" or suffix == ".yaml":
                self.load_yaml_to_vars()

        self.create_new_vars()

    def load_yaml_to_vars(self):
        with open(self.scenario_f, 'r') as stream:
            try:
                scenario_yaml = yaml.safe_load(stream)
                self.vars['scenario_vars'] = {k: v for k, v in scenario_yaml.items() if v is not None}
                for k, v in scenario_yaml.items():
                    if k not in self.vars:
                        self.vars.update({k: v})
            except yaml.YAMLError as exc:
                print(exc)

    def create_new_vars(self):
        if self.vars['project'].startswith('/'):
            self.vars['project_name'] = os.path.basename(self.vars['project'])
        else:
           self.vars['project_name'] = self.vars['project']

    def get_vars(self, args):
        variables = {}
        args_split = split_args(args)
        for arg in args_split:
            variables.update(parse_kv(arg))
        return variables

    def check_platform_avaiable(self):
        """Validates the platform specified is ready for use."""
        res = subprocess.run("{} --version".format(self.binary), shell=True,
                             stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        success_or_exit(res.returncode, req_exc.service_down(self.installation))

    @staticmethod
    def verify_scenario_exists(scenarios_dir, scenario):
        """Verifies scenario exists."""
        for p, d, files in os.walk(scenarios_dir):
            for f in files:
                until_dot_pattern = re.compile(r"^[^.]*")
                file_without_suffix = re.search(until_dot_pattern, f).group(0)
                file_name = f
                if f.endswith('.j2'):
                    file_name = f[:-3]
                if file_without_suffix == scenario:
                    scenario_file_path = p + '/' + f
                    scenario_file = file_name
                    return scenario_file_path, scenario_file
        success_or_exit(1, usage_exc.missing_scenario(scenario))

    @staticmethod
    def execute_cmd(cmd, cwd=None):
        subprocess.run(cmd, shell=True, cwd=cwd)

    def get_template(self, name):
        """Returns jinja2 template."""
        with open(name, 'r+') as open_f:
            template_content = open_f.read()
        return template_content

    def write_rendered_scenario(self, scenario):
        with open(self.scenario_f, 'w+') as f:
            f.write(scenario)

    def render_scenario(self):
        j2_env = j2.Environment(loader=j2.FunctionLoader(
            self.get_template), trim_blocks=True, undefined=j2.StrictUndefined)
        j2_env.filters['env_override'] = filters.env_override
        template = j2_env.get_template(self.scenario_fpath)
        try:
            rendered_scenario = template.render(vars=self.vars)
        except j2.exceptions.UndefinedError as e:
            missing_arg = re.findall(r'no attribute (.*)', e.message)[0].strip("'")
            LOG.error(usage_exc.missing_arg(missing_arg))
            sys.exit(2)
        self.write_rendered_scenario(rendered_scenario)
