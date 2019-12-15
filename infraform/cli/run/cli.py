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
import logging
import importlib
import sys

from infraform.cli import utils
from infraform.exceptions.usage import missing_scenario_arg
from infraform.exceptions.utils import success_or_exit

LOG = logging.getLogger(__name__)


def main(args):
    """Runner main entry."""
    if not args.scenario and not args.vars:
        LOG.error(missing_scenario_arg())
        sys.exit(2)
    if args.scenario and not args.platform:
        args.platform = utils.guess_platform(args.scenario)
    if not args.scenario and not args.platform:
        success_or_exit(1, "Couldn't figure out which platform to use. \
Please specify --platform")
    Platform = getattr(importlib.import_module(
        "infraform.platforms.{}".format(args.platform)),
        args.platform.capitalize())
    platform = Platform(args=args)
    platform.prepare()
    platform.run()
