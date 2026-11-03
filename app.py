import json
from pathlib import Path

import streamlit as st
from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    OpenAI,
    RateLimitError,
)


CONFIG_PATH = Path(__file__).resolve().with_name("config.json")


def read_config():
    try:
        config = json.loads(CONFIG_PATH.read_text(encoding="utf-8-sig"))
    except FileNotFoundError:
        raise ValueError("Không tìm thấy config.json cạnh app.py. Xem README để tạo lại.") from None
    except (OSError, UnicodeError, json.JSONDecodeError):
        raise ValueError("Không đọc được config.json. Hãy kiểm tra quyền đọc và cú pháp JSON.") from None
    if not isinstance(config, dict):
        raise ValueError("config.json phải chứa một JSON object.")
    for field in ("openai_api_key", "model"):
        if not isinstance(config.get(field), str):
            raise ValueError(f"Trường {field} trong config.json phải là chuỗi.")
    if not config["model"].strip():
        raise ValueError("Hãy điền model trong config.json.")
    return {field: config[field].strip() for field in ("openai_api_key", "model")}


def call_model(config, messages):
    if not config["openai_api_key"]:
        raise ValueError("Chưa có API key. Hãy điền openai_api_key trong config.json rồi bấm Send lại.")
    with OpenAI(
        api_key=config["openai_api_key"],
        base_url="https://api.openai.com/v1",
        timeout=120.0,
        max_retries=0,
    ) as client:
        response = client.responses.create(
            model=config["model"], input=messages, store=False
        )
    if response.status != "completed":
        raise ValueError("API chưa hoàn tất phản hồi. Hãy thử gửi lại; lượt này chưa được lưu vào lịch sử.")
    if not response.output_text or not response.output_text.strip():
        raise ValueError("API không trả về văn bản để hiển thị. Lượt này chưa được lưu vào lịch sử.")
    return response.output_text


def main():
    st.title("Central Hub Local")
    try:
        config = read_config()
    except ValueError as exc:
        st.error(str(exc))
        st.stop()
    st.caption(f"Model: {config['model']}")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    with st.form("prompt_form"):
        prompt = st.text_area("Nhập prompt")
        sent = st.form_submit_button("Send")
    if sent:
        if not prompt.strip():
            st.warning("Hãy nhập prompt trước khi bấm Send.")
        else:
            try:
                # Đọc lại cấu hình ở mỗi lần gửi, không cache API key.
                config = read_config()
                messages = st.session_state.messages + [{"role": "user", "content": prompt}]
                with st.spinner("Đang chờ phản hồi…"):
                    answer = call_model(config, messages)
            except ValueError as exc:
                st.error(str(exc))
            except AuthenticationError:
                st.error("API key không hợp lệ hoặc đã bị thu hồi. Hãy kiểm tra config.json.")
            except RateLimitError:
                st.error("API đang giới hạn yêu cầu hoặc tài khoản hết quota. Hãy kiểm tra hạn mức và thanh toán API.")
            except APITimeoutError:
                st.error("API chưa phản hồi trong thời gian chờ. Hãy thử lại sau.")
            except APIConnectionError:
                st.error("Không kết nối được OpenAI API. Hãy kiểm tra mạng hoặc proxy.")
            except APIStatusError as exc:
                st.error(f"OpenAI API trả lỗi HTTP {exc.status_code}. Hãy kiểm tra quyền truy cập model, cấu hình và trạng thái dịch vụ.")
            else:
                st.session_state.messages = messages + [{"role": "assistant", "content": answer}]
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


if __name__ == "__main__":
    main()
