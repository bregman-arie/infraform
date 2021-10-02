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
from fabric import Connection
import logging
import os
from patchwork.files import exists
import patchwork.transfers
import re

from infraform.context import suppress_output

LOG = logging.getLogger(__name__)


def get_file_content(file_path):
    """Returns file content."""
    with open(file_path, 'r+') as f:
        file_content = f.read()
    return file_content


def get_file_path(path, file_name, exact_match=True):
    for root, dirs, files in os.walk(path):
        if exact_match:
            if file_name in files:
                return os.path.join(root, file_name)
        else:
            for file in files:
                if file_name in file:
                    return os.path.join(root, file)


def get_match_until_first_dot(string):
    """Returns the matched pattern until first dot.

    For example: 'scenario1.py.j2' -> 'scenario'
    """
    until_dot_pattern = re.compile(r"^[^.]*")
    return re.search(until_dot_pattern, string).group(0)


def transfer(host, source, dest):
    conn = Connection(host)
    if host != "localhost" and host != "127.0.0.1":
        with suppress_output():
            patchwork.transfers.rsync(c, source, dest)
            conn.run("chmod +x {}".format(dest))
    else:
        cp_command = "cp -r {} {}".format(source, dest)
        conn.run(cp_command)


def remove_remote_dir(host, path, directory):
    c = Connection(host)
    if exists(c, path):
        with c.cd(path):
            c.run("rm -rf {}".format(directory))
            LOG.info("directory {} removed from host {}".format(
                crayons.cyan(path), crayons.cyan(host)))
    else:
        LOG.info("directory {} doesn't exists on {}".format(
            crayons.cyan(path), crayons.cyan(host)))


def create_remote_dir(host, path):
    c = Connection(host)
    c.run("mkdir -p {}".format(path))
