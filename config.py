"""
Utilities Misc Proxy 7

This module provides functionality for utilities misc proxy 7.

Author: Auto-generated
Date: 2025-11-01
"""

import asyncio

from libs.utils import ask_question, print_error, print_status, print_success
from proxybroker import Broker
from requests import get


async def show(proxies, proxy_list):
    while len(proxy_list) < 50:
        proxy = await proxies.get()
        if proxy is None:
            break

        print_success(
            "[" + str(len(proxy_list) + 1) + "/50]",
            "Proxy found:",
            proxy.as_json()["host"] + ":" + str(proxy.as_json()["port"]),
        )

        proxy_list.append(proxy.as_json()["host"] + ":" + str(proxy.as_json()["port"]))

        pass
    pass


def find_proxies():
    """find_proxies function."""

    proxy_list = []
    proxies = asyncio.Queue()
    broker = Broker(proxies)
    tasks = asyncio.gather(
        broker.find(types=["HTTPS"], limit=50), show(proxies, proxy_list)
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)

    if len(proxy_list) % 5 != 0 and len(proxy_list) > 5:
        proxy_list = proxy_list[: len(proxy_list) - (len(proxy_list) % 5)]

    return proxy_list
