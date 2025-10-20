.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


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
