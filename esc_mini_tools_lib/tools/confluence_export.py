# -*- coding: utf-8 -*-

"""
Confluence Export Tool - URL Transformation Module

This module provides functionality to convert various Confluence page URL formats
to the REST API format for exporting page content.
"""

import typing as T
import re
import json
from enum import Enum
from functools import cached_property
from urllib.parse import urlparse, parse_qs

from pydantic import BaseModel, Field
from atlas_doc_parser.api import NodeDoc
from docpack_confluence.api import Page, Entity, ConfluencePageFieldEnum
from sanhe_confluence_sdk.methods.page.get_page import GetPageResponse


# ------------------------------------------------------------------------------
# URL converter
# ------------------------------------------------------------------------------
class ConfluenceUrlPattern(str, Enum):
    """Enum representing different Confluence URL patterns."""

    # fmt: off
    STANDARD_PAGE = "standard_page"  # /spaces/{space}/pages/{id}/{title}
    PAGE_WITH_QUERY = "page_with_query"  # /spaces/{space}/pages/{id}/{title}?param=value
    EDIT_PAGE = "edit_page"  # /spaces/{space}/pages/edit-v2/{id}
    DRAFT_PAGE = "draft_page"  # /pages/resumedraft.action?draftId={id}
    UNKNOWN = "unknown"
    # fmt: on


def identify_url_pattern(url: str) -> ConfluenceUrlPattern:
    """
    Identify which Confluence URL pattern the given URL matches.

    :param url: The Confluence page URL to identify
    :return: The pattern type as a ConfluenceUrlPattern enum value

    Examples:
        >>> identify_url_pattern("https://domain.atlassian.net/wiki/spaces/SPACE/pages/123/Title")
        ConfluenceUrlPattern.STANDARD_PAGE

        >>> identify_url_pattern("https://domain.atlassian.net/wiki/spaces/SPACE/pages/123/Title?atlOrigin=xyz")
        ConfluenceUrlPattern.PAGE_WITH_QUERY

        >>> identify_url_pattern("https://domain.atlassian.net/wiki/spaces/SPACE/pages/edit-v2/123")
        ConfluenceUrlPattern.EDIT_PAGE

        >>> identify_url_pattern("https://domain.atlassian.net/wiki/pages/resumedraft.action?draftId=123")
        ConfluenceUrlPattern.DRAFT_PAGE
    """
    try:
        parsed = urlparse(url)
        path = parsed.path
        query = parsed.query

        # Pattern 4: Draft page - /pages/resumedraft.action?draftId={id}
        if "/pages/resumedraft.action" in path and "draftId=" in query:
            return ConfluenceUrlPattern.DRAFT_PAGE

        # Pattern 3: Edit page - /spaces/{space}/pages/edit-v2/{id}
        if "/pages/edit-v2/" in path:
            return ConfluenceUrlPattern.EDIT_PAGE

        # Pattern 1 & 2: Standard page - /spaces/{space}/pages/{id}/{title}
        # Use regex to match the pattern
        standard_pattern = r"/spaces/[^/]+/pages/\d+"
        if re.search(standard_pattern, path):
            if query:
                return ConfluenceUrlPattern.PAGE_WITH_QUERY
            else:
                return ConfluenceUrlPattern.STANDARD_PAGE

        return ConfluenceUrlPattern.UNKNOWN

    except Exception:
        return ConfluenceUrlPattern.UNKNOWN


def extract_page_id_from_standard_url(url: str) -> str | None:
    """
    Extract page ID from standard Confluence page URL.

    Pattern: https://{domain}/wiki/spaces/{space}/pages/{pageId}/{title}

    :param url: Standard Confluence page URL
    :return: Page ID as string, or None if extraction fails
    """
    pattern = r"/spaces/[^/]+/pages/(\d+)"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None


def extract_page_id_from_page_with_query_url(url: str) -> str | None:
    """
    Extract page ID from Confluence page URL with query parameters.

    Pattern: https://{domain}/wiki/spaces/{space}/pages/{pageId}/{title}?param=value

    :param url: Confluence page URL with query parameters
    :return: Page ID as string, or None if extraction fails
    """
    # Same logic as standard URL since query params don't affect the path
    return extract_page_id_from_standard_url(url)


def extract_page_id_from_edit_url(url: str) -> str | None:
    """
    Extract page ID from Confluence edit page URL.

    Pattern: https://{domain}/wiki/spaces/{space}/pages/edit-v2/{pageId}

    :param url: Confluence edit page URL
    :return: Page ID as string, or None if extraction fails
    """
    pattern = r"/pages/edit-v2/(\d+)"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None


def extract_page_id_from_draft_url(url: str) -> str | None:
    """
    Extract page ID from Confluence draft page URL.

    Pattern: https://{domain}/wiki/pages/resumedraft.action?draftId={pageId}

    :param url: Confluence draft page URL
    :return: Page ID as string, or None if extraction fails
    """
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    draft_id = query_params.get("draftId", [None])[0]
    return draft_id


def convert_to_api_url(url: str) -> str | None:
    """
    Convert any supported Confluence page URL to REST API format.

    Target format: https://{domain}/wiki/rest/api/content/{pageId}?expand=body.atlas_doc_format

    :param url: Any supported Confluence page URL
    :return: REST API URL, or None if conversion fails

    Examples:
        >>> url = "https://sanhehu.atlassian.net/wiki/spaces/TECHGARDEN/pages/461242370/Title"
        >>> convert_to_api_url(url)
        'https://sanhehu.atlassian.net/wiki/rest/api/content/461242370?expand=body.atlas_doc_format'
    """
    # Identify the URL pattern
    pattern = identify_url_pattern(url)

    # Extract page ID based on pattern
    page_id = None
    if pattern == ConfluenceUrlPattern.STANDARD_PAGE:
        page_id = extract_page_id_from_standard_url(url)
    elif pattern == ConfluenceUrlPattern.PAGE_WITH_QUERY:
        page_id = extract_page_id_from_page_with_query_url(url)
    elif pattern == ConfluenceUrlPattern.EDIT_PAGE:
        page_id = extract_page_id_from_edit_url(url)
    elif pattern == ConfluenceUrlPattern.DRAFT_PAGE:
        page_id = extract_page_id_from_draft_url(url)

    if not page_id:
        return None

    # Extract base domain from original URL
    parsed = urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"

    # Construct REST API URL
    api_url = f"{base_url}/wiki/rest/api/content/{page_id}?expand=body.atlas_doc_format"
    return api_url


class ConfluenceUrlTransformInput(BaseModel):
    """Input model for Confluence URL transformation."""

    url: str = Field(
        description="The Confluence page URL to transform to REST API format"
    )

    def main(self):
        """
        Transform the Confluence URL to REST API format.

        :return: ConfluenceUrlTransformOutput with the transformation result
        """
        pattern = identify_url_pattern(self.url)
        api_url = convert_to_api_url(self.url)

        return ConfluenceUrlTransformOutput(
            input=self,
            pattern=pattern,
            api_url=api_url,
            success=api_url is not None,
        )


class ConfluenceUrlTransformOutput(BaseModel):
    """Output model for Confluence URL transformation."""

    input: ConfluenceUrlTransformInput = Field(description="The original input")
    pattern: ConfluenceUrlPattern = Field(description="The identified URL pattern type")
    api_url: str | None = Field(
        description="The transformed REST API URL, or None if transformation failed"
    )
    success: bool = Field(description="Whether the transformation was successful")


# ------------------------------------------------------------------------------
# API response to markdown
# ------------------------------------------------------------------------------
def get_body_in_atlas_doc_format_from_page_data(
    page_data: dict[str, T.Any],
) -> dict[str, T.Any]:
    return json.loads(page_data["body"]["atlas_doc_format"]["value"])


class Record(BaseModel):
    """
    A data model representing a single Confluence page record.

    This model wraps the raw page data from the Confluence REST API and provides
    derived properties for accessing the page title, atlas doc data, web UI URL,
    markdown content, and structured XML output. The ``md`` and ``xml`` fields
    are regular Pydantic fields (not cached properties) so that they can be
    assigned by the caller — this is required because frontend applications
    depend on the type system and need assignable fields.

    :param url: The original Confluence page URL.
    :param page_data: The raw page data dictionary from the Confluence REST API.
    :param xml: The structured XML output of the page content. Populated by
        :meth:`ConfluencePageExportInput.main`.
    :param md: The markdown representation of the page content. Populated by
        :meth:`ConfluencePageExportInput.main`.
    :param success: Whether the export was successful. Set to ``True`` by
        :meth:`ConfluencePageExportInput.main` after successful processing.

    .. versionchanged:: 0.1.9

        Refactored to use ``GetPageResponse`` and ``NodeDoc`` for deriving
        title, atlas doc data, web UI URL, markdown, and XML content.

    .. versionchanged:: 0.1.10

        Renamed ``md`` and ``xml`` cached properties to ``md_value`` and
        ``xml_value``. Added ``md`` and ``xml`` as regular Pydantic fields
        so they can be assigned by the caller.
    """

    url: str = Field()
    page_data: dict[str, T.Any] = Field()
    xml: str | None = Field(default=None)
    md: str | None = Field(default=None)
    success: bool = Field(default=False)

    @cached_property
    def site_url(self) -> str:
        """
        Derive the site base URL from the page URL.

        :return: The base URL (scheme + netloc), e.g. ``https://domain.atlassian.net``.
        """
        return "/".join(self.url.split("/")[:3])

    @cached_property
    def get_page_response(self) -> GetPageResponse:
        """
        Parse the raw page data into a ``GetPageResponse`` object.

        :return: A ``GetPageResponse`` instance wrapping the raw page data.
        """
        return GetPageResponse(_raw_data=self.page_data)

    @cached_property
    def title(self) -> str:
        """
        Get the page title from the API response.

        :return: The page title string.
        """
        return self.get_page_response.title

    @cached_property
    def atlas_doc_data(self) -> dict[str, T.Any]:
        """
        Parse the atlas_doc_format body from the API response.

        :return: A dictionary representing the atlas doc format content.
        """
        return json.loads(self.get_page_response.body.atlas_doc_format.value)

    @cached_property
    def webui_url(self) -> str:
        """
        Construct the full web UI URL for the Confluence page.

        :return: The web UI URL, e.g.
            ``https://domain.atlassian.net/wiki/spaces/SPACE/pages/123/Title``.
        """
        return f"{self.site_url}/wiki{self.get_page_response.links.webui}"

    @cached_property
    def md_value(self) -> str:
        """
        Generate the markdown content from the atlas doc data.

        Converts the atlas doc format to markdown using ``NodeDoc`` and
        prepends a level-1 heading with the page title.

        :return: The markdown string with title header.

        .. versionchanged:: 0.1.10

            Renamed from ``md`` to ``md_value`` to avoid conflict with the
            ``md`` Pydantic field.
        """
        node_doc = NodeDoc.from_dict(
            dct=self.atlas_doc_data,
        )
        md = node_doc.to_markdown(ignore_error=True)
        lines = [
            f"# {self.title}",
            "",
        ]
        lines.extend(md.splitlines())
        md = "\n".join(lines)
        return md.rstrip()

    @cached_property
    def xml_value(self) -> str:
        """
        Generate the structured XML output from the page content.

        Produces an XML document with fields defined by
        ``ConfluencePageFieldEnum``, including source type, Confluence URL,
        title, and markdown content.

        :return: The XML string representing the page content.

        .. versionchanged:: 0.1.10

            Renamed from ``xml`` to ``xml_value`` to avoid conflict with the
            ``xml`` Pydantic field.
        """
        TAB = " " * 2
        lines = list()
        lines.append("<document>")

        field = ConfluencePageFieldEnum.source_type.value
        lines.append(f"{TAB}<{field}>Confluence Page</{field}>")

        field = ConfluencePageFieldEnum.confluence_url.value
        lines.append(f"{TAB}<{field}>{self.webui_url}</{field}>")

        field = ConfluencePageFieldEnum.title.value
        lines.append(f"{TAB}<{field}>{self.title}</{field}>")

        field = ConfluencePageFieldEnum.markdown_content.value
        lines.append(f"{TAB}<{field}>")
        lines.append(self.md_value)
        lines.append(f"{TAB}</{field}>")

        lines.append("</document>")

        return "\n".join(lines)


class ConfluencePageExportInput(BaseModel):
    """
    Input model for exporting Confluence page content.

    Takes a list of :class:`Record` objects and processes each one to generate
    markdown and XML representations. After processing, each record's ``md``,
    ``xml``, and ``success`` fields are populated.

    :param records: A list of :class:`Record` objects to export.
    :param wanted_fields: An optional list of field names to include in the
        export output. If ``None``, all fields are included.

    .. versionchanged:: 0.1.9

        Updated to use ``Record.xml`` for export output instead of the old
        ``ConfluencePage`` helper.

    .. versionchanged:: 0.1.10

        Updated to assign ``record.md`` and ``record.xml`` from
        ``record.md_value`` and ``record.xml_value`` respectively.
    """

    records: list[Record] = Field()
    wanted_fields: list[str] | None = Field(default=None)

    def main(self) -> "ConfluencePageExportOutput":
        """
        Export all records to structured XML and markdown.

        Iterates over each :class:`Record`, computes the XML and markdown
        content via ``xml_value`` and ``md_value``, assigns them to the
        record's ``xml`` and ``md`` fields, and marks the record as successful.
        If an error occurs during processing, the record is skipped.

        :return: A :class:`ConfluencePageExportOutput` containing the
            concatenated XML text of all successfully exported records.
        """
        docs = list()
        for record in self.records:
            try:
                record.xml = record.xml_value
                record.md = record.md_value
                docs.append(record.xml)
                record.success = True
            except Exception as e:
                pass
        text = "\n".join(docs)
        return ConfluencePageExportOutput(
            input=self,
            text=text,
        )


class ConfluencePageExportOutput(BaseModel):
    """
    Output model for Confluence page export.

    Contains the original input and the concatenated XML text of all
    successfully exported records.

    :param input: The original :class:`ConfluencePageExportInput`.
    :param text: The concatenated XML output of all successfully processed
        records.

    .. versionchanged:: 0.1.9

        Updated to contain XML output generated from ``Record.xml``.
    """

    input: ConfluencePageExportInput = Field()
    text: str = Field()
