import requests
from typing import Dict, List, Optional, Union
from time import sleep

class DefiLlamaAPI:
    def __init__(self):
        self.base_url = 'https://api.llama.fi'
        self.coins_url = 'https://coins.llama.fi'
        self.session = requests.Session()
        self._rate_limit_delay = 2  # seconds between requests

    def _make_request(self, endpoint: str, base: str = None) -> dict:
        """Make a rate-limited request to the DefiLlama API"""
        if base is None:
            base = self.base_url
        
        url = f'{base}{endpoint}'
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            sleep(self._rate_limit_delay)  # Rate limiting
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f'API request failed: {str(e)}')

    def get_dex_overview(self) -> Dict:
        """Get overview of all DEXs"""
        return self._make_request('/overview/dexs')

    def get_protocol_data(self, protocol: str = 'uniswap') -> Dict:
        """Get detailed data for a specific protocol"""
        return self._make_request(f'/protocol/{protocol}')

    def get_chain_dexs(self, chain: str) -> Dict:
        """Get DEX data for a specific chain"""
        return self._make_request(f'/overview/dexs/{chain}')

    def get_token_prices(self, tokens: List[str]) -> Dict:
        """Get current prices for tokens (format: 'chain:token_address')"""
        token_str = ','.join(tokens)
        return self._make_request(f'/prices/current/{token_str}', base=self.coins_url)

    def get_protocol_tvl(self, protocol: str = 'uniswap') -> Dict:
        """Get TVL data for a specific protocol"""
        return self._make_request(f'/tvl/{protocol}')

    def get_dex_volume_breakdown(self, protocol: str = 'uniswap') -> Dict:
        """Get detailed volume breakdown for a DEX"""
        return self._make_request(f'/summary/dexs/{protocol}')