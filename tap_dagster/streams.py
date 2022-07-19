"""Stream type classes for tap-dagster."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_dagster.client import DagsterStream


class RunsStream(DagsterStream):
    """Define custom stream."""
    name = "runs"
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"
    schema = th.PropertiesList(
        th.Property("name", th.StringType),
        th.Property(
            "runId",
            th.StringType,
            description=""
        ),
        th.Property(
            "jobName",
            th.StringType,
            description=""
        ),
        th.Property(
            "startTime",
            th.DateTimeType,
            description=""
        ),
        th.Property(
            "endTime",
            th.DateTimeType,
            description=""
        ),
        th.Property(
            "status",
            th.StringType,
            description=""
        ),
        th.Property(
            "mode",
            th.StringType,
            description=""
        ),
    ).to_dict()
    primary_keys = ["id"]
    replication_key = "startTime"
    query = """
        query ($afterCursor: String!, $updatedAfter: Float!) {
            runsOrError(
                filter: {updatedAfter: $updatedAfter} 
                cursor: $afterCursor
                limit: 10
            ) { 
                __typename
                ... on Runs {
                    results {
                        runId
                        jobName
                        startTime
                        endTime
                        status
                        mode
                        assetMaterializations {
                            timestamp
                            metadataEntries {
                                label
                            }
                        }
                    }
                }
            }
        }
        """
