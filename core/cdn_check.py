import dns.resolver

def check_cdn(headers, hostname):
    known_cdns = {
        'Cloudflare': ['cf-ray', 'cloudflare'],
        'Akamai': ['akamai', 'akamai.net', 'akamaitechnologies.com'],
        'Fastly': ['fastly', 'fastly.net'],
        'Amazon CloudFront': ['x-amz-cf', 'cloudfront.net'],
        'Google Cloud CDN': ['x-goog', 'google', 'goog'],
        'Microsoft Azure CDN': ['x-ms-cdn', 'azureedge.net'],
        'Vercel': ['vercel', 'x-vercel'],
        'Netlify': ['netlify', 'x-nf'],
        'Sucuri': ['sucuri'],
        'StackPath': ['stackpath'],
        'BunnyCDN': ['bunnycdn'],
    }

    matches = {}

    # Phase 1: Header-based detection
    for cdn_name, indicators in known_cdns.items():
        for k, v in headers.items():
            haystack = f"{k}:{v}".lower()
            for indicator in indicators:
                if indicator.lower() in haystack:
                    matches[cdn_name] = matches.get(cdn_name, 0) + 1

    # Phase 2: DNS CNAME-based detection (if available)
    try:
        answers = dns.resolver.resolve(hostname, 'CNAME')
        for rdata in answers:
            cname = str(rdata).lower()
            for cdn_name, indicators in known_cdns.items():
                for indicator in indicators:
                    if indicator.lower() in cname:
                        matches[cdn_name] = matches.get(cdn_name, 0) + 1
    except:
        pass  # Skip if no CNAME or resolver fails

    # Phase 3: Final decision
    if not matches:
        return "Unknown"
    
    # Sort based on confidence (most matches = highest score)
    sorted_cdns = sorted(matches.items(), key=lambda x: x[1], reverse=True)
    best_match = sorted_cdns[0][0]
    confidence = sorted_cdns[0][1]

    return {
        "detected": best_match,
        "confidence": confidence,
        "alternatives": [cdn for cdn, score in sorted_cdns[1:]]
    }
