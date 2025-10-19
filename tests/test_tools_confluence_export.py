# -*- coding: utf-8 -*-

from esc_mini_tools_lib.tools.confluence_export import (
    ConfluenceUrlPattern,
    identify_url_pattern,
    extract_page_id_from_standard_url,
    extract_page_id_from_page_with_query_url,
    extract_page_id_from_edit_url,
    extract_page_id_from_draft_url,
    convert_to_api_url,
    ConfluenceUrlTransformInput,
    ConfluenceUrlTransformOutput,
)


class TestIdentifyUrlPattern:
    """Test URL pattern identification."""

    def test_standard_page(self):
        url = "https://alice.atlassian.net/wiki/spaces/MYSPACE/pages/123456789/My+Document+Title"
        pattern = identify_url_pattern(url)
        assert pattern == ConfluenceUrlPattern.STANDARD_PAGE

    def test_page_with_query(self):
        url = "https://alice.atlassian.net/wiki/spaces/MYSPACE/pages/123456789/My+Document+Title?atlOrigin=eyJpIjoiM2ZhNjA0OWNlZTA4NGYxZGIxNTQ4NzAwNjczYmJhNWUiLCJwIjoiYyJ9"
        pattern = identify_url_pattern(url)
        assert pattern == ConfluenceUrlPattern.PAGE_WITH_QUERY

    def test_edit_page(self):
        url = "https://alice.atlassian.net/wiki/spaces/MYSPACE/pages/edit-v2/123456789"
        pattern = identify_url_pattern(url)
        assert pattern == ConfluenceUrlPattern.EDIT_PAGE

    def test_draft_page(self):
        url = "https://alice.atlassian.net/wiki/pages/resumedraft.action?draftId=123456789"
        pattern = identify_url_pattern(url)
        assert pattern == ConfluenceUrlPattern.DRAFT_PAGE

    def test_unknown_pattern(self):
        url = "https://alice.atlassian.net/wiki/some/unknown/path"
        pattern = identify_url_pattern(url)
        assert pattern == ConfluenceUrlPattern.UNKNOWN


class TestExtractPageIdFromStandardUrl:
    """Test page ID extraction from standard URLs."""

    def test_standard_url(self):
        url = "https://alice.atlassian.net/wiki/spaces/MYSPACE/pages/123456789/My+Document+Title"
        page_id = extract_page_id_from_standard_url(url)
        assert page_id == "123456789"

    def test_invalid_url(self):
        url = "https://alice.atlassian.net/wiki/some/invalid/path"
        page_id = extract_page_id_from_standard_url(url)
        assert page_id is None


class TestExtractPageIdFromPageWithQueryUrl:
    """Test page ID extraction from URLs with query parameters."""

    def test_page_with_query(self):
        url = "https://alice.atlassian.net/wiki/spaces/MYSPACE/pages/123456789/My+Document+Title?atlOrigin=eyJpIjoiM2ZhNjA0OWNlZTA4NGYxZGIxNTQ4NzAwNjczYmJhNWUiLCJwIjoiYyJ9"
        page_id = extract_page_id_from_page_with_query_url(url)
        assert page_id == "123456789"

    def test_invalid_url(self):
        url = "https://alice.atlassian.net/wiki/some/invalid/path?param=value"
        page_id = extract_page_id_from_page_with_query_url(url)
        assert page_id is None


class TestExtractPageIdFromEditUrl:
    """Test page ID extraction from edit URLs."""

    def test_edit_url(self):
        url = "https://alice.atlassian.net/wiki/spaces/MYSPACE/pages/edit-v2/123456789"
        page_id = extract_page_id_from_edit_url(url)
        assert page_id == "123456789"

    def test_invalid_url(self):
        url = "https://alice.atlassian.net/wiki/some/invalid/path"
        page_id = extract_page_id_from_edit_url(url)
        assert page_id is None


class TestExtractPageIdFromDraftUrl:
    """Test page ID extraction from draft URLs."""

    def test_draft_url(self):
        url = "https://alice.atlassian.net/wiki/pages/resumedraft.action?draftId=123456789"
        page_id = extract_page_id_from_draft_url(url)
        assert page_id == "123456789"

    def test_url_without_draft_id(self):
        url = "https://alice.atlassian.net/wiki/pages/resumedraft.action?otherparam=value"
        page_id = extract_page_id_from_draft_url(url)
        assert page_id is None


class TestConvertToApiUrl:
    """Test URL conversion to API format."""

    def test_standard_page_conversion(self):
        url = "https://alice.atlassian.net/wiki/spaces/MYSPACE/pages/123456789/My+Document+Title"
        api_url = convert_to_api_url(url)
        expected = "https://alice.atlassian.net/wiki/rest/api/content/123456789?expand=body.atlas_doc_format"
        assert api_url == expected

    def test_page_with_query_conversion(self):
        url = "https://alice.atlassian.net/wiki/spaces/MYSPACE/pages/123456789/My+Document+Title?atlOrigin=eyJpIjoiM2ZhNjA0OWNlZTA4NGYxZGIxNTQ4NzAwNjczYmJhNWUiLCJwIjoiYyJ9"
        api_url = convert_to_api_url(url)
        expected = "https://alice.atlassian.net/wiki/rest/api/content/123456789?expand=body.atlas_doc_format"
        assert api_url == expected

    def test_edit_page_conversion(self):
        url = "https://alice.atlassian.net/wiki/spaces/MYSPACE/pages/edit-v2/123456789"
        api_url = convert_to_api_url(url)
        expected = "https://alice.atlassian.net/wiki/rest/api/content/123456789?expand=body.atlas_doc_format"
        assert api_url == expected

    def test_draft_page_conversion(self):
        url = "https://alice.atlassian.net/wiki/pages/resumedraft.action?draftId=123456789"
        api_url = convert_to_api_url(url)
        expected = "https://alice.atlassian.net/wiki/rest/api/content/123456789?expand=body.atlas_doc_format"
        assert api_url == expected

    def test_invalid_url_conversion(self):
        url = "https://alice.atlassian.net/wiki/some/invalid/path"
        api_url = convert_to_api_url(url)
        assert api_url is None


class TestConfluenceUrlTransformInput:
    """Test the Pydantic input/output models."""

    def test_successful_transformation(self):
        input_obj = ConfluenceUrlTransformInput(
            url="https://alice.atlassian.net/wiki/spaces/MYSPACE/pages/123456789/My+Document+Title"
        )
        output = input_obj.main()

        assert isinstance(output, ConfluenceUrlTransformOutput)
        assert output.success is True
        assert output.pattern == ConfluenceUrlPattern.STANDARD_PAGE
        assert output.api_url == "https://alice.atlassian.net/wiki/rest/api/content/123456789?expand=body.atlas_doc_format"
        assert output.input == input_obj

    def test_failed_transformation(self):
        input_obj = ConfluenceUrlTransformInput(
            url="https://alice.atlassian.net/wiki/invalid/path"
        )
        output = input_obj.main()

        assert isinstance(output, ConfluenceUrlTransformOutput)
        assert output.success is False
        assert output.pattern == ConfluenceUrlPattern.UNKNOWN
        assert output.api_url is None
        assert output.input == input_obj


if __name__ == "__main__":
    from esc_mini_tools_lib.tests import run_cov_test

    run_cov_test(
        __file__,
        "esc_mini_tools_lib.tools.confluence_export",
        preview=False,
    )
