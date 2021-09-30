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


def execute_on_remote_host(commands, hosts, warn_on_fail=False,
                           cwd=None, hide_output=False):
    """Execute commands remotely on a given list of hosts

    Args:
        commands (list): List of commands to execute
        hosts (list): List of hosts on which the commands will be executed
        warn_on_fail (bool): A flag used to determine whether to warn
                             only when a failure occurs and keep running
        cwd (str): the working directory where to execute the commands

    Returns:
        list: a list of results (fabric run results) for each executed command
    """
    results = []
    for host in hosts:
        c = Connection(host)
        for cmd in commands:
            try:
                if cwd:
                    with c.cd(cwd):
                        LOG.debug(crayons.red(
                            "Executing: {} in {}".format(cmd, cwd)))
                        res = c.run(cmd, warn=warn_on_fail, hide=hide_output)
                else:
                    if not hide_output:
                        LOG.debug(crayons.red("Executing: {}".format(cmd)))
                    res = c.run(cmd, warn=warn_on_fail, hide=hide_output)
                results.append(res)
            except invoke.exceptions.UnexpectedExit:
                if not hide_output:
                    LOG.error("{}: {} on {}. Exiting now...".format(
                        crayons.red("Failed to execute"), crayons.yellow(cmd),
                        crayons.cyan(host)))
                sys.exit(2)
    return results


def execute_on_local_host(commands, warn_on_fail=False,
                          cwd=None, hide_output=False):
    """Execute given commands on local host."""
    pass


def execute_cmd(commands, hosts=None, warn_on_fail=False, cwd=None,
                hide_output=False):
    """Execute given commands on remote hosts or locally."""
    if hosts:
        res = execute_on_remote_host(commands, hosts, warn_on_fail, cwd,
                                     hide_output=hide_output)
    else:
        res = execute_on_local_host(commands, warn_on_fail, cwd,
                                    hide_output=hide_output)
    return res
