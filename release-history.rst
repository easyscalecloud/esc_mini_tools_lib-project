.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.1.9 (2026-02-06)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Refactor ``confluence_export`` tool to generate Markdown and XML from ``atlas_doc`` format using the ``atlas_doc_parser`` library.
- Add new ``Record`` model that wraps page data with ``GetPageResponse`` and ``NodeDoc`` to derive:
    - ``title``: Page title from the API response
    - ``atlas_doc_data``: Parsed atlas_doc format data
    - ``webui_url``: Web UI URL for the page
    - ``md``: Markdown content with title header
    - ``xml``: XML output using ``ConfluencePageFieldEnum`` for structured document export
- Update ``ConfluencePageExportInput`` to use ``record.xml`` for export output instead of the old ``ConfluencePage`` helper.

**Dependencies**

- Upgrade ``atlas_doc_parser`` from 0.1.x to 1.0.1 (major version upgrade).
- Replace ``docpack`` with ``docpack-confluence>=0.1.3`` for Confluence-specific document packaging.

**Test Updates**

- Update tests to include ``_links.webui`` field in mock data and assert the generated markdown content.


0.1.8 (2025-10-23)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add ``handle_consecutive_punctuation`` function to handle 2-3 consecutive identical Chinese punctuation marks (e.g., ``。。。`` → ``...``, ``？？？`` → ``???``)
- Add ``find_pair_markers`` and ``remove_spaces_around_paired_markers`` functions to handle spaces inside paired markers like ``**``
- Add ``post_process_paired_markers`` function to remove unwanted spaces inside paired markers after all other processing

**Bugfixes**

- Fix quote spacing bug in ``handle_space_between_chinese_and_english``: ASCII quotes followed by Chinese characters now correctly add space (e.g., ``"Python"是`` → ``"Python" 是``)
- Fix opening/closing quote detection using quote state tracking to properly distinguish between opening quotes (e.g., ``从"A"``) and closing quotes (e.g., ``"你好"``)
- Fix space handling around ASCII punctuation and Chinese characters with special rules for closing punctuation (``,.:;?!``) and opening punctuation (``([{"'``)
- Add handling for Chinese colon inside paired markers: ``**参考资源：**`` now correctly converts to ``**参考资源:**`` without extra space before ``:``

**Test Updates**

- Enable and fix test case for consecutive exclamation marks: ``连续感叹！！！下一句`` → ``连续感叹!!! 下一句``
- Add test cases for consecutive periods and question marks
- Fix test case expectation for ``从"A"到"B"只需1天。`` to include proper spacing around numbers and Chinese characters
- Add test case for mixed Chinese punctuation with paired markers: ``注意：**这很着急，也很重要。**``


0.1.7 (2025-10-21)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Bugfixes**

- Upgrade docpack from 0.1.5 to 0.1.6 to fix another singleton cache issue in diskcache usage.


0.1.6 (2025-10-21)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Bugfixes**

- Upgrade docpack from 0.1.4 to 0.1.5 to fix singleton cache issue in diskcache usage.


0.1.5 (2025-10-20)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add ``count_llm_token`` tool for counting tokens in text using tiktoken (gpt-4o encoding).

**Minor Improvements**

- Add comprehensive unit tests for ``count_llm_token`` tool with 100% code coverage.


0.1.4 (2025-10-19)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Minor Improvements**

- Add optional ``md`` field to ``Record`` model in ``confluence_export`` tool to store markdown content.
- Update ``ConfluencePageExportInput`` export logic to populate markdown field during export.


0.1.3 (2025-10-19)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Bugfixes**

- Fix ``wanted_fields`` default value assignment in ``ConfluencePageExportInput`` to use ``Field(default=None)`` directly.


0.1.2 (2025-10-19)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add ``confluence_export`` tool for transforming Confluence page URLs to REST API format.

**Minor Improvements**

- Add comprehensive unit tests for ``confluence_export`` tool with 95%+ code coverage.


0.1.1 (2025-10-19)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add ``add_up_two_number`` tool for basic arithmetic operations.
- Add ``chinese_to_english_punctuation`` tool for converting Chinese punctuation to English format.

**Miscellaneous**

- First release
