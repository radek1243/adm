#!/usr/bin/python3

from ansible.module_utils.basic import AnsibleModule
import paramiko
import paramiko.client
import paramiko.ecdsakey
import paramiko.hostkeys
import paramiko.pkey

ALLOWED_HOST_KEYS = ['ecdsa-sha2-nistp256']

def run_module():
    module_args = dict(
       path=dict(type='str',required=True),
       ip=dict(type='str',required=True),
       port=dict(type='str',required=False, default='22'),
       key_type=dict(type='str',required=False,default='ecdsa-sha2-nistp256')
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    if module.params['key_type'] in ALLOWED_HOST_KEYS:
        transport = paramiko.Transport(module.params['ip']+":"+module.params['port'])
        transport.get_security_options().key_types = [module.params['key_type']]
        try:
            transport.start_client(timeout=3)
            public_key = transport.get_remote_server_key()
            transport.close()
            entry = paramiko.hostkeys.HostKeys.hash_host(module.params['ip'])
            keys = paramiko.hostkeys.HostKeys(module.params['path'])
            keys.add(entry, public_key.get_name(), public_key)
            keys.save(module.params['path'])
            result['changed'] = True
            module.exit_json(**result)
        except paramiko.SSHException:
            module.fail_json(msg="Cannot contact to server!", **result)
        except OSError:
            module.fail_json(msg="Can not open or save file with known_hosts keys!", **result)
    else:
        module.fail_json(msg="Unsupported key type!", **result)

def main():
    run_module()

if __name__ == '__main__':
    main()