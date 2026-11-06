"""Shared low-level primitives for the local runtime and diagnostic UI."""
import hashlib
import json
import re
from pathlib import Path

from openai import OpenAI


HUB_CI_PATH = Path(__file__).resolve().parent / "Central Hub" / "HUB_CI_v1.1.md"
HUB_ROUTER_PATH = HUB_CI_PATH.with_name("HUB_ROUTER_v1.1.yaml")
HUB_ARCHITECTURE_PATH = HUB_CI_PATH.with_name("HUB_ARCHITECTURE_v1.10.md")
HUB_CATALOG_PATH = HUB_CI_PATH.with_name("HUB_PACKAGE_CATALOG_v1.10.yaml")
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
RUNTIME_MODE = "Central Hub - Local Runtime"
T7_BINDINGS_PATH = Path(__file__).resolve().parent / "runtime" / "HUB_LOCAL_BINDINGS_v0.1.json"
LEAF_FIELDS = ("module_id", "runtime_role", "application_scope", "reason")
LEAF_SCHEMA = {
    "type": "object",
    "properties": {
        "selected_leaves": {"type": "array", "items": {
            "type": "object", "properties": {key: {"type": "string"} for key in LEAF_FIELDS},
            "required": list(LEAF_FIELDS), "additionalProperties": False,
        }},
        "unresolved_blockers": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["selected_leaves", "unresolved_blockers"], "additionalProperties": False,
}


def t7_catalog_identities(text, section, id_field):
    # Read only exact scalar identity fields in the current catalogs' flat entry lists.
    # This is not YAML semantic/applicability evaluation or a general YAML consumer.
    identities = {}
    current = None
    inside = False
    for line in text.splitlines():
        if line == section + ":":
            inside = True
            continue
        if not inside:
            continue
        if line and not line[0].isspace() and not line.startswith("- "):
            break
        match = re.fullmatch(r"- " + id_field + r": ([A-Z0-9-]+)", line)
        if match:
            current = match[1]
            if current in identities:
                raise ValueError("T7: Catalog có identity trùng lặp.")
            identities[current] = {id_field: current}
        elif current:
            match = re.fullmatch(r"  (entrypoint_module_id|runtime_role|status|version): ([^ ]+)", line)
            if match:
                key, value = match.groups()
                if key in identities[current]:
                    raise ValueError("T7: Catalog có trường identity trùng lặp.")
                identities[current][key] = value.strip("'\"")
    required = {id_field, "runtime_role", "status", "version"}
    if id_field == "package_id":
        required.add("entrypoint_module_id")
    if not identities or any(set(value) != required for value in identities.values()):
        raise ValueError("T7: Không đọc được identity Catalog chính xác.")
    return identities


def t7_read(path):
    try:
        return path.read_bytes().decode("utf-8")
    except (OSError, UnicodeError):
        raise ValueError(f"T7: Không đọc được {path.name}; không chuyển chế độ hoặc dùng nguồn thay thế.") from None


def t7_load_bindings(text):
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate key")
            result[key] = value
        return result

    try:
        manifest = json.loads(text, object_pairs_hook=unique_object)
        if (set(manifest) != {"binding_version", "status", "host_purpose", "retrieval_authority", "packages"}
            or manifest["binding_version"] != "0.1" or manifest["status"] != "ACTIVE"
            or manifest["retrieval_authority"] != "LOCAL_RUNTIME_FILE"
            or not isinstance(manifest["host_purpose"], str) or not manifest["host_purpose"].strip()):
            raise ValueError()
        packages = manifest["packages"]
        if set(packages) != {"HUB-PKG-TECHNICAL", "HUB-PKG-CONCEPT-DEVELOPMENT"}:
            raise ValueError()
        technical = packages["HUB-PKG-TECHNICAL"]
        concept = packages["HUB-PKG-CONCEPT-DEVELOPMENT"]
        if set(technical) != {"entrypoint"} or set(concept) != {"entrypoint", "local_catalog", "leaves"}:
            raise ValueError()
        if not isinstance(concept["leaves"], list) or len(concept["leaves"]) != 3:
            raise ValueError()
        artifacts = [technical["entrypoint"], concept["entrypoint"], concept["local_catalog"], *concept["leaves"]]
        expected = [("HUB-DOM-TECHNICAL", "REASONING_PROFILE", "1.0"),
                    ("HUB-DOM-CONCEPT-DEVELOPMENT", "DOMAIN_CONTROL", "1.1"),
                    ("HUB-CATALOG-CONCEPT-DEVELOPMENT", "PACKAGE_CATALOG", "1.1"),
                    ("HUB-DOM-CREATIVE", "DOMAIN_CONTROL", "1.1"),
                    ("HUB-CAP-BRAINSTORM", "CAPABILITY", "1.1"),
                    ("HUB-CAP-DEBATE", "CAPABILITY", "1.0")]
        for artifact, identity in zip(artifacts, expected):
            if (set(artifact) != {"module_id", "runtime_role", "version", "path", "sha256"}
                or (artifact["module_id"], artifact["runtime_role"], artifact["version"]) != identity
                or not all(isinstance(value, str) for value in artifact.values())
                or not re.fullmatch(r"[0-9a-f]{64}", artifact["sha256"])):
                raise ValueError()
        return packages
    except (ValueError, TypeError, KeyError, AttributeError):
        raise ValueError("T7: HUB_LOCAL_BINDINGS_v0.1.json không hợp lệ; yêu cầu chưa gửi API.") from None


def t7_concept_binding_view(bindings):
    concept = bindings["HUB-PKG-CONCEPT-DEVELOPMENT"]
    return "[T7 CONCEPT LOCAL BINDING AVAILABILITY]\n" + json.dumps({
        "retrieval_authority": "LOCAL_RUNTIME_FILE",
        "package_id": "HUB-PKG-CONCEPT-DEVELOPMENT",
        "entrypoint": {key: concept["entrypoint"][key] for key in ("module_id", "runtime_role", "version")},
        "local_catalog": {key: concept["local_catalog"][key] for key in ("module_id", "runtime_role", "version")},
        "locally_bound_leaves": [
            {key: leaf[key] for key in ("module_id", "runtime_role", "version")}
            for leaf in concept["leaves"]
        ],
        "selection_rule": (
            "This is storage-binding availability only. Select leaves only under the exact supplied "
            "Concept core/Catalog semantics. Body retrieval and SHA-256 verification happen after selection."
        ),
    }, ensure_ascii=False)


def t7_retrieve(artifact):
    repo = Path(__file__).resolve().parent
    relative = Path(artifact["path"])
    try:
        if relative.is_absolute() or relative.drive or ".." in relative.parts:
            raise ValueError()
        path = (repo / relative).resolve()
        if not path.is_relative_to(repo / "runtime"):
            raise ValueError()
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != artifact["sha256"]:
            raise ValueError()
        return data.decode("utf-8")
    except (OSError, UnicodeError, ValueError, RuntimeError):
        raise ValueError(f"T7: {artifact['module_id']} không truy xuất được hoặc sai path/SHA-256/UTF-8; phần phụ thuộc bị chặn, không fallback.") from None


def t7_structured(client, config, messages, instructions, schema, name):
    response = client.responses.create(
        model=config["model"], input=messages, instructions=instructions, store=False,
        text={"format": {"type": "json_schema", "name": name, "schema": schema, "strict": True}},
    )
    try:
        if response.status != "completed" or any(
            part.type == "refusal" for item in response.output if item.type == "message" for part in item.content
        ):
            raise ValueError()
        record = json.loads(response.output_text)
        key, fields = ("selected_packages", ROUTE_PACKAGE_FIELDS) if schema is ROUTE_SCHEMA else ("selected_leaves", LEAF_FIELDS)
        if (not isinstance(record, dict) or set(record) != set(schema["required"])
            or not isinstance(record["unresolved_blockers"], list)
            or not all(isinstance(value, str) for value in record["unresolved_blockers"])
            or (key == "selected_packages" and not isinstance(record["task_scope"], str))
            or not isinstance(record[key], list)
            or not all(isinstance(item, dict) and set(item) == set(fields)
                       and all(isinstance(value, str) for value in item.values()) for item in record[key])):
            raise ValueError()
        return record
    except (ValueError, TypeError, AttributeError):
        raise ValueError("T7: Phản hồi lựa chọn không hợp lệ; không đoán hoặc thử lại; chưa lưu lượt.") from None
