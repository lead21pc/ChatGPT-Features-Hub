# Central Hub v1.1 — kết quả đóng trial tích hợp

Ngày ghi nhận: 2026-10-19 (Asia/Bangkok).
Nguồn bằng chứng: USER_REPORTED LIVE OBSERVATIONS, do người dùng cung cấp trong yêu cầu đóng trial. Codex ghi nhận, không trực tiếp tái hiện hoặc truy cập deployment. Đây là verification record trong repository, không phải runtime control.

**Phân loại cuối: LIVE INTEGRATION PARTIAL.** I01–I07/I09–I10 PASS; I08 UNVERIFIABLE. Các success path yêu cầu đã vượt trial; nhánh lỗi Library thật chưa kiểm được. PARTIAL không biểu thị lỗi chức năng tích hợp. SUCCESS PATH VERIFIED != FAILURE PATH VERIFIED. UNVERIFIABLE != FAIL.

## Deployment assumptions và bootstrap reconciliation

Kết quả áp dụng cho lần rerun sau khi người dùng đối chiếu và sửa setup của live Project: Project Instructions dùng nội dung `HUB_CI_v1.1-candidate.md`; exact delegation tới `HUB_ROUTER_v1.1-integration-candidate.yaml`; core Sources đi kèm là `HUB_ARCHITECTURE_v1.0-integration-candidate.md` và `HUB_PACKAGE_CATALOG_v1.0-integration-candidate.yaml`. Đây là danh tính bộ trial theo ngữ cảnh được cung cấp, không có bản export/hash live của từng core source để Codex xác nhận byte-exact. Không bịa số dòng đọc Router/Catalog hoặc tool trace chưa được cung cấp.

TECHNICAL binding duy nhất là Library / `Central Hub Config`; bốn package còn lại giữ exact Project Sources. Không dùng Project Source TECHNICAL cũ như authority song song. Các điều kiện này mô tả setup của trial; không chứng minh bộ promotion mới đã được cài.

Lần chạy trước thất bại vì setup deployment:

- Candidate delegation chưa được thiết lập có hiệu lực cho trial đó.
- Project Source `AIS_PIPELINE` cũ tham chiếu `AIS_ROUTER_v1.0.yaml`.
- Nguồn hiện hành đúng là `AIS_PIPELINE_v1.0.md`, yêu cầu `AIS_ROUTER_v1.1.yaml`.
- Sau khi đối chiếu và thay đúng setup, bootstrap PASS; full rerun cho kết quả dưới đây.

**DEPLOYMENT SETUP FAILURE — RESOLVED.** Không phân loại lần lỗi setup này thành Router architecture failure. Nguồn AIS local hiện hành đã yêu cầu Router v1.1; không cần sửa kiến trúc AIS hoặc Router để xử lý source live lỗi thời.

## Artifact Library quan sát được

| Trường | Giá trị |
| --- | --- |
| Module ID | HUB-DOM-TECHNICAL |
| Package ID | HUB-PKG-TECHNICAL |
| Runtime role | REASONING_PROFILE |
| Status / artifact Version | ACTIVE / 1.0 |
| Library root | Central Hub Config |
| library_file_id | libfile_bab7d55cd85c819198291acf135099fd |
| Artifact | HUB-DOM-TECHNICAL_v1.0.md |
| FULL_FILE | 19/19, has_more=false |
| Library version_id | 1 — metadata đã báo ở mốc trước; khác artifact Version 1.0 |

Object identity và header là binding thực được báo; không suy ra runtime có direct-object fetch API. Surface file_id đã ghi ở Catalog vẫn chỉ phục vụ provenance/debug, không thay canonical binding.

## I01–I10: quan sát và kết quả

| Case | Kết quả | Bằng chứng quan sát do người dùng báo |
| --- | --- | --- |
| I01 ORDINARY BASELINE | PASS | Package set NONE; không specialization source read, không pipeline. |
| I02 TECHNICAL AUTO-SELECTION | PASS | Tự chọn HUB-PKG-TECHNICAL / HUB-DOM-TECHNICAL từ prompt kỹ thuật thông thường; exact Library artifact ở trên; FULL_FILE 19/19, has_more=false, đủ header ACTIVE/1.0; không fallback Project Source TECHNICAL cũ. |
| I03 DEACTIVATION | PASS | Yêu cầu thông thường kế tiếp route NONE; không giữ activation TECHNICAL từ turn trước. |
| I04 CREATIVE PRESERVATION | PASS | HUB-PKG-CREATIVE / HUB-DOM-CREATIVE; exact CREATIVE_v1.0.md trong Project Sources; FULL_FILE 9/9; không Library lookup. |
| I05 BRAINSTORM PRESERVATION | PASS | HUB-PKG-BRAINSTORM / HUB-CAP-BRAINSTORM; exact BRAINSTORM_v1.0.md trong Project Sources; FULL_FILE 43/43; không Library lookup. |
| I06 TECHNICAL + BRAINSTORM | PASS | Đồng thời chọn TECHNICAL Library và BRAINSTORM Project Sources; không winner-take-all; không AIS. |
| I07 TECHNICAL + AIS | PASS | HUB-PKG-TECHNICAL + HUB-PKG-AIS; TECHNICAL 19/19; AIS_PIPELINE_v1.0.md 19/19 từ Project Sources và exact AIS_ROUTER_v1.1.yaml 104/104; AIS được chọn và sở hữu research internals; không version/lookalike fallback. |
| I08 TECHNICAL LIBRARY FAILURE | UNVERIFIABLE | Không có cách an toàn làm bound Library artifact thật unavailable mà không sửa deployment live. Không dùng fake ID hoặc simulated substitute; không chuyển thành PASS hoặc FAIL. |
| I09 SCOPE SWITCH | PASS | TECHNICAL → NONE → TECHNICAL; đánh giá lại từng scope; FULL_FILE TECHNICAL tại mỗi scope kỹ thuật được chọn. |
| I10 ROUTE INSPECTION | PASS | HUB-PKG-TECHNICAL; HUB-DOM-TECHNICAL; REASONING_PROFILE; Library / Central Hub Config; ACTIVE/1.0; FULL_FILE 19/19; pipeline NONE; unresolved dependency NONE. |

CREATIVE/BRAINSTORM vẫn theo legacy exact-source contract; các Module ID trên là routing identity từ Catalog, không phải xác nhận source đã có new Library header. Không yêu cầu hidden reasoning. ImageT không phải case live riêng trong I01–I10; không suy thành ImageT live PASS từ việc giữ nguyên package binding hoặc static regression.

## Ranh giới bằng chứng no-fallback

- STATIC/SPEC: PASS ở mốc integration; kiểm lại riêng bằng suite khi chuẩn bị promotion.
- LIVE VERIFIED SUCCESS PATHS: không fallback được quan sát trong các đường chạy thành công đã báo.
- LIVE UNVERIFIED FAILURE PATH: I08 UNVERIFIABLE; chưa chứng minh runtime thực hiện no-fallback khi exact Library binding thật lỗi.

Không claim LIVE FAILURE-PATH VERIFIED. Không tạo failure-injection framework để đóng khoảng trống này. Các failure contract vẫn giữ nguyên; phần chưa quan sát không bị chuyển thành lỗi chức năng, cũng không được nâng thành PASS.

## Phạm vi kết luận

Trial candidate đã kiểm các success path nêu trên theo báo cáo người dùng. Bốn artifact promotion chỉ bỏ điều kiện trial dành riêng cho core, đổi exact tên tham chiếu và cập nhật bằng chứng; normal action authorization, routing, composition và mixed-storage binding được giữ. Local preparation không deploy. Test spec gốc giữ nguyên như snapshot trước trial; kết quả này là bản ghi đóng trial tương ứng.
