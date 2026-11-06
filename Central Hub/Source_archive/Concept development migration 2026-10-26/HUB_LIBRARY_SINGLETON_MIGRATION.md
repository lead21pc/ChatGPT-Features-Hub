# Central Hub v1.1 — CREATIVE và BRAINSTORM Library singleton

Repository v1.1: ACTIVE. Project deployment: NOT_VERIFIED trong mốc local này. Không upload tự động, không stage/commit/push. Bộ promotion đã chấp nhận được sao chép vào root. Sửa tại chỗ ngày 2026-10-26 làm rõ hai đường identity Library trong Router/Architecture; lựa chọn package và composition giữ nguyên. Không thêm binding mode hoặc schema Catalog.

TECHNICAL Library và ImageT giữ nguyên bindings. AIS giữ binding mode LEGACY_PROJECT_SOURCE; bản chính thức repository từ 2026-10-21 là pipeline v1.1/router v1.2, Project deployment NOT_PERFORMED. Danh sách nguồn cài thủ công dưới đây đã cập nhật theo revision đó. Trial trước có LIVE INTEGRATION PARTIAL theo báo cáo người dùng: các success path PASS, I08 UNVERIFIABLE. Không chạy lại I01–I10, không tạo failure injection. CREATIVE identity verification vẫn NOT_PERFORMED. BRAINSTORM đã được kiểm tra trực tiếp qua UI ở phạm vi bên dưới; kết quả legacy không là bằng chứng Library migration, UI resolution cũng không chứng minh Hub execution.

## Hai file cần upload

Hai artifact đích dưới **Library / Central Hub Config**; trước khi upload phải kiểm tra object đã có. Không tạo bản ACTIVE trùng. Nếu cần upload thì dùng nguyên file hiện hành:

- `library_modules/HUB-DOM-CREATIVE_v1.0.md`: HUB-DOM-CREATIVE / HUB-PKG-CREATIVE / DOMAIN_CONTROL / ACTIVE / 1.0.
- `library_modules/HUB-CAP-BRAINSTORM_v1.0.md`: HUB-CAP-BRAINSTORM / HUB-PKG-BRAINSTORM / CAPABILITY / ACTIVE / 1.0.

Đây là bản có header runtime, không phải source legacy cùng tên ngắn. Không upload lại TECHNICAL, không dùng trial wrapper. Phần thân của từng module giữ byte-exact sau H1 của source cũ. Không thêm Refines/Complements/Requires hoặc package-local Catalog.

## Thứ tự cài đặt thủ công

1. Lưu Project Instructions và source roster hiện đang dùng để rollback. Kiểm tra object đã có trong đúng `Central Hub Config`; chỉ upload file còn thiếu, không tạo bản trùng. Upload không là identity verification hoặc scoped application.
2. Resolve trong đúng root và đọc **FULL_FILE** từng object: đối chiếu Module ID, Package ID, Runtime role, Scope, Status ACTIVE, artifact Version 1.0 và đúng body. Ưu tiên `library_file_id`/Library `version_id` đã xác minh khi nền tảng cung cấp và hỗ trợ. Nếu không có internal identity dùng được, thực hiện listing/search chỉ trong `Central Hub Config`, mở object cụ thể và kiểm tra đầy đủ các ứng viên có thể khớp, kể cả khác tên; hoàn tất pagination/loading liên quan. Phải xác lập đúng một identity ACTIVE hợp lệ trong phạm vi quan sát đủ dùng. Một item trên một màn hình không đủ; ứng viên chưa đọc hoặc coverage thiếu giữ UNRESOLVED, nhiều identity hợp lệ thì block. Không chấp nhận snippet/header-only. Không suy Library version_id từ artifact Version hoặc “Current version”.
3. Trong `HUB_PACKAGE_CATALOG_v1.0.yaml` ở root, chỉ cập nhật `location` theo bằng chứng thực: internal IDs có thể giữ null nếu nền tảng không cung cấp; filename/path quan sát được chỉ là gợi ý tìm ứng viên, không thay identity verification. Chỉ ghi locator object bền vững nếu đã chứng minh tính hữu ích/ổn định; không tự dùng URL viewer. Sau khi một đường identity đạt, mới ghi resolution/verification đúng mức chứng cứ và giữ giới hạn kiểm tra trùng. Không claim smoke PASS trước khi chạy. Null không cho phép search ngoài root hoặc dùng repository/source cũ. Nếu chưa xác lập exact identity thì dừng cài phần migration, giữ deployment đang dùng; không dùng Catalog chưa resolve để giả rằng package đã sẵn sàng. Mỗi lần thực thi vẫn phải chọn, đọc và xác minh object theo Router; metadata đã ghi không chứng minh lần đọc mới.
4. **PROJECT INSTRUCTIONS:** toàn bộ nội dung root `HUB_CI_v1.1.md`.
5. **PROJECT SOURCES:** root `HUB_ROUTER_v1.1.yaml`, `HUB_ARCHITECTURE_v1.0.md`, `HUB_PACKAGE_CATALOG_v1.0.yaml` đã ghi nhận hai exact bindings. Thay core candidate/trial tương ứng, không để nhiều bộ core cùng làm authority. Giữ chính xác các nguồn pipeline sau:

   - `tool_pipelines/AIS/AIS_PIPELINE_v1.1.md`
   - `tool_pipelines/AIS/AIS_ROUTER_v1.2.yaml`
   - `tool_pipelines/ImageT/IMAGE_CONTROLLER_v1.1.md`
   - `tool_pipelines/ImageT/IMAGE_SOURCE_ROUTER.yaml`
   - `tool_pipelines/ImageT/manifest.yaml`
   - `tool_pipelines/ImageT/READY_GATE_v1.0.md`
   - `tool_pipelines/ImageT/IMAGE_ANTI_PRIOR.md`
   - `tool_pipelines/ImageT/config.md`

   Giữ tên source và nội dung hiện hành; pipeline tự resolve dependency. Không đổi preference inactive/direct-input-only.
6. **LIBRARY:** giữ nguyên TECHNICAL ACTIVE/1.0, `library_file_id=libfile_bab7d55cd85c819198291acf135099fd`, Library version_id `1`; dùng các object CREATIVE/BRAINSTORM đã xác minh ở bước 2, không upload lại object đã có. Đây là ba singleton, mỗi package direct entrypoint.
7. Sau khi hai Library artifact đã FULL_FILE/identity verified, khi chuyển sang Catalog mới, **gỡ khỏi live Project Sources** `CREATIVE_v1.0.md` và `BRAINSTORM_v1.0.md`. Không để chúng làm fallback/authority song song. TECHNICAL source cũ tiếp tục không thuộc bộ v1.1. Không xóa repository copies hoặc gỡ nguồn không liên quan.
8. Chạy bốn smoke case dưới đây sau khi exact delegation và bindings đã cài. Không upload tài liệu này, tests, candidate snapshots hoặc result records như runtime controls.

## S01–S04 — chỉ chuẩn bị, NOT_RUN

| Case | Prompt | Kết quả cần quan sát |
| --- | --- | --- |
| S01 — BASELINE | Viết lại câu này thân thiện hơn: “Vui lòng gửi tài liệu trước 5 giờ chiều.” | Package set NONE; không specialization/pipeline không cần thiết. |
| S02 — CREATIVE | Viết cảnh ngắn hai người bạn gặp lại ở ga tàu, dùng hành động và nhịp câu để thể hiện khoảng cách giữa họ; chi tiết phải có chức năng, không giải thích trực tiếp cảm xúc. | HUB-PKG-CREATIVE / HUB-DOM-CREATIVE tự được chọn; exact Library module ACTIVE/1.0 trong Central Hub Config, FULL_FILE và đúng identity/header; không Project Source fallback. |
| S03 — BRAINSTORM | Với ý tưởng thành phố tồn tại nhờ giữ bí mật, đảo giả định thành bắt buộc công khai; phát triển ba nhánh khác cơ chế, mỗi nhánh có hệ quả bậc hai. | HUB-PKG-BRAINSTORM / HUB-CAP-BRAINSTORM tự được chọn; exact Library ACTIVE/1.0, FULL_FILE và đúng identity/header; không Project Source fallback. |
| S04 — CREATIVE + BRAINSTORM | Từ tiền đề thành phố vận hành bằng bí mật, phát triển ba nhánh song song bằng cách đảo hoặc nới giả định. Với mỗi nhánh, viết một cảnh ngắn có hành động, nhịp và chi tiết chức năng để cho thấy hệ quả bậc hai. Chưa chọn nhánh cuối. | Cả CREATIVE và BRAINSTORM từ Library, đọc đầy đủ đúng hai bound objects; đóng góp có scope, không winner-take-all. Không tự gọi AIS/ImageT. |

Ghi bằng chứng quan sát: CI/Router/Catalog thực dùng, package/module chọn, exact object/root, artifact Version so với Library version_id, FULL_FILE/has_more, header, binding location, hành vi trả lời và fallback attempt. Ghi PASS/FAIL/UNVERIFIABLE theo bằng chứng; route tự khai không đủ chứng minh read. Không yêu cầu hidden reasoning. Không thử controlled Library failure.

## Kiểm tra identity BRAINSTORM qua UI — 2026-10-26

Nguồn bằng chứng: `CODEX_UI_OBSERVED`, Opera / ChatGPT Library; chỉ kiểm tra identity/read, không gửi prompt hoặc chạy module. Root được mở bằng UI và kiểm tra lại tại `https://chatgpt.com/library/d/6ad3caddadf48191a3ef74e1cfc6e5f7?tab=all`, heading `Library Central Hub Config`. Đây là URL root đã quan sát, không phải object locator hoặc cam kết ổn định của URL.

- Listing không lọc sau khi hoàn tất loading và đi tới cuối bảng hiển thị hai tệp, không có thư mục con hoặc nút pagination/load-more được hiển thị: `HUB-CAP-BRAINSTORM_v1.0.md` và `HUB-DOM-CREATIVE_v1.0.md`. Menu filter không có lựa chọn được đánh dấu. Search bằng `BRAINSTORM` trong `Search folder` trả một tệp sau khi loading kết thúc; xóa query trả lại hai tệp.
- Mở object BRAINSTORM từ listing của root, đọc toàn bộ văn bản trong viewer từ H1 tới đoạn cuối của Output behavior. Header khớp `HUB-CAP-BRAINSTORM / HUB-PKG-BRAINSTORM / CAPABILITY / ACTIVE / 1.0`, có Scope. Phần thân được đối chiếu nội dung với artifact repository: phân nhánh, đảo/nới giả định, hệ quả bậc hai, feedback, nối tiền đề và giữ phương án song song đều khớp về nội dung/trách nhiệm. Không tuyên bố so sánh byte-exact hoặc backend `has_more` mà UI không cung cấp.
- Đọc header của tệp còn lại để kiểm tra candidate khác tên: nó khai `HUB-DOM-CREATIVE / HUB-PKG-CREATIVE / DOMAIN_CONTROL`, không phải identity BRAINSTORM. Không dùng nó làm control hoặc xác minh behavior CREATIVE.
- Kết luận: `NO DUPLICATE OBSERVED IN SUFFICIENT SCOPED SEARCH`; đúng một identity BRAINSTORM hợp lệ trong listing/search quan sát được. Không chứng minh tính duy nhất toàn Library hoặc backend; nếu surface bỏ sót object không hiển thị, bằng chứng này không bao phủ nó. Phải kiểm tra lại khi root/nội dung thay đổi hoặc trước scoped execution theo Router.
- `File info`/`Version history` không cung cấp usable internal IDs trong lần kiểm tra trước; lần này không suy hoặc tạo chúng. `library_file_id`, `library_version_id`, durable `locator` giữ null. `observed_path` chỉ ghi đường dẫn hiển thị để tìm candidate trong root; không chứng minh object URL bền vững.
- Catalog ghi `RESOLVED` với verification phân loại rõ `CODEX_UI_OBSERVED_FULL_FILE_HEADERS_BODY_SCOPED_IDENTITY`, chỉ cho root-scoped resolution này. `HUB_RUNTIME_RETRIEVAL_NOT_VERIFIED`, `EXECUTION_NOT_RUN`; contract correction chưa deploy. Không upload, sửa Library object hoặc dùng non-Library fallback. Micro-test, S01–S04, AFM-015 A/B/C và AIS composition đều không chạy.

## Rollback có chủ đích

Nếu chưa chuyển deployment thì giữ nguyên bộ đang chạy. Nếu đã chuyển và cần quay về, khôi phục source roster/Instructions đã lưu. Để quay về đầy đủ v1.0: khôi phục root `HUB_CI_v1.0.md`, `HUB_ROUTER_v1.0.yaml`, các source `TECHNICAL_v1.0.md`, `CREATIVE_v1.0.md`, `BRAINSTORM_v1.0.md`; gỡ core v1.1 khỏi deployment; giữ AIS/ImageT hiện hành và Library objects nguyên trạng nhưng không được v1.0 chọn. ROLLBACK != FALLBACK. Không đổi Catalog sang legacy tự động khi Library lỗi.

Nguồn rollback v1.0/legacy hiện nằm byte-exact dưới `Source_archive/Central Hub legacy v1.0/`, giữ cấu trúc đường dẫn cũ bên trong. Khi người dùng chủ động rollback, lấy đúng file từ đó; không có đọc archive trong runtime. Receipt: `Source_archive/HUB_LEGACY_ARCHIVE_RECEIPT_2026-10-19.json`. Các đường dẫn source cũ nêu trong phần rollback là vị trí tương đối bên trong nhóm archive này.
