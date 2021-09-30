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
import logging
import sys
# from ansible.parsing.splitter import split_args, parse_kv
import crayons

from infraform.executor import Executor
from infraform.utils import process

LOG = logging.getLogger(__name__)


class Platform(object):

    def __init__(self, args=None):
        if args:
            self.args = {k: v for k, v in vars(args).items() if v is not None}

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

    def prepare(self, hosts):
        pass

    def run(self, hosts=None):
        """Execute platform commands."""
        LOG.info("{}: {} on host {}".format(
            crayons.yellow("running command"),
            crayons.cyan(self.RUN_CMD),
            crayons.cyan(','.join(hosts))))
        LOG.info("----- Scenario Output START-----")
        process.execute_cmd(commands=[self.RUN_CMD], hosts=hosts)
        LOG.info("----- Scenario Output END-----")
