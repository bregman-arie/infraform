# Copyright 2020 Arie Bregman
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
NAME = "docker compose"
PACKAGE = 'docker'
BINARY = '/usr/local/bin/docker-compose'
READINESS_CHECK = ["docker-compose --version", "systemctl status docker"]
INSTALLATION = ["curl -L $(curl -s https://api.github.com/repos/docker/c\
ompose/releases/latest | grep browser_download_url | cut -d '\"' -f 4 | grep L\
inux | grep x86_64$) -o docker-compose", "sudo mv docker-compose /usr/local/bin\
&& sudo chmod +x /usr/local/bin/docker-compose",
                "sudo dnf config-manager --add-repo=https://download.dock\
er.com/linux/centos/docker-ce.repo",
                "sudo dnf install --nobest -y docker-ce",
                "sudo systemctl start docker"]
RUN = ["docker-compose up -d"]
REMOVE = ["docker-compose stop", "docker-compose rm"]
