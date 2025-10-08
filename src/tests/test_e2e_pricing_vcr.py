import os
import vcr
from pulsebot.utils.pricing import fetch_price_usd


def test_fetch_price_usd_vcr():
    # Compute absolute cassette path and use record_mode='none' to avoid writing
    cassette_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'tests', 'cassettes', 'pricing_api_vcr.yaml'))
    vcr_inst = vcr.VCR()
    # The cassette contains a response for api.example.com for bitcoin at specific endpoint
    with vcr_inst.use_cassette(cassette_path, record_mode='none'):
        price = fetch_price_usd('BTC/USD', exchange=None, fallback_api='https://api.example.com/simple/price?ids=bitcoin&vs_currencies=usd')
    # Our cassette encodes bitcoin->usd 55000.0; fetch_price_usd should return that value
    assert price == 55000.0
