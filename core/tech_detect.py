import requests
from builtwith import parse
from urllib.parse import urlparse
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (HarpyScan)",
    "Accept": "text/html,application/xhtml+xml"
}

def builtwith_tech(url):
    try:
        return parse(url)
    except Exception as e:
        return {"error": f"BuiltWith failed: {str(e)}"}

def detect_cms(url, technologies):
    cms_signatures = {
        'WordPress': ['wp-content', 'wp-includes', 'wp-login', 'wp-admin'],
        'Joomla': ['option=com_', '/administrator/', 'Joomla!'],
        'Drupal': ['/sites/default/', 'drupal.js', 'Drupal.settings'],
        'Magento': ['Magento', '/skin/frontend/', '/media/catalog/'],
        'Shopify': ['cdn.shopify.com', 'myshopify.com'],
        'WooCommerce': ['woocommerce', 'wc-ajax', 'wp-content/plugins/woocommerce'],
        'OpenCart': ['index.php?route=', '/catalog/view/theme/', 'opencart'],
        'PrestaShop': ['/modules/', 'prestashop', 'var prestashop'],
        'TYPO3': ['typo3conf', 'typo3temp', 'TYPO3'],
        'BigCommerce': ['bigcommerce', 'cdn.bc0a.com'],
        'Squarespace': ['squarespace.com', 'static.squarespace.com'],
    }

    cms_info = {}

    try:
        res = requests.get(url, headers=HEADERS, timeout=10, verify=False)
        html = res.text.lower()
        for cms, sigs in cms_signatures.items():
            for sig in sigs:
                if sig.lower() in html or sig.lower() in url.lower():
                    cms_info[cms] = f"Matched signature: {sig}"
                    break
    except Exception as e:
        cms_info["error"] = str(e)

    # BuiltWith override (for stronger signal)
    if 'cms' in technologies:
        for tech in technologies['cms']:
            cms_info[tech] = 'Detected via BuiltWith'

    return cms_info

def detect_js_frameworks(url):
    js_signatures = {
        'jQuery': ['jquery', 'jquery.min.js'],
        'React': ['react', 'react-dom'],
        'Vue.js': ['vue', 'vuex'],
        'Angular': ['angular', 'angular.js', 'ng-app'],
        'Alpine.js': ['alpine', 'x-data'],
        'Svelte': ['svelte'],
        'Next.js': ['__NEXT_DATA__', '_next/static/'],
        'Nuxt.js': ['__NUXT__', '/_nuxt/'],
    }

    detected = {}
    try:
        res = requests.get(url, headers=HEADERS, timeout=10, verify=False)
        html = res.text.lower()
        soup = BeautifulSoup(html, 'html.parser')

        # Cek script tags & HTML body
        scripts = [s.get('src', '') for s in soup.find_all('script') if s.get('src')]
        inline = soup.text

        for lib, sigs in js_signatures.items():
            for sig in sigs:
                if any(sig in s for s in scripts) or sig in inline:
                    detected[lib] = f"Matched: {sig}"
                    break
    except Exception as e:
        detected["error"] = str(e)

    return detected
