#!/usr/bin/python3

from ansible.module_utils.basic import AnsibleModule

def run_module():
    module_args = dict(
       path=dict(type='str',required=True),
       client=dict(type='str',required=True),
       rw=dict(type='bool',required=True),
       sec=dict(type='list',elements='str',choices=['sys','krb5','krb5i','krb5p'],required=False, default='sys'),
       mode=dict(type='list',elements='str',choices=['sync','async'],required=False, default='sync'),
       subtree_check=dict(type='bool',required=False, default=True),
       root_squash=dict(type='bool',required=False,default=True),
       all_squash=dict(type='bool',required=False,default=False),
       anonuid=dict(type='int',required=False),
       anongid=dict(type='int',required=False)
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    #to do

def main():
    run_module()

if __name__ == '__main__':
    main()