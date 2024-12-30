from ldap3 import Server, Connection, Tls
import ldap3
import ssl
import getpass
import argparse
import ldap_utils
from check_adgroup import check_adgroup

def make_users_yaml(src_group, username, ps, domain: str) -> str:
        src_group_info = check_adgroup(src_group, username, ps, domain)
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
                yaml_text="users:\n"
                if c.bind():
                    for member in src_group_info['attributes']['member']:
                        c.search(
                            search_base,
                            search_filter="(distinguishedName="+member+")",
                            attributes=['*','uidNumber','gidNumber']        
                        )
                        user = c.response[0]['attributes']
                        yaml_text+="  - { login: "+user['userPrincipalName']+", uid: "+str(user['uidNumber'])+" }\n"
                    c.unbind()
                    return yaml_text

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u","--user",required=True)
    parser.add_argument("-s","--source",required=True)
    parser.add_argument("-d","--domain",required=True)
    args = parser.parse_args()
    ps = getpass.getpass("Entry password for your LDAP login: ")
    print(make_users_yaml(args.source, args.user, ps, args.domain))

if __name__ == '__main__':
        main()