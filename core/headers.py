import requests

def get_headers(url):
    """Ambil HTTP headers dari target URL."""
    try:
        response = requests.get(url, timeout=10, verify=False)
        return response.headers
    except Exception as e:
        return {"error": str(e)}

def check_security_headers(headers):
    """Cek header keamanan dengan analisis nilai dan kepatuhan standar."""
    checks = {
        'Strict-Transport-Security': {
            "status": "Not Found",
            "advice": "Implement HSTS with max-age >= 31536000 (1 year)."
        },
        'Content-Security-Policy': {
            "status": "Not Found",
            "advice": "Define a CSP to prevent XSS attacks."
        },
        'X-Frame-Options': {
            "status": "Not Found",
            "advice": "Use 'DENY' or 'SAMEORIGIN' to prevent clickjacking."
        },
        'X-Content-Type-Options': {
            "status": "Not Found",
            "advice": "Set to 'nosniff' to prevent MIME-sniffing."
        },
        'X-XSS-Protection': {
            "status": "Not Found",
            "advice": "Set to '1; mode=block' to enable basic XSS protection."
        },
        'Referrer-Policy': {
            "status": "Not Found",
            "advice": "Set to 'strict-origin-when-cross-origin' for better privacy."
        },
        'Permissions-Policy': {
            "status": "Not Found",
            "advice": "Define a Permissions Policy to control browser features."
        },
    }

    # Cek setiap header
    for header, detail in checks.items():
        if header in headers:
            value = headers[header]
            if value:
                # Tambahkan validasi spesifik (contoh: HSTS)
                if header == 'Strict-Transport-Security' and 'max-age=' in value:
                    try:
                        max_age = int(value.split('max-age=')[1].split(';')[0])
                        if max_age < 31536000:
                            detail["status"] = f"Present but weak (max-age={max_age})"
                        else:
                            detail["status"] = "Present and strong"
                    except ValueError:
                        detail["status"] = "Malformed value"
                else:
                    detail["status"] = f"Present ({value})"
            else:
                detail["status"] = "Empty value"

    return checks
