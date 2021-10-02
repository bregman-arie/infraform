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
import importlib
import logging
import sys
from ansible.parsing.splitter import split_args, parse_kv
import crayons

from infraform.executor import Executor
from infraform.utils import process

LOG = logging.getLogger(__name__)


class Platform(object):

    def __init__(self, variables={}):
        self.vars = {}
        if variables:
            args_split = split_args(variables)
            for arg in args_split:
                self.vars.update(parse_kv(arg))

    def adjust_hosts(self):
        LOG.info("To fix, run the following:\n{}".format(
            crayons.green("\n".join(self.installation))))
        ans = input("Do you want me to try and fix that for you with the\
 commands above? [yY/nN]: ")
        if ans.lower() == "y":
            exe = Executor(
                commands=self.installation + ['sudo dnf install rsync -y'],
                hosts=self.args['hosts'])
            exe.run()
        else:
            LOG.info("Fine then, have a nice day :)")
            sys.exit(2)

    def pre(self, host, cwd):
        LOG.info("{}: {} on host {}".format(
            crayons.yellow("running command"),
            crayons.cyan('\n'.join(self.pre_commands)),
            crayons.cyan(host)))
        process.execute_cmd(commands=self.pre_commands, host=host, cwd=cwd)

    def run(self, host, cwd):
        """Execute platform commands."""
        self.pre(host=host, cwd=cwd)
        LOG.info("{}: {} on host {}".format(
            crayons.yellow("running command"),
            crayons.cyan('\n'.join(self.run_commands)),
            crayons.cyan(host)))
        LOG.info("----- Scenario Output START-----")
        process.execute_cmd(commands=self.run_commands, host=host, cwd=cwd)
        LOG.info("----- Scenario Output END-----")
        self.post()

    def post(self, host, cwd):
        pass

    @staticmethod
    def create_platform(platform, scenario_vars):
        """Returns platform instance based on the given platform argument."""
        Platform = getattr(importlib.import_module(
            "infraform.platforms.{}".format(platform)),
            platform.capitalize())
        LOG.info("{}: {}".format(crayons.green("platform"),
                                 platform))
        platform_instance = Platform(variables=scenario_vars)
        return platform_instance
