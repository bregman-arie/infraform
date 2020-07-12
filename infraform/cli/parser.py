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
import argparse

from infraform.cli.show import parser as show_parser
from infraform.cli.rm import parser as rm_parser
from infraform.cli.run import parser as run_parser
from infraform.cli.list import parser as list_parser
from infraform.cli.ssh import parser as ssh_parser


def create_parser():
    """Returns argument parser"""

    # Top level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser.add_argument('--debug', '-d', action='store_true',
                        dest="debug", help='Turn on debug')

    run_parser.add_run_parser(subparsers)
    rm_parser.add_rm_parser(subparsers)
    list_parser.add_list_parser(subparsers)
    show_parser.add_show_parser(subparsers)
    ssh_parser.add_ssh_parser(subparsers)

    return parser
