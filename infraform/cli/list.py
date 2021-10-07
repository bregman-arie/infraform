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
import logging

from infraform.list import list_scenarios

LOG = logging.getLogger(__name__)


def add_list_parser(subparsers):
    """The parser for sub command 'list'."""
    list_parser = subparsers.add_parser("list")
    list_parser.set_defaults(func=main)
    list_parser.add_argument('-p', '--path',
                             dest="show_path",
                             action='store_true',
                             help='Show the path of the scenario')


def main(args):
    """Runner main entry."""
    LOG.info("Listing scenarios...\n")
    list_scenarios(show_path=args.show_path)
    LOG.info("\nTo display a scenario use {}\nTo run a scenario use {}".format(
        crayons.yellow("ifr show <scenario_name>"),
        crayons.yellow("ifr run <scenario_name>")))
