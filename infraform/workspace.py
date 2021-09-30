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
import os
import shutil

LOG = logging.getLogger(__name__)


class Workspace(object):

    def __init__(self, root='.infraform', subdir=None):
        if subdir:
            self.root = os.path.join(root, subdir)
        else:
            self.root = root
        if os.path.exists(self.root):
            self.cleanup()
        self.create()

    def create(self):
        if not os.path.exists(self.root):
            os.makedirs(self.root)
            LOG.info("{}: {}".format(crayons.yellow("workspace created"),
                                     self.root))
        else:
            self.cleanup()

    def cleanup(self):
        shutil.rmtree(self.root)
        LOG.info("{}: {}".format(crayons.yellow("workspace removed"),
                                 self.root))
