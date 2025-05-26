import dns.resolver

def get_dns_records(hostname):
    records = {}
    try:
        answers = dns.resolver.resolve(hostname, 'A')
        records['A'] = [str(r) for r in answers]
    except:
        records['A'] = []
    try:
        answers = dns.resolver.resolve(hostname, 'MX')
        records['MX'] = [str(r.exchange) for r in answers]
    except:
        records['MX'] = []
    return records