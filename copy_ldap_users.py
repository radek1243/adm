from ldap3 import Server, Connection, Tls
import ldap3
import ssl
import getpass
import argparse
import ldap_utils
from check_adgroup import check_adgroup

def copy_adusers(src_group, dest_group, username, ps, domain: str):
        src_group_info = check_adgroup(src_group, username, ps, domain)
        dest_group_info = check_adgroup(dest_group, username, ps, domain)
        dcs = ldap_utils.find_dcs(domain)
        for dc in dcs:
                tls = Tls(validate=ssl.CERT_NONE, version=ssl.PROTOCOL_TLSv1_2)
                tmp = domain.split(".")
                search_base = ""
                for t in tmp:
                        search_base+="DC="+t+","
                search_base=search_base.removesuffix(",")
                server = Server(dc, use_ssl=True, tls=tls)
                c = Connection(
                server, user=username, password=ps, authentication="SIMPLE")
                if c.bind():
                    mod_list=list()
                    for member in src_group_info['attributes']['member']:
                            mod_list.append((ldap3.MODIFY_INCREMENT,[member]))
                    result = c.modify(
                                dest_group_info['dn'],
                                {'member': mod_list}
                        )
                    if result:
                                print('***Users were copied***')
                    else:
                                print('***Error when copying users!*** '+c['result'])
                    c.unbind()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u","--user",required=True)
    parser.add_argument("-s","--source",required=True)
    parser.add_argument("-dst","--dest",required=True)
    parser.add_argument("-d","--domain",required=True)
    args = parser.parse_args()
    ps = getpass.getpass("Entry password for your LDAP login: ")
    copy_adusers(args.source, args.dest, args.user, ps, args.domain)

if __name__ == '__main__':
        main()