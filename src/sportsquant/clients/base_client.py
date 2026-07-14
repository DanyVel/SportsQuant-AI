"""
Base client for external APIs.
"""

from __future__ import annotations

from typing import Any
from urllib.parse import urljoin

from sportsquant.data.downloader import BaseDownloader
from sportsquant.data.models import ResponseData


class BaseClient:
    """
    Base client for communicating with external APIs.
    """

    def __init__(
        self,
        base_url: str,
        downloader: BaseDownloader | None = None,
        default_headers: dict[str, str] | None = None,
    ) -> None:
        """
        Initialize the base client.

        Parameters
        ----------
        base_url : str
            Base URL of the API.
        downloader : BaseDownloader | None, optional
            Downloader used to perform HTTP requests.
            If None, a new BaseDownloader is created.
        default_headers : dict[str, str] | None, optional
            Default headers included in every request.
        """
        self._base_url = base_url.rstrip("/") + "/"
        self._downloader = downloader or BaseDownloader()
        self._default_headers = default_headers or {}

    @property
    def base_url(self) -> str:
        """
        Base URL for the API.
        """
        return self._base_url

    @property
    def downloader(self) -> BaseDownloader:
        """
        HTTP downloader used by this client.
        """
        return self._downloader

    def build_url(self, endpoint: str) -> str:
        """
        Build a complete URL from an endpoint.

        Parameters
        ----------
        endpoint : str
            API endpoint.

        Returns
        -------
        str
            Complete URL.
        """
        return urljoin(self._base_url, endpoint.lstrip("/"))

    def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        timeout: int | None = None,
    ) -> ResponseData:
        """
        Send a GET request.

        Parameters
        ----------
        endpoint : str
            API endpoint.
        params : dict[str, Any] | None, optional
            Query parameters.
        headers : dict[str, str] | None, optional
            Request headers.
        timeout : int | None, optional
            Request timeout in seconds.

        Returns
        -------
        ResponseData
            HTTP response.
        """
        merged_headers = {
            **self._default_headers,
            **(headers or {}),
        }

        return self.downloader.get(
            url=self.build_url(endpoint),
            params=params,
            headers=merged_headers,
            timeout=timeout,
        )