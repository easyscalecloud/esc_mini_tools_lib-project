# -*- coding: utf-8 -*-

from pydantic import BaseModel, Field
from chinese_to_english_punctuation.api import process

from ..logger import logger


class ChineseToEnglishPunctuationInput(BaseModel):
    text: str = Field(description="The text to convert.")

    def main(self):
        logger.info(f"text = {self.text!r}")  # for debug only
        result = process(self.text)
        logger.info(f"{result = }")  # for debug only
        return ChineseToEnglishPunctuationOutput(
            input=self,
            result=result,
        )


class ChineseToEnglishPunctuationOutput(BaseModel):
    input: ChineseToEnglishPunctuationInput = Field()
    result: str = Field(
        description="The text with Chinese punctuation converted to English."
    )
