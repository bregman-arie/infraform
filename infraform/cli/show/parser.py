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
from infraform.cli.show import cli as show_cli


def add_show_parser(subparsers):
    """The parser for sub command 'show'."""
    show_parser = subparsers.add_parser("show")
    show_parser.set_defaults(func=show_cli.main)
    show_parser.add_argument('scenario',
                             type=str,
                             help='scenario name')
