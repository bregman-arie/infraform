#!/bin/bash

git clone gitlab.cee.redhat.com:majopela/os-dataminer-jupyter-ansible.git
cd os-dataminer-jupyter-ansible
ansible-playbook main-devel-env.yml \
                 -i inventory-devel \
                 --extra-vars="hash_salt=12345"