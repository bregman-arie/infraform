provider "openstack" {
  cloud = "{{ vars['cloud'] }}"
}

resource "openstack_compute_instance_v2" "test-server" {
  name = "test-server"
}
