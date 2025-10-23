# -*- coding: utf-8 -*-

from dataclasses import dataclass
from pydantic import BaseModel, Field
from pathlib import Path

dir_here = Path(__file__).absolute().parent
p_input = dir_here / "input.txt"
p_output = dir_here / "output.txt"

chinese_punctuation = "，、。；：？！""''（）【】《》"


@dataclass
class PairMatch:
    """
    表示一对闭合标记的匹配信息

    :param marker: 标记符号，如 "**"、"()"、"[]" 等
    :param open_start: 开始标记的起始位置（索引）
    :param open_end: 开始标记的结束位置（索引，不包含）
    :param close_start: 结束标记的起始位置（索引）
    :param close_end: 结束标记的结束位置（索引，不包含）
    """
    marker: str
    open_start: int
    open_end: int
    close_start: int
    close_end: int


def find_pair_markers(line: str, marker: str) -> list[PairMatch]:
    """
    在字符串中查找成对的标记

    对于相同的开始和结束标记（如 **），会将找到的标记按顺序两两配对。
    例如：第1个和第2个配对，第3个和第4个配对，以此类推。

    :param line: 要搜索的字符串
    :param marker: 要匹配的标记，如 "**"

    :return: 匹配到的成对标记列表
    """
    matches = []
    positions = []

    # 找到所有标记的位置
    start = 0
    while True:
        pos = line.find(marker, start)
        if pos == -1:
            break
        positions.append(pos)
        start = pos + len(marker)

    # 将位置两两配对（第1个和第2个，第3个和第4个，...）
    for i in range(0, len(positions) - 1, 2):
        open_pos = positions[i]
        close_pos = positions[i + 1]
        matches.append(
            PairMatch(
                marker=marker,
                open_start=open_pos,
                open_end=open_pos + len(marker),
                close_start=close_pos,
                close_end=close_pos + len(marker),
            )
        )

    return matches


def remove_spaces_around_paired_markers(line: str, matches: list[PairMatch]) -> str:
    """
    移除成对标记内侧的空格

    对于每一对标记：
    - 移除开始标记后面的空格（内侧）
    - 移除结束标记前面的空格（内侧）

    从后往前处理每一对标记，避免修改字符串后索引变化的问题。
    对于每一对，先处理结束标记前的空格，再处理开始标记后的空格。

    :param line: 要处理的字符串
    :param matches: 成对标记的匹配列表

    :return: 处理后的字符串
    """
    if not matches:
        return line

    # 按开始位置从后往前排序，确保修改不影响前面的索引
    sorted_matches = sorted(matches, key=lambda m: m.open_start, reverse=True)

    result = line
    for match in sorted_matches:
        # 先处理结束标记前面的空格
        space_count = 0
        pos = match.close_start
        while pos - space_count - 1 >= 0 and result[pos - space_count - 1] == " ":
            space_count += 1
        if space_count > 0:
            result = result[: pos - space_count] + result[pos:]

        # 再处理开始标记后面的空格
        # 注意：删除close前的空格不影响open_end的位置（因为在前面）
        space_count = 0
        pos = match.open_end
        while pos + space_count < len(result) and result[pos + space_count] == " ":
            space_count += 1
        if space_count > 0:
            result = result[:pos] + result[pos + space_count :]

    return result


def post_process_paired_markers(line: str) -> str:
    """
    后处理：移除成对标记内侧的多余空格

    目前支持的标记：
    - ** (Markdown粗体)

    这个函数会按顺序处理多个标记类型，每次处理完一个标记类型后，
    将修改后的字符串作为下一个标记类型的输入。

    :param line: 要处理的字符串

    :return: 处理后的字符串
    """
    # 可以扩展到其他标记，如 "()", "[]", "<>" 等
    markers_to_process = ["**"]

    for marker in markers_to_process:
        matches = find_pair_markers(line, marker)
        line = remove_spaces_around_paired_markers(line, matches)

    return line


def _process_last_special_char(line: str, tokens: list[str], char: str):
    try:
        if line.rstrip()[-1] == char:
            tokens.append("")
    except IndexError:
        pass


def handle_dou_hao(line: str) -> str:
    """
    中文逗号 ， → 英文逗号 ,
    并在逗号后添加一个空格
    """
    tokens = [token.strip() for token in line.split("，") if token.strip()]
    _process_last_special_char(line, tokens, "，")
    return ", ".join(tokens).strip()


def handle_dun_hao(line: str) -> str:
    """
    中文顿号 、 → 英文逗号 ,
    并在逗号后添加一个空格
    """
    tokens = [token.strip() for token in line.split("、") if token.strip()]
    _process_last_special_char(line, tokens, "、")
    return ", ".join(tokens).strip()


def handle_ju_hao(line: str) -> str:
    """
    中文句号 。 → 英文句号 .
    并在句号后添加一个空格
    """
    tokens = [token.strip() for token in line.split("。") if token.strip()]
    _process_last_special_char(line, tokens, "。")
    return ". ".join(tokens).strip()


def handle_mao_hao(line: str) -> str:
    """
    中文冒号 ： → 英文冒号 :
    并在冒号后添加一个空格
    """
    tokens = [token.strip() for token in line.split("：") if token.strip()]
    _process_last_special_char(line, tokens, "：")
    return ": ".join(tokens).strip()


def handle_fen_hao(line: str) -> str:
    """
    中文分号 ； → 英文分号 ;
    并在分号后添加一个空格
    """
    tokens = [token.strip() for token in line.split("；") if token.strip()]
    _process_last_special_char(line, tokens, "；")
    return "; ".join(tokens).strip()


def handle_wen_hao(line: str) -> str:
    """
    中文问号 ？ → 英文问号 ?
    并在问号后添加一个空格
    """
    tokens = [token.strip() for token in line.split("？") if token.strip()]
    _process_last_special_char(line, tokens, "？")
    return "? ".join(tokens).strip()


def handle_exclamation(line: str) -> str:
    """
    中文感叹号 ！ → 英文感叹号 !
    并在感叹号后添加一个空格
    """
    tokens = [token.strip() for token in line.split("！") if token.strip()]
    _process_last_special_char(line, tokens, "！")
    return "! ".join(tokens).strip()


def handle_zuo_kuo_hao(line: str) -> str:
    """
    中文左括号 （ → 英文左括号 (
    并在左括号前添加一个空格
    """
    tokens = [token.strip() for token in line.split("（") if token.strip()]
    return " (".join(tokens).strip()


def handle_you_kuo_hao(line: str) -> str:
    """
    中文右括号 ） → 英文右括号 )
    并在右括号后添加一个空格. 但如果右括号之后是一个特殊标点符号, 则不添加空格.
    """
    tokens = [token.strip() for token in line.split("）") if token.strip()]
    # print(tokens)  # for debug only
    new_tokens = list()
    for ith, token in enumerate(tokens):
        new_tokens.append(token)
        try:
            next_token = tokens[ith + 1]
            if next_token[0] in ",.:;?!":
                new_tokens.append(")")
            else:
                new_tokens.append(") ")
        except IndexError:
            break
    try:
        if line.rstrip()[-1] == "）":
            new_tokens.append(")")
    except IndexError:
        pass
    # print(new_tokens)  # for debug only
    return "".join(new_tokens).strip()


def handle_zuo_shuang_yin_hao(line: str) -> str:
    """
    中文左双引号 “ → 英文左双引号 "
    并在左双引号前添加一个空格
    """
    tokens = [token.strip() for token in line.split("“") if token.strip()]
    return ' "'.join(tokens).strip()


def handle_you_shuang_yin_hao(line: str) -> str:
    """
    中文右双引号 ” → 英文右双引号 "
    并在右双引号后添加一个空格. 但如果右双号之后是一个特殊标点符号, 则不添加空格.
    """
    tokens = [token.strip() for token in line.split("”") if token.strip()]
    # print(tokens)  # for debug only
    new_tokens = list()
    for ith, token in enumerate(tokens):
        new_tokens.append(token)
        try:
            next_token = tokens[ith + 1]
            if next_token[0] in ",.:;?!)":
                new_tokens.append('"')
            else:
                new_tokens.append('" ')
        except IndexError:
            break
    try:
        if line.rstrip()[-1] == "”":
            new_tokens.append('"')
    except IndexError:
        pass
    # print(new_tokens)  # for debug only
    return "".join(new_tokens).strip()


def handle_space_between_chinese_and_english(line: str) -> str:
    """
    Add space between Chinese and English characters/numbers.
    Goes through character by character and maintains two consecutive characters.
    If one is an English letter/number (a-z, A-Z, 0-9) and the other is non-ASCII, add space between them.
    Also adds space between English letters and numbers.
    """
    if not line:
        return line

    result = []
    prev_char = None

    for current_char in line:
        # Check if we need to add space between prev_char and current_char
        if prev_char is not None:
            # Check character types
            prev_is_english = prev_char.isalpha() and ord(prev_char) < 128
            current_is_english = current_char.isalpha() and ord(current_char) < 128
            prev_is_number = prev_char.isdigit()
            current_is_number = current_char.isdigit()
            prev_is_non_ascii = ord(prev_char) >= 128
            current_is_non_ascii = ord(current_char) >= 128

            # Add space in the following cases:
            if (
                # 1. Between English letter and non-ASCII character, example: "Eng中文"
                (prev_is_english and current_is_non_ascii)
                # 2. Between non-ASCII character and English letter, example: "中文Eng"
                or (prev_is_non_ascii and current_is_english)
                # 3. Between number and non-ASCII character, example: "100中文"
                or (prev_is_number and current_is_non_ascii)
                # 4. Between non-ASCII character and number, example: "中文100"
                or (prev_is_non_ascii and current_is_number)
            ):
                result.append(" ")

        result.append(current_char)
        prev_char = current_char

    return "".join(result)


def handle_everything(line: str) -> str:
    line = handle_dou_hao(line)
    line = handle_dun_hao(line)
    line = handle_ju_hao(line)
    line = handle_mao_hao(line)
    line = handle_fen_hao(line)
    line = handle_wen_hao(line)
    line = handle_exclamation(line)
    line = handle_zuo_kuo_hao(line)
    line = handle_you_kuo_hao(line)
    line = handle_zuo_shuang_yin_hao(line)
    line = handle_you_shuang_yin_hao(line)
    # Add spaces between Chinese and English after all punctuation conversions
    line = handle_space_between_chinese_and_english(line)
    # Post-process to remove spaces inside paired markers
    line = post_process_paired_markers(line)
    return line


def process(text: str) -> str:
    lines = text.splitlines()
    new_lines = [handle_everything(line) for line in lines]
    return "\n".join(new_lines)


class ChineseToEnglishPunctuationInput(BaseModel):  # pragma: no cover
    text: str = Field()

    def main(self):
        result = process(self.text)
        return ChineseToEnglishPunctuationOutput(
            input=self,
            result=result,
        )


class ChineseToEnglishPunctuationOutput(BaseModel):  # pragma: no cover
    input: ChineseToEnglishPunctuationInput = Field()
    result: str = Field()
