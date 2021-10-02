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

from infraform.utils import file as file_utils

LOG = logging.getLogger(__name__)


class Workspace(object):

    def __init__(self, subdir, root_dir_path='/tmp/.infraform', host='localhost'):
        self.subdir = subdir
        self.root_dir_path = root_dir_path
        self.path = os.path.join(root_dir_path, subdir)
        self.host = host
        if host != 'localhost' and host != '127.0.0.1':
            self.cleanup()
            self.create()

    def create(self):
        if self.host == "localhost" or self.host == "127.0.0.1":
            os.makedirs(self.path)
            LOG.info("{}: {}".format(crayons.yellow("workspace created"),
                                     self.path))
        else:
            file_utils.create_remote_dir(host=self.host, path=self.path)
            LOG.info("workspace {} created on host {}".format(
            crayons.cyan(self.path), crayons.cyan(self.host)))

    def cleanup(self):
        if self.host == "localhost" or self.host == "127.0.0.1":
            try:
                shutil.rmtree(self.path)
                LOG.info("{}: {}".format(crayons.yellow("workspace removed"),
                                     self.root_dir_path))
            except FileNotFoundError:
                pass
        else:
            file_utils.remove_remote_dir(
                host=self.host, path=self.path, directory=self.subdir)
