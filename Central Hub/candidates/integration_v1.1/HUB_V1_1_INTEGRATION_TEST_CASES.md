# Central Hub v1.1 — thử tích hợp thủ công

Status: CANDIDATE / NOT ACTIVE production. LIVE INTEGRATION: NOT_RUN.
STATIC CONTRACT TEST != SPEC SIMULATION != LIVE PROJECT TEST.

Mục tiêu: thử toàn bộ CI → Router → Catalog → binding → scoped application. Bằng chứng người dùng cung cấp cho riêng ACTIVE TECHNICAL/1.0 (V01/V02 PASS, FULL_FILE 19/19, has_more=false) không thay kết quả stack. Không yêu cầu hidden chain-of-thought.

## Cài đặt thủ công cho trial được ủy quyền

Trước khi thử, lưu nội dung Project Instructions và danh sách Project Sources đang dùng để rollback. Ghi rõ: “Tôi cho phép thử thủ công đúng bộ integration candidate v1.1 đã cài; chưa promotion production hoặc package candidate khác.” Chỉ người dùng thực hiện cài đặt; việc tạo các file local này không cài Project.

**PROJECT INSTRUCTIONS:** thay bằng toàn bộ nội dung `HUB_CI_v1.1-candidate.md` trong thư mục này. CI chỉ đổi một tham chiếu Router so với v1.0.

**PROJECT SOURCES:** thêm đúng ba file trong thư mục này:

- `HUB_ROUTER_v1.1-integration-candidate.yaml`
- `HUB_ARCHITECTURE_v1.0-integration-candidate.md`
- `HUB_PACKAGE_CATALOG_v1.0-integration-candidate.yaml`

Giữ các nguồn hiện hành sau, không đổi nội dung:

- `domains/creative/CREATIVE_v1.0.md`
- `capabilities/BRAINSTORM_v1.0.md`
- `tool_pipelines/AIS/AIS_PIPELINE_v1.0.md`
- `tool_pipelines/AIS/AIS_ROUTER_v1.1.yaml`
- `tool_pipelines/ImageT/IMAGE_CONTROLLER_v1.1.md`
- `tool_pipelines/ImageT/IMAGE_SOURCE_ROUTER.yaml`
- `tool_pipelines/ImageT/manifest.yaml`
- `tool_pipelines/ImageT/READY_GATE_v1.0.md`
- `tool_pipelines/ImageT/IMAGE_ANTI_PRIOR.md`
- `tool_pipelines/ImageT/config.md`

Đường dẫn trên xác định nguồn repository; nguồn upload phải giữ filename chính xác. Nếu Project Sources làm phẳng thư mục, đối chiếu `source_name` cùng nguồn khai báo; trùng tên hoặc không xác lập được exact source thì chặn. Pipeline tiếp tục tự resolve dependency; root Catalog không enumerate chúng. Giữ nguyên trạng thái preference inactive/direct-input-only; không upload preference như active control.

Trong **live Project**, gỡ nguồn cũ `TECHNICAL_v1.0.md` (`domains/technical/TECHNICAL_v1.0.md`) để tránh hai authority. Thay/gỡ `HUB_ROUTER_v1.0.yaml` khỏi runtime Sources khi thử. Nếu các core design cũ `HUB_ROUTER_v1.1-candidate.yaml`, `HUB_ARCHITECTURE_v0.1.md`, `HUB_PACKAGE_CATALOG_v0.1.yaml` đang được upload như control, gỡ chúng để chỉ bộ integration được resolve. Không gỡ nguồn không liên quan. Không xóa bất kỳ bản repository nào.

**LIBRARY:** ACTIVE TECHNICAL/1.0 đã có trong `Central Hub Config`; giữ nguyên object `libfile_bab7d55cd85c819198291acf135099fd`, Library version_id `1`. Không upload lại trial/candidate hoặc dùng file local thay retrieval. Không upload test spec, tests, evidence records hoặc archive làm runtime control.

## Quan sát và tiêu chí

Mỗi case ghi: Project Instructions thực dùng; Router/Catalog thực đọc; package/module được chọn; artifact/object identity; location; FULL_FILE và has_more; giá trị header thực thấy; pipeline calls; response behavior; fallback attempts; PASS/FAIL/UNVERIFIABLE. Ghi nguồn bằng chứng (tool trace hoặc báo cáo có thể quan sát). Route report tự khai không đủ chứng minh Library read; thiếu bằng chứng quyết định thì UNVERIFIABLE. Không suy PASS từ static tests hoặc từ việc output có vẻ đúng.

Với TECHNICAL yêu cầu đúng `HUB-PKG-TECHNICAL`, `HUB-DOM-TECHNICAL`, `REASONING_PROFILE`, `ACTIVE`, artifact Version `1.0`, root và object đã binding; Library version_id `1` là metadata riêng. FULL_FILE phải đủ toàn bộ file, không chỉ header/snippet. Legacy source không có new Module header: ghi N/A và exact-source/full-read evidence; không giả header verification.

## I01–I10

| Case | Prompt gửi trong Project | Kết quả và bằng chứng cần có |
| --- | --- | --- |
| I01 — ORDINARY BASELINE | Viết lời nhắn hai câu cảm ơn đồng nghiệp đã giúp chuyển lịch họp. | Empty specialization set / NONE; baseline đủ dùng; không Library lookup hoặc pipeline call. |
| I02 — TECHNICAL AUTO-SELECTION | Sau khi đổi cấu hình cache, ứng dụng đôi lúc trả dữ liệu cũ dù database đã cập nhật. Hãy nối triệu chứng với các cơ chế khả dĩ và đề xuất phép thử phân biệt chúng trước khi sửa. Chưa cho phép thay đổi hệ thống. | Không nêu TECHNICAL hoặc Module ID trong prompt. Router tự chọn HUB-PKG-TECHNICAL; exact Library ACTIVE/1.0 FULL_FILE + headers; phân biệt giả thuyết/bằng chứng và phép thử. Không dùng Project Source cũ. |
| I03 — DEACTIVATION | Viết lại câu này thân thiện hơn: “Cuộc họp chuyển sang 10 giờ sáng mai.” | Gửi ngay sau I02; TECHNICAL không được giữ như mode; không specialization nếu không cần. |
| I04 — CREATIVE PRESERVATION | Viết cảnh ngắn hai người bạn gặp lại ở ga tàu; dùng hành động, nhịp câu và chi tiết có chức năng để thể hiện khoảng cách giữa họ, không giải thích trực tiếp cảm xúc. | CREATIVE exact Project Source/full read; giữ premise và scope; không Library discovery cho CREATIVE. |
| I05 — BRAINSTORM PRESERVATION | Với tiền đề thành phố vận hành bằng cách giữ bí mật, hãy đảo giả định thành bắt buộc công khai thông tin; phát triển ba nhánh khác cơ chế, theo hệ quả bậc hai và một phản hồi vào tiền đề. | BRAINSTORM exact Project Source/full read; không Library lookup cho capability; không tự gọi pipeline. CREATIVE chỉ nếu có đóng góp riêng thực sự. |
| I06 — TECHNICAL + BRAINSTORM | Một hệ thống phân phối nước thường thiếu nước cuối tuyến dù tổng cấp đủ. Nối các giả thuyết cơ chế với phép thử phân biệt, rồi đảo hoặc nới hai giả định vận hành để phát triển các phương án và hệ quả bậc hai. Chưa sửa hệ thống. | Cùng phần việc cần TECHNICAL Library + BRAINSTORM Project Source; hai đóng góp có scope, không thay thế nhau; không tự cấp authorization thay đổi. |
| I07 — TECHNICAL + AIS | Hãy tra cứu tài liệu chính thức PostgreSQL hiện hành để kiểm chứng các cơ chế có thể khiến truy vấn ở replica thấy dữ liệu cũ sau khi primary đã commit; phân biệt giả thuyết và đề xuất phép thử phù hợp với giới hạn nguồn. | TECHNICAL Library; AIS Project Source được Hub chọn độc lập do yêu cầu xác minh ngoài; AIS sở hữu research internals và evidence. Không yêu cầu ImageT. |
| I08 — TECHNICAL LIBRARY FAILURE | Chỉ lặp prompt I02 khi đã có cách gây lỗi truy xuất tạm thời, có kiểm soát và khôi phục an toàn. | Case tùy chọn. Không sửa/xóa Library object để tạo lỗi. Nếu không gây lỗi hoặc không quan sát được an toàn: UNVERIFIABLE. Khi lỗi thật: chặn phần phụ thuộc, không fallback nguồn TECHNICAL cũ/Memory/repo/root khác; tiếp tục baseline độc lập đủ dùng. |
| I09 — SCOPE CHANGE | Gửi lần lượt prompt I02 → I03 → I02 trong cùng chat. | Mỗi turn đánh giá lại: TECHNICAL → NONE → TECHNICAL. Đọc lại nếu read evidence không còn đủ; không coi lần kích hoạt trước là quyền kích hoạt hiện tại. |
| I10 — ROUTE INSPECTION | Với yêu cầu chẩn đoán cache ở I02, hãy báo ngắn tuyến thực dùng: Package ID, Module ID, binding location, scope, Router/Catalog đã đọc và trạng thái đọc artifact; không trình bày suy nghĩ riêng tư. | Báo route và observable evidence trung thực. Nêu unresolved nếu chưa đọc; không fabricate FULL_FILE. Object/header phải đối chiếu trace khi có. |

Mọi case hiện `NOT_RUN`. I08 không chạy an toàn thì ghi `UNVERIFIABLE`, không PASS. Header mismatch, partial file và duplicate identity được kiểm bằng static/spec; live failure coverage vẫn cần quan sát riêng, không tái diễn giải V01/V02.

## Rollback có chủ đích

1. Khôi phục Project Instructions v1.0 đã lưu (`HUB_CI_v1.0.md`).
2. Khôi phục active `HUB_ROUTER_v1.0.yaml` trong Project Sources.
3. Khôi phục Project Source `TECHNICAL_v1.0.md` đúng nguồn cũ nếu đã gỡ; CREATIVE/BRAINSTORM/AIS/ImageT giữ nguyên.
4. Gỡ ba core integration Architecture/Catalog/Router khỏi Project Sources.
5. Giữ Library artifact nguyên trạng, đánh dấu không dùng trong ghi chép triển khai nếu cần.

ROLLBACK != FALLBACK. Thực hiện đảo cài đặt rõ ràng; Router không tự rollback khi Library lỗi. Repository candidate vẫn giữ để review.
