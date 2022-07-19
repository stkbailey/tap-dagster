"""GraphQL client handling, including DagsterStream base class."""

import pendulum
import requests
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk.exceptions import FatalAPIError, RetriableAPIError
from singer_sdk.streams import GraphQLStream


class DagsterStream(GraphQLStream):
    """Dagster stream class."""

    next_page_token_jsonpath = "$.data.runsOrError.results[-1].runId"

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config["api_url"]

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        headers["Dagster-Cloud-Api-Token"] = self.config.get("auth_token")
        return headers

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        return {
            "afterCursor": next_page_token or "",
            "updatedAfter": pendulum.instance(self.get_starting_timestamp(context)).float_timestamp,
        }

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        # TODO: Use records JSONPath instead.
        resp_json = response.json()
        for row in resp_json.get("data", {}).get("runsOrError", {}).get("results"):  # TODO: Generalize for any stream
            row["startTime"] = pendulum.from_timestamp(row["startTime"])
            if row["endTime"]:
                row["endTime"] = pendulum.from_timestamp(row["endTime"])
            yield row

    def validate_response(self, response: requests.Response) -> None:
        if (
            response.status_code in self.extra_retry_statuses
            or 500 <= response.status_code < 600
        ):
            msg = self.response_error_message(response)
            details = response.json().get("errors", [])[0].get("message")
            error_msg = f"{msg} - {details}"
            raise RetriableAPIError(error_msg, response)
        elif 400 <= response.status_code < 500:
            msg = self.response_error_message(response)
            details = response.json().get("errors", [])[0].get("message")
            error_msg = f"{msg} - {details}"
            raise FatalAPIError(error_msg)

    def post_process(self, row: dict, context: Optional[dict] = None) -> dict:
        """As needed, append or transform raw data to match expected structure."""
        # TODO: Delete this method if not needed.
        return row
