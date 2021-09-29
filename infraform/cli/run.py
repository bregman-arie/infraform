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
import os

from infraform.orchestrator import Orchestrator

LOG = logging.getLogger(__name__)


def add_run_parser(subparsers):
    """The parser for sub command 'run'."""
    run_parser = subparsers.add_parser("run")
    run_parser.set_defaults(func=main)
    run_parser.add_argument('scenario',
                            nargs=1,
                            help='An Infraform file or any other type \
                            that is supported by Infraform')
    run_parser.add_argument('--platform', dest="platform_name",
                            help="The platform to use \
(podman, docker, terraform, shell, python)")
    run_parser.add_argument('--vars', dest="scenario_vars",
                            default="",
                            help="extra variables")
    run_parser.add_argument('--skip-check', dest="skip_check",
                            action="store_true",
                            help="Skip requirements check")
    run_parser.add_argument('--hosts', dest="hosts",
                            default="", nargs='*',
                            help="host(s) to execute the scenario/command on \
by specifying host name or user@host")
    run_parser.add_argument('--commands', dest="commands",
                            default="", nargs='*',
                            help="Command(s) to execute instead of a scenario")
    run_parser.add_argument('--scenarios-dir', '-sd', dest="scenarios_dir",
                            default=(os.path.dirname(
                                __file__) + '/..' + '/scenarios'),
                            help="The path of the directory where \
                            to look for Scenarios")


def main(args):
    """Runner main entry."""
    # TODO(abregman): do actually something with debug
    del args.debug
    del args.func

    orc = Orchestrator(**vars(args))
    orc.prepare()
    orc.run()
