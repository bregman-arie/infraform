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
import crayons
from fabric import Connection
import invoke
import logging
import sys

LOG = logging.getLogger(__name__)


def execute_on_remote_host(commands, host, warn_on_fail=False,
                           cwd='/tmp', hide_output=False):
    """Execute commands remotely on a given host addresss

    Args:
        commands (list): List of commands to execute
        host (str): an host on which the commands will be executed
        warn_on_fail (bool): A flag used to determine whether to warn
                             only when a failure occurs and keep running
        cwd (str): the working directory where to execute the commands

    Returns:
        list: a list of results (fabric run results) for each executed command
    """
    c = Connection(host)
    with c.cd(cwd):
        for cmd in commands:
            try:
                if not hide_output:
                    LOG.debug(crayons.red("Executing: {}".format(cmd)))
                res = c.run(cmd, warn=warn_on_fail, hide=hide_output)
            except invoke.exceptions.UnexpectedExit:
                if not hide_output:
                    LOG.error("{}: {} on {}. Exiting now...".format(
                        crayons.red("Failed to execute"),
                        crayons.yellow(cmd),
                        crayons.cyan(host)))
                sys.exit(2)
    return res


def execute_on_local_host(commands, warn_on_fail=False,
                          cwd=None, hide_output=False):
    """Execute given commands on local host."""
    pass


def execute_cmd(commands, host=None, warn_on_fail=False, cwd="/tmp",
                hide_output=False):
    """Execute given commands on remote host or locally."""
    if host:
        res = execute_on_remote_host(commands, host, warn_on_fail, cwd,
                                     hide_output=hide_output)
    else:
        res = execute_on_local_host(commands, warn_on_fail, cwd,
                                    hide_output=hide_output)
    return res
