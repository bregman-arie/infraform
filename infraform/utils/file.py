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
import os
import re


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
