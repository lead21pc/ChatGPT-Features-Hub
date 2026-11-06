# Central Hub v1.1 — kế hoạch promotion thủ công

Trạng thái local: PREPARED_NOT_DEPLOYED. Bốn core file dùng trạng thái runtime ACTIVE để sẵn sàng cài bình thường; đây không phải bằng chứng đã deploy. Không có thao tác stage/commit/push hoặc đổi Project/Library trong mốc chuẩn bị này.

Trial candidate: LIVE INTEGRATION PARTIAL theo báo cáo người dùng; I01–I07/I09–I10 PASS, I08 UNVERIFIABLE. Lỗi setup delegation/AIS source ban đầu: DEPLOYMENT SETUP FAILURE — RESOLVED. Chi tiết tại `../integration_v1.1/HUB_V1_1_LIVE_INTEGRATION_RESULT.md`, chỉ là verification record.

## Delta chính xác từ candidate

- CI: chỉ thay `HUB_ROUTER_v1.1-integration-candidate.yaml` bằng `HUB_ROUTER_v1.1.yaml`; không thêm nội dung.
- Router: version label thành 1.1; core ACTIVE/active=true; thay hai exact core filenames và status của chúng; bỏ điều kiện kích hoạt chỉ dành cho manual trial, dùng installed exact CI delegation cho normal runtime. Candidate package vẫn không được tự admission. Không đổi stages, package selection, closure, composition, binding dispatch, failure behavior, pipeline authorization hoặc persistence.
- Architecture: core ACTIVE; cập nhật tên/trạng thái triển khai và kết quả trial; bỏ các phát biểu “chỉ được dùng cho trial”/“integration NOT_RUN” đã lỗi thời. Giữ contract kỹ thuật, scope và ownership.
- Catalog: core ACTIVE/active=true/runtime_ready=true nghĩa đủ điều kiện làm runtime control sau khi cài đúng bộ; deployment vẫn PREPARED_NOT_DEPLOYED. Giữ đúng năm package và toàn bộ danh tính, version, location, applicability, quan hệ. Chỉ cập nhật activation/evidence metadata; ImageT không được nâng thành live verified.
- Không có migration package mới, fallback hoặc quyền hành động mới. Bốn file là một bộ runtime tương thích; test/result/plan không là runtime control.

## Cài thủ công

1. Lưu nội dung Project Instructions và source roster hiện đang live để đối chiếu/rollback. Đối chiếu bộ trial đã vượt rerun; không dùng AIS source lỗi thời từ lần setup đầu.
2. **PROJECT INSTRUCTIONS:** thay toàn bộ nội dung candidate CI bằng `HUB_CI_v1.1.md` trong thư mục này. Không ghép thêm architecture notes.
3. **PROJECT SOURCES:** thay đúng ba core candidate tương ứng:

   | Gỡ/thay core trial | Cài core runtime từ thư mục này |
   | --- | --- |
   | HUB_ROUTER_v1.1-integration-candidate.yaml | HUB_ROUTER_v1.1.yaml |
   | HUB_ARCHITECTURE_v1.0-integration-candidate.md | HUB_ARCHITECTURE_v1.0.md |
   | HUB_PACKAGE_CATALOG_v1.0-integration-candidate.yaml | HUB_PACKAGE_CATALOG_v1.0.yaml |

4. **LIBRARY:** giữ nguyên `Central Hub Config/HUB-DOM-TECHNICAL_v1.0.md`, ACTIVE/1.0, `library_file_id=libfile_bab7d55cd85c819198291acf135099fd`, Library version_id `1`. Không upload lại, đổi object hoặc migration TECHNICAL thêm lần nữa. Không thêm Project Source TECHNICAL cũ vào bộ v1.1.
5. **LEGACY SOURCES:** giữ nguyên những file hiện hành dưới đây, đúng filename và nội dung đã dùng sau bootstrap reconciliation:

   - `domains/creative/CREATIVE_v1.0.md`
   - `capabilities/BRAINSTORM_v1.0.md`
   - `tool_pipelines/AIS/AIS_PIPELINE_v1.0.md` — phải yêu cầu `AIS_ROUTER_v1.1.yaml`, không v1.0.
   - `tool_pipelines/AIS/AIS_ROUTER_v1.1.yaml`
   - `tool_pipelines/ImageT/IMAGE_CONTROLLER_v1.1.md`
   - `tool_pipelines/ImageT/IMAGE_SOURCE_ROUTER.yaml`
   - `tool_pipelines/ImageT/manifest.yaml`
   - `tool_pipelines/ImageT/READY_GATE_v1.0.md`
   - `tool_pipelines/ImageT/IMAGE_ANTI_PRIOR.md`
   - `tool_pipelines/ImageT/config.md`

   Giữ filename source chính xác; không đổi nội bộ pipeline, không kích hoạt preference inactive. Chỉ thay core files nêu trên; không gỡ nguồn không liên quan.
6. Đối chiếu exact delegation CI → Router → Architecture/Catalog và roster trước khi dùng normal runtime. Không để các bộ core cũ/trial đồng thời làm authority. Không upload test spec, result, plan, tests hoặc archive vào Project Sources như runtime control.

Promotion này chưa được Codex thực hiện trong Project. Kết quả trial gắn với bộ candidate; việc cài bộ đổi tên/trạng thái cần được người dùng đối chiếu thực tế. Static equivalence không tự chứng minh bootstrap của deployment mới.

## Rollback về v1.0

1. Khôi phục Project Instructions bằng `HUB_CI_v1.0.md` đã lưu.
2. Khôi phục `HUB_ROUTER_v1.0.yaml` trong Project Sources.
3. Gỡ bộ v1.1 `HUB_ROUTER_v1.1.yaml`, `HUB_ARCHITECTURE_v1.0.md`, `HUB_PACKAGE_CATALOG_v1.0.yaml` khỏi deployment.
4. Khôi phục Project Source `domains/technical/TECHNICAL_v1.0.md` (filename `TECHNICAL_v1.0.md`) nếu quay lại đầy đủ behavior v1.0.
5. Giữ CREATIVE/BRAINSTORM/AIS/ImageT hiện hành. Library TECHNICAL có thể giữ nguyên nhưng không dùng trong route v1.0.

Repository copies của v1.0 và trial vẫn giữ để lịch sử/rollback. ROLLBACK != FALLBACK: người dùng đảo cài đặt rõ ràng; Router không tự chọn source cũ khi Library lỗi.

## Phần còn chưa kiểm chứng

I08 actual Library-binding failure vẫn UNVERIFIABLE; direct-object retrieval capability chưa được xác lập chỉ từ object identity. Trial không cung cấp export/hash live của từng core source hoặc case ImageT riêng. Bộ promotion chưa deploy; không claim live bootstrap hoặc live failure-path verification cho bộ mới. Không cần tạo hạ tầng thử lỗi để hoàn tất mốc chuẩn bị này.
