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

from runtime_host import (
    HUB_CI_PATH,
    HUB_ROUTER_PATH,
    HUB_ARCHITECTURE_PATH,
    HUB_CATALOG_PATH,
    T7_BINDINGS_PATH,
    ROUTE_PACKAGE_FIELDS,
    ROUTE_SCHEMA,
    LEAF_FIELDS,
    LEAF_SCHEMA,
    RUNTIME_MODE,
    t7_catalog_identities,
    t7_read,
    t7_load_bindings,
    t7_concept_binding_view,
    t7_retrieve,
    t7_structured,
)


CONFIG_PATH = Path(__file__).resolve().with_name("config.json")
TECHNICAL_PATH = Path(__file__).resolve().parent / "runtime" / "packages" / "technical" / "HUB-DOM-TECHNICAL_v1.0.md"
T2_BINDING_BRIDGE = (
    "\n\n[T2 LOCAL TEST BINDING]\n"
    "In T2, HUB-DOM-TECHNICAL is manually selected for the current user request/task portion. "
    "This note only supplies manual selection because Hub Router is intentionally not loaded; "
    "it does not simulate Router behavior or change TECHNICAL semantics.\n\n"
)
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
MODES = ("T0 - Raw API", "T1 - Hub CI", "T2 - Hub CI + Technical", "T3 - Hub Routing Inspect", "T4 - Hub CI + Concept Core", "T5 - Concept Scoped Leaves", "T6 - Concept + Technical Composition", "T7 - Router Local Retrieval", "T8 - Authoring Lifecycle", "T9 - AIS Local Execution")


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


def call_model(config, messages, mode=RUNTIME_MODE):
    if mode == RUNTIME_MODE:
        from m1 import call_runtime
        return call_runtime(config, messages)[0]
    if mode == MODES[9]:
        from t9 import call_t9
        return call_t9(config, messages)[0]
    if mode == MODES[8]:
        from t8 import call_t8
        return call_t8(config, messages)[0]
    if mode == MODES[7]:
        return call_t7(config, messages)[0]
    if not config["openai_api_key"]:
        raise ValueError("Chưa có API key. Hãy điền openai_api_key trong config.json rồi bấm Send lại.")
    instructions = {}
    if mode == MODES[1]:
        try:
            instructions["instructions"] = HUB_CI_PATH.read_bytes().decode("utf-8")
        except (OSError, UnicodeError):
            raise ValueError("T1: Không đọc được HUB_CI_v1.1.md. Hãy kiểm tra tệp, quyền đọc và mã hóa UTF-8; yêu cầu chưa được gửi, không chuyển sang T0.") from None
    elif mode == MODES[2]:
        try:
            ci = HUB_CI_PATH.read_bytes().decode("utf-8")
        except (OSError, UnicodeError):
            raise ValueError("T2: Không đọc được HUB_CI_v1.1.md; yêu cầu chưa được gửi, không chuyển sang T1/T0.") from None
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
                f"T3: Không đọc được {path.name}. "
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


T7_BINDING_NOTE = (
    "[T7 LOCAL HOST BINDING]\n"
    "T7 changes host storage/retrieval binding only. For artifacts explicitly listed in "
    "HUB_LOCAL_BINDINGS_v0.1.json, LOCAL_RUNTIME_FILE is the current T7 binding authority. "
    "An artifact becomes executable only after the platform reads it and verifies its declared SHA-256. "
    "This is a local-host successor binding, not fallback from failed LIBRARY_MODULE. "
    "ChatGPT Library location/resolution fields in the Hub and local catalogs remain historical "
    "source-host metadata and do not block eligibility under an explicit T7 local binding. "
    "All non-storage semantics of Hub CI, Router, Architecture, Catalog and module bodies remain unchanged. "
    "Unlisted packages/artifacts remain unavailable and must not be emulated. "
    "Selection != retrieval != execution. Availability does not activate a package or leaf.\n"
)


def call_t7(config, messages):
    """Return (normal answer, small structured selection/retrieval trace). No live tests here."""
    if not config["openai_api_key"]:
        raise ValueError("T7: Chưa có API key.")
    controls = [t7_read(path) for path in (HUB_CI_PATH, HUB_ROUTER_PATH, HUB_ARCHITECTURE_PATH, HUB_CATALOG_PATH)]
    binding_text = t7_read(T7_BINDINGS_PATH)
    bindings = t7_load_bindings(binding_text)
    catalog = t7_catalog_identities(controls[3], "packages", "package_id")
    trace = {"root_selected_package_ids": [], "locally_retrieved_package_ids": [],
             "concept_selected_leaf_ids": [], "locally_retrieved_module_ids": [], "unresolved_blockers": []}
    blockers = trace["unresolved_blockers"]
    bodies = {}
    accepted = []
    leaf_selections = []

    def retrieve(artifact):
        body = t7_retrieve(artifact)
        trace["locally_retrieved_module_ids"].append(artifact["module_id"])
        return body

    def handoff():
        return T7_BINDING_NOTE + "\n[T7 VERIFIED EXECUTION HANDOFF]\n" + json.dumps({
            "task_scope": route["task_scope"], "selected_packages": accepted,
            "selected_leaves": leaf_selections, **trace,
            "retrieval_evidence": "Only locally_retrieved_module_ids passed full local SHA-256 retrieval. "
                "Apply supplied artifacts only in their selected scopes. Block unavailable dependent specialized "
                "work; continue independent supported/baseline portions and expose material blockers. Do not emulate missing artifacts.",
        }, ensure_ascii=False)

    with OpenAI(api_key=config["openai_api_key"], base_url="https://api.openai.com/v1",
                timeout=120.0, max_retries=0) as client:
        route = t7_structured(client, config, messages, "\n\n".join(controls + [T7_BINDING_NOTE,
            "Perform TASK_SCOPE and ROOT_PACKAGE_SELECTION only under the exact supplied controls for the current "
            "request using relevant conversation context. Select packages by semantic applicability before local "
            "storage availability. Do not inspect or infer package leaf inventory at root. Do not suppress a "
            "semantically required package because its local body may be unavailable; the platform validates "
            "retrieval after selection. Do not report expected post-selection retrieval availability as a routing "
            "blocker. Return exact root Catalog identities and scoped reasons. No package bodies have been retrieved "
            "yet. An empty selection is valid."]), ROUTE_SCHEMA, "hub_t7_root")
        blockers.extend(route["unresolved_blockers"])
        seen = set()
        for selection in route["selected_packages"]:
            package_id = selection["package_id"]
            trace["root_selected_package_ids"].append(package_id)
            identity = catalog.get(package_id)
            if (identity is None or package_id in seen or any(selection[key] != identity[key]
                for key in ("entrypoint_module_id", "runtime_role"))):
                blockers.append(f"{package_id}: unknown, duplicate or mismatched root identity; selected portion blocked.")
                continue
            seen.add(package_id)
            accepted.append(selection)
            if package_id not in bindings:
                blockers.append(f"{package_id}: unavailable in T7 LOCAL_RUNTIME_FILE; specialized portion blocked; must not be emulated.")
                continue
            package = bindings[package_id]
            entry = package["entrypoint"]
            try:
                if (entry["module_id"] != identity["entrypoint_module_id"]
                    or entry["runtime_role"] != identity["runtime_role"]
                    or entry["version"] != identity["version"] or identity["status"] != "ACTIVE"):
                    raise ValueError(f"{package_id}: binding/Catalog identity mismatch; package blocked.")
                core = retrieve(entry)
                if "local_catalog" in package:
                    local = retrieve(package["local_catalog"])
                    leaf_catalog = t7_catalog_identities(local, "entries", "module_id")
                    # The catalog interface identity is declared by the root, not inferred from a filename.
                    local_id = package["local_catalog"]
                    package_block = controls[3].split("- package_id: " + package_id + "\n", 1)[1].split("\n- package_id:", 1)[0]
                    interface_block = package_block.split("  local_catalog:\n", 1)[1].split("    location:", 1)[0]
                    expected_interface = {**local_id, "package_id": package_id, "status": "ACTIVE"}
                    for key in ("module_id", "package_id", "runtime_role", "status", "version"):
                        scalar = f"    {key}: "
                        root_value = [line[len(scalar):].strip("'\"") for line in interface_block.splitlines()
                                      if line.startswith(scalar)]
                        if root_value != [expected_interface[key]]:
                            raise ValueError(f"{package_id}: local Catalog interface identity mismatch.")
                    bodies[package_id] = [core, local]
                else:
                    bodies[package_id] = [core]
                trace["locally_retrieved_package_ids"].append(package_id)
            except (ValueError, IndexError) as exc:
                blockers.append(f"{package_id}: required interface blocked: {exc}")

        concept_id = "HUB-PKG-CONCEPT-DEVELOPMENT"
        if concept_id in bodies:
            local_result = t7_structured(client, config, messages, "\n\n".join([
                controls[0], handoff(), t7_concept_binding_view(bindings), *bodies[concept_id],
                "Perform Concept-local leaf selection only for the current selected Concept scopes. "
                "Use the exact supplied core and Catalog semantics. The T7 Concept binding view changes storage "
                "binding only: old ChatGPT Library resolution fields do not block selection of a locally bound leaf. "
                "Specialized leaf bodies are intentionally retrieved only after this selection phase, so their "
                "expected not-yet-retrieved state is not an unresolved blocker. Report only semantic/control/identity "
                "blockers that prevent a valid selection. Return zero or more scoped leaf identities and blockers."]),
                LEAF_SCHEMA, "hub_t7_concept")
            blockers.extend(local_result["unresolved_blockers"])
            requested = {}
            for leaf in local_result["selected_leaves"]:
                module_id = leaf["module_id"]
                trace["concept_selected_leaf_ids"].append(module_id)
                identity = leaf_catalog.get(module_id)
                bound = next((a for a in bindings[concept_id]["leaves"] if a["module_id"] == module_id), None)
                if (identity is None or bound is None or identity["status"] != "ACTIVE"
                    or leaf["runtime_role"] != identity["runtime_role"]
                    or any(bound[key] != identity[key] for key in ("module_id", "runtime_role", "version"))):
                    blockers.append(f"{module_id}: unknown, unbound or mismatched leaf identity; leaf portion blocked.")
                    continue
                leaf_selections.append(leaf)
                requested[module_id] = bound
            for bound in bindings[concept_id]["leaves"]:
                if bound["module_id"] in requested:
                    try:
                        bodies[concept_id].append(retrieve(bound))
                    except ValueError as exc:
                        blockers.append(str(exc))

        instructions = [controls[0], handoff()]
        for package_id in ("HUB-PKG-TECHNICAL", concept_id):
            instructions.extend(bodies.get(package_id, []))
        response = client.responses.create(model=config["model"], input=messages,
                                           instructions="\n\n".join(instructions), store=False)
        if response.status != "completed" or not response.output_text or not response.output_text.strip():
            raise ValueError("T7: API chưa hoàn tất hoặc thiếu văn bản; lượt này chưa được lưu vào lịch sử.")
        return response.output_text, trace


def main():
    st.title("Central Hub Local")
    try:
        config = read_config()
    except ValueError as exc:
        st.error(str(exc))
        st.stop()
    st.caption(f"Model: {config['model']}")
    mode = st.radio("Chế độ", (RUNTIME_MODE, *MODES))
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
