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
import re

from difflib import SequenceMatcher
import logging
from pathlib import Path
import sys
from ansible.parsing.splitter import split_args, parse_kv
import crayons
import jinja2 as j2
import yaml

from infraform.executor import Executor
from infraform.executor import Executor
from infraform import filters
from infraform.exceptions import requirements as req_exc
from infraform.exceptions import usage as usage_exc
from infraform.exceptions.utils import success_or_exit

LOG = logging.getLogger(__name__)


class Platform(object):

    SCENARIOS_PATH = os.path.dirname(__file__) + '/../scenarios'
    READINESS_CHECK = []

    def __init__(self, args, installation=None, run=None,
                 readiness_check=None, binary=None, name=None, rm=None):
        # Set arguments provided by the user
        self.args = {k: v for k, v in vars(args).items() if v is not None}
        
        self.installation = installation
        self.run = run
        self.binary = binary
        self.name = name
        self.readiness_check = readiness_check
        # Array of commands to run in order to check the host is ready
        if "hosts" in self.args:
            self.READINESS_CHECK.append("rsync --version")
        # vars are used for feeding scenario templates (jinja2)
        if 'vars' in self.args:
            self.vars = self.get_vars(self.args['vars'])
        if not self.args['skip_check'] and hasattr(self, 'READINESS_CHECK'):
            self.check_platform_avaiable()
        # If user specified scenario, make sure it exists
        if 'scenario' in self.args:
            self.set_scenario_path_dir()
            self.render_scenario()
            _, suffix = os.path.splitext(self.scenario_f)
            # Load YAML based scenario and save in self.vars
            if suffix == ".yml" or suffix == ".yaml" or suffix == ".ifr":
                self.load_yaml_to_vars()
        # Create additional vars based on passed ones
        self.create_new_vars()
        # Create a workspace where all the files will be saved
        self.create_workspace_dir()

    def set_scenario_path_dir(self):
        self.scenario_fpath, self.scenario_f = self.verify_scenario_exists(
            self.SCENARIOS_PATH, self.args['scenario'])
        self.scenario_dir_path = os.path.dirname(self.scenario_fpath)
        self.scenario_dir_name = self.scenario_dir_path.split('/')[-1]
        print("==== {}".format(self.scenario_dir_name))

    def create_workspace_dir(self):
        """Create infraform workspace."""
        ifr_dir = str(Path.home()) + '/.infraform'
        if not os.path.exists(ifr_dir):
            os.mkdir(ifr_dir)

    def load_yaml_to_vars(self):
        """Load any scenario YAML directives to variables."""
        with open(self.scenario_f, 'r') as stream:
            try:
                scenario_yaml = yaml.safe_load(stream)
                try:
                    self.vars['scenario_vars'] = {
                        k: v for k, v
                        in scenario_yaml.items() if v is not None}
                except AttributeError:
                    LOG.error(crayons.cyan("I'm sorry, but it \
looks like the scenario {} is empty".format(self.scenario_f)))
                    sys.exit(2)
                for k, v in scenario_yaml.items():
                    if k not in self.vars:
                        self.vars.update({k: v})
            except yaml.YAMLError as exc:
                LOG.error(exc)

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

    def check_platform_avaiable(self):
        """Validates the platform specified is ready for use."""
        exe = Executor(commands=self.READINESS_CHECK,
                       hosts=self.args['hosts'], warn_on_fail=True,
                       hide_output=True)
        results = exe.run()
        if not results or any(res.exited for res in results):
            LOG.error(req_exc.missing_reqs(
                self.installation,
                hosts=self.args['hosts'],
                failed_cmds=[res.command for res in results if
                             res.exited != 0]))
            self.install_reqs()

    @staticmethod
    def verify_scenario_exists(scenarios_dir, scenario):
        """Verifies scenario exists."""
        similar = []
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
                elif SequenceMatcher(None, file_without_suffix,
                                     scenario).ratio() >= 0.25 and ".ifr" in f:
                    similar.append(file_without_suffix)
        if similar:
            LOG.info("Perhaps you meant:\n\n{}".format(
                crayons.yellow("\n".join(similar))))
        success_or_exit(1, usage_exc.missing_scenario(scenario))

    def get_template(self, name):
        """Returns jinja2 template."""
        with open(name, 'r+') as open_f:
            template_content = open_f.read()
        return template_content

    def write_rendered_scenario(self, scenario):
        """Save the rendered scenario."""
        with open('./' + self.scenario_f, 'w+') as f:
            f.write(scenario)

    def render_scenario(self):
        """Render a scenario and save to disk."""
        j2_env = j2.Environment(loader=j2.FunctionLoader(
            self.get_template), trim_blocks=True, undefined=j2.StrictUndefined)
        j2_env.filters['env_override'] = filters.env_override
        template = j2_env.get_template(self.scenario_fpath)
        try:
            rendered_scenario = template.render(vars=self.vars)
        except j2.exceptions.UndefinedError as e:
            LOG.error(e)
            missing_arg = re.findall(
                r'no attribute (.*)', e.message)[0].strip("'")
            LOG.error(usage_exc.missing_arg(missing_arg))
            sys.exit(2)
        self.write_rendered_scenario(rendered_scenario)

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
        # For example .../scenarios/docker-compose/elk -> elk
        self.target_dir = os.path.dirname(self.scenario_fpath).split('/')[-1]

        if "hosts" in self.args:
            LOG.debug(crayons.blue("# Preparing remote environment"))
            for host in self.args['hosts']:
                self.prepare_remote_host(host, target_dir)
        else:
            LOG.debug(crayons.blue("# Preparing local environment"))
            self.prepare_local_host(target_dir)
    
    def run(self):
        """Execute platform commands."""
        try:
            cmds = self.vars['execute'].split("\n")
        except KeyError:
            cmds = self.RUN
        hosts = []
        if "hosts" in self.args:
            hosts = self.args['hosts']
        exe = Executor(commands=cmds, hosts=hosts, working_dir=self.execution_dir)
        results = exe.run()
        [success_or_exit(res.exited) for res in results]
        return results

    def rm(self):
        LOG.info("Removing")
        cmd = self.vars['remove']
        res = subprocess.run(cmd, shell=True, cwd=self.execution_dir)
        success_or_exit(res.returncode)
        return res
