# Authoring 0.7 — promotion trong M2 local runtime

Ngày 2026-11-05 (Asia/Bangkok). Phạm vi: Central-Hub-Local; checkpoint `c619a5a6895cf0d9aa67a92ebb46f36a8bb9e228`. Không bắt đầu M3/M4. Bản ghi promotion 0.6 được giữ byte-exact tại `Source_archive/Authoring 0.7 M2 2026-11-05/AUTHORING_PROMOTION.md`.

Authoring ACTIVE/0.7 giữ nguyên HUB-CAP-AUTHORING / HUB-PKG-AUTHORING / CAPABILITY. Toàn bộ ngữ nghĩa từ “For the current turn only” giống candidate đã thử live. Khi bỏ mục source isolation mới, phần hành vi kế thừa giống nguyên 0.6. Không thêm package, Router axis, parser, context engine, source registry hoặc persistence layer.

Architecture 1.8 mục 6/8 và Router contracts yêu cầu exact Architecture/Catalog pins. Bộ kế nhiệm 1.9 chỉ cập nhật hợp đồng phiên bản và mô tả source admission; Router 1.1 chỉ đổi pins. Hub CI không đổi. Catalog giữ nguyên toàn bộ entries ngoài Authoring. Identity ChatGPT Library vẫn UNRESOLVED; promotion local không chứng minh cài đặt hoặc deployment ChatGPT.

`runtime/HUB_LOCAL_BINDINGS_v0.2.json` (T8 diagnostic) và v0.3 (M1 runtime) cùng trỏ đến bản runtime Authoring 0.7 byte-exact. Hash shared-package pin của T9 cập nhật tương ứng; AIS entries và hành vi AIS không đổi. Python nhận `isolated:boolean` từ model, kiểm tra shape/invariants và truyền vào trace/handoff; không phân tích trigger hoặc xóa history. inactive => isolated false; contributor != NONE => isolated false; P1/P2/P3 có thể đi cùng isolated.

Nguồn được nhận: yêu cầu hiện tại sau trigger, tài liệu được cung cấp trong yêu cầu ấy và tài liệu truy cập được được định danh đủ rõ trong chính yêu cầu ấy. Lịch sử/ngữ cảnh nền không được dẫn chiếu vẫn hiển thị cho model nhưng không được nhận làm task material. Controls và giới hạn target vẫn bắt buộc. Clarification/reauthor cần trigger mới, không kế thừa source selection.

## Bằng chứng và giới hạn

CANDIDATE LIVE PASS: I1 và I3; đúng một Responses API call mỗi ca, max_retries=0, không tools. Nguyên controls, inputs/outputs, SHA-256, versions và đánh giá nằm dưới `m2_evidence/authoring_0_7/` ở repo root. Reference outputs và tiêu chí chấm không gửi cho model.

STATIC/SPEC PASS: 117/117 local với socket.connect bị chặn; 33/33 focused upstream; compile 59 file Python; git diff --check PASS. ACTIVE LOCAL RUNTIME LIVE PASS: đúng một top-level request, 3 Responses API calls completed, không retry. Root chỉ chọn Authoring; admission/handoff và trace ghi isolated=true; blocker rỗng. Prompt cuối giữ hai lựa chọn chưa quyết định, không nhập CANARY_ACTIVE_PRIOR hoặc quyết định cũ; không tool/target execution. Các lớp bằng chứng được ghi riêng trong `VERIFICATION.md` và `m2_evidence/authoring_0_7/`.

Giới hạn mirror-wide upstream do thiếu Git objects lịch sử gốc và Project Feather files được người dùng báo trước; không phân loại thành lỗi Authoring 0.7. Focused Authoring suite được chạy trực tiếp tại mirror này. Không chạy lại toàn suite upstream trong promotion này.

ImageT và package ngoài phạm vi không đổi. Không tuyên bố Library installation/retrieval, Project deployment hoặc mọi dạng activation đã được kiểm live. Preset, malformed, no-persistence và blocker có bằng chứng static/mock, không phải chiến dịch live bổ sung.

Module tiền nhiệm 0.6, Architecture/Catalog 1.8 và snapshots Router/promotion docs được giữ trong một nhóm `Source_archive/Authoring 0.7 M2 2026-11-05/`, có `ARCHIVE_RECEIPT.json`. Runtime predecessor 0.6 được giữ tại `runtime/packages/authoring/source_archive/`. Candidate 0.7 và mọi bằng chứng cũ không đổi. Tests lịch sử 0.6 dùng snapshot đúng phiên bản; active 0.7 được kiểm riêng trong `test_authoring_07.py`, cùng static/mock T8/M1.
