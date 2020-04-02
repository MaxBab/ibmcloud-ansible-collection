#!/usr/bin/env python

# GNU General Public License v3.0+


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import geo as sdk_geo


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_is_zone_info
short_description: Retrieve information about zones per region.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Retrieve information about zones available per region on IBM Cloud.
notes:
    - The result contains a list of zones.
requirements:
    - "ibmcloud-python-sdk"
options:
    region:
        description:
            - Region name where to list the zone(s).
        required: true
    zone:
        description:
            - Restrict results to zone with name matching.
        required: false
extends_documentation_fragment:
    - ibmcloud
'''

EXAMPLES = '''
# Retrieve zone list for a specific region and register the value
- ic_is_zone_info:
    region: us-south
  register: zones

# Display regions registered value
- debug:
    var: regions

# Retrieve specific zone for a specific region
- ic_is_zone_info:
    region: us-south
    zone: us-south-1
'''


def run_module():
    module_args = dict(
        region=dict(
            type='str',
            required=True),
        zone=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    geo = sdk_geo.Geo()

    region = module.params['region']
    zone = module.params['zone']

    if zone:
        result = geo.get_region_zone(region, zone)
        if "errors" in result:
            module.fail_json(msg=result["errors"])
    else:
        result = geo.get_region_zones(region)
        if "errors" in result:
            module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()