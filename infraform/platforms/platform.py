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

from infraform.exceptions import requirements as req_exc
from infraform.exceptions import usage as usage_exc

LOG = logging.getLogger(__name__)


class Platform(object):

    SCENARIOS_PATH = os.path.dirname(__file__) + '/../scenarios'

    def __init__(self, args, required_args=[]):
        self.args = {k: v for k, v in vars(args).items() if v is not None}
        # vars are used for feeding scenario templates (jinja2)
        self.vars = self.get_vars(self.args['vars'])
        self.validate_required_args(required_args)
        self.check_platform_avaiable()

        # If user specific scenario, make sure it exists
        if 'scenario' in self.args:
            self.verify_scenario_exists()

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
        self.success_or_exit(res.returncode, req_exc.service_down(self.installation))

    @staticmethod
    def success_or_exit(rc, message=None):
        if rc != 0:
            LOG.error(message)
            sys.exit(2)

    def validate_required_args(self, required_args):
        """Validates all required args were passed by the user."""
        for req in required_args:
            if req not in self.args:
                self.success_or_exit(1, usage_exc.missing_arg(req))

    def verify_scenario_exists(self):
        """Verifies scenario exists."""
        for p, d, files in os.walk(self.SCENARIOS_PATH):
            for f in files:
                if os.path.splitext(f)[0] == self.args['scenario']:
                    self.scenario_path = p
                    self.scenario_name = os.path.splitext(f)[0]
                    self.scenario_file_path = p + '/' + f
                    self.scenario_file = f
                    return
        self.success_or_exit(1, usage_exc.missing_scenario(
            self.args['scenario']))

    @staticmethod
    def execute_cmd(cmd, cwd=None):
        subprocess.run(cmd, shell=True, cwd=cwd)

    def get_template(self, name):
        """Returns jinja2 template."""
        with open(name, 'r+') as open_f:
            template_content = open_f.read()
        return template_content

    def write_rendered_scenario(self, scenario):
        with open(self.scenario_file, 'w+') as f:
            f.write(scenario)

    def render_scenario(self):
        j2_env = j2.Environment(loader=j2.FunctionLoader(
            self.get_template), trim_blocks=True, undefined=j2.StrictUndefined)
        template = j2_env.get_template(self.scenario_file_path)
        try:
            rendered_scenario = template.render(vars=self.vars)
        except j2.exceptions.UndefinedError as e:
            missing_arg = re.findall(r'(.*) is undefined', e.message)[0].strip("'")
            LOG.error(usage_exc.missing_arg(missing_arg))
            sys.exit(2)
        self.write_rendered_scenario(rendered_scenario)
