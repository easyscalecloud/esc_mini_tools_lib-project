# esc_mini_tools_lib public API reference

All symbols below are re-exported from `esc_mini_tools_lib/api.py` and are the
only supported entry points. Every tool is a Pydantic v2 `BaseModel` pair:
`XxxInput.main() -> XxxOutput`, and every `XxxOutput` carries `input` (the
originating `XxxInput`) plus the payload field.

`AddUpTwoNumberInput.main()` and `CountLlmTokenInput.main()` emit debug lines to
stdout through the module-level `vislog` logger in
`esc_mini_tools_lib/logger.py`. Silence it there if the output is unwanted.

---

## AddUpTwoNumberInput

```python
class AddUpTwoNumberInput(BaseModel):
    v1: int | float
    v2: int | float

    def main(self) -> AddUpTwoNumberOutput: ...
```

Adds `v1 + v2`. Both fields are required. The declared type is `T_NUM =
Union[int, float]`, so Pydantic coerces numeric strings such as `"10"` to `int`.

## AddUpTwoNumberOutput

```python
class AddUpTwoNumberOutput(BaseModel):
    input: AddUpTwoNumberInput
    result: int | float
```

---

## ChineseToEnglishPunctuationInput

```python
class ChineseToEnglishPunctuationInput(BaseModel):
    text: str

    def main(self) -> ChineseToEnglishPunctuationOutput: ...
```

Converts Chinese full-width punctuation to English ASCII punctuation and
normalizes spacing. Handles `，、。：；？！（）“”`, collapses runs of 2–3
identical `。？！` into `...` / `???` / `!!!`, inserts a space between adjacent
CJK and ASCII letters or digits, and strips spaces inside Markdown `**bold**`
markers.

Processing is **line by line**, and these invariants matter for Markdown and
reStructuredText input:

- **Leading indentation is preserved verbatim** (spaces and tabs), so fenced
  code blocks and indented literal blocks survive intact.
- Trailing whitespace is stripped; whitespace-only lines become empty lines.
- A trailing newline on the input is not preserved (`str.splitlines()` +
  `"\n".join()`).
- Content inside code blocks is **not** skipped — punctuation is converted
  everywhere, including inside fences. Only indentation is protected.

## ChineseToEnglishPunctuationOutput

```python
class ChineseToEnglishPunctuationOutput(BaseModel):
    input: ChineseToEnglishPunctuationInput
    result: str
```

---

## ConfluenceUrlTransformInput

```python
class ConfluenceUrlTransformInput(BaseModel):
    url: str

    def main(self) -> ConfluenceUrlTransformOutput: ...
```

Detects which of four Confluence URL shapes `url` is, extracts the page id, and
rebuilds it as `https://{domain}/wiki/rest/api/content/{pageId}?expand=body.atlas_doc_format`.
Recognized shapes: standard `/spaces/{space}/pages/{id}/{title}`, the same with
a query string, edit `/spaces/{space}/pages/edit-v2/{id}`, and draft
`/pages/resumedraft.action?draftId={id}`.

Never raises on a malformed URL — an unrecognized URL yields
`success=False`, `api_url=None`, `pattern=UNKNOWN`. Always check `success`.

## ConfluenceUrlTransformOutput

```python
class ConfluenceUrlTransformOutput(BaseModel):
    input: ConfluenceUrlTransformInput
    pattern: ConfluenceUrlPattern   # str Enum: standard_page | page_with_query | edit_page | draft_page | unknown
    api_url: str | None
    success: bool
```

`pattern` is a `str`-subclassing Enum, so it compares equal to its string value.

---

## ConfluencePageExportInput

```python
class ConfluencePageExportInput(BaseModel):
    records: list[Record]
    wanted_fields: list[str] | None = None

    def main(self) -> ConfluencePageExportOutput: ...
```

Takes pages you have **already fetched** from the Confluence REST API (this
library does no HTTP) and renders each one to markdown and XML.

`.main()` mutates the records in place: for each record it assigns
`record.md`, `record.xml`, and sets `record.success = True`. **Failures are
swallowed** — a record that raises during rendering is silently skipped with
`success` left `False`, and nothing is logged. Inspect `record.success` per
record rather than trusting the returned text to be complete.

`wanted_fields` is currently accepted but not applied by `.main()`.

### Supporting type: `Record`

`Record` is required to build `ConfluencePageExportInput` but is **not**
re-exported from `api.py`; import it from
`esc_mini_tools_lib.tools.confluence_export`.

```python
class Record(BaseModel):
    url: str                      # the original Confluence page URL
    page_data: dict[str, Any]     # raw REST API response for the page
    xml: str | None = None        # populated by ConfluencePageExportInput.main()
    md: str | None = None         # populated by ConfluencePageExportInput.main()
    success: bool = False

    site_url: str                 # cached_property — scheme + netloc of url
    get_page_response: GetPageResponse   # cached_property
    title: str                    # cached_property — page title
    atlas_doc_data: dict[str, Any]       # cached_property — parsed atlas_doc_format body
    webui_url: str                # cached_property — full web UI URL
    md_value: str                 # cached_property — markdown, prefixed with "# {title}"
    xml_value: str                # cached_property — <document> XML wrapping the markdown
```

`md`/`xml` are plain assignable fields while `md_value`/`xml_value` are the
computed `cached_property` versions — the split exists so frontends that rely on
the type system can assign the fields directly. Reading `md_value`/`xml_value`
on incomplete `page_data` will raise; that is the failure `.main()` swallows.

## ConfluencePageExportOutput

```python
class ConfluencePageExportOutput(BaseModel):
    input: ConfluencePageExportInput
    text: str    # "\n".join of every successfully rendered record.xml
```

---

## CountLlmTokenInput

```python
class CountLlmTokenInput(BaseModel):
    text: str

    def main(self) -> CountLlmTokenOutput: ...
```

Counts tokens with `tiktoken.encoding_for_model("gpt-4o")`. The encoding is
hardcoded — there is no parameter to select a different model. The first call in
a process may download the encoding file, which needs network access.

## CountLlmTokenOutput

```python
class CountLlmTokenOutput(BaseModel):
    input: CountLlmTokenInput
    result: int
```

---

## Key scenarios

**Run any tool.** Every tool is the same three lines:

```python
from esc_mini_tools_lib.api import CountLlmTokenInput

output = CountLlmTokenInput(text="Hello world!").main()
print(output.result)        # 3
print(output.input.text)    # round-trip back to the input
```

**Clean up a mixed Chinese/English Markdown document without breaking code blocks.**

```python
from esc_mini_tools_lib.api import ChineseToEnglishPunctuationInput

src = '```python\ndef f(a, b):\n    """中文，注释。"""\n    return a + b\n```'
print(ChineseToEnglishPunctuationInput(text=src).main().result)
# ```python
# def f(a, b):
#     """中文, 注释. """
#     return a + b
# ```
```

**Export Confluence pages: URL -> fetch -> render.** The library converts the
URL and renders the payload; fetching is yours to do.

```python
from esc_mini_tools_lib.api import (
    ConfluenceUrlTransformInput,
    ConfluencePageExportInput,
)
from esc_mini_tools_lib.tools.confluence_export import Record

transform = ConfluenceUrlTransformInput(url=page_url).main()
if not transform.success:
    raise ValueError(f"unsupported URL: {page_url}")

page_data = your_http_client.get(transform.api_url).json()   # not provided by this library

record = Record(url=page_url, page_data=page_data)
export = ConfluencePageExportInput(records=[record]).main()

if record.success:          # check per record; main() swallows failures
    print(record.md)        # markdown
    print(export.text)      # concatenated XML of all successful records
```
