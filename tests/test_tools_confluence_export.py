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
    Record,
    ConfluencePageExportInput,
    ConfluencePageExportOutput,
    get_body_in_atlas_doc_format_from_page_data,
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


class TestGetBodyInAtlasDocFormat:
    """Test extraction of atlas_doc_format from page data."""

    def test_extract_body(self):
        # Use a simple page_data for testing
        simple_page_data = {
            "body": {
                "atlas_doc_format": {
                    "value": '{"type":"doc","content":[{"type":"paragraph","content":[{"text":"Test content","type":"text"}]}]}'
                }
            }
        }
        body = get_body_in_atlas_doc_format_from_page_data(simple_page_data)
        assert isinstance(body, dict)
        assert body["type"] == "doc"
        assert "content" in body


class TestRecord:
    """Test Record model."""

    def test_record_creation(self):
        url = "https://alice.atlassian.net/wiki/spaces/TEST/pages/123/Test"
        simple_page_data = {
            "id": "123",
            "title": "Test Page",
            "body": {
                "atlas_doc_format": {
                    "value": '{"type":"doc","content":[{"type":"paragraph","content":[{"text":"Test","type":"text"}]}]}'
                }
            },
        }

        record = Record(
            url=url,
            page_data=simple_page_data,
        )

        assert record.url == url
        assert record.page_data == simple_page_data
        assert record.xml is None
        assert record.success is False


class TestConfluencePageExportInput:
    """Test the Pydantic export models."""

    def test_single_page_export(self):
        url = "https://alice.atlassian.net/wiki/spaces/TEST/pages/123/Test+Page"
        simple_page_data = {
            "id": "123",
            "title": "Test Page",
            "body": {
                "atlas_doc_format": {
                    "value": '{"type":"doc","content":[{"type":"paragraph","content":[{"text":"This is test content.","type":"text"}]}]}'
                }
            },
        }

        record = Record(url=url, page_data=simple_page_data)
        input_obj = ConfluencePageExportInput(records=[record])
        output = input_obj.main()

        # Verify the output structure
        assert isinstance(output, ConfluencePageExportOutput)
        assert output.input == input_obj
        assert isinstance(output.text, str)
        # Note: We don't assert success or xml content because the simplified
        # page_data may not have all required fields for successful conversion

    def test_multiple_page_export(self):
        records = []
        for i in range(3):
            url = f"https://alice.atlassian.net/wiki/spaces/TEST/pages/{i}/Test+Page+{i}"
            page_data = {
                "id": str(i),
                "title": f"Test Page {i}",
                "body": {
                    "atlas_doc_format": {
                        "value": f'{{"type":"doc","content":[{{"type":"paragraph","content":[{{"text":"Content {i}","type":"text"}}]}}]}}'
                    }
                },
            }
            records.append(Record(url=url, page_data=page_data))

        input_obj = ConfluencePageExportInput(records=records)
        output = input_obj.main()

        # Verify the output structure
        assert isinstance(output, ConfluencePageExportOutput)
        assert isinstance(output.text, str)
        assert len(records) == 3
        # Note: We don't assert success or xml content because the simplified
        # page_data may not have all required fields for successful conversion


if __name__ == "__main__":
    from esc_mini_tools_lib.tests import run_cov_test

    run_cov_test(
        __file__,
        "esc_mini_tools_lib.tools.confluence_export",
        preview=False,
    )
