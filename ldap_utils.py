import dns.resolver

def find_dcs(domain: str) -> list[str]:
        l = list[str]()
        answer = dns.resolver.resolve(qname='_ldap._tcp.'+domain,rdtype="SRV",tcp=True)
        for a in answer:
                adc: list[str] = a.to_text().split(" ")
                l.append(adc[adc.__len__()-1].removesuffix("."))
        return l

def print_attributes(result):
        if result:
                for key, value in result['attributes'].items():
                        print(key+": "+value.__str__())
        else:
                print("Error when trying to obtain user info! "+result)