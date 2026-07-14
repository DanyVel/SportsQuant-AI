"""
Base HTTP downloader for the data layer.
"""

from __future__ import annotations

from typing import Any

import requests
from requests import Response, Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from sportsquant.data.base import BaseDataComponent
from sportsquant.data.exceptions import DownloadError
from sportsquant.data.models import ResponseData


class BaseDownloader(BaseDataComponent):
    """
    Base class for HTTP downloads.
    """

    DEFAULT_TIMEOUT = 30
    DEFAULT_RETRIES = 3
    BACKOFF_FACTOR = 1

    STATUS_FORCE_LIST = (
        429,
        500,
        502,
        503,
        504,
    )

    def __init__(self) -> None:
        super().__init__()

        self.session: Session = self._create_session()

    def _create_session(self) -> Session:
        """
        Create and configure an HTTP session.
        """

        session = requests.Session()

        retry = Retry(
            total=self.DEFAULT_RETRIES,
            backoff_factor=self.BACKOFF_FACTOR,
            status_forcelist=self.STATUS_FORCE_LIST,
            allowed_methods=["HEAD", "GET", "OPTIONS"],
        )

        adapter = HTTPAdapter(
            max_retries=retry,
        )

        session.mount("https://", adapter)
        session.mount("http://", adapter)

        session.headers.update(
            {
                "User-Agent": "SportsQuant-AI/0.1",
                "Accept": "application/json",
            }
        )

        return session

    def get(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        timeout: int | None = None,
    ) -> ResponseData:
        """
        Execute a GET request.

        Parameters
        ----------
        url : str
            Request URL.
        params : dict[str, Any] | None, optional
            Query parameters.
        headers : dict[str, str] | None, optional
            HTTP headers.
        timeout : int | None, optional
            Request timeout in seconds.

        Returns
        -------
        ResponseData
            HTTP response.
        """

        timeout = timeout or self.DEFAULT_TIMEOUT

        self.logger.info("GET %s", url)

        try:
            response: Response = self.session.get(
                url=url,
                params=params,
                headers=headers,
                timeout=timeout,
            )

            response.raise_for_status()

            return ResponseData(
                success=True,
                status_code=response.status_code,
                data=response.json(),
            )

        except requests.RequestException as exc:
            self.logger.exception("Download failed")

            raise DownloadError(str(exc)) from exc