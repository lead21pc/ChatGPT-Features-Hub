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
HUB_CI_PATH = Path(__file__).resolve().parent / "upstream" / "Central Hub" / "HUB_CI_v1.1.md"
TECHNICAL_PATH = Path(__file__).resolve().parent / "runtime" / "packages" / "technical" / "HUB-DOM-TECHNICAL_v1.0.md"
T2_BINDING_BRIDGE = (
    "\n\n[T2 LOCAL TEST BINDING]\n"
    "In T2, HUB-DOM-TECHNICAL is manually selected for the current user request/task portion. "
    "This note only supplies manual selection because Hub Router is intentionally not loaded; "
    "it does not simulate Router behavior or change TECHNICAL semantics.\n\n"
)
HUB_ROUTER_PATH = HUB_CI_PATH.with_name("HUB_ROUTER_v1.1.yaml")
HUB_ARCHITECTURE_PATH = HUB_CI_PATH.with_name("HUB_ARCHITECTURE_v1.8.md")
HUB_CATALOG_PATH = HUB_CI_PATH.with_name("HUB_PACKAGE_CATALOG_v1.8.yaml")
CONCEPT_CORE_PATH = Path(__file__).resolve().parent / "runtime" / "packages" / "concept-development" / "HUB-DOM-CONCEPT-DEVELOPMENT_v1.1.md"
CONCEPT_CATALOG_PATH = CONCEPT_CORE_PATH.with_name("HUB-CATALOG-CONCEPT-DEVELOPMENT_v1.1.yaml")
CREATIVE_PATH = CONCEPT_CORE_PATH.with_name("HUB-DOM-CREATIVE_v1.1.md")
BRAINSTORM_PATH = CONCEPT_CORE_PATH.with_name("HUB-CAP-BRAINSTORM_v1.1.md")
DEBATE_PATH = CONCEPT_CORE_PATH.with_name("HUB-CAP-DEBATE_v1.0.md")
T5_CALIBRATION_ADAPTER = (
    "\n\n[T5 LOCAL CALIBRATION]\n"
    "HUB-PKG-CONCEPT-DEVELOPMENT is manually selected for the current request/task portion; "
    "Router package selection and execution are intentionally absent. "
    "The supplied Concept core and local Catalog govern exact control spans, leaf selection and applicability. "
    "All three supplied leaf bodies are available under T5 local test bindings only and may execute "
    "only when the core/Catalog select them for a valid current-user-authored span. "
    "Availability does not activate a leaf. Specialized behavior ends at that span's standalone # "
    "terminator, with no persistence; ordinary unscoped concept work remains core behavior. "
    "This local calibration does not change or claim old ChatGPT Library resolution, "
    "migrate Library bindings or simulate Router behavior.\n\n"
)
T6_COMPOSITION_ADAPTER = (
    "\n\n[T6 LOCAL COMPOSITION CALIBRATION]\n"
    "HUB-PKG-TECHNICAL and HUB-PKG-CONCEPT-DEVELOPMENT are manually supplied for T6 composition calibration; "
    "Router selection/retrieval is intentionally absent. Apply each package only to task portions materially "
    "within its existing applicability/responsibility. Participation does not expand authority; neither package "
    "dominates the other. Technical mechanism reasoning must not decide fictional canon, concept acceptance "
    "or design state. Concept/leaf work must not fabricate technical evidence, resolve technical uncertainty "
    "or override Technical diagnosis. Exact Concept leaf activation remains owned by Concept core/Catalog; "
    "availability does not activate leaves and specialized behavior does not persist beyond valid spans. "
    "Existing old-host binding metadata remains unchanged. Debate may remain blocked where the current Catalog "
    "requires unresolved old binding verification; preserve this as evidence without bypassing it. "
    "Authoring is intentionally absent because its current old-host binding is unresolved; no Authoring "
    "behavior may be emulated or claimed. This is not Router-integrated retrieval or local Library binding migration.\n\n"
)
T4_BINDING_NOTE = (
    "\n\n[T4 LOCAL MANUAL SELECTION]\n"
    "HUB-PKG-CONCEPT-DEVELOPMENT is manually selected for this request/task portion "
    "because Router execution is intentionally outside this calibration. "
    "The supplied local Catalog is the selection metadata required by the supplied core. "
    "No specialized leaf body is available in T4. Valid explicit leaf spans may be "
    "identified from metadata, but their specialized execution is blocked and must not be performed. "
    "Continue sufficient ordinary unscoped concept work through the shared core. "
    "This note does not change Concept semantics, claim Library retrieval, simulate Router "
    "behavior or establish local binding migration.\n\n"
)
T3_SIMULATION_ADAPTER = (
    "[T3 ROUTING INSPECTION]\n"
    "This is Router eligibility.simulation only, a test-only metadata view. "
    "Perform TASK_SCOPE and ROOT_PACKAGE_SELECTION for the current user request "
    "under the supplied exact Hub controls. Stop after root selection: package "
    "retrieval and execution are intentionally not performed. Do not install headers "
    "or claim Library/local retrieval, module application, deployment or tool execution. "
    "Return a route inspection record only. NONE (an empty selected_packages array) "
    "is valid when no package materially contributes."
)
ROUTE_PACKAGE_FIELDS = (
    "package_id", "entrypoint_module_id", "runtime_role", "application_scope", "reason"
)
ROUTE_SCHEMA = {
    "type": "object",
    "properties": {
        "task_scope": {"type": "string"},
        "selected_packages": {"type": "array", "items": {
            "type": "object",
            "properties": {
                **{field: {"type": "string"} for field in ROUTE_PACKAGE_FIELDS},
                "runtime_role": {"type": "string", "description": "Exact runtime_role identifier from the root Catalog."},
            },
            "required": list(ROUTE_PACKAGE_FIELDS),
            "additionalProperties": False,
        }},
        "unresolved_blockers": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["task_scope", "selected_packages", "unresolved_blockers"],
    "additionalProperties": False,
}
MODES = ("T0 - Raw API", "T1 - Hub CI", "T2 - Hub CI + Technical", "T3 - Hub Routing Inspect", "T4 - Hub CI + Concept Core", "T5 - Concept Scoped Leaves", "T6 - Concept + Technical Composition")


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


def call_model(config, messages, mode=MODES[0]):
    if not config["openai_api_key"]:
        raise ValueError("Chưa có API key. Hãy điền openai_api_key trong config.json rồi bấm Send lại.")
    instructions = {}
    if mode == MODES[1]:
        try:
            instructions["instructions"] = HUB_CI_PATH.read_bytes().decode("utf-8")
        except (OSError, UnicodeError):
            raise ValueError("T1: Không đọc được upstream/Central Hub/HUB_CI_v1.1.md. Hãy kiểm tra tệp, quyền đọc và mã hóa UTF-8; yêu cầu chưa được gửi, không chuyển sang T0.") from None
    elif mode == MODES[2]:
        try:
            ci = HUB_CI_PATH.read_bytes().decode("utf-8")
        except (OSError, UnicodeError):
            raise ValueError("T2: Không đọc được upstream/Central Hub/HUB_CI_v1.1.md; yêu cầu chưa được gửi, không chuyển sang T1/T0.") from None
        try:
            technical = TECHNICAL_PATH.read_bytes().decode("utf-8")
        except (OSError, UnicodeError):
            raise ValueError("T2: Không đọc được runtime/packages/technical/HUB-DOM-TECHNICAL_v1.0.md. Hãy kiểm tra tệp, quyền đọc và mã hóa UTF-8; yêu cầu chưa được gửi, không chuyển sang T1/T0.") from None
        instructions["instructions"] = ci + T2_BINDING_BRIDGE + technical
    elif mode == MODES[4]:
        controls = []
        for path in (HUB_CI_PATH, CONCEPT_CORE_PATH, CONCEPT_CATALOG_PATH):
            try:
                controls.append(path.read_bytes().decode("utf-8"))
            except (OSError, UnicodeError):
                raise ValueError(
                    f"T4: Không đọc được {path.name}. Hãy kiểm tra tệp, quyền đọc và mã hóa UTF-8; "
                    "yêu cầu chưa được gửi, không chuyển sang T2/T1/T0."
                ) from None
        instructions["instructions"] = controls[0] + T4_BINDING_NOTE + controls[1] + controls[2]
    elif mode == MODES[5]:
        controls = []
        for path in (HUB_CI_PATH, CONCEPT_CORE_PATH, CONCEPT_CATALOG_PATH,
                     CREATIVE_PATH, BRAINSTORM_PATH, DEBATE_PATH):
            try:
                controls.append(path.read_bytes().decode("utf-8"))
            except (OSError, UnicodeError):
                raise ValueError(
                    f"T5: Không đọc được {path.name}. Hãy kiểm tra tệp, quyền đọc và mã hóa UTF-8; "
                    "yêu cầu chưa được gửi, không chuyển sang T4/T2/T1/T0."
                ) from None
        instructions["instructions"] = controls[0] + T5_CALIBRATION_ADAPTER + "".join(controls[1:])
    elif mode == MODES[6]:
        controls = []
        for path in (HUB_CI_PATH, TECHNICAL_PATH, CONCEPT_CORE_PATH, CONCEPT_CATALOG_PATH,
                     CREATIVE_PATH, BRAINSTORM_PATH, DEBATE_PATH):
            try:
                controls.append(path.read_bytes().decode("utf-8"))
            except (OSError, UnicodeError):
                raise ValueError(
                    f"T6: Không đọc được {path.name}. Hãy kiểm tra tệp, quyền đọc và mã hóa UTF-8; "
                    "yêu cầu chưa được gửi, không chuyển sang chế độ khác."
                ) from None
        instructions["instructions"] = controls[0] + T6_COMPOSITION_ADAPTER + "".join(controls[1:])
    with OpenAI(
        api_key=config["openai_api_key"],
        base_url="https://api.openai.com/v1",
        timeout=120.0,
        max_retries=0,
    ) as client:
        response = client.responses.create(
            model=config["model"], input=messages, store=False, **instructions
        )
    if response.status != "completed":
        raise ValueError("API chưa hoàn tất phản hồi. Hãy thử gửi lại; lượt này chưa được lưu vào lịch sử.")
    if not response.output_text or not response.output_text.strip():
        raise ValueError("API không trả về văn bản để hiển thị. Lượt này chưa được lưu vào lịch sử.")
    return response.output_text


def inspect_route(config, prompt):
    if not config["openai_api_key"]:
        raise ValueError("T3: Chưa có API key. Hãy điền openai_api_key trong config.json.")
    controls = []
    for path in (HUB_CI_PATH, HUB_ROUTER_PATH, HUB_ARCHITECTURE_PATH, HUB_CATALOG_PATH):
        try:
            controls.append(path.read_bytes().decode("utf-8"))
        except (OSError, UnicodeError):
            raise ValueError(
                f"T3: Không đọc được upstream/Central Hub/{path.name}. "
                "Hãy kiểm tra tệp, quyền đọc và mã hóa UTF-8; yêu cầu chưa được gửi, không chuyển sang chế độ khác."
            ) from None
    with OpenAI(
        api_key=config["openai_api_key"],
        base_url="https://api.openai.com/v1",
        timeout=120.0,
        max_retries=0,
    ) as client:
        response = client.responses.create(
            model=config["model"],
            instructions="\n\n".join(controls + [T3_SIMULATION_ADAPTER]),
            input=[{"role": "user", "content": prompt}],
            text={"format": {"type": "json_schema", "name": "hub_route_inspection",
                             "schema": ROUTE_SCHEMA, "strict": True}},
            store=False,
        )
    if response.status != "completed":
        raise ValueError("T3: API chưa hoàn tất phản hồi; chưa lưu bản ghi định tuyến.")
    try:
        refused = any(part.type == "refusal" for item in response.output if item.type == "message"
                      for part in item.content)
        output_text = response.output_text
    except (AttributeError, TypeError):
        raise ValueError("T3: Cấu trúc phản hồi API không hợp lệ; chưa lưu bản ghi định tuyến.") from None
    if refused:
        raise ValueError("T3: API từ chối yêu cầu; chưa lưu bản ghi định tuyến.")
    if not isinstance(output_text, str) or not output_text.strip():
        raise ValueError("T3: API không trả về văn bản; chưa lưu bản ghi định tuyến.")
    try:
        record = json.loads(output_text)
    except json.JSONDecodeError:
        raise ValueError("T3: JSON không hợp lệ; chưa lưu bản ghi định tuyến.") from None
    if (
        not isinstance(record, dict)
        or set(record) != set(ROUTE_SCHEMA["required"])
        or not isinstance(record["task_scope"], str)
        or not isinstance(record["selected_packages"], list)
        or not isinstance(record["unresolved_blockers"], list)
        or not all(isinstance(blocker, str) for blocker in record["unresolved_blockers"])
        or not all(isinstance(package, dict) and set(package) == set(ROUTE_PACKAGE_FIELDS)
                   and all(isinstance(value, str) for value in package.values())
                   for package in record["selected_packages"])
    ):
        raise ValueError("T3: Bản ghi không đúng cấu trúc schema; chưa lưu bản ghi định tuyến.")
    return record


def main():
    st.title("Central Hub Local")
    try:
        config = read_config()
    except ValueError as exc:
        st.error(str(exc))
        st.stop()
    st.caption(f"Model: {config['model']}")
    mode = st.radio("Chế độ", MODES)
    st.caption(f"Chế độ đang dùng: {mode}")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "response_modes" not in st.session_state:
        st.session_state.response_modes = {}
    if "route_records" not in st.session_state:
        st.session_state.route_records = []
    if mode == MODES[3]:
        st.caption("T3 chỉ kiểm tra định tuyến cho prompt hiện tại; dừng trước truy xuất và thực thi package. Dùng session mới để so sánh sạch.")
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
                    if mode == MODES[3]:
                        record = inspect_route(config, prompt)
                    else:
                        answer = call_model(config, messages, mode)
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
                if mode == MODES[3]:
                    st.session_state.route_records.append({"prompt": prompt, "record": record})
                else:
                    st.session_state.messages = messages + [{"role": "assistant", "content": answer}]
                    st.session_state.response_modes[len(messages)] = mode
    for index, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                st.caption(st.session_state.response_modes.get(index, MODES[0]))
            st.markdown(message["content"])
    for route in st.session_state.route_records:
        st.caption(MODES[3])
        st.text(route["prompt"])
        if not route["record"]["selected_packages"]:
            st.caption("T3: NONE — không chọn package.")
        st.json(route["record"])


if __name__ == "__main__":
    main()
