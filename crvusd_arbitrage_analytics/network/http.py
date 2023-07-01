"""
General utility for http requests.
https://github.com/curveresearch/curvesim/blob/main/curvesim/network/http.py
"""
import json
import os
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

stop_rule = stop_after_attempt(8)
wait_rule = wait_random_exponential(multiplier=1.5, min=2, max=60)


class HTTP:
    @staticmethod
    @retry(stop=stop_rule, wait=wait_rule)
    async def get(url, params=None):

        kwargs = {"url": url, "headers": {"Accept-Encoding": "gzip"}}

        if params is not None:
            kwargs.update({"params": params})
        if os.environ["http_proxy"] is not None:
            kwargs.update({"proxy": os.environ["http_proxy"]})

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
        if os.environ["http_proxy"] is not None:
            kwargs.update({"proxy": os.environ["HTTP_PROXY"]})

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