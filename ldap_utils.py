import dns.resolver

def find_dcs(domain: str) -> list[str]:
        l = list[str]()
        answer = dns.resolver.resolve(qname='_ldap._tcp.'+domain,rdtype="SRV",tcp=True)
        for a in answer:
                adc: list[str] = a.to_text().split(" ")
                l.append(adc[adc.__len__()-1].removesuffix("."))
        return l
