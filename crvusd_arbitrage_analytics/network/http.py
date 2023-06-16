"""
General utility for http requests.
https://github.com/curveresearch/curvesim/blob/main/curvesim/network/http.py
"""
import json
import aiohttp
from aiohttp import ClientResponseError
from tenacity import retry, stop_after_attempt, wait_random_exponential

class HttpClientError():
    """Raised for errors from async HTTP client request."""

    def __init__(self, status, message, url=None):
        # super().__init__(status, message)
        self.status = status
        self.message = message
        self.url = url

    def __repr__(self):
        return f"HttpClientError({self.status}, {self.message}, url={self.url})"

stop_rule = stop_after_attempt(2)
wait_rule = wait_random_exponential(multiplier=1, min=2, max=5)


class HTTP:
    @staticmethod
    @retry(stop=stop_rule, wait=wait_rule)
    async def get(url, params=None):

        kwargs = {"url": url, "headers": {"Accept-Encoding": "gzip"}}

        if params is not None:
            kwargs.update({"params": params})

        try:
            async with aiohttp.request("GET", **kwargs) as resp:
                resp.raise_for_status()
                json_data = await resp.read()
                json_data = json.loads(json_data)
        except ClientResponseError as e:
            message = e.message
            status = e.status
            url = e.request_info.url
            # pylint: disable-next=raise-missing-from
            raise HttpClientError(status, message, url)

        return json_data

    @staticmethod
    @retry(stop=stop_rule, wait=wait_rule)
    async def post(url, json=None):
        kwargs = {"url": url, "headers": {"Accept-Encoding": "gzip"}}

        if json is not None:
            kwargs.update({"json": json})

        try:
            async with aiohttp.request("POST", **kwargs) as resp:
                resp.raise_for_status()
                json_data = await resp.json()
        except ClientResponseError as e:
            message = e.message
            status = e.status
            url = e.request_info.url
            # pylint: disable-next=raise-missing-from
            raise HttpClientError(status, message, url)

        return json_data