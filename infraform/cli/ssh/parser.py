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
from infraform.cli.ssh import cli as ssh_cli


def add_ssh_parser(subparsers):
    """The parser for sub command 'ssh'."""
    ssh_parser = subparsers.add_parser("ssh")
    ssh_parser.set_defaults(func=ssh_cli.main)
    ssh_parser.add_argument('--debug', dest="debug",
                            action="store_true",
                            help="Enable debug level logging")
