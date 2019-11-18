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

from infraform.platforms.platform import Platform

LOG = logging.getLogger(__name__)


class Terraform(Platform):

    PACKAGE = 'terraform'
    BINARY = 'terraform'
    INSTALLATION = (
        "export version=0.12.10\nwget https://releases.hashicorp.com" +
        "/terraform/${version}/terraform_${version}_linux_amd64.zip" +
        "\nunzip terraform_${version}_linux_amd64.zip" +
        "\nsudo mv terraform /usr/local/bin/")

    def __init__(self, args):
        self.binary = self.BINARY
        self.package = self.PACKAGE
        self.installation = self.INSTALLATION
        super(Terraform, self).__init__(args)

    def prepare(self):
        self.execute_cmd('terraform init')

    def run(self):
        self.execute_cmd('terraform apply')
