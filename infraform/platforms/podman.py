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
import podman

from infraform.platforms.platform import Platform

LOG = logging.getLogger(__name__)


class Podman(Platform):

    PACKAGE = 'podman'

    def prepare(self):
        pass

    def run(self):
        try:
            with podman.Client() as client:
                print(client.images.list())
        except ConnectionError as exception:
            LOG.error(exception)
            LOG.error(self.raise_service_down())
