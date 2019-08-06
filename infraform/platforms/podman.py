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
import jinja2 as j2
import logging
import os
import re
import subprocess
import sys

from infraform.exceptions import usage
from infraform.platforms.platform import Platform

LOG = logging.getLogger(__name__)


class Podman(Platform):

    PACKAGE = 'podman'
    DOCKERFILE_TEMPLATE = (os.path.dirname(__file__) +
                           '/templates/Dockerfile.j2')

    def __init__(self, args):
        super(Podman, self).__init__(args)

    def prepare(self):
        if self.image_not_exists():
            LOG.warning("Couldn't find image: {}. Switching to image building".format(self.image))
            dockerfile_path = self.write_dockerfile(self.generate_dockerfile())
            self.build_image(dockerfile_path)

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

    def get_template(self, name):
        """Returns jinja2 Dockerfile template."""
        with open(name, 'r+') as open_f:
            template_content = open_f.read()
        return template_content

    def generate_dockerfile(self):
        j2_env = j2.Environment(loader=j2.FunctionLoader(
            self.get_template), trim_blocks=True, undefined=j2.StrictUndefined)
        template = j2_env.get_template(self.DOCKERFILE_TEMPLATE)
        try:
            rendered_file = template.render(args=self.args)
        except j2.exceptions.UndefinedError as e:
            missing_arg = re.findall(r"'([^']*)'", e.message)[0]
            LOG.error(usage.missing_arg(missing_arg))
            LOG.error(usage.general_usage())
            sys.exit(2)
        return rendered_file

    def write_dockerfile(self, df_content, df_path="Dockerfile"):
        with open(df_path, 'w+') as f:
            f.write(df_content)
        return df_path

    def build_image(self, df_path):
        """Builds image given df path."""
        res = subprocess.run("podman build -f {}".format(df_path),
                             shell=True)
        if res.returncode != 0:
            sys.exit(2)
        return res
