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
from infraform.cli.list import cli as list_cli


def add_list_parser(subparsers):
    """The parser for sub command 'list'."""
    list_parser = subparsers.add_parser("list")
    list_parser.set_defaults(func=list_cli.main)
    list_parser.add_argument('-p', '--path',
                             dest="show_path",
                             action='store_true',
                             help='Show the path of the scenario')
