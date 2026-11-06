# AFM-002 — full-module differentiation stress pilot

Status: `NON_AUTHORITATIVE_WORKING_COPY`; `PHASE_2_COMPLETE`; `AFM-002_FULL_MODULE_STRESS_PASS`; `EXPERIMENT_STOPPED`. Đây là đầu vào thử nghiệm do người dùng cung cấp, không phải source FTH, Hub control, Library binding hay canon authority. Phase 1 chỉ chuẩn bị điều kiện FULL_FILE; không đề xuất tái cấu trúc FTH.

## Provenance và nguồn

- Repository `lead21pc/chatgpt-ci-worldbuilding`; preflight branch `main`, local HEAD và remote `origin/main` `8ba24079dd4225ac84cafa263a6b0616d7fb3d37`; working tree/index sạch.
- Source `Project Feather Core/11_STATUS_CIVIL_LABOR_CURRENT.md`, `Module ID: AFM-002`, `Runtime role: CURRENT_SOURCE`, `Load mode: FULL_FILE`.
- [AFM-002_FULL_FILE_SNAPSHOT.md](AFM-002_FULL_FILE_SNAPSHOT.md): bản sao nguyên byte của source tại preflight, 55.643 byte, SHA-256 `b814636063a61e52a9b9f0c948a2a722ba96d58b6a3dffcd27ed087c03f68e82`.
- Header `CURRENT_SOURCE` và Module ID bên trong snapshot là nguyên văn của source FTH, không cấp authority, activation hoặc admission cho bản sao thử nghiệm. `CURRENT_SOURCE != TEST SNAPSHOT`. Snapshot không tự cập nhật; nếu source đổi, kiểm lại baseline trước khi dùng.
- `FULL_FILE REMAINS THE BASELINE`: envelope không thay source hoặc tóm tắt thay toàn bộ snapshot. Source FTH tiếp tục có authority theo bộ FTH; output thử nghiệm không tự sửa canon.

## Scope và owner

Thử khả năng dùng một full-module working snapshot khi AFM-002 chứa nhiều trục khác nhau. Đây là bài test hành vi của điều kiện full-file, không là kết luận rằng module phải tách. `FULL_FILE PASS != GLOBAL FTH PASS`; `FAIL != PROOF OF MODULARIZATION`.

AFM-002 quản lý legal/civic status ontology, Civil/labor interfaces và các namespace kinh tế/truy cập trong scope AetherFire. `AFM-013` giữ national profile; `AFM-003` giữ chi tiết nghề Undie, entry/exit/mobility/work/access và Undi; `AFM-010` giữ kiến trúc terminal/dịch vụ chung, không thay quyền AFM-002 về status và economic namespace. Pointer không phải hard dependency, không chứng minh owner khác đã được đọc. Không suy canon ngoài miền từ tên/pointer; không dùng repository, archive hoặc snapshot làm fallback cho Hub control Library.

Civil voluntary ở đầu vào, admission không tự động; assignment phù hợp sau admission là nghĩa vụ, có căn cứ appeal/reassessment, upkeep và pay tách biệt. Citizen có thể hành nghề Undie, nhưng compatibility giữa nghĩa vụ Civil và nghề Undie chưa chốt. Legal/civic status, social standing, class/color, job, Career Rank, Zone, Credits, Contribution Points, Access Profile và background là các trục cần xét đúng scope; khác trục không có nghĩa không thể có quan hệ được nguồn chốt. Không áp nguyên tắc quốc gia AetherFire thành luật chung mọi nước.

## Open state liên quan

Các ID dưới đây là điểm dẫn từ `Project Feather Core/92_OPEN_ISSUES_CURRENT.md` tại preflight, không thay FULL_FILE source hoặc giải quyết UNKNOWN:

- `AF-CR-OPEN-001`: cơ quan/eligibility/screening, admission, matching/priority, assignment validation, reserve/reassignment và giới hạn điều động/relocation còn mở.
- `AF-CR-OPEN-003`: pay/upkeep/housing chi tiết, full labor code, giờ/nghỉ/y tế, full appeal/discipline ladder và giới hạn còn mở.
- `AF-CR-OPEN-005`: immigration/residency/citizenship sequence, completion/reintegration, re-entry và compatibility Undie còn mở.
- `AF-OPEN-008`: employer powers/liability, authority và full service/access matrix Civil còn mở dù public neutrality và một số rights đã chốt.
- `AF-TECH-001`: nhiều triển khai terminal/Guest Pass, access, legal recognition, recovery/exit, privacy và authority còn mở. Thiết bị/access không tự thay status hay xác lập quyền nhập cư.

`UNKNOWN != FALSE`; danh sách này không chứng minh không còn UNKNOWN khác. Tách CURRENT, branch-local ASSUMPTION và PROPOSAL khi material; không nhập đề xuất thành state hay dùng owner chưa đọc như nguồn đã xác minh.

## Cách thực hiện sau khi được phép

Mỗi F1/F2/F3 dùng chat sạch riêng trong actual Central Hub. Cung cấp FULL_FILE README/envelope này và FULL_FILE [snapshot](AFM-002_FULL_FILE_SNAPSHOT.md), rồi chỉ gửi block prompt của case trong [TEST_CASES.md](TEST_CASES.md). Không gửi rubric/đáp án đánh giá cho model; không nạp sẵn lore owner khác và không ép Hub chọn leaf. Nếu thiếu nguồn decisive, giữ phần phụ thuộc có điều kiện hoặc chặn đúng phần; tiếp tục phần độc lập có đủ input.

Lưu chính xác input, output, model/surface, thời điểm, nguồn/control đã cung cấp, actual read evidence và blocker có thể quan sát. Tự báo đã đọc không tự chứng minh FULL_FILE. Thiếu output hoặc read evidence quyết định là giới hạn evidence, không tự gán semantic fail. Không dựa vào snapshot làm FTH runtime authority.

Phase 1 không chạy live, không tạo output, không tạo slice hoặc split control. Các nhãn `NOT_RUN` trong `TEST_CASES.md` ghi trạng thái tại thời điểm chuẩn bị Phase 1; kết quả Phase 2 được ghi dưới đây. Không stage/commit/push/deploy, sửa Library, FTH CURRENT hoặc Hub control trong Phase 1.

## Kết quả Phase 2 và kết thúc thí nghiệm

Người dùng cung cấp kết quả đánh giá bên ngoài Codex cho ba live Central Hub case: **F1 PASS; F2 PASS; F3 PASS**. `AFM-002_FULL_MODULE_STRESS_PASS` là kết quả được người dùng báo cáo; Codex không nhận output nguyên văn trong tác vụ ghi nhận này và không tự tái hiện hoặc đánh giá lại các lượt runtime. Không có bằng chứng repository cho thấy test input đã ghi khác bộ case được chuẩn bị.

Theo đánh giá được cung cấp, phát triển Civil cục bộ không viết lại ontology ngoài scope; status, Civil participation, profession, Career Rank, Access Profile và provenance được phân biệt, cùng các quan hệ đã chốt; UNKNOWN và branch-local assumption được giữ; ranh giới AFM-003/AFM-010 được nhận diện; không bịa canon owner khác hoặc từ chối không cần thiết phần AFM-002 độc lập; proposal không thành current canon. Không quan sát material semantic-entanglement failure trong F1/F2/F3 theo kết quả được báo cáo.

`OBSERVED GRANULARITY FAILURE: NONE IN TESTED SCOPE`; `IMMEDIATE AFM-002 MODULARIZATION REQUIREMENT: NOT ESTABLISHED`. Thí nghiệm dừng vì full-module condition PASS; split control không cần thiết và không được tạo. Không thực hiện admission hoặc sửa canon FTH. Kết quả này không là global FTH/Hub validation, không bảo đảm các module khác, revision tương lai hay mọi lần chạy sẽ PASS, và không loại trừ khả năng một split về sau có ích.
