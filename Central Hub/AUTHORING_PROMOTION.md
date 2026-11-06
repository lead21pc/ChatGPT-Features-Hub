# Authoring 0.7 — promotion vào Central Hub nguồn

Ngày 2026-11-05 (Asia/Bangkok). Người dùng duyệt promotion sau audit `ACCEPT WITH LOCAL CORRECTION`. Baseline repo nguồn: branch `main`, HEAD `b3f470a46c87c4bfad68d74bf031f78d7abc87b4`, working tree/index sạch.

## Bộ active trong repository

Hub CI/Router 1.1; Architecture/Catalog 1.9; Authoring `HUB-CAP-AUTHORING / HUB-PKG-AUTHORING / CAPABILITY / ACTIVE / 0.7`. CI giữ nguyên byte, Router chỉ đổi contracts pins. Catalog `identity_binding` đã sửa sang exact stack 1.9; mọi package ngoài Authoring giữ nguyên.

v0.7 thêm exact `/AUTHOR <OUTPUT_TARGET> ISOLATED` và `/AUTHOR <OUTPUT_TARGET> P<n> ISOLATED`. Chỉ nhận task material được cung cấp hoặc định danh đủ rõ trong yêu cầu hiện tại, vẫn giữ mandatory controls và quyền target. Không có suffix thì giữ hành vi 0.6; preset và contributor composition không đổi. Không thêm parser, package, registry, persistent mode hoặc API host vào repo nguồn.

## Bằng chứng đã có và giới hạn

Nguồn chuyển giao là các control trong `upstream/Central Hub/` của [Central-Hub-Local tại commit cố định](https://github.com/lead21pc/Central-Hub-Local/tree/b2246460dba2c74c00eaff9022497abef5784f3b/upstream/Central%20Hub). Candidate 0.7 gốc đã có trong repo nguồn; body active từ dòng “For the current turn only” khớp candidate. Bỏ mục source isolation thì body kế thừa khớp v0.6.

[Bằng chứng M2 đầy đủ](https://github.com/lead21pc/Central-Hub-Local/tree/b2246460dba2c74c00eaff9022497abef5784f3b/m2_evidence/authoring_0_7) và [verification của host local](https://github.com/lead21pc/Central-Hub-Local/blob/b2246460dba2c74c00eaff9022497abef5784f3b/VERIFICATION.md): candidate I1/I3 PASS, một API call mỗi ca; một active local request PASS với ba API calls, `isolated=true`, blocker rỗng, không tool/target execution. Đây là RECORDED CANDIDATE / LOCAL API LIVE EVIDENCE, không phải lần tái hiện trong tác vụ promotion này hoặc bằng chứng ChatGPT Library/Project.

Ngày 2026-11-05, người dùng xác nhận Authoring 0.7 trong Central Hub vừa promotion đã chạy live thành công. Phân loại: **USER_CONFIRMED_LIVE_PASS** cho đường Authoring 0.7 / Architecture-Catalog 1.9 / CI-Router 1.1 trong phạm vi xác nhận này. Codex không trực tiếp chạy lại hoặc quan sát phiên live; không có danh sách ca, raw input/output, model/run time hay receipt Library object/FULL_FILE được cung cấp. Không suy PASS cho mọi target/preset/ISOLATED case hoặc exact production identity từ xác nhận tổng quát này.

Xác nhận mới supersede trạng thái live NOT ESTABLISHED của đường Authoring 0.7 đã báo trước đó; không đổi nhãn bằng chứng API/local hoặc lịch sử v0.6. Việc cài/switch Project không do Codex thực hiện; exact Library identity/FULL_FILE binding vẫn NOT_VERIFIED / UNRESOLVED.

## Kiểm chứng và lưu predecessor

Các test lịch sử v0.6 được trỏ về snapshot đúng revision. `tests/test_authoring_07.py` kiểm active module, no-suffix preservation, exact Catalog/Router/Architecture binding, package ngoài scope, cú pháp spec và archive receipt bằng thư viện kiểm thử sẵn có; không import host local.

Năm predecessor (module 0.6, Architecture/Catalog 1.8, snapshots Router/promotion) được lưu nguyên byte tại `Source_archive/Authoring 0.7 M2 2026-11-05/`, kèm `ARCHIVE_RECEIPT.json`. Archive chỉ là lịch sử/rollback có chủ đích, không phải runtime fallback.

Kiểm chứng sau promotion: **232/232 full Hub tests PASS**, gồm **5/5 active Authoring 0.7 tests**; toàn bộ kết nối socket bị chặn. `compileall` **19 file Python PASS**; `git diff --check` PASS. Ngoài tests lịch sử Authoring, các test dùng current Catalog/Architecture được đổi pin sang 1.9, giữ nguyên kiểm tra package behavior. Một kiểm tra lịch sử Concept tiếp tục so sánh đúng snapshot trước promotion; không bỏ assertion để làm suite xanh. Không chạy API live.

Đối chiếu hash xác nhận CI, mọi package ngoài Authoring, candidate sources và các archive cũ không đổi. Năm predecessor khớp byte-exact trước/sau lưu trữ; `.gitattributes` trong nhóm archive ngăn Git chuẩn hóa bytes. Quét secrets trong file mới/sửa không phát hiện credential.

## Cài đặt hoặc rollback có chủ đích

Promotion repository không tự cài đặt. Khi có quyền triển khai riêng: thay đúng Authoring 0.7 trong Library / Central Hub Config, xác minh đúng một object ACTIVE, FULL_FILE/identity/body và phạm vi duplicate; cài Router 1.1 với Architecture/Catalog 1.9 như một bộ tương thích. Giữ CI 1.1. Không dùng repo/archive làm nguồn thay thế khi Library resolution thất bại. Chỉ kết luận live ChatGPT sau bằng chứng riêng cho bộ đã cài.

Nếu cần rollback được cho phép, khôi phục đồng bộ bộ 0.6/1.8 từ archive, gồm snapshot Router, rồi kiểm lại binding; không giữ hai bộ như hai authority active. Không tự rollback hoặc kích hoạt pipeline/target.

Tác vụ này không gọi API live, triển khai Project/Library, push hoặc mở lại M3/M4 của host local.
