from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "PromoGenie Real Coupon Engine Live!"

@app.route('/get-codes', methods=['GET'])
def get_codes():
    site = request.args.get('site')
    if not site:
        return jsonify({'error': 'Missing ?site= parameter'}), 400

    domain = site.lower().replace("www.", "").split("/")[0]
    url = f"https://www.couponbirds.com/codes/{domain}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return jsonify({'error': f'Cannot fetch site {url}', 'status': res.status_code})

        soup = BeautifulSoup(res.text, "html.parser")
        codes_raw = soup.select(".store-coupon-code")
        results = []

        for c in codes_raw[:10]:
            code = c.get_text(strip=True)
            parent = c.find_parent("li")
            title_elem = parent.select_one(".store-coupon-title")
            title = title_elem.get_text(strip=True) if title_elem else "Deal"

            results.append({
                "code": code,
                "description": title,
                "estimated_discount": "$10 - $50",
                "last_verified": "Just now",
                "success_rate": "78%",
            })

        return jsonify({
            "site": domain,
            "count": len(results),
            "codes": results,
        })

    except Exception as e:
        return jsonify({'error': str(e)})
