provider "openstack" {
  {% if 'cloud' in vars %}
     cloud = "{{ vars['cloud'] }}"
  {% else %}
     auth_url = "{{ vars['auth_url'] }}"
     password = "{{ vars['password'] }}"
     user_name = "{{ vars['username'] }}"
     tenant_name = "{{ vars['tenant_name'] }}"
     domain_name = "{{ vars['domain_name'] }}"
  {% endif %}
}

resource "openstack_compute_instance_v2" "test-server" {
  name = "{{ vars['instance_name']|default('test-server') }}"
  image_name = "{{ vars['image_name']|default('rhel-7.6-server-x86_64-latest') }}"
  flavor_name = "{{ vars['flavor_name']|default('m1.small') }}"

network {
    name = "{{ vars['network_name'] }}"
  }
}
