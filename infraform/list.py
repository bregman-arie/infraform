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
import os
import re

LOG = logging.getLogger(__name__)

SCENARIOS_PATH = os.path.dirname(__file__) + '/../infraform/scenarios'

def list_scenarios():
    for (dirpath, dirnames, filenames) in os.walk(SCENARIOS_PATH):
        for f in filenames:
            until_dot_pattern = re.compile(r"^[^.]*")
            file_without_suffix = re.search(until_dot_pattern, f).group(0)
            LOG.info(file_without_suffix)
