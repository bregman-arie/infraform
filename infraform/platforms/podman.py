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

from infraform.platforms.platform import Platform

LOG = logging.getLogger(__name__)


class Podman(Platform):

    PACKAGE = 'podman'

    def __init__(self, project=None, tester=None, branch=None):
        super(Podman, self).__init__(project, tester, branch)

    def prepare(self):
        if self.image_not_exists():
            LOG.warning("Couldn't find image: {}".format(self.image))
            self.generate_Dockerfile()

    def run(self):
        try:
            subprocess.run("podman run {}".format(self.image),
                           shell=True)
        except ConnectionError as exception:  # noqa
            LOG.error(exception)
            LOG.error(self.raise_service_down())

    def image_not_exists(self):
        """Returns true if image exists."""
        res = subprocess.run("podman inspect {}".format(self.image),
                             shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.DEVNULL)
        return res.returncode

    def generate_Dockerfile(self):
        pass
