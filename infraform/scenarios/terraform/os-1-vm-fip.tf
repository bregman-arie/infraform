provider "openstack" {
  cloud = "upshift-component-ci"
}

resource "openstack_compute_instance_v2" "test-server" {
  name = "test-server"
}
