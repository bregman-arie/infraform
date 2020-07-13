# Copyright 2020 Arie Bregman
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

from infraform.platforms.platform import Platform
from infraform.platforms.vars import shell as shell_vars

LOG = logging.getLogger(__name__)


class Shell(Platform):

    def __init__(self, args):

        super(Shell, self).__init__(
            args, binary=shell_vars.BINARY,
            readiness_check=shell_vars.READINESS_CHECK,
            installation=shell_vars.INSTALLATION,
            platform_name=shell_vars.NAME,
            run_platform=shell_vars.RUN)
