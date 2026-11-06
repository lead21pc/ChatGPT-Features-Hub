# Báo cáo migration Central Hub — 2026-10-17

Trạng thái: architecture mới đã triển khai trực tiếp trong local working copy. Không candidate/shadow package. Không deployment, stage, commit, push, branch/tag/worktree mới. Một thư mục FSP rỗng còn bị Windows khóa; không còn file hoặc standalone control ở đó.

## A. Nguồn và baseline

- Repository local: `<WORKSHOPS_REPO>`.
- Target: `<WORKSHOPS_REPO>\Central Hub`.
- Branch: `main`; HEAD: `8ecc4f3dcb8d75d7543462ffdcedd2f100a299c2`.
- Baseline dirty: 33 entry (26 tracked deletion, 2 tracked modification, 5 untracked entry) thuộc Project Feather Core; không chồng write scope. Index ban đầu không có staged change.
- READ: governance/global baseline và ba cây source FSP/AIS/ImageT ở working copy. WRITE: Central Hub và gỡ predecessor đã archive tại đúng ba cây nguồn được task chỉ định. Không sửa global CI/rationale/governance hoặc Project Feather Core/worlds.
- Không fallback GitHub: mọi source bắt buộc đọc được local. Không truy vấn/sync remote.
- Đã đọc nội dung đầy đủ các tệp sau (đường dẫn tính từ repository root):

- `SYSTEM_CONTEXT.md`
- `AGENTS.md`
- `llm-controls/global-instructions/ChatGPT Project Global Native/chatgpt v9.0.txt`
- `llm-controls/global-instructions/ChatGPT Project Global Native/DESIGN_RATIONALE.md`
- `llm-controls/Friendly Support Project/FSP_CI_v0.3.1.md`
- `llm-controls/Friendly Support Project/router/FSP_ROUTER_v0.2.md`
- `llm-controls/Friendly Support Project/profiles/CREATIVE_v0.1.md`
- `llm-controls/Friendly Support Project/profiles/TECHNICAL_v0.1.md`
- `llm-controls/Friendly Support Project/overlays/BRAINSTORM_v0.1.md`
- `Authorize Integrity Search/README.md`
- `Authorize Integrity Search/Authorize Integrity Search CI/AIS_CI_v0.1.md`
- `Authorize Integrity Search/Authorize Integrity Search Modules/AIS_SOURCE_ROUTER_v0.1.yaml`
- `Authorize Integrity Search/tests/ROUTE_TEST_CASES.md`
- `Image Transcendent/Image Transcendent CI/ImageT_v1.0.0.md`
- `Image Transcendent/Image Transcendent CI/README.md`
- `Image Transcendent/Image Transcendent Modules/IMAGE_SOURCE_ROUTER.yaml`
- `Image Transcendent/Image Transcendent Modules/manifest.yaml`
- `Image Transcendent/Image Transcendent Modules/IMAGE_ANTI_PRIOR.md`
- `Image Transcendent/Image Transcendent Modules/config.md`
- `Image Transcendent/Image Transcendent Modules/HUMANOID_CHARACTER_DESIGN_PREFERENCE.md`
- `Image Transcendent/Image Transcendent Modules/YAML_MIGRATION_NOTES.md`
- `Image Transcendent/Image Transcendent CI/ImageT_v1.0.0-ready-gate-candidate.md`
- `Image Transcendent/Image Transcendent CI/READY_GATE_CANDIDATE_TESTS.md`
- `Image Transcendent/Image Transcendent Modules/ROUTE_TEST_CASES.md`
- `Image Transcendent/Image Transcendent Modules/tests/test_yaml_routing.py`
- `Image Transcendent/Image Transcendent Modules/PREFERENCE_M2_TEST_PLAN.md`

Các predecessor cũ khác và archive có sẵn chỉ được kiểm kê/sao lưu bytes/hash; không được lấy làm authority active hoặc đọc để khôi phục hành vi.

## B. Tệp mới trong Hub

20 tệp ngoài archive, gồm báo cáo này:

- `HUB_CI_v1.0.md`
- `HUB_ROUTER_v1.0.yaml`
- `MIGRATION_REPORT.md`
- `README.md`
- `capabilities/BRAINSTORM_v1.0.md`
- `domains/creative/CREATIVE_v1.0.md`
- `domains/technical/TECHNICAL_v1.0.md`
- `tests/HUB_ROUTE_TEST_CASES.md`
- `tests/test_hub_contracts.py`
- `tool_pipelines/AIS/AIS_PIPELINE_v1.0.md`
- `tool_pipelines/AIS/AIS_ROUTER_v1.0.yaml`
- `tool_pipelines/AIS/tests/ROUTE_TEST_CASES.md`
- `tool_pipelines/ImageT/IMAGE_ANTI_PRIOR.md`
- `tool_pipelines/ImageT/IMAGE_CONTROLLER_v1.0.md`
- `tool_pipelines/ImageT/IMAGE_SOURCE_ROUTER.yaml`
- `tool_pipelines/ImageT/config.md`
- `tool_pipelines/ImageT/manifest.yaml`
- `tool_pipelines/ImageT/preferences/HUMANOID_CHARACTER_DESIGN_PREFERENCE.md`
- `tool_pipelines/ImageT/tests/READY_GATE_TEST_CASES.md`
- `tool_pipelines/ImageT/tests/ROUTE_TEST_CASES.md`

Thêm `Source_archive/README.md`, `Source_archive/ARCHIVE_RECEIPT.json` và 36 tệp lưu nguồn được liệt kê ở D. Tổng Hub: 58 tệp.

## C. Mapping và chủ sở hữu

Đánh giá proposal: ACCEPT WITH LOCAL CORRECTION. Xác nhận của người dùng rằng Ready Gate là baseline active thay metadata candidate trong nguồn cũ; người dùng cũng xác nhận hành vi Ready Gate đã được thử live trong ImageT Project gốc. Đây là user-confirmed project state, không phải xác nhận tích hợp Central Hub đã thử live. Global ChatGPT v9.0 giữ nguyên ở vị trí dùng chung; chỉ là semantic baseline của Hub, không bị archive.

| Nguồn cũ | Đích mới (từ Hub root) | Thay đổi |
| --- | --- | --- |
| `chatgpt v9.0.txt + phần riêng FSP_CI_v0.3.1.md` | `HUB_CI_v1.0.md` | Giữ các owner v9.0; thêm support/fiction và delegation; không ghép FSP CI nguyên khối. |
| `FSP_ROUTER_v0.2.md` | `HUB_ROUTER_v1.0.yaml` | Ba trục độc lập; không chọn thao tác hội thoại hoặc dependency nội bộ pipeline. |
| `CREATIVE_v0.1.md` | `domains/creative/CREATIVE_v1.0.md` | Giữ cơ chế phát triển sáng tạo, bỏ phần global trùng. |
| `TECHNICAL_v0.1.md` | `domains/technical/TECHNICAL_v1.0.md` | Giữ cơ chế, chẩn đoán, phép kiểm phân biệt và hồi quy. |
| `BRAINSTORM_v0.1.md` | `capabilities/BRAINSTORM_v1.0.md` | Thân kỹ thuật từ Branching trở đi giữ nguyên; sửa role/host. |
| `AIS_CI_v0.1.md` | `tool_pipelines/AIS/AIS_PIPELINE_v1.0.md` | Bỏ nested CI và owner toàn turn; giữ mediation, scope và evidence handoff. |
| `AIS_SOURCE_ROUTER_v0.1.yaml` | `tool_pipelines/AIS/AIS_ROUTER_v1.0.yaml` | DIRECT thành Hub bypass; giữ search_contract/source_policy, thêm tool-facing instruction/pre-call check. |
| `AIS tests/ROUTE_TEST_CASES.md` | `tool_pipelines/AIS/tests/ROUTE_TEST_CASES.md` | Port đủ 28 ca; bypass và entry theo Hub. |
| `ImageT_v1.0.0.md + phần Ready Gate của bản ready-gate` | `tool_pipelines/ImageT/IMAGE_CONTROLLER_v1.0.md` | Controller subordinate; Ready Gate active theo xác nhận người dùng; không dùng candidate layer. |
| `IMAGE_SOURCE_ROUTER.yaml` | `tool_pipelines/ImageT/IMAGE_SOURCE_ROUTER.yaml` | Controller ở Project Sources; không chọn/thay Project instructions; đọc lại mỗi operation/retry. |
| `manifest.yaml` | `tool_pipelines/ImageT/manifest.yaml` | Inventory controller/modules nội bộ, phiên bản/hash/compatibility; không Hub manifest. |
| `IMAGE_ANTI_PRIOR.md + config.md` | `tool_pipelines/ImageT/IMAGE_ANTI_PRIOR.md + config.md` | Giữ byte-exact cả hai tệp và phiên bản. |
| `HUMANOID_CHARACTER_DESIGN_PREFERENCE.md` | `tool_pipelines/ImageT/preferences/HUMANOID_CHARACTER_DESIGN_PREFERENCE.md` | Chỉ đổi baseline reference/provenance; giữ candidate/inactive/direct-input experiment, không promotion. |
| `ROUTE_TEST_CASES.md + READY_GATE_CANDIDATE_TESTS.md` | `tool_pipelines/ImageT/tests/ROUTE_TEST_CASES.md + READY_GATE_TEST_CASES.md` | Giữ preservation cases và 22 Ready Gate cases; sửa topology thành active controller. |
| `tests/test_yaml_routing.py` | `tests/test_hub_contracts.py` | Port các kiểm inventory/hash/compatibility/preservation/missing source; thay installed-CI oracle bằng controller oracle, thêm Hub/AIS và Ready Gate transitions. |

Rà soát duplicate owner (REVIEWED_TEXT): Hub CI giữ output/grounding/turn/state/truth/general verification/action reports; Hub Router chỉ selection/scope/dependency trực tiếp. CREATIVE giữ phát triển sản phẩm hư cấu; TECHNICAL giữ cơ chế/chẩn đoán/thay đổi có giới hạn; BRAINSTORM giữ năm nhóm kỹ thuật. AIS giữ lock/source policy/evidence merge/coverage nghiên cứu. ImageT giữ field authority/operation lock/prompt/Ready Gate/visible verification. Constraint trong pipeline chỉ ràng buộc operation đã giao, không tái chọn stage toàn turn. Không có owner cạnh tranh, coordinator/registry/Hub manifest/domain router/AIS anti-prior mới.

## D. Archive và xác minh

36/36 tệp, 214.904 bytes, SHA-256 đích trùng nguồn trước khi gỡ. Receipt chứa hash đầy đủ/bytes/path cho từng tệp. Bảng dưới đồng thời là danh sách gỡ khỏi vị trí active cũ. Tên archive cũ chuyển thành historical_sources để có đúng một Source_archive root; bytes không đổi.

| Đường dẫn cũ từ repository root | Đích từ Hub root | SHA-256 |
| --- | --- | --- |
| `llm-controls/Friendly Support Project/FSP_CI_v0.2.md` | `Source_archive/Friendly Support Project/FSP_CI_v0.2.md` | `3de265f54e26ebd1be9888591db6b8552aa4c0a9e500b2f2c4effb19397a4915` |
| `llm-controls/Friendly Support Project/FSP_CI_v0.3.1.md` | `Source_archive/Friendly Support Project/FSP_CI_v0.3.1.md` | `193879ab921f95655e2b507b76eef075bee3897236e98d541b1bc015fbf7ede8` |
| `llm-controls/Friendly Support Project/FSP_CI_v0.3.md` | `Source_archive/Friendly Support Project/FSP_CI_v0.3.md` | `ed42fad5d1a36ca92ee0102e4051a9690dd53c1bb1e09b2d6299ae1d1fe5b6a4` |
| `llm-controls/Friendly Support Project/overlays/BRAINSTORM_v0.1.md` | `Source_archive/Friendly Support Project/overlays/BRAINSTORM_v0.1.md` | `4af3173fd85c0f116549aa5588d6a31b646f332b642b62f1f499fb123cc39917` |
| `llm-controls/Friendly Support Project/profiles/CREATIVE_v0.1.md` | `Source_archive/Friendly Support Project/profiles/CREATIVE_v0.1.md` | `471177aa863b46afacbe4eda663f89bcc7bffcec870bd00e387a9df8a4a4e631` |
| `llm-controls/Friendly Support Project/profiles/TECHNICAL_v0.1.md` | `Source_archive/Friendly Support Project/profiles/TECHNICAL_v0.1.md` | `a866cb9e0d001cc906143b08f8fd31a9176b69db7379e5d0ddd211bb2a494492` |
| `llm-controls/Friendly Support Project/router/FSP_ROUTER_v0.1.md` | `Source_archive/Friendly Support Project/router/FSP_ROUTER_v0.1.md` | `2c88df7cf9d067041ea18a92f53fb3ff24f8bb84f593344c5e0021e20e72d165` |
| `llm-controls/Friendly Support Project/router/FSP_ROUTER_v0.2.md` | `Source_archive/Friendly Support Project/router/FSP_ROUTER_v0.2.md` | `e60c83cd316b90db4684abdb9645d3a503508631699e99224c056d05f5d3b54f` |
| `llm-controls/Friendly Support Project/source_archive/FSP_CI_v0.1.md` | `Source_archive/Friendly Support Project/historical_sources/FSP_CI_v0.1.md` | `5a8bf3492fe4ab1f4fba097b1eed51aaace02afb6bc8ce8645f4e732135db714` |
| `llm-controls/Friendly Support Project/source_archive/Project CI v0.1 — Controlled Flexible Interaction.txt` | `Source_archive/Friendly Support Project/historical_sources/Project CI v0.1 — Controlled Flexible Interaction.txt` | `c4f71b6e9e9b249cdf909d9ee314607d53fca4c52b83f85c0847f80ad825b005` |
| `Authorize Integrity Search/Authorize Integrity Search CI/AIS_CI_v0.1.md` | `Source_archive/Authorize Integrity Search/Authorize Integrity Search CI/AIS_CI_v0.1.md` | `6ad515e8f60ca148a31dfe14c561d3372d82d2e09a3f119bf4f779ac2dc00487` |
| `Authorize Integrity Search/Authorize Integrity Search Modules/AIS_SOURCE_ROUTER_v0.1.yaml` | `Source_archive/Authorize Integrity Search/Authorize Integrity Search Modules/AIS_SOURCE_ROUTER_v0.1.yaml` | `851499d58c29b3722bfcfdb93b26cbb43b6506ddb3febc50df9e5b19478389f0` |
| `Authorize Integrity Search/README.md` | `Source_archive/Authorize Integrity Search/README.md` | `82bfcd84c3e1c30df6bae8d08ea2c4773af056ec8a08cf3192a7cbb882ecab0b` |
| `Authorize Integrity Search/tests/ROUTE_TEST_CASES.md` | `Source_archive/Authorize Integrity Search/tests/ROUTE_TEST_CASES.md` | `4f80e43bac7edd4a48491978db7ceb7543220d76beab0c3a297a68b72b8cc762` |
| `Image Transcendent/Image Transcendent CI/.gitattributes` | `Source_archive/Image Transcendent/Image Transcendent CI/.gitattributes` | `d5ee7a79f983554a67325d8159570fa9b5e2130078a124bc1ee6fc0c3af6e489` |
| `Image Transcendent/Image Transcendent CI/ImageT_v1.0.0-ready-gate-candidate.md` | `Source_archive/Image Transcendent/Image Transcendent CI/ImageT_v1.0.0-ready-gate-candidate.md` | `ec4553319aec54403a5ceaf94598fddc099e03aa99f5ea9380e28a0adaf389ee` |
| `Image Transcendent/Image Transcendent CI/ImageT_v1.0.0.md` | `Source_archive/Image Transcendent/Image Transcendent CI/ImageT_v1.0.0.md` | `21302c724c6c3358f25fd45e084d23db674600309311ce08a8e8f8f9bca89bc6` |
| `Image Transcendent/Image Transcendent CI/README.md` | `Source_archive/Image Transcendent/Image Transcendent CI/README.md` | `71e7f96f6a2478a3deb03ec5c2da3cb0fa4a027d7548d236e4f9064a7b9dfd95` |
| `Image Transcendent/Image Transcendent CI/READY_GATE_CANDIDATE_TESTS.md` | `Source_archive/Image Transcendent/Image Transcendent CI/READY_GATE_CANDIDATE_TESTS.md` | `8a3f6ebd333a0d758037a0b90b78613a7da1dcc85f75bb2c966fb40d49a8c499` |
| `Image Transcendent/Image Transcendent CI/source_archive/CI.md` | `Source_archive/Image Transcendent/Image Transcendent CI/historical_sources/CI.md` | `a2bce4ef9275b99441ac420c4cee36ad98d053278e9fd9519a7f7765ccdacebc` |
| `Image Transcendent/Image Transcendent Modules/.gitattributes` | `Source_archive/Image Transcendent/Image Transcendent Modules/.gitattributes` | `ea35f200b65189346372e8bf0754ecdbc13227ad1a79fbbfb4755242dd36b8c1` |
| `Image Transcendent/Image Transcendent Modules/config.md` | `Source_archive/Image Transcendent/Image Transcendent Modules/config.md` | `20b08b3b99b237eebeec0442024e0818245d0b0bebc2fb756e972aca67d4d3d7` |
| `Image Transcendent/Image Transcendent Modules/HUMANOID_CHARACTER_DESIGN_PREFERENCE.md` | `Source_archive/Image Transcendent/Image Transcendent Modules/HUMANOID_CHARACTER_DESIGN_PREFERENCE.md` | `3652c341c3f3c5c4caefeca107643b40c58c4ff721c4aa26a3be49095fb7a16e` |
| `Image Transcendent/Image Transcendent Modules/IMAGE_ANTI_PRIOR.md` | `Source_archive/Image Transcendent/Image Transcendent Modules/IMAGE_ANTI_PRIOR.md` | `f08a1d1a09c8b31cd3fe6ed80b38b19f2c662e15f7e192b42c8a5e044aa69b5c` |
| `Image Transcendent/Image Transcendent Modules/IMAGE_SOURCE_ROUTER.yaml` | `Source_archive/Image Transcendent/Image Transcendent Modules/IMAGE_SOURCE_ROUTER.yaml` | `b621ff4922edf75cd6f9f49e57e11b59747691568db02651a478792c6c0416c9` |
| `Image Transcendent/Image Transcendent Modules/manifest.yaml` | `Source_archive/Image Transcendent/Image Transcendent Modules/manifest.yaml` | `51b1f28e0295f5781e57945268c594564fad3fc934a05b4b4b8dd42ad20f5538` |
| `Image Transcendent/Image Transcendent Modules/PREFERENCE_M2_TEST_PLAN.md` | `Source_archive/Image Transcendent/Image Transcendent Modules/PREFERENCE_M2_TEST_PLAN.md` | `0d0d73224a1b692a28fc24f8e97705fd1b9ad926eb2bd17c2bec2cfd58c61b63` |
| `Image Transcendent/Image Transcendent Modules/ROUTE_TEST_CASES.md` | `Source_archive/Image Transcendent/Image Transcendent Modules/ROUTE_TEST_CASES.md` | `bd2123617d2d45b61e74a6c947794a8cc85720f0d259293826a444bae47fc860` |
| `Image Transcendent/Image Transcendent Modules/source_archive/02-02-config-1.md` | `Source_archive/Image Transcendent/Image Transcendent Modules/historical_sources/02-02-config-1.md` | `1458eff9790c02bf146cca48232a7d352308a00f8fa1b684eba5a32b94ff8faa` |
| `Image Transcendent/Image Transcendent Modules/source_archive/03-01-IMAGE_SOURCE_ROUTER-1-.md` | `Source_archive/Image Transcendent/Image Transcendent Modules/historical_sources/03-01-IMAGE_SOURCE_ROUTER-1-.md` | `aac3d5326c663334332a5c95e9ebb41445e9df61ea23311cada316fb946b2abc` |
| `Image Transcendent/Image Transcendent Modules/source_archive/HUMANOID_CHARACTER_DESIGN_PREFERENCE_v0.1.0-candidate.md` | `Source_archive/Image Transcendent/Image Transcendent Modules/historical_sources/HUMANOID_CHARACTER_DESIGN_PREFERENCE_v0.1.0-candidate.md` | `2e4663e4b897d9c144cee5f8199c3ad5d768608f27bb2778e81573cb09e70442` |
| `Image Transcendent/Image Transcendent Modules/source_archive/IMAGE_ANTI_PRIOR.md` | `Source_archive/Image Transcendent/Image Transcendent Modules/historical_sources/IMAGE_ANTI_PRIOR.md` | `3083b0a6de6843845f50c5a23073864254dddfec651ef9d5ede6d749dbc0033e` |
| `Image Transcendent/Image Transcendent Modules/source_archive/IMAGE_SOURCE_ROUTER.md` | `Source_archive/Image Transcendent/Image Transcendent Modules/historical_sources/IMAGE_SOURCE_ROUTER.md` | `de3daf811c5b14e03ea24dc101655aa0d177153a29c6c6c7c768ee76b6732227` |
| `Image Transcendent/Image Transcendent Modules/source_archive/manifest.md` | `Source_archive/Image Transcendent/Image Transcendent Modules/historical_sources/manifest.md` | `609bc18cec5ec1868732b50e9bddf169c4ecb56df1c36d2f8d6c7b4ff9e5dbc2` |
| `Image Transcendent/Image Transcendent Modules/tests/test_yaml_routing.py` | `Source_archive/Image Transcendent/Image Transcendent Modules/tests/test_yaml_routing.py` | `3c9a74dfead36b7f34763f84410792caffae84057856c19e2f482add206f61ea` |
| `Image Transcendent/Image Transcendent Modules/YAML_MIGRATION_NOTES.md` | `Source_archive/Image Transcendent/Image Transcendent Modules/YAML_MIGRATION_NOTES.md` | `9247c395c96c1cf1f7f3c954414aa820452d27e7132c3a4c616824435c6f2243` |

Archive chỉ lịch sử; không route, fallback, tự phục hồi hoặc tự promotion. Checker skill ban đầu trả BLOCKED vì nguồn ngoài artifact root; đây là giới hạn giả định layout của helper, không conflict với migration mà user chỉ định. Kiểm layout sau khi dựng Hub trả PASS_SHARED tại Source_archive root; receipt/hash và kiểm resolved paths thực hiện riêng cho cross-root migration. Không sửa helper hoặc source bytes.

## E. Vị trí standalone đã gỡ

- Authorize Integrity Search: gỡ toàn bộ file và cây thư mục cũ sau xác minh archive.
- Image Transcendent: gỡ toàn bộ file và cây thư mục cũ sau xác minh archive.
- llm-controls/Friendly Support Project: gỡ toàn bộ 10 file và các thư mục con; root rỗng còn bị tiến trình khác khóa. Hai lần Remove-Item báo `The process cannot access the file ... because it is being used by another process.` Không cưỡng chế đóng tiến trình. Git không theo dõi thư mục rỗng; đây là việc dọn thư mục còn lại, không phải kiến trúc standalone còn hoạt động.

## F. Kích thước và định dạng Hub CI

- LF characters: **7496**.
- CRLF characters: **7555**.
- UTF-8 bytes thực: **7500**.
- Không BOM; file dùng LF; CRLF vẫn còn 445 ký tự dưới trần 8.000. Không lấp đầy ngân sách.

## G. Hub Router

- YAML parse và conservative subset pass; không duplicate key/anchor/alias/merge/custom tag/implicit date/boolean mơ hồ.
- DOMAIN/CAPABILITY/TOOL_PIPELINE độc lập; NONE không có file, không persistent mode. Mixed task scope theo phần; hỗ trợ các tổ hợp yêu cầu bằng selection riêng.
- Mọi control path được map đều tồn tại. Thiếu control quyết định: nêu đúng dependency, chặn phần phụ thuộc, làm phần độc lập; baseline chỉ khi đủ, không claim tương đương. Không archive route/latest-version discovery.

## H. AIS

- Chỉ VERIFY/RESEARCH/EXPLORE; DIRECT cũ chỉ còn như lịch sử hoặc lời giải thích bypass.
- search_contract giữ đúng trường hiện có, được làm rõ operation/evidence purpose, conditions/versions, roles và protected state. Không schema thứ hai.
- Lock -> tool-facing instruction -> pre-call check -> execution -> evidence merge -> coverage/support -> Hub. Gate không là approval mặc định.
- source_policy được bảo toàn bằng canonical hash: freshness/primary/direct/corroboration/conflict/injection/read support/Memory. Handoff giữ actual reads, findings, conditions, inference, conflicts/gaps, coverage và actual actions. Unresolved không thành verified.

## I. ImageT

Ghi nhận migration và correction đặc tả trước promotion; cấu hình versioned hiện hành được ghi ở mục M.

- Controller subordinate active trong Project Sources; manifest không chọn/thay Hub CI. Local manifest giữ inventory/version/hash/compatibility, template optional_absent, preference candidate inactive/direct-only.
- Anti-prior/config byte-exact. Authority/operation-lock/prompt body giữ ngữ nghĩa nguyên văn, chỉ đổi This CI thành This controller; Ready Gate body nguyên văn từ nguồn cũ, kiểm bằng fixed hash.
- Ready Gate active cho CREATE/EDIT/VARIATION/CORRECT/retry: đúng prompt version, phê duyệt một call, revision/stale invalidates, không ngầm retry, không generation khi chưa duyệt. ANALYZE không tạo ảnh/không Ready Gate.
- Ready Gate là runtime prompt-authorization boundary bắt buộc; `READY_GATE_TEST_CASES.md` là required normative migration/regression oracle, không phải runtime Source hoặc optional test collateral. Đã sửa OBSERVED MIGRATION DEVIATION: bản port rút gọn giữ R01–R22 nhưng làm yếu preparation, topology và acceptance/evidence framing. Correction phục hồi vai trò này, không đổi runtime controller.
- ORIGINAL IMAGET READY GATE: USER-CONFIRMED PRIOR LIVE VALIDATION. Hành vi đã được thử live trong ImageT Project gốc theo xác nhận người dùng; current sources không có original live call trace/submitted payload để Codex tự tái xác minh hoặc claim đã truy cập.
- STATIC MIGRATION PRESERVATION: controller giữ nguyên thân Ready Gate và fixed hash. CENTRAL HUB LIVE TEST: NOT RUN. Bảo toàn cấu trúc/hành vi đã biết không chứng minh deployment hoặc tích hợp Central Hub đã thử live.
- Xác minh sau ảnh theo visible evidence: PASS/LOCAL_FAIL/STRUCTURAL_FAIL/UNVERIFIABLE. Tool result không tự thành default; reference chỉ theo role đã giao. Không activation từ listing/applicability; mỗi operation/retry đọc lại sources.

## J. Kiểm chứng

`python -B -m unittest discover -s tests -v`: **12/12 PASS, không skip** ở lần cuối trước báo cáo. PyYAML có sẵn 6.0.3, không đổi dependency.

| Lớp chứng cứ | Kết quả / giới hạn |
| --- | --- |
| STATIC CONTRACT TEST | Topology, owner order/size, YAML, exact inventory/hash/header/compatibility, byte preservation, source policy/Brainstorm/Ready Gate preservation, archive receipt và absence của file cũ pass. |
| SPEC SIMULATION | Oracle thử nghiệm kiểm missing/corrupt/incompatible/template mismatch/archive path, inactive preference, unknown selection và Ready Gate one-call/revision/stale/context loss. Oracle không thực thi model hoặc tool. |
| REVIEWED_TEXT | 30 ca Hub, 28 ca AIS và 22 ca Ready Gate; các ImageT preservation cases được port. Đối chiếu contract, không phải 80 runtime PASS. |
| ORIGINAL IMAGET READY GATE | USER-CONFIRMED PRIOR LIVE VALIDATION; theo project state người dùng xác nhận, không phải original payload do Codex quan sát trong task này. |
| CENTRAL HUB LIVE PROJECT / WORK / IMAGE TOOL | NOT RUN; không deploy, không gọi công cụ nghiên cứu/ảnh để thử tích hợp Hub. |

Kiểm hồi quy: baseline v9.0 giữ thứ tự GROUNDING -> TURN FUNCTION -> TRUTH STATUS, distinction observation/inference/assumption; hỗ trợ cảm xúc và viết hư cấu không ép specialization; các subordinate không giữ mode/đổi stage hoặc tự activate; ImageT anti-prior/config/negatives/reference/edit locality được bảo toàn. Test không chứng minh model luôn làm đúng.

## K. Phần cần runtime và giới hạn còn lại

- Cần thử Project/Work thật để biết control có được đọc/tuân thủ, tool có đủ access, evidence có đủ support và composition có giữ scope qua nhiều lượt.
- Ready Gate đã được thử live trong ImageT Project gốc theo xác nhận người dùng; tích hợp ImageT trong Central Hub chưa thử live. Thử Hub sau này cần quan sát version/approval/freshness và hard constraints của ảnh trong môi trường tích hợp; điều này không trì hoãn correction bảo toàn migration. Payload backend không quan sát được phải UNVERIFIABLE.
- Tất cả ca live cần ghi model/surface/date/sources, input, calls/reads/output; bước thử nằm trong từng test case file. Task migration không cấp quyền deployment/generation.
- Dọn root FSP rỗng cần tiến trình đang giữ thư mục nhả khóa. Không cần phục hồi file nguồn cũ để làm việc với Hub.

## L. Git và diff

- So baseline bằng porcelain -z: đủ 33 entry cũ giữ nguyên, task chỉ thêm đúng 36 unstaged deletion và một entry untracked Central Hub/.
- So byte-exact `git ls-files --stage -z`: index không đổi. Branch/HEAD không đổi. Không stage/commit/push/tag/PR/remote mutation/deployment.
- Diff tracked trong scope: 36 file cũ bị gỡ. Tệp Hub mới chưa tracked nên git diff thông thường chưa hiện additions/renames; receipt và danh sách B/D mô tả migration thực.
- Scoped git diff --check pass với cr-at-eol để không sửa CRLF lịch sử. Tệp active mới được kiểm UTF-8/BOM/whitespace trực tiếp vì chưa staged.

Baseline porcelain (đường dẫn từ repository root):

```text
 D Project Feather Core/New Canon and Consideration/AetherFire_Cold_Storage_Prototype_2026-10-02/00_AETHERFIRE_CONSOLIDATION_INDEX.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Cold_Storage_Prototype_2026-10-02/Anti-Drift Source/AetherFire_Anti_Drift_Source_Router_v4.0.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Cold_Storage_Prototype_2026-10-02/CANDIDATE_STATUS.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Cold_Storage_Prototype_2026-10-02/Cold Storage/AETHERFIRE_COLD_PACKAGE.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Cold_Storage_Prototype_2026-10-02/Cold Storage/COLD_STORAGE_AUDIT_AND_DEPLOYMENT.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Cold_Storage_Prototype_2026-10-02/Cold Storage/SOURCE_STORAGE_INVENTORY.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Cold_Storage_Prototype_2026-10-02/MANIFEST.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Cold_Storage_Prototype_2026-10-02/tests/test_cold_package.py
 D Project Feather Core/New Canon and Consideration/AetherFire_Cold_Storage_Prototype_2026-10-02/tools/build_cold_package.py
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/CODEX_SOFT_REFACTOR_HANDOFF.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/DIRECTORY_LAYOUT_TARGET.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/MODULE_ADMISSION_CHECKLIST.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/Migration/SAMPLE_THE_KINGDOM_DMZ_DECOMPOSITION.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/Migration/THE_KINGDOM_MIGRATION_WORKSHEET.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/README.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/SOURCE_STRUCTURE_STANDARD.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/Samples/SAMPLE_LOST_CIVILIZATION_MODULE.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/Samples/SAMPLE_POLITY_IMPLEMENTATION_AF_CIVIC_TERMINAL.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/Samples/SAMPLE_SHARED_INTERFACE_CONTACT_VERIFICATION.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/Templates/TEMPLATE_CURRENT_SOURCE.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/Templates/TEMPLATE_LOST_HISTORICAL_CURRENT.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/Templates/TEMPLATE_POLITY_IMPLEMENTATION_CURRENT.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/Templates/TEMPLATE_SHARED_INTERFACE_CURRENT.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/Templates/TEMPLATE_SPECIALIZED_CAPABILITY_CURRENT.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/Templates/TEMPLATE_WORKING_PROPOSAL.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/manifest.json
 M Project Feather Core/tests/control-regressions/README.md
 M Project Feather Core/tools/router_candidate.py
?? Project Feather Core/Anti-Drift Source/candidates/FTH_Anti_Drift_Source_Router_v5.1.yaml
?? Project Feather Core/Source_Archive/AetherFire_Cold_Storage_Prototype_2026-10-02/
?? Project Feather Core/Source_Archive/AetherFire_Source_Structure_Pack_v1/
?? Project Feather Core/tests/control-regressions/router-v5.1-fthx-probes.json
?? Project Feather Core/tests/test_router_fthx_candidate.py
```

Porcelain sau migration:

```text
 D Authorize Integrity Search/Authorize Integrity Search CI/AIS_CI_v0.1.md
 D Authorize Integrity Search/Authorize Integrity Search Modules/AIS_SOURCE_ROUTER_v0.1.yaml
 D Authorize Integrity Search/README.md
 D Authorize Integrity Search/tests/ROUTE_TEST_CASES.md
 D Image Transcendent/Image Transcendent CI/.gitattributes
 D Image Transcendent/Image Transcendent CI/ImageT_v1.0.0-ready-gate-candidate.md
 D Image Transcendent/Image Transcendent CI/ImageT_v1.0.0.md
 D Image Transcendent/Image Transcendent CI/README.md
 D Image Transcendent/Image Transcendent CI/READY_GATE_CANDIDATE_TESTS.md
 D Image Transcendent/Image Transcendent CI/source_archive/CI.md
 D Image Transcendent/Image Transcendent Modules/.gitattributes
 D Image Transcendent/Image Transcendent Modules/HUMANOID_CHARACTER_DESIGN_PREFERENCE.md
 D Image Transcendent/Image Transcendent Modules/IMAGE_ANTI_PRIOR.md
 D Image Transcendent/Image Transcendent Modules/IMAGE_SOURCE_ROUTER.yaml
 D Image Transcendent/Image Transcendent Modules/PREFERENCE_M2_TEST_PLAN.md
 D Image Transcendent/Image Transcendent Modules/ROUTE_TEST_CASES.md
 D Image Transcendent/Image Transcendent Modules/YAML_MIGRATION_NOTES.md
 D Image Transcendent/Image Transcendent Modules/config.md
 D Image Transcendent/Image Transcendent Modules/manifest.yaml
 D Image Transcendent/Image Transcendent Modules/source_archive/02-02-config-1.md
 D Image Transcendent/Image Transcendent Modules/source_archive/03-01-IMAGE_SOURCE_ROUTER-1-.md
 D Image Transcendent/Image Transcendent Modules/source_archive/HUMANOID_CHARACTER_DESIGN_PREFERENCE_v0.1.0-candidate.md
 D Image Transcendent/Image Transcendent Modules/source_archive/IMAGE_ANTI_PRIOR.md
 D Image Transcendent/Image Transcendent Modules/source_archive/IMAGE_SOURCE_ROUTER.md
 D Image Transcendent/Image Transcendent Modules/source_archive/manifest.md
 D Image Transcendent/Image Transcendent Modules/tests/test_yaml_routing.py
 D Project Feather Core/New Canon and Consideration/AetherFire_Cold_Storage_Prototype_2026-10-02/00_AETHERFIRE_CONSOLIDATION_INDEX.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Cold_Storage_Prototype_2026-10-02/Anti-Drift Source/AetherFire_Anti_Drift_Source_Router_v4.0.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Cold_Storage_Prototype_2026-10-02/CANDIDATE_STATUS.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Cold_Storage_Prototype_2026-10-02/Cold Storage/AETHERFIRE_COLD_PACKAGE.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Cold_Storage_Prototype_2026-10-02/Cold Storage/COLD_STORAGE_AUDIT_AND_DEPLOYMENT.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Cold_Storage_Prototype_2026-10-02/Cold Storage/SOURCE_STORAGE_INVENTORY.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Cold_Storage_Prototype_2026-10-02/MANIFEST.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Cold_Storage_Prototype_2026-10-02/tests/test_cold_package.py
 D Project Feather Core/New Canon and Consideration/AetherFire_Cold_Storage_Prototype_2026-10-02/tools/build_cold_package.py
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/CODEX_SOFT_REFACTOR_HANDOFF.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/DIRECTORY_LAYOUT_TARGET.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/MODULE_ADMISSION_CHECKLIST.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/Migration/SAMPLE_THE_KINGDOM_DMZ_DECOMPOSITION.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/Migration/THE_KINGDOM_MIGRATION_WORKSHEET.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/README.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/SOURCE_STRUCTURE_STANDARD.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/Samples/SAMPLE_LOST_CIVILIZATION_MODULE.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/Samples/SAMPLE_POLITY_IMPLEMENTATION_AF_CIVIC_TERMINAL.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/Samples/SAMPLE_SHARED_INTERFACE_CONTACT_VERIFICATION.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/Templates/TEMPLATE_CURRENT_SOURCE.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/Templates/TEMPLATE_LOST_HISTORICAL_CURRENT.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/Templates/TEMPLATE_POLITY_IMPLEMENTATION_CURRENT.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/Templates/TEMPLATE_SHARED_INTERFACE_CURRENT.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/Templates/TEMPLATE_SPECIALIZED_CAPABILITY_CURRENT.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/Templates/TEMPLATE_WORKING_PROPOSAL.md
 D Project Feather Core/New Canon and Consideration/AetherFire_Source_Structure_Pack_v1/manifest.json
 M Project Feather Core/tests/control-regressions/README.md
 M Project Feather Core/tools/router_candidate.py
 D llm-controls/Friendly Support Project/FSP_CI_v0.2.md
 D llm-controls/Friendly Support Project/FSP_CI_v0.3.1.md
 D llm-controls/Friendly Support Project/FSP_CI_v0.3.md
 D llm-controls/Friendly Support Project/overlays/BRAINSTORM_v0.1.md
 D llm-controls/Friendly Support Project/profiles/CREATIVE_v0.1.md
 D llm-controls/Friendly Support Project/profiles/TECHNICAL_v0.1.md
 D llm-controls/Friendly Support Project/router/FSP_ROUTER_v0.1.md
 D llm-controls/Friendly Support Project/router/FSP_ROUTER_v0.2.md
 D llm-controls/Friendly Support Project/source_archive/FSP_CI_v0.1.md
 D llm-controls/Friendly Support Project/source_archive/Project CI v0.1 — Controlled Flexible Interaction.txt
?? Central Hub/
?? Project Feather Core/Anti-Drift Source/candidates/FTH_Anti_Drift_Source_Router_v5.1.yaml
?? Project Feather Core/Source_Archive/AetherFire_Cold_Storage_Prototype_2026-10-02/
?? Project Feather Core/Source_Archive/AetherFire_Source_Structure_Pack_v1/
?? Project Feather Core/tests/control-regressions/router-v5.1-fthx-probes.json
?? Project Feather Core/tests/test_router_fthx_candidate.py
```

## M. Post-migration local correction — Ready Gate versioned promotion

Baseline lượt này: repository local, branch main, HEAD 679da3e074fafbac3be627397794abae578f587e; ba thay đổi local từ lượt correction đặc tả được giữ và tiếp tục. Task chỉ implementation local; không stage/commit/push/deploy/branch/tag/worktree.

OBSERVED MIGRATION DEVIATION: Ready Gate là hành vi active nhưng còn nhúng, chưa được quản lý version/hash/inventory/compatibility riêng. Theo requirement mới đã chấp nhận, promotion thành official required ImageT runtime control, không candidate hoặc experiment và không thiết kế lại Hub.

### Phiên bản và đường dẫn hiện hành

| Component | Cũ | Mới | Lý do |
| --- | --- | --- | --- |
| Ready Gate | embedded, chưa version riêng | READY_GATE_v1.0.md / 1.0 | Release chính thức đầu tiên, theo quy ước hai phần của controller mới trong Hub |
| ImageT controller | IMAGE_CONTROLLER_v1.0.md / 1.0 | IMAGE_CONTROLLER_v1.1.md / 1.1 | Chuyển owner approval và thêm required dependency; sửa reference/negative boundary ở Prompt Gate |
| ImageT router | 3.0.0 | 3.1.0 | Thêm resolution/loading của Ready Gate cho generation; giữ format_version 1 |
| ImageT manifest | 2.0.0 | 2.1.0 | Thêm required inventory/hash/compatibility, bỏ ready_gate status cấp release bị trùng |
| AIS router | AIS_ROUTER_v1.0.yaml / 1.0 | AIS_ROUTER_v1.1.yaml / 1.1 | Sửa hẹp combination-support leak trong EVIDENCE_MERGE |

Controller/AIS router giữ quy ước filename hai phần của Hub; router/manifest ImageT giữ quy ước ba phần đã có. Các bump nhỏ phản ánh mở rộng contract trong cùng format, không tạo thế hệ kiến trúc mới. Hub Router chỉ đổi control path IMAGET, giữ 1.0 và mọi route/selection. AIS pipeline chỉ đổi router reference, giữ 1.0. Preference chỉ đổi BASELINE_CONTROLLER path và hash tương ứng, giữ 0.1.1-candidate/inactive/direct-input-only. Hub CI, domain, BRAINSTORM, anti-prior và config không đổi byte/version.

### Ownership và manifest

Manifest sở hữu đúng một entry ready_gate: active, required, version '1.0', exact filename/local_path READY_GATE_v1.0.md và SHA-256 `c61bccbc88560c40a9f600473d84b54c7f6b27f527eea6b713f78615d04de1d5`. Controller compatibility pin ready_gate '1.0', router '3.1.0', prior_guard '1.1.0', anti_drift '2.0.0'. Không có Ready Gate manifest/router/registry/state engine riêng. Tests không nằm trong runtime inventory.

Controller xây operation lock/prompt, kiểm Prompt Gate và xác minh ảnh; không giữ full approval body. ImageT router resolve/load đúng artifact từ manifest và reload freshness, chỉ cho generation operations/retries. Ready Gate sở hữu execution snapshot/version/state, interpretation/invalidation/consumption và exact one-call authorization. Tool thực thi thật. Hub chỉ chọn IMAGET; Ready Gate không áp cho AIS, Work/browser hoặc general actions.

### Bảo toàn và stress corrections

Phần giao thức phê duyệt nguyên gốc được giữ nguyên văn tại `## Preserved approval protocol` trong official control; SHA-256 cũ `c1360811a98e27b6ddabbf008d9b82ffd54610b0bf5a8948c8f37092340fd322` tiếp tục được kiểm. Không thay nghĩa YES/NO/YES BUT/ambiguous/old-version approval, ANALYZE exemption, consumed approval, stale/context loss hoặc uncertain-submission/no silent retry. Các bổ sung được phép: header/version/owner, snapshot đầy đủ, reference resolution và OPEN != FORBIDDEN. Không lấy hash thay đổi tự thân làm bằng chứng cải thiện.

READY SNAPSHOT vN gắn PENDING_APPROVAL với exact prompt, assets/roles, options, inputs, operation-lock identity/protected constraints, completions/preference additions, intentionally open fields, negatives và source freshness basis. Prompt đã qua Prompt Gate không được Ready Gate rewrite. References phải resolve trước approval; không asset thì REFERENCES: NONE. AIS EVIDENCE SOURCE != IMAGE GENERATOR REFERENCE ASSET. UNKNOWN/UNSPECIFIED không tự thành prohibition: mọi negative phải có user/logical/active-source authority tại controller Prompt Gate; không tự thêm "no horse". AIS evidence merge giữ components riêng: evidence A + context/evidence B không hỗ trợ A+B nếu quan hệ chưa được chứng minh.

Controller, router, Ready Gate và preference hashes được recompute từ bytes thực vào đúng manifest owner. Anti-prior/config hashes giữ nguyên. Không có hash cascade ngoài các entry đã đổi bytes.

### Regression oracle và bằng chứng

READY_GATE_TEST_CASES.md giữ tên vì TARGET: READY_GATE 1.0 và APPLIES_TO nêu version/file rõ; ROLE: NON_RUNTIME_NORMATIVE_ORACLE, STATUS: REQUIRED_REGRESSION_SPEC. R01–R22 giữ đủ và nguyên văn; R03–R08 dùng fresh conversations riêng, R09–R19 dùng multi-turn. X01 buộc AIS -> BRAINSTORM -> TECHNICAL -> CREATIVE -> IMAGET -> READY GATE, với scoped evidence, fictional mechanism, unsupported combination, research-source/asset split, open field, exact roles và numbered PENDING_APPROVAL/zero-call trước duyệt.

Local unittest: **17/17 PASS, không skip**. Kiểm tĩnh: YAML conservative, files/headers/hashes/compatibility, đúng một owner/entry, delegation, protocol preservation, source policy, normative anchors. Oracle mô phỏng: các generation path vào pending, missing/corrupt/incompatible/unreadable Ready Gate phải dừng; archive/embedded fallback bị cấm; ANALYZE bypass; approval một call/revision/stale/consumption. X01 là REVIEWED_TEXT, không claim đã chạy stress test bằng model trong task này.

ORIGINAL IMAGET READY GATE: previously live-tested per USER-CONFIRMED PROJECT STATE. CENTRAL HUB PROMOTED READY GATE: static/spec tested; LIVE PROJECT INTEGRATION NOT RUN. Current sources không chứa original live payload trace để claim đã truy cập/tái kiểm. Backend payload không quan sát được phải UNVERIFIABLE; displayed prompt không chứng minh exact submitted payload.

### Predecessor và Git scope

Theo lệnh không sửa một byte Source_archive, không thêm/đổi archive hoặc receipt; 38 file archive giữ nguyên. Hai predecessor controller/AIS router đã được xác minh nguyên byte so snapshot và Git HEAD trước khi bỏ tên cũ khỏi vùng active. Bản trước thay đổi nằm tại Git HEAD 679da3e074fafbac3be627397794abae578f587e; đây là provenance lịch sử, không fallback runtime hoặc quyền rollback tự động. Chỉ dẫn không ghi archive của user được ưu tiên so với archive workflow mặc định.

Không thay đổi index/HEAD/branch hoặc remote. Bảng B/C và log A–L lưu lịch sử migration trước promotion; mọi active version/path sau promotion theo mục M và manifest hiện hành. Task này không deploy hoặc thử image tool.
