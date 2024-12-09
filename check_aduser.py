#!/usr/bin/python3
#Script requires krb5-user and python3-ldap3 packages
#Description:
#Skrypt dodający uidNumber i gidNumber dla użytkownikow wczytywanych z pliku users.txt
#Plik users.txt musi być w formacie upn;uidNumber
#Skrypt do uwierzytelnienia z AD używa mechanizmu kerberos
#Skrypt na podstawie upn określa z jakiej domeny jest login, laczy sie do odpowiedniego kontrolera i ustawia odpowiednie parametry wczytanymi wartosciami
import dns.resolver
from ldap3 import Server, Connection, Tls
import ssl
import getpass
import argparse
import dns


def find_dcs(domain: str) -> list[str]:
        l = list[str]()
        answer = dns.resolver.resolve(qname='_ldap._tcp.'+domain,rdtype="SRV",tcp=True)
        for a in answer:
                adc: list[str] = a.to_text().split(" ")
                l.append(adc[adc.__len__()-1].removesuffix("."))
        return l

def check_aduser(upn, username, ps, domain: str):
        icdcs = find_dcs(domain)
        for dc in icdcs:
                tls = Tls(validate=ssl.CERT_NONE, version=ssl.PROTOCOL_TLSv1_2)
                #dns.query. - zrobić wyszukiwanie kontrolerów na bazie domeny
                tmp = domain.split(".")
                search_base = ""
                for t in tmp:
                        search_base+="DC="+t+","
                search_base=search_base.removesuffix(",")
                server = Server(dc, use_ssl=True, tls=tls)
                c = Connection(
                server, user=username, password=ps, authentication="SIMPLE")
                if c.bind():
                #print("Pobieranie atrybutów uzytkownika")
                        c.search(
                                search_base,
                                search_filter="(userPrincipalName="+upn+")",
                                attributes=['*']
                        )
                        result = c.response[0]
                        if result:
                                print(result)
                        else:
                                print("Blad przy pobieraniu użytkownika "+result)
                        c.unbind()
                        break

parser = argparse.ArgumentParser()
parser.add_argument("-u","--user",required=True)
parser.add_argument("--upn",required=True)
parser.add_argument("-d","--domain",required=False, default="intercars.local")
args = parser.parse_args()
ps = getpass.getpass("Podaj haslo do Twojego loginu AD: ")
check_aduser(args.upn, args.user, ps, args.domain)

