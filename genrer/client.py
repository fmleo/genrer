import logging
import os
from typing import List

import requests
import eyed3

from genrer.constants import WS_PATH, LASTFM_ERRORS


class Client:
    logger: logging.Logger
    api_key: str
    work_dir: str
    cache_dir: str

    def __init__(
        self, api_key: str, work_dir: str, debug_level: str = "WARNING"
    ) -> None:
        self.logger = logging.getLogger("genrer")
        self.logger.setLevel(debug_level)

        self.cache_dir = os.path.join(
            os.getenv("XDG_CACHE_HOME", default=os.path.expanduser("~/.cache")),
            "genrer/",
        )

        self.logger.debug(self.cache_dir)

        if not os.path.isdir(self.cache_dir):
            os.mkdir(self.cache_dir)

        self.work_dir = work_dir
        self.api_key = api_key

    def _make_request(
        self, endpoint: str, method: str = "GET", params: dict = None, data: dict = None
    ) -> dict:
        """makes requests to the lastfm audioscrobbler webservice

        Args:
            endpoint (str): webservice endpoint (e.g.: track.getInfo)
            method (str): request method. Defaults to "GET"
            params (dict, optional): url parameters. Defaults to None.
            data (dict, optional): _description_. Defaults to None.

        Returns:
            dict: _description_
        """
        if not params:
            params = {}
        params["api_key"] = self.api_key

        # method in the webservice calls refer to what resource you're fetching
        # e.g. ?method=track.getInfo
        params["method"] = endpoint

        if not data:
            data = {}

        response = requests.request(
            method=method, url=f"{WS_PATH}{endpoint}", params=params, data=data
        )

        self.logger.info("made request to %s [%d]", response.url, response.status_code)

        return response.json()
