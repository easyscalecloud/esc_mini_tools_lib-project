---
name: pypi-esc_mini_tools_lib
description: A reusable library of mini tools exposed as Pydantic models, for adding two numbers, converting Chinese full width punctuation into English ASCII punctuation while preserving code block indentation, transforming Confluence page URLs into REST API URLs, exporting Confluence pages into markdown and XML, and counting LLM tokens with tiktoken. Public symbols include AddUpTwoNumberInput, AddUpTwoNumberOutput, ChineseToEnglishPunctuationInput, ChineseToEnglishPunctuationOutput, ConfluenceUrlTransformInput, ConfluenceUrlTransformOutput, ConfluencePageExportInput, ConfluencePageExportOutput, CountLlmTokenInput and CountLlmTokenOutput. Every tool follows one uniform shape where the caller builds an Input model and calls its main method to receive an Output model. Generated for esc_mini_tools_lib version 0.1.11. Higher installed versions should generally be compatible, lower versions may still work but correctness is not guaranteed.
---

# esc_mini_tools_lib

A library of small, self-contained tools with Pydantic-based APIs, designed for
multi-platform deployment in web apps, serverless functions, and AI systems.

**The one idiom that covers the whole library:** every tool is a pair of Pydantic
models. Construct the `*Input` model, call `.main()`, get back the `*Output`
model. `Output.input` always holds the originating input; the payload lives in
`Output.result` (or `Output.text` for the Confluence export).

## Import

```python
from esc_mini_tools_lib.api import AddUpTwoNumberInput
import esc_mini_tools_lib.api as esc_mini_tools_lib   # then esc_mini_tools_lib.AddUpTwoNumberInput
```

## Public API

- `AddUpTwoNumberInput` — Adds two int or float values; call `.main()`.
- `AddUpTwoNumberOutput` — Result of the addition.
- `ChineseToEnglishPunctuationInput` — Converts Chinese full-width punctuation in a text block to English ASCII punctuation with correct spacing; call `.main()`.
- `ChineseToEnglishPunctuationOutput` — The converted text.
- `ConfluenceUrlTransformInput` — Turns any supported Confluence page URL into its REST API URL; call `.main()`.
- `ConfluenceUrlTransformOutput` — The API URL, the detected URL pattern, and a success flag.
- `ConfluencePageExportInput` — Renders a batch of fetched Confluence pages into markdown and XML; call `.main()`.
- `ConfluencePageExportOutput` — The concatenated XML of all successfully exported pages.
- `CountLlmTokenInput` — Counts tiktoken tokens in a string using the gpt-4o encoding; call `.main()`.
- `CountLlmTokenOutput` — The token count.

This library ships no CLI.

## More detail

For signatures, field semantics, and key examples see `ref/public-api.md`.
