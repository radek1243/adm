#!/usr/bin/python3
#Script to check users via LDAP
from ldap3 import Server, Connection, Tls
import ssl
import getpass
import argparse
import ldap_utils

def check_aduser(upn, username, ps, domain: str):
        icdcs = ldap_utils.find_dcs(domain)
        for dc in icdcs:
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
                        c.search(
                                search_base,
                                search_filter="(userPrincipalName="+upn+")",
                                attributes=['*','uidNumber','gidNumber']
                        )
                        result = c.response[0]
                        c.unbind()
                        return result
def main():
        parser = argparse.ArgumentParser()
        parser.add_argument("-u","--user",required=True)
        parser.add_argument("--upn",required=True)
        parser.add_argument("-d","--domain",required=True)
        args = parser.parse_args()
        ps = getpass.getpass("Entry password for your LDAP login: ")
        ldap_utils.print_attributes(check_aduser(args.upn, args.user, ps, args.domain))

if __name__ == '__main__':
        main()

