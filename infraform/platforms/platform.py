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
import subprocess
import sys

from infraform.exceptions import requirements

LOG = logging.getLogger(__name__)


class Platform(object):

    def __init__(self, args):
        self.args = {k: v for k, v in vars(args).items() if v is not None}
        self.check_platform_avaiable()

    def check_platform_avaiable(self):
        res = subprocess.run("{} --version".format(self.binary), shell=True,
                             stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        if res.returncode != 0:
            LOG.error(requirements.raise_service_down(self.PACKAGE))
            sys.exit(2)
