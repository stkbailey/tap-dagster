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
            "updateTime",
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
        th.Property(
            "solidSelection",
            th.StringType,
            description=""
        ),
        th.Property(
            "stepKeysToExecute",
            th.StringType,
            description=""
        ),
        # th.Property(
        #     "runConfig",
        #     th.StringType,
        #     description=""
        # ),
        th.Property(
            "runConfigYaml",
            th.StringType,
            description=""
        ),
        th.Property(
            "repositoryOrigin",
            th.ObjectType(
                th.Property(
                    "id",
                    th.StringType,
                    description=""
                ),
                th.Property(
                    "repositoryLocationName",
                    th.StringType,
                    description=""
                ),
                th.Property(
                    "repositoryName",
                    th.StringType,
                    description=""
                )
            ),
            description=""
        ),
        th.Property(
            "stats",
            th.ObjectType(
                th.Property(
                    "stepsSucceeded",
                    th.IntegerType,
                    description=""
                ),
                th.Property(
                    "stepsFailed",
                    th.IntegerType,
                    description=""
                ),
                th.Property(
                    "materializations",
                    th.IntegerType,
                    description=""
                ),
                th.Property(
                    "expectations",
                    th.IntegerType,
                    description=""
                ),
                th.Property(
                    "enqueuedTime",
                    th.NumberType,
                    description=""
                ),
                th.Property(
                    "launchTime",
                    th.NumberType,
                    description=""
                ),
                th.Property(
                    "startTime",
                    th.NumberType,
                    description=""
                ),
                th.Property(
                    "endTime",
                    th.NumberType,
                    description=""
                )
            )
        ),
        th.Property(
            "assetMaterializations",
            th.ArrayType(
                th.ObjectType(
                    th.Property(
                        "timestamp",
                        th.StringType,
                        description=""
                    ),
                    th.Property(
                        "message",
                        th.StringType,
                        description=""
                    ),
                    th.Property(
                        "level",
                        th.StringType,
                        description=""
                    ),
                    th.Property(
                        "stepKey",
                        th.StringType,
                        description=""
                    ),
                    th.Property(
                        "eventType",
                        th.StringType,
                        description=""
                    ),
                    th.Property(
                        "label",
                        th.StringType,
                        description=""
                    ),
                    th.Property(
                        "description",
                        th.StringType,
                        description=""
                    ),
                    th.Property(
                        "metadataEntries",
                        th.ArrayType(
                            th.ObjectType(
                                th.Property(
                                    "label",
                                    th.StringType,
                                    description=""
                                ),
                                th.Property(
                                    "description",
                                    th.StringType,
                                    description=""
                                ),
                                th.Property(
                                    "typeName",
                                    th.StringType,
                                    description=""
                                ),
                                th.Property(
                                    "boolValue",
                                    th.BooleanType,
                                    description=""
                                ),
                                th.Property(
                                    "floatValue",
                                    th.NumberType,
                                    description=""
                                ),
                                th.Property(
                                    "intValue",
                                    th.IntegerType,
                                    description=""
                                ),
                                th.Property(
                                    "intRepr",
                                    th.StringType,
                                    description=""
                                ),
                                th.Property(
                                    "jsonString",
                                    th.StringType,
                                    description=""
                                ),
                                th.Property(
                                    "mdStr",
                                    th.StringType,
                                    description=""
                                ),
                                th.Property(
                                    "path",
                                    th.StringType,
                                    description=""
                                ),
                                th.Property(
                                    "artifactModule",
                                    th.StringType,
                                    description=""
                                ),
                                th.Property(
                                    "artifactName",
                                    th.StringType,
                                    description=""
                                ),
                                th.Property(
                                    "text",
                                    th.StringType,
                                    description=""
                                ),
                                th.Property(
                                    "url",
                                    th.StringType,
                                    description=""
                                )
                            )
                        )
                    )
                )
            )
        )
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
                        startTime
                        endTime
                        updateTime
                        jobName
                        status
                        mode
                        solidSelection
                        stepKeysToExecute
                        runConfigYaml
                        repositoryOrigin {
                            id
                            repositoryLocationName
                            repositoryName
                        }
                        stats {
                            ... on RunStatsSnapshot {
                                stepsSucceeded
                                stepsFailed
                                materializations
                                expectations
                                enqueuedTime
                                launchTime
                                startTime
                                endTime
                            }
                        }
                        assetMaterializations {
                            timestamp
                            message
                            level
                            stepKey
                            eventType
                            label
                            description
                            metadataEntries {
                                label
                                description
                                typeName: __typename
                                ... on BoolMetadataEntry {
                                    boolValue
                                }
                                ... on FloatMetadataEntry {
                                    floatValue
                                }
                                ... on IntMetadataEntry {
                                    intValue
                                    intRepr
                                }
                                ... on JsonMetadataEntry {
                                    jsonString
                                }
                                ... on MarkdownMetadataEntry {
                                    mdStr
                                }
                                ... on PathMetadataEntry {
                                    path
                                }
                                ... on PythonArtifactMetadataEntry {
                                    artifactModule: module
                                    artifactName: name
                                }
                                ... on TextMetadataEntry {
                                    text
                                }
                                ... on UrlMetadataEntry {
                                    url
                                }
                            }
                        }
                    }
                }
            }
        }
    """
