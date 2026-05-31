import re
from typing import Any

from app.config import settings


def validate_single_choice(question: dict, answer: dict) -> list[str]:
    selected = answer.get("selected", [])
    config = question.get("config", {})
    options = config.get("options", [])
    valid_ids = {opt["id"] for opt in options}

    if not selected:
        return [f"题目「{question['title']}」请选择一个选项"]
    if len(selected) > 1:
        return [f"题目「{question['title']}」只能选择一个选项"]

    invalid = [s for s in selected if s not in valid_ids]
    if invalid and not config.get("allow_other"):
        return [f"题目「{question['title']}」包含无效选项"]
    return []


def validate_multiple_choice(question: dict, answer: dict) -> list[str]:
    selected = answer.get("selected", [])
    config = question.get("config", {})
    options = config.get("options", [])
    valid_ids = {opt["id"] for opt in options}
    min_sel = config.get("min_select", 1)
    max_sel = config.get("max_select")
    errors = []

    if len(selected) < min_sel:
        errors.append(f"题目「{question['title']}」至少选择{min_sel}项")
    if max_sel and len(selected) > max_sel:
        errors.append(f"题目「{question['title']}」最多选择{max_sel}项")

    invalid = [s for s in selected if s not in valid_ids]
    if invalid and not config.get("allow_other"):
        errors.append(f"题目「{question['title']}」包含无效选项")
    return errors


def validate_image_choice(question: dict, answer: dict) -> list[str]:
    selected = answer.get("selected", [])
    config = question.get("config", {})
    options = config.get("options", [])
    valid_ids = {opt["id"] for opt in options}
    multiple = config.get("multiple", False)

    if not selected:
        return [f"题目「{question['title']}」请选择一个选项"]
    if not multiple and len(selected) > 1:
        return [f"题目「{question['title']}」只能选择一个选项"]

    invalid = [s for s in selected if s not in valid_ids]
    if invalid:
        return [f"题目「{question['title']}」包含无效选项"]
    return []


def validate_text(question: dict, answer: dict) -> list[str]:
    text = answer.get("text", "")
    stripped = text.strip()
    config = question.get("config", {})
    errors = []

    if question.get("required") and not stripped:
        return [f"题目「{question['title']}」不能为空"]

    min_len = config.get("min_length")
    max_len = config.get("max_length")
    if min_len and len(stripped) < min_len:
        errors.append(f"题目「{question['title']}」至少输入{min_len}个字符")
    if max_len and len(stripped) > max_len:
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


def validate_date(question: dict, answer: dict) -> list[str]:
    value = answer.get("value")
    if value is None or not isinstance(value, str) or not value.strip():
        return [f"题目「{question['title']}」请选择日期"]
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", value.strip()):
        return [f"题目「{question['title']}」日期格式不正确"]
    return []


def validate_time(question: dict, answer: dict) -> list[str]:
    value = answer.get("value")
    if value is None or (isinstance(value, str) and not value.strip()):
        return [f"题目「{question['title']}」请选择时间"]
    return []


def validate_matrix(question: dict, answer: dict) -> list[str]:
    matrix = answer.get("matrix", {})
    config = question.get("config", {})
    rows = config.get("rows", [])
    columns = config.get("columns", [])
    valid_col_ids = {col["id"] for col in columns}
    q_type = question.get("type", "")
    errors = []

    if question.get("required"):
        missing_rows = [r for r in rows if r["id"] not in matrix]
        if missing_rows:
            names = "、".join(r["label"] for r in missing_rows[:3])
            errors.append(f"题目「{question['title']}」请完成以下行的选择：{names}")
            return errors

    for row in rows:
        row_id = row["id"]
        if row_id not in matrix:
            continue
        val = matrix[row_id]
        if q_type == "matrix_single":
            if val not in valid_col_ids:
                errors.append(f"题目「{question['title']}」行「{row['label']}」选项无效")
        elif q_type == "matrix_multi":
            if not isinstance(val, list):
                errors.append(f"题目「{question['title']}」行「{row['label']}」格式错误")
            else:
                invalid = [v for v in val if v not in valid_col_ids]
                if invalid:
                    errors.append(f"题目「{question['title']}」行「{row['label']}」包含无效选项")
        elif q_type == "matrix_rating":
            if not isinstance(val, (int, float)) or val < 1:
                errors.append(f"题目「{question['title']}」行「{row['label']}」请评分")

    return errors


def validate_ranking(question: dict, answer: dict) -> list[str]:
    ranked = answer.get("ranked", [])
    config = question.get("config", {})
    items = config.get("items", [])
    valid_ids = {item["id"] for item in items}

    if len(ranked) != len(items):
        return [f"题目「{question['title']}」请对所有选项进行排序"]
    invalid = [r for r in ranked if r not in valid_ids]
    if invalid:
        return [f"题目「{question['title']}」包含无效排序项"]
    if len(set(ranked)) != len(ranked):
        return [f"题目「{question['title']}」排序项不能重复"]
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


def validate_file_upload(question: dict, answer: dict) -> list[str]:
    files = answer.get("files", [])
    config = question.get("config", {})
    max_files = config.get("max_files", 3)

    if question.get("required") and not files:
        return [f"题目「{question['title']}」请上传文件"]
    if len(files) > max_files:
        return [f"题目「{question['title']}」最多上传{max_files}个文件"]
    return []


def validate_cascading(question: dict, answer: dict) -> list[str]:
    cascading = answer.get("cascading", [])
    if question.get("required") and not cascading:
        return [f"题目「{question['title']}」请选择"]
    return []


def validate_phone(question: dict, answer: dict) -> list[str]:
    text = answer.get("text", "").strip()
    if not text and not question.get("required"):
        return []
    if not re.match(r"^1[3-9]\d{9}$", text):
        return [f"题目「{question['title']}」请输入正确的手机号"]
    return []


def validate_email(question: dict, answer: dict) -> list[str]:
    text = answer.get("text", "").strip()
    if not text and not question.get("required"):
        return []
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", text):
        return [f"题目「{question['title']}」请输入正确的邮箱地址"]
    return []


def validate_address(question: dict, answer: dict) -> list[str]:
    addr = answer.get("address", {})
    config = question.get("config", {})
    detail_level = config.get("detail_level", "district")

    required_fields = ["province"]
    if detail_level in ("city", "district", "street"):
        required_fields.append("city")
    if detail_level in ("district", "street"):
        required_fields.append("district")

    errors = []
    for field in required_fields:
        val = addr.get(field, "").strip()
        if not val:
            field_names = {"province": "省份", "city": "城市", "district": "区县"}
            errors.append(f"题目「{question['title']}」请填写{field_names.get(field, field)}")

    if config.get("show_detail_input") and question.get("required"):
        if not addr.get("detail", "").strip():
            errors.append(f"题目「{question['title']}」请填写详细地址")

    return errors


def validate_dropdown(question: dict, answer: dict) -> list[str]:
    selected = answer.get("selected", [])
    config = question.get("config", {})
    options = config.get("options", [])
    valid_ids = {opt["id"] for opt in options}

    if not selected:
        return [f"题目「{question['title']}」请选择一个选项"]
    if len(selected) > 1:
        return [f"题目「{question['title']}」只能选择一个选项"]
    if selected[0] not in valid_ids:
        return [f"题目「{question['title']}」选项无效"]
    return []


VALIDATORS = {
    "single_choice": validate_single_choice,
    "multiple_choice": validate_multiple_choice,
    "text_single": validate_text,
    "text_multi": validate_text,
    "dropdown": validate_dropdown,
    "date": validate_date,
    "time": validate_time,
    "rating": validate_rating,
    "nps": validate_nps,
    "matrix_single": validate_matrix,
    "matrix_multi": validate_matrix,
    "matrix_rating": validate_matrix,
    "ranking": validate_ranking,
    "slider": validate_slider,
    "file_upload": validate_file_upload,
    "image_choice": validate_image_choice,
    "cascading": validate_cascading,
    "phone": validate_phone,
    "email": validate_email,
    "address": validate_address,
    "statement": None,
}


def _is_answer_empty(q_type: str, answer: Any) -> bool:
    """Check if an answer is effectively empty based on question type."""
    if answer is None or answer == {}:
        return True
    if q_type in ("text_single", "text_multi", "phone", "email"):
        return not answer.get("text", "").strip()
    if q_type in ("single_choice", "multiple_choice", "dropdown", "image_choice"):
        return not answer.get("selected")
    if q_type in ("rating", "nps", "slider", "date", "time"):
        return answer.get("value") is None
    if q_type in ("matrix_single", "matrix_multi", "matrix_rating"):
        return not answer.get("matrix")
    if q_type == "ranking":
        return not answer.get("ranked")
    if q_type == "file_upload":
        return not answer.get("files")
    if q_type == "cascading":
        return not answer.get("cascading")
    if q_type == "address":
        addr = answer.get("address", {})
        return not any(v.strip() for v in addr.values() if isinstance(v, str))
    return False


def validate_response(questions: list[dict], answers: dict[str, Any]) -> list[str]:
    errors = []
    for question in questions:
        q_id = question["id"]
        q_type = question.get("type", "")
        answer = answers.get(q_id)

        if q_type == "statement":
            continue

        empty = _is_answer_empty(q_type, answer)

        if question.get("required") and empty:
            errors.append(f"题目「{question['title']}」为必答题")
            continue

        if empty:
            continue

        validator = VALIDATORS.get(q_type)
        if validator:
            type_errors = validator(question, answer)
            errors.extend(type_errors)

    return errors
