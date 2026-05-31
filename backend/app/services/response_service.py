import re
from typing import Any


def validate_required(question: dict, answer: Any) -> list[str]:
    if answer is None:
        return [f"题目「{question['title']}」为必答题"]
    return []


def validate_single_choice(question: dict, answer: dict) -> list[str]:
    selected = answer.get("selected", [])
    if not selected:
        return [f"题目「{question['title']}」请选择一个选项"]
    if len(selected) > 1:
        return [f"题目「{question['title']}」只能选择一个选项"]
    return []


def validate_multiple_choice(question: dict, answer: dict) -> list[str]:
    selected = answer.get("selected", [])
    config = question.get("config", {})
    min_sel = config.get("min_select", 1)
    max_sel = config.get("max_select")
    errors = []
    if len(selected) < min_sel:
        errors.append(f"题目「{question['title']}」至少选择{min_sel}项")
    if max_sel and len(selected) > max_sel:
        errors.append(f"题目「{question['title']}」最多选择{max_sel}项")
    return errors


def validate_text(question: dict, answer: dict) -> list[str]:
    text = answer.get("text", "")
    config = question.get("config", {})
    errors = []
    min_len = config.get("min_length")
    max_len = config.get("max_length")
    if min_len and len(text) < min_len:
        errors.append(f"题目「{question['title']}」至少输入{min_len}个字符")
    if max_len and len(text) > max_len:
        errors.append(f"题目「{question['title']}」最多输入{max_len}个字符")
    return errors


def validate_rating(question: dict, answer: dict) -> list[str]:
    value = answer.get("value")
    config = question.get("config", {})
    max_rating = config.get("max_rating", 5)
    if value is None or not isinstance(value, (int, float)):
        return [f"题目「{question['title']}」请提供评分"]
    if value < 1 or value > max_rating:
        return [f"题目「{question['title']}」评分范围为1-{max_rating}"]
    return []


def validate_nps(question: dict, answer: dict) -> list[str]:
    value = answer.get("value")
    if value is None or not isinstance(value, (int, float)):
        return [f"题目「{question['title']}」请提供评分"]
    if value < 0 or value > 10:
        return [f"题目「{question['title']}」评分范围为0-10"]
    return []


def validate_matrix(question: dict, answer: dict) -> list[str]:
    matrix = answer.get("matrix", {})
    config = question.get("config", {})
    rows = config.get("rows", [])
    if question.get("required") and len(matrix) < len(rows):
        return [f"题目「{question['title']}」请完成所有行的选择"]
    return []


def validate_ranking(question: dict, answer: dict) -> list[str]:
    ranked = answer.get("ranked", [])
    config = question.get("config", {})
    items = config.get("items", [])
    if len(ranked) != len(items):
        return [f"题目「{question['title']}」请对所有选项进行排序"]
    return []


def validate_slider(question: dict, answer: dict) -> list[str]:
    value = answer.get("value")
    config = question.get("config", {})
    min_val = config.get("min", 0)
    max_val = config.get("max", 100)
    if value is None or not isinstance(value, (int, float)):
        return [f"题目「{question['title']}」请拖动滑块选择"]
    if value < min_val or value > max_val:
        return [f"题目「{question['title']}」值范围为{min_val}-{max_val}"]
    return []


def validate_phone(question: dict, answer: dict) -> list[str]:
    text = answer.get("text", "")
    if not re.match(r"^1[3-9]\d{9}$", text):
        return [f"题目「{question['title']}」请输入正确的手机号"]
    return []


def validate_email(question: dict, answer: dict) -> list[str]:
    text = answer.get("text", "")
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", text):
        return [f"题目「{question['title']}」请输入正确的邮箱地址"]
    return []


VALIDATORS = {
    "single_choice": validate_single_choice,
    "multiple_choice": validate_multiple_choice,
    "text_single": validate_text,
    "text_multi": validate_text,
    "dropdown": validate_single_choice,
    "date": None,
    "time": None,
    "rating": validate_rating,
    "nps": validate_nps,
    "matrix_single": validate_matrix,
    "matrix_multi": validate_matrix,
    "matrix_rating": validate_matrix,
    "ranking": validate_ranking,
    "slider": validate_slider,
    "file_upload": None,
    "image_choice": validate_single_choice,
    "cascading": None,
    "phone": validate_phone,
    "email": validate_email,
    "address": None,
    "statement": None,
}


def validate_response(questions: list[dict], answers: dict[str, Any]) -> list[str]:
    errors = []
    for question in questions:
        q_id = question["id"]
        q_type = question.get("type", "")
        answer = answers.get(q_id)

        if question.get("required") and (answer is None or answer == {}):
            errors.append(f"题目「{question['title']}」为必答题")
            continue

        if answer is None or answer == {} or q_type == "statement":
            continue

        validator = VALIDATORS.get(q_type)
        if validator:
            type_errors = validator(question, answer)
            errors.extend(type_errors)

    return errors
