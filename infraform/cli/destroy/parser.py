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
from infraform.cli.destroy import cli as destroy_cli


def add_destroy_parser(subparsers):
    """The parser for sub command 'destroy'."""
    destroy_parser = subparsers.add_parser("destroy")
    destroy_parser.set_defaults(func=destroy_cli.main)
    destroy_parser.add_argument('--name', '-n',
                                dest="name",
                                help='Name of the resource to remove.')
    destroy_parser.add_argument('--scenario', '-s',
                                  dest="scenario",
                                  help='Predefined scenario to use for exection')
    destroy_parser.add_argument('--platform', dest="platform",
                                  help="The platform to use (podman, docker, etc.)")
    destroy_parser.add_argument('--vars', dest="vars",
                                  default="",
                                  help="extra variables")
