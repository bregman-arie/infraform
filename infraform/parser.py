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

from infraform.create import cli as create_cli


def add_create_parser(subparsers):
    """The parser for sub command 'create'."""
    create_parser = subparsers.add_parser("create")
    create_parser.set_defaults(func=create_cli.main)
    create_parser.add_argument('--links', '-l',
                               dest="list_links",
                               help='List all available and chosen links.')
    create_parser.add_argument('--tester', '-t',
                               dest="tester",
                               help='The name of the tests env to use.')
    create_parser.add_argument('--branch', '-b',
                               dest="branch",
                               help='The name of the branch to use.')
    create_parser.add_argument('--project', '-p',
                               dest="project",
                               help="The name of the project to use.")
    create_parser.add_argument(
        '--platform',
        dest="platform",
        default="docker",
        help="The platform to use for creating the infrastructure.")


def create_parser():
    """Returns argument parser"""

    # Top level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser.add_argument('--debug', '-d', action='store_true',
                        dest="debug", help='Turn on debug')

    add_create_parser(subparsers)

    return parser
