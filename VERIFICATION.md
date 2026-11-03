# Kết quả kiểm chứng Giai đoạn 1

Ngày kiểm chứng: 2026-11-03 (Asia/Bangkok).

`STATIC / LOCAL APP VERIFIED`

`USER-PROVIDED LIVE API VERIFIED`

Giai đoạn 1 đạt PASS theo xác nhận của người dùng ngày 2026-11-03: hai prompt kiểm thử live đã PASS trên đường Streamlit → config → OpenAI API → GPT-5.6 Sol → response hiển thị, với Central Hub chưa tham gia. Đây là bằng chứng do người dùng cung cấp; Codex chưa trực tiếp tái hiện live API call.

Đã kiểm tra bằng Python 3.11.9, openai 2.38.0, streamlit 1.58.0:

- Import SDK/app và biên dịch Python: đạt.
- Đọc config thật; từ chối config thiếu, JSON lỗi, sai kiểu hoặc model rỗng: đạt.
- Streamlit AppTest: tiêu đề, model, prompt rỗng, key rỗng và không thêm lượt thất bại vào lịch sử: đạt.
- SDK thật với HTTP transport mô phỏng, không gửi ra mạng: payload đúng model, chỉ có user/assistant, `store=False`, response hiển thị trong UI và hai lượt hội thoại đúng thứ tự: đạt.
- HTTP mô phỏng 401/429/404/500, mất kết nối, timeout, response rỗng/chưa hoàn tất; không retry, không thay lịch sử khi lỗi, đọc lại key khi gửi: đạt.
- Server Streamlit thật tại loopback: trang HTTP 200 và health `ok`; đã dừng server sau kiểm tra: đạt.
- So sánh SHA-256 toàn bộ 212 tệp và toàn bộ đường dẫn thư mục giữa nguồn và bản sao: khớp. Bao gồm cả cache có sẵn trong nguồn; không chạy test hoặc sửa nội dung bản sao.
- `git diff --check` cho các file app/tài liệu mới: đạt. Kiểm tra toàn bản sao báo whitespace có sẵn (gồm CRLF và các dòng trong patch nguồn); giữ nguyên theo yêu cầu sao chép byte-exact, không sửa để làm sạch kiểm tra này.

Baseline tại thời điểm kiểm chứng local ban đầu: workspace chưa có app và chưa thuộc repo nào. Đã tạo repo Git local, branch `main`, lúc đó chưa có HEAD/commit hoặc remote. Các file mới có đánh dấu intent-to-add để xem diff, lúc đó chưa stage nội dung hoặc commit. `config.json` được bỏ qua. Repo nguồn có working tree sạch, branch `main`, HEAD `b3f470a46c87c4bfad68d74bf031f78d7abc87b4` khi sao chép. Không sửa repo nguồn.

Lịch sử bằng chứng: lần kiểm chứng local ban đầu ghi `LIVE API VERIFIED: NOT RUN` vì môi trường Codex thiếu API key. Xác nhận hai prompt live đã PASS từ người dùng thay thế trạng thái live trước đó; kết quả local và mô phỏng bên trên vẫn giữ nguyên phạm vi bằng chứng.

# Kết quả kiểm chứng Giai đoạn 2

Ngày kiểm chứng: 2026-11-04 (Asia/Bangkok). Phần Giai đoạn 1 ở trên được giữ nguyên như bằng chứng lịch sử.

Baseline: repo `<LOCAL_REPO>`, branch `main`, HEAD `60578279835b248c59c95b14be59070e40e7471b`; working tree và staging sạch trước khi sửa. Không commit, push, tạo branch, tag hay remote trong Giai đoạn 2.

`STAGE 2 STATIC / LOCAL APP VERIFIED: PASS`

- `python -X utf8 -m compileall -q app.py test_app.py`: đạt. Import app/SDK qua bộ kiểm thử: đạt.
- `python -X utf8 -m unittest -v test_app`: 6/6 đạt; SDK thật dùng HTTP transport mô phỏng, không gửi mạng trong bộ kiểm thử này.
- T0: payload vẫn đúng `model`, `input`, `store=False`; không có `instructions`, không đọc CI ngay cả khi CI không khả dụng.
- T1: mỗi request đọc lại đúng `HUB_CI_v1.1.md`; toàn bộ `instructions` mã hóa lại UTF-8 khớp bytes nguồn, không strip, sửa BOM hoặc chuẩn hóa CRLF. Kiểm thử thêm hai nội dung giả khác nhau liên tiếp để phát hiện cache hoặc biến đổi văn bản.
- Hai lượt ở từng chế độ giữ đúng thứ tự user/assistant. AppTest gửi bốn lượt T0 → T1 → T1 → T0: giữ lịch sử chung, nhãn đúng trên từng phản hồi, nhãn không lọt vào payload; UI có đúng hai lựa chọn và T0 là mặc định.
- CI thiếu, lỗi quyền đọc, lỗi I/O hoặc UTF-8: báo lỗi T1 rõ ràng trước khi tạo client API, không chuyển sang T0. AppTest với CI thiếu/lỗi quyền đọc xác nhận lịch sử và prompt còn nguyên, không phát sinh request.
- So sánh SHA-256 trước/sau toàn bộ 212 tệp dưới `upstream/Central Hub/`: khớp cả tập đường dẫn và bytes; `git diff --exit-code -- upstream/`: đạt. Không sửa hoặc chạy test trong bản sao.
- CI nguồn: 7.889 bytes; SHA-256 `7bb946874663627060d28e47674decb07ba99f51acbffb6550db98d65746157b`.
- `git diff --check`: đạt. Không đổi dependency, model, timeout, retry, lưu API hoặc định dạng lịch sử gửi API; metadata nhãn chỉ giữ riêng trong Streamlit session.

`STAGE 2 LIVE API T1: PASS`

Codex đã dùng key hiện có trong `config.json`, không in key, gửi hai request API thật bằng AppTest qua app → SDK → `https://api.openai.com/v1` → `gpt-5.6-sol`:

1. Prompt `Chỉ trả lời: T1 OK` → phản hồi `T1 OK`.
2. Prompt `Tôi vừa yêu cầu bạn trả lời gì?` → phản hồi `Bạn vừa yêu cầu tôi chỉ trả lời: “T1 OK”.`.

Cả hai phản hồi được render, gắn nhãn T1; lịch sử gồm user → assistant → user → assistant. Đây là bằng chứng kết nối API thật và hội thoại T1 cơ bản; không chứng minh tuân thủ toàn bộ quy tắc CI. Chưa kiểm tra thủ công bằng trình duyệt ở Giai đoạn 2; chưa chạy lại live T0 (bằng chứng live T0 Giai đoạn 1 vẫn do người dùng cung cấp). Không tái chạy mọi tình huống lỗi API của Giai đoạn 1.

Để kiểm tra thủ công: chạy lệnh Streamlit trong README, mở session mới, chọn T1 và gửi hai prompt trên; xác nhận nhãn T1 cạnh cả hai phản hồi và câu thứ hai nhắc đúng `T1 OK`. Mở session mới với T0 để so sánh đối chứng mà không mang lịch sử T1.

# Kết quả kiểm chứng T2 — chọn thủ công Technical

Ngày kiểm chứng: 2026-11-04 (Asia/Ho_Chi_Minh). Toàn bộ bằng chứng Giai đoạn 1/2 phía trên được giữ nguyên.

Baseline: branch `main`, HEAD `60578279835b248c59c95b14be59070e40e7471b`; các thay đổi Giai đoạn 2 được tiếp tục tại chỗ. Không reset/revert/stage/commit/push/tag/branch hoặc sửa remote.

`T2 STATIC / LOCAL APP VERIFIED: PASS`

- Thêm đúng một chế độ `T2 - Hub CI + Technical`; T0 và T1 giữ hành vi cũ.
- T2 đọc lại `HUB_CI_v1.1.md` và `runtime/packages/technical/HUB-DOM-TECHNICAL_v1.0.md` mỗi request.
- `instructions` của T2 có thứ tự: Hub CI nguyên văn → bridge chọn thủ công tối thiểu bằng tiếng Anh → Technical nguyên văn.
- Bridge chỉ nói Technical được chọn thủ công cho request/task portion hiện tại vì Router cố ý không nạp; không mô phỏng Router và không đổi semantics của Technical.
- Technical nguồn: `upstream/Central Hub/candidates/promotion/HUB-DOM-TECHNICAL_v1.0.md`, ACTIVE, Version 1.0, 1.869 bytes; SHA-256 `fb42257b74597d5b680e5334cf1a132f04f17eb708a507444da0f3fe4a9f73d4`.
- Technical runtime: `runtime/packages/technical/HUB-DOM-TECHNICAL_v1.0.md`, byte-exact với nguồn trên, cùng SHA-256.
- `python -X utf8 -m compileall -q app.py test_app.py`: đạt.
- `python -X utf8 -m unittest -v test_app`: 9/9 đạt sau correction bridge.
- T0 không đọc Hub CI hoặc Technical và không gửi `instructions`.
- T1 đọc Hub CI nhưng không đọc Technical; payload `instructions` vẫn đúng Hub CI.
- T2 đọc cả hai mỗi request; kiểm thử giả với BOM/CRLF xác nhận không strip hoặc chuẩn hóa nội dung control.
- CI/Technical thiếu, lỗi quyền đọc, I/O hoặc UTF-8 trong T2: lỗi trước API và không fallback T1/T0.
- AppTest xác nhận chuyển T0 → T1 → T2 → T1 → T0 → T2 vẫn giữ lịch sử chung và đúng nhãn phản hồi.
- Toàn bộ 212 tệp dưới `upstream/` vẫn byte-identical với snapshot trước T2; `git diff --exit-code -- upstream/` đạt.
- Không nạp Router, Architecture, Root Catalog, Concept, Authoring, AIS, ImageT hoặc package khác; không thêm routing engine/eval framework/hạ tầng tương lai.

`T2 LIVE API: PASS CHO ĐƯỜNG GỌI; A/B HÀNH VI SẠCH ĐÃ CHẠY`

Lần live đầu do Codex chạy dùng hai prompt bị PowerShell thay dấu tiếng Việt bằng `?`. Lần đó chứng minh đường T2 → API thật → response hoạt động, nhưng không được dùng làm bằng chứng chính về hành vi.

Sau correction bridge, phép thử A/B sạch dùng file UTF-8 và session riêng cho từng mode, cùng hai prompt:

1. `Máy tính thỉnh thoảng khựng 1-2 giây khi mở nhiều tab. Chưa có log hay số liệu. Hãy chẩn đoán nguyên nhân.`
2. `Vậy nguyên nhân nào là chắc chắn nhất?`

T1 và T2 đều:
- không biến triệu chứng thành nguyên nhân đã xác nhận;
- giữ nhiều giả thuyết cạnh tranh khi thiếu dữ liệu;
- ưu tiên RAM/hoán đổi chỉ như giả thuyết cần kiểm tra;
- từ chối khẳng định nguyên nhân chắc chắn ở lượt hai;
- đưa kiểm tra phân biệt bằng RAM/CPU/ổ đĩa/tab/tiện ích/GPU.

Quan sát khác biệt trong một cặp A/B này:
- T2 trình bày chuỗi cơ chế và các giả thuyết cạnh tranh có cấu trúc rõ hơn một chút.
- T1 đã thực hiện phần lớn cùng kỷ luật chẩn đoán, nên phép thử này chưa chứng minh Technical tạo cải thiện lớn.
- Không thấy T2 làm câu trả lời cứng hơn hoặc làm mất khả năng chẩn đoán.
- Một cặp A/B không đủ để kết luận mức đóng góp ổn định của Technical; cần thêm case phân biệt nếu muốn đánh giá giá trị biên của module.

Trạng thái bằng chứng hiện tại:

```text
T2 HOST PATH
= VERIFIED

TECHNICAL LOCAL BYTE-EXACT BINDING
= VERIFIED

BASIC LIVE TECHNICAL BEHAVIOR
= OBSERVED

TECHNICAL ADDED VALUE OVER T1
= NOT YET ESTABLISHED
```

T2 hoàn tất trong phạm vi một module chọn thủ công. Chưa bắt đầu T3/Router.

# Kết quả kiểm chứng T3 — mô phỏng chọn root package

Ngày kiểm chứng: 2026-11-04 (Asia/Bangkok). Giữ nguyên toàn bộ bằng chứng T0/T1/T2 phía trên; câu kết phần T2 mô tả thời điểm hoàn tất T2, trước lần triển khai này.

Baseline T3: repo `<LOCAL_REPO>`, branch `main`, HEAD `60578279835b248c59c95b14be59070e40e7471b`; staging trống. Trước T3 đã có `M README.md`, `M VERIFICATION.md`, `M app.py`, `?? runtime/`, `?? test_app.py`. Các thay đổi đó được giữ lại. Không stage, commit, push, tag, tạo branch hoặc sửa remote.

`T3 IMPLEMENTED / STATIC VERIFIED; LIVE ROUTE INSPECTION OBSERVED`

- Thêm `T3 - Hub Routing Inspect` và hàm `inspect_route` riêng. Hàm `call_model` giữ nguyên hành vi T0/T1/T2. T3 chỉ gửi prompt hiện tại; lưu bản ghi riêng trong session, không đưa JSON hay adapter T3 vào lịch sử hoặc chỉ dẫn T0/T1/T2.
- Mỗi request T3 đọc nguyên bytes, giải mã UTF-8 của đúng CI 1.1, Router 1.1, Architecture 1.8, Catalog 1.8 từ upstream; thêm adapter tiếng Anh tối thiểu. Không tạo control kế nhiệm hoặc binding thay thế. Model thực hiện TASK_SCOPE và ROOT_PACKAGE_SELECTION theo `eligibility.simulation`; dừng trước truy xuất/thực thi package.
- Responses API dùng `text.format.type=json_schema`, `strict=true`, `store=False`, model cấu hình `gpt-5.6-sol`, URL `https://api.openai.com/v1`; timeout 120 giây và không retry như các mode cũ. Không truyền tools hoặc trạng thái hội thoại API. SDK đang cài `openai==2.38.0` hỗ trợ tham số `text`; không đổi dependency. Đã tra và mở [tài liệu OpenAI về Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs?api-mode=responses).
- Schema chỉ gồm task_scope, selected_packages với năm trường root routing và unresolved_blockers; NONE là mảng selected_packages rỗng. Python chỉ kiểm tra cấu trúc/kiểu dữ liệu, không đối chiếu applicability, sửa lựa chọn hoặc xây semantic router. Không chọn leaf, mở Requires closure, đọc package body, giải quyết Library/filesystem binding hoặc thực thi công cụ.

## Kiểm chứng tĩnh và hồi quy

- Baseline trước T3: `python -X utf8 -m unittest -v test_app` đạt 9/9.
- Sau T3: `python -X utf8 -m compileall -q app.py test_app.py test_t3.py` đạt; `python -X utf8 -m unittest -v test_app test_t3` đạt 14/14, gồm nguyên chín ca hồi quy T0/T1/T2 và năm ca T3. Chỉ thu hẹp vòng lặp regression `app.MODES` thành `app.MODES[:3]` vì T3 có hàm riêng; giữ nguyên các khẳng định cũ.
- Kiểm thử qua SDK thật với HTTP transport giả xác nhận mỗi request đọc lại đúng bốn control, không đọc package body hoặc bất kỳ path khác. Lượt thứ hai thay nội dung cả bốn control bằng dữ liệu có BOM/CRLF, xác nhận payload giữ nguyên nội dung và không cache.
- Payload chỉ gồm model, input, instructions, text và store; schema strict và `store=False` đúng. Không đưa lịch sử trước vào request T3.
- AppTest xác nhận JSON hợp lệ và NONE được hiển thị, có nhãn T3, không làm thay đổi messages/response_modes; chuyển T3 → T0 → T3 không đưa bản ghi T3 vào lời gọi thông thường hoặc đưa lịch sử T0 vào T3.
- JSON lỗi, sai root/field/kiểu, field thừa, refusal, incomplete, văn bản rỗng, output rỗng/null, content null hoặc text null đều báo lỗi rõ; không thêm bản ghi, giữ prompt và bản ghi thành công trước đó.
- Với từng CI/Router/Architecture/Catalog: FileNotFoundError, PermissionError, OSError và UTF-8 không hợp lệ đều dừng trước khi tạo client API, không gọi call_model và không fallback. AppTest tái hiện thiếu tệp/lỗi quyền cho cả bốn control, không tăng số request hoặc thay đổi trạng thái đã lưu.
- SHA-256 và tập đường dẫn toàn bộ 212 tệp upstream khớp snapshot trước T3; `git diff --exit-code -- upstream/` đạt. Technical runtime T2 vẫn byte-exact với nguồn promotion v1.0. Không chạy test/compileall trong upstream.
- `git diff --check` đạt. Các tệp app/tài liệu/kiểm thử được giải mã UTF-8; không đưa BOM vào tệp mới.

## SHA-256 bốn control đã dùng

Tất cả đường dẫn bên dưới thuộc `upstream/Central Hub/`; đây là hash của bytes thực tế, không phải văn bản đã ghép.

| Control | SHA-256 |
| --- | --- |
| HUB_CI_v1.1.md | `7bb946874663627060d28e47674decb07ba99f51acbffb6550db98d65746157b` |
| HUB_ROUTER_v1.1.yaml | `93318547108e0779a1812e5cd6c916302a52dda2a628334bdb75e07ccaae283c` |
| HUB_ARCHITECTURE_v1.8.md | `a1e5dc45ca816ec255454545b833879a35f72bf259da97837ed02fe908a2b91e` |
| HUB_PACKAGE_CATALOG_v1.8.yaml | `906558e2f033d40b1686aee6748d4a0006dbbf56b441528a797465c92379eea0` |

## Live T3: kết quả và phân loại

Codex trực tiếp chạy qua AppTest → app → SDK → OpenAI API thật → `gpt-5.6-sol`, dùng key trong config.json mà không in key. Mỗi ca có một AppTest session mới và đúng một prompt, không có lịch sử/previous_response_id. Prompt lấy từ tệp Python UTF-8, không truyền tiếng Việt inline qua PowerShell; xác nhận không chứa dấu `?` hoặc ký tự thay thế. Đã khôi phục dấu tiếng Việt trong bảy prompt bị mất dấu của yêu cầu ban đầu. Không truyền ảnh hoặc tuyên bố cụ thể vào F/G vì chỉ kiểm tra root routing.

Kỳ vọng được dùng làm giả thuyết để đối chiếu với Catalog; không đưa đáp án kỳ vọng vào request model.

| Ca | Giả thuyết | Root thực tế, lần chạy cuối | Nhận định từ lý do trả về |
| --- | --- | --- | --- |
| A — trò chuyện về thư mục cá nhân | NONE | NONE | Khớp: trò chuyện nhẹ, không cần đóng góp chuyên biệt. |
| B — giải thích RAM/SSD | NONE | NONE | Khớp: giải thích cơ bản, Catalog loại trừ trường hợp chỉ giải thích kỹ thuật đơn giản. |
| C — chẩn đoán máy khựng chưa có log | TECHNICAL | HUB-PKG-TECHNICAL | Khớp: cần suy luận cơ chế và phân biệt nguyên nhân khi chưa có dữ liệu. |
| D — audit thể chế thuế ký ức | CONCEPT-DEVELOPMENT | HUB-PKG-CONCEPT-DEVELOPMENT + HUB-PKG-TECHNICAL | Root Concept khớp trực tiếp; có lựa chọn bổ sung Technical cần đọc theo giới hạn dưới đây. |
| E — /AUTHOR CODEX | AUTHORING | HUB-PKG-AUTHORING | Khớp: dòng đầu không trống đúng chữ hoa, dấu cách và không có nội dung thừa. |
| F — tìm nguồn kiểm chứng | AIS | HUB-PKG-AIS | Khớp: yêu cầu rõ việc tìm và đối chiếu bằng chứng bên ngoài. |
| G — xóa vật thể trong ảnh | IMAGET | HUB-PKG-IMAGET | Khớp: yêu cầu chỉnh ảnh thực tế. |

Cả bảy ca lần cuối đều nhận bản ghi hợp lệ, hiển thị JSON đúng bản ghi đã phân tích, có nhãn T3, không có UI error/exception và không thêm messages thông thường. Đây là bằng chứng live cho chọn root và hiển thị, không chứng minh tuân thủ toàn bộ Hub.

Lịch sử chỉnh định dạng: lần live đầu cũng hoàn tất cả bảy ca và có cùng tập root như lần cuối. D/F/G dịch runtime_role thành `Điều khiển lĩnh vực`, `Hồ sơ suy luận`, `Quy trình công cụ` thay vì giữ định danh Catalog. Đã thêm đúng một mô tả cho trường runtime_role trong schema: `Exact runtime_role identifier from the root Catalog.`; không thay applicability, adapter hoặc thuật toán chọn. Sau đó chạy lại độc lập toàn bộ bảy ca. Các runtime_role ở lần cuối giữ đúng DOMAIN_CONTROL, REASONING_PROFILE, CAPABILITY và TOOL_PIPELINE. Hai lượt chạy là 14 request live; không phải 14 ca độc lập khác nhau.

Sai lệch/giới hạn còn lại:

- D chọn thêm Technical ở cả hai lần. Lý do lần cuối là lần theo cơ chế, nguyên nhân–hệ quả và vòng phản hồi. Catalog cho phép suy luận cơ chế xuyên chủ đề và Router chọn package set, không chọn duy nhất một winner, nên chọn thêm không tự chứng minh vi phạm. Tuy nhiên, lý do chưa làm rõ đóng góp riêng cần thiết ngoài Concept Development; phân loại là lựa chọn bổ sung có căn cứ applicability nhưng nguy cơ chọn thừa chưa được loại trừ. Không gắn PASS cho giả thuyết Concept-only, không sửa Python hoặc Router để ép kết quả.
- C ghi thiếu log và chưa áp dụng mô-đun trong unresolved_blockers dù việc chọn root đã hoàn tất. Đây là giới hạn độ chính xác về phạm vi của blocker: thiếu log ngăn kết luận nguyên nhân thực tế, không ngăn root selection. F/G vẫn định tuyến được khi thiếu tuyên bố/ảnh cụ thể; chúng chưa sẵn sàng cho thực thi, nhưng T3 không kiểm chứng mức sẵn sàng đó.
- Schema và kiểm tra Python chỉ bảo đảm cấu trúc; không chứng minh mọi ID/role/lý do đều đúng Catalog trong các request tương lai. Mô tả runtime_role đã cải thiện bảy ca quan sát, chưa chứng minh không bao giờ dịch sai. Không có semantic validator hoặc heuristic tự sửa route.
- Chưa kiểm tra thủ công trên trình duyệt; UI được kiểm tra bằng Streamlit AppTest. Không tuyên bố package retrieval, FULL_FILE, binding Library/local, module application, deployment hay tool execution. Không tải Technical/Concept/Authoring/AIS/ImageT body ở T3. Không bắt đầu T4.

## Bản ghi live lần cuối

Phần JSON sau giữ nguyên prompt, route record và kết quả hiển thị từ lần chạy cuối, gồm thời gian UTC và hashes. Các trường errors/exceptions rỗng là quan sát AppTest; không là bằng chứng thực thi package.

```json
{
  "started_utc": "2026-11-03T17:38:50.774854+00:00",
  "model": "gpt-5.6-sol",
  "controls_sha256": {
    "HUB_CI_v1.1.md": "7bb946874663627060d28e47674decb07ba99f51acbffb6550db98d65746157b",
    "HUB_ROUTER_v1.1.yaml": "93318547108e0779a1812e5cd6c916302a52dda2a628334bdb75e07ccaae283c",
    "HUB_ARCHITECTURE_v1.8.md": "a1e5dc45ca816ec255454545b833879a35f72bf259da97837ed02fe908a2b91e",
    "HUB_PACKAGE_CATALOG_v1.8.yaml": "906558e2f033d40b1686aee6748d4a0006dbbf56b441528a797465c92379eea0"
  },
  "cases": [
    {
      "case": "A",
      "prompt": "Tôi chỉ muốn trò chuyện một chút về cách tổ chức thư mục cá nhân.",
      "errors": [],
      "exceptions": [],
      "record": {
        "task_scope": "Trò chuyện nhẹ về cách tổ chức thư mục cá nhân; không cần phân tích cơ chế chuyên sâu, kiểm chứng bên ngoài, tạo ảnh hay dùng công cụ.",
        "selected_packages": [],
        "unresolved_blockers": []
      },
      "rendered_record_matches": true,
      "normal_history_empty": true
    },
    {
      "case": "B",
      "prompt": "Giải thích RAM và SSD khác nhau thế nào.",
      "errors": [],
      "exceptions": [],
      "record": {
        "task_scope": "Giải thích cơ bản sự khác nhau giữa RAM và SSD. Chỉ kiểm tra định tuyến đến cấp gói; không truy xuất hay áp dụng mô-đun.",
        "selected_packages": [],
        "unresolved_blockers": []
      },
      "rendered_record_matches": true,
      "normal_history_empty": true
    },
    {
      "case": "C",
      "prompt": "Máy tính thỉnh thoảng khựng 1-2 giây khi mở nhiều tab. Chưa có log hay số liệu. Hãy chẩn đoán nguyên nhân.",
      "errors": [],
      "exceptions": [],
      "record": {
        "task_scope": "Chẩn đoán hiện tượng máy tính thỉnh thoảng khựng 1–2 giây khi mở nhiều tab; hiện chưa có log hoặc số liệu nên cần giữ nhiều giả thuyết và phân biệt nguyên nhân bằng dấu hiệu hoặc phép đo.",
        "selected_packages": [
          {
            "package_id": "HUB-PKG-TECHNICAL",
            "entrypoint_module_id": "HUB-DOM-TECHNICAL",
            "runtime_role": "REASONING_PROFILE",
            "application_scope": "Lập các giả thuyết về CPU, RAM, bộ nhớ ảo, ổ đĩa, trình duyệt, tiện ích mở rộng hoặc tiến trình nền; xác định phép kiểm tra giúp phân biệt chúng.",
            "reason": "Yêu cầu là chẩn đoán cơ chế và phân biệt các nguyên nhân khi chưa có dữ liệu, khớp trực tiếp với phạm vi của gói Technical."
          }
        ],
        "unresolved_blockers": [
          "Chưa có log hoặc số liệu nên chưa thể kết luận nguyên nhân thực tế. Theo giới hạn mô phỏng, chưa truy xuất hay áp dụng mô-đun."
        ]
      },
      "rendered_record_matches": true,
      "normal_history_empty": true
    },
    {
      "case": "D",
      "prompt": "Audit tính nhất quán nhân quả của một thể chế hư cấu nơi ký ức bị đánh thuế.",
      "errors": [],
      "exceptions": [],
      "record": {
        "task_scope": "Kiểm toán tính nhất quán nhân quả của thể chế hư cấu trong đó ký ức bị đánh thuế; chỉ chọn gói ở cấp gốc, không truy xuất hay thực thi mô-đun.",
        "selected_packages": [
          {
            "package_id": "HUB-PKG-CONCEPT-DEVELOPMENT",
            "entrypoint_module_id": "HUB-DOM-CONCEPT-DEVELOPMENT",
            "runtime_role": "DOMAIN_CONTROL",
            "application_scope": "Phân tích tính nhất quán và quan hệ nhân quả của khái niệm thể chế hư cấu.",
            "reason": "Yêu cầu trực tiếp là kiểm toán nhân quả có giới hạn đối với một khái niệm hư cấu, khớp rõ với phạm vi của gói Concept Development."
          },
          {
            "package_id": "HUB-PKG-TECHNICAL",
            "entrypoint_module_id": "HUB-DOM-TECHNICAL",
            "runtime_role": "REASONING_PROFILE",
            "application_scope": "Lập luận theo cơ chế để phân biệt nguyên nhân, hệ quả và các vòng phản hồi trong thể chế.",
            "reason": "Việc kiểm toán nhân quả cần lần theo cơ chế và kiểm tra các quan hệ nguyên nhân–hệ quả, nên gói Technical có đóng góp độc lập, cụ thể."
          }
        ],
        "unresolved_blockers": []
      },
      "rendered_record_matches": true,
      "normal_history_empty": true
    },
    {
      "case": "E",
      "prompt": "/AUTHOR CODEX",
      "errors": [],
      "exceptions": [],
      "record": {
        "task_scope": "Mô phỏng định tuyến ở mức siêu dữ liệu cho yêu cầu có dòng đầu tiên không trống khớp chính xác `/AUTHOR CODEX`; chỉ thực hiện TASK_SCOPE và ROOT_PACKAGE_SELECTION.",
        "selected_packages": [
          {
            "package_id": "HUB-PKG-AUTHORING",
            "entrypoint_module_id": "HUB-CAP-AUTHORING",
            "runtime_role": "CAPABILITY",
            "application_scope": "Soạn nội dung cho đích CODEX theo kích hoạt chính xác `/AUTHOR CODEX`.",
            "reason": "Dòng đầu tiên do người dùng viết khớp chính xác điều kiện áp dụng của gói Authoring, gồm đúng chữ hoa, một dấu cách ASCII và không có nội dung thừa."
          }
        ],
        "unresolved_blockers": []
      },
      "rendered_record_matches": true,
      "normal_history_empty": true
    },
    {
      "case": "F",
      "prompt": "Tìm nguồn bên ngoài để kiểm chứng tuyên bố này.",
      "errors": [],
      "exceptions": [],
      "record": {
        "task_scope": "Tìm nguồn bên ngoài để kiểm chứng một tuyên bố; ở bước mô phỏng này chỉ chọn gói gốc, chưa có nội dung tuyên bố để thực hiện kiểm chứng.",
        "selected_packages": [
          {
            "package_id": "HUB-PKG-AIS",
            "entrypoint_module_id": "HUB-PIPE-AIS",
            "runtime_role": "TOOL_PIPELINE",
            "application_scope": "Tìm kiếm và đối chiếu bằng chứng bên ngoài cho tuyên bố được cung cấp.",
            "reason": "Yêu cầu nêu rõ việc tìm nguồn bên ngoài để kiểm chứng, khớp trực tiếp với phạm vi thu thập và xác minh bằng chứng của AIS."
          }
        ],
        "unresolved_blockers": []
      },
      "rendered_record_matches": true,
      "normal_history_empty": true
    },
    {
      "case": "G",
      "prompt": "Chỉnh ảnh này để bỏ vật thể ở nền.",
      "errors": [],
      "exceptions": [],
      "record": {
        "task_scope": "Chỉnh sửa ảnh để xóa một vật thể ở phần nền. Chỉ kiểm tra định tuyến đến bước chọn gói gốc; không truy xuất gói, áp dụng mô-đun hay thực thi công cụ.",
        "selected_packages": [
          {
            "package_id": "HUB-PKG-IMAGET",
            "entrypoint_module_id": "HUB-PIPE-IMAGET",
            "runtime_role": "TOOL_PIPELINE",
            "application_scope": "Chỉnh sửa ảnh thực tế để loại bỏ vật thể ở nền.",
            "reason": "Yêu cầu trực tiếp chỉnh sửa ảnh, khớp phạm vi của ImageT."
          }
        ],
        "unresolved_blockers": []
      },
      "rendered_record_matches": true,
      "normal_history_empty": true
    }
  ],
  "finished_utc": "2026-11-03T17:39:20.476519+00:00"
}
```

# Kết quả kiểm chứng T3 — kiểm tra định tuyến root package

Ngày kiểm chứng: 2026-11-04 (Asia/Ho_Chi_Minh). T3 tiếp tục từ T0/T1/T2 hiện có; không thay đổi bằng chứng cũ.

`T3 STATIC / LOCAL APP VERIFIED: PASS`

T3 thêm đúng một chế độ `T3 - Hub Routing Inspect`. Chế độ này chỉ dùng `eligibility.simulation` đã có trong Router để thực hiện `TASK_SCOPE` và `ROOT_PACKAGE_SELECTION`; dừng trước truy xuất package, đọc package body, áp dụng module hoặc gọi công cụ.

Mỗi request T3 đọc lại đúng bốn control active:

- `HUB_CI_v1.1.md` — SHA-256 `7bb946874663627060d28e47674decb07ba99f51acbffb6550db98d65746157b`
- `HUB_ROUTER_v1.1.yaml` — SHA-256 `93318547108e0779a1812e5cd6c916302a52dda2a628334bdb75e07ccaae283c`
- `HUB_ARCHITECTURE_v1.8.md` — SHA-256 `a1e5dc45ca816ec255454545b833879a35f72bf259da97837ed02fe908a2b91e`
- `HUB_PACKAGE_CATALOG_v1.8.yaml` — SHA-256 `906558e2f033d40b1686aee6748d4a0006dbbf56b441528a797465c92379eea0`

Sau bốn control là một adapter simulation tối thiểu bằng tiếng Anh, chỉ giới hạn output ở route inspection và cấm suy diễn retrieval/execution. Model vẫn quyết định package theo ngữ nghĩa; Python không dùng heuristic hoặc bảng luật để chọn package.

Responses API dùng Structured Outputs với JSON schema strict và `store=False`. Bản ghi chỉ có `task_scope`, `selected_packages` với Package ID / Entrypoint Module ID / Runtime role / application scope / reason, và `unresolved_blockers`. `selected_packages: []` biểu thị NONE.

Kiểm thử cuối:
- `python -X utf8 -m compileall -q app.py test_app.py test_t3.py`: đạt.
- `python -X utf8 -m unittest -v test_app test_t3`: 14/14 đạt ở lần chạy cuối.
- T0/T1/T2 regression tiếp tục đạt.
- T3 đọc đúng bốn control mỗi request và không đọc package body.
- Control thiếu/lỗi đọc/lỗi UTF-8: dừng trước API, không fallback.
- Phản hồi incomplete/refusal/không có text/JSON sai cấu trúc: không tạo route record.
- Route records nằm riêng, không làm bẩn history T0/T1/T2.
- Toàn bộ 212 tệp trong `upstream/` khớp snapshot trước/sau; `git diff --exit-code -- upstream/` đạt.
- Technical runtime T2 vẫn byte-exact với nguồn.
- `git diff --check` đạt.

`T3 LIVE ROOT ROUTING SMOKE: SCOPED PASS WITH ONE NON-EXCLUSIVE CASE`

Bảy request live độc lập được chạy bằng `gpt-5.6-sol`, mỗi case trong session mới và prompt UTF-8 sạch. Không package body hoặc tool nào được thực thi.

| Case | Prompt rút gọn | Kết quả root selection |
| --- | --- | --- |
| A | trò chuyện nhẹ về tổ chức thư mục | NONE |
| B | giải thích RAM và SSD | NONE |
| C | chẩn đoán máy khựng, chưa có log | `HUB-PKG-TECHNICAL` |
| D | audit nhân quả thể chế hư cấu | `HUB-PKG-CONCEPT-DEVELOPMENT` + `HUB-PKG-TECHNICAL` |
| E | `/AUTHOR CODEX` | `HUB-PKG-AUTHORING` |
| F | tìm nguồn bên ngoài để kiểm chứng | `HUB-PKG-AIS` |
| G | chỉnh ảnh bỏ vật thể nền | `HUB-PKG-IMAGET` |

A/B xác nhận baseline NONE và ranh giới Technical không tự kích hoạt cho giải thích kỹ thuật đơn giản. C/E/F/G khớp trực tiếp applicability của Root Catalog. Các bản ghi sau correction giữ đúng định danh `runtime_role` từ Catalog: `REASONING_PROFILE`, `DOMAIN_CONTROL`, `CAPABILITY`, `TOOL_PIPELINE`.

Case D không phải mismatch rõ ràng. Concept Development được chọn đúng cho bounded concept/causal audit. Technical cũng được model chọn với lý do lần theo cơ chế và quan hệ nguyên nhân-hệ quả; Router cho phép package set nhiều phần tử và Catalog mô tả Technical là reasoning profile xuyên chủ đề. Tuy nhiên, phép thử hiện tại chưa chứng minh Technical tạo đóng góp độc lập cần thiết ngoài trách nhiệm causal analysis đã có của Concept Development. Vì vậy D được giữ là `NON_EXCLUSIVE / NEED-NOT-ESTABLISHED`, không nâng thành failure và cũng không dùng để chứng minh Technical bắt buộc phải đồng chọn.

Giới hạn bằng chứng:

```text
T3 ROUTE API PATH
= VERIFIED

ROOT PACKAGE SELECTION
= SCOPED LIVE PASS FOR A/B/C/E/F/G
  + NON-EXCLUSIVE D OBSERVATION

PACKAGE RETRIEVAL
= NOT RUN

PACKAGE BODY APPLICATION
= NOT RUN

TOOL EXECUTION
= NOT RUN

LOCAL LIBRARY/FILESYSTEM BINDING MIGRATION
= NOT STARTED
```

T3 không tạo local Router/Catalog/Architecture successor, không sửa binding ChatGPT hiện tại và không bắt đầu T4.

# Kết quả kiểm chứng T4 — Concept Development core chọn thủ công

Ngày kiểm chứng: 2026-11-04 (Asia/Ho_Chi_Minh). Baseline trước T4 là commit \`476cf3a\` đã được push lên \`origin/main\`. T4 được triển khai local sau checkpoint đó; không stage, commit hoặc push T4 trong bước này.

\`T4 IMPLEMENTED / STATIC VERIFIED / LIVE BEHAVIOR OBSERVED\`

## Phạm vi triển khai

T4 thêm chế độ \`T4 - Hub CI + Concept Core\`. Đây là hiệu chuẩn chọn package thủ công, tương tự T2: \`HUB-PKG-CONCEPT-DEVELOPMENT\` được giả định đã được chọn cho phần yêu cầu hiện tại. Router không thực hiện package selection trong T4.

Mỗi request T4 đọc lại theo đúng thứ tự:

1. \`HUB_CI_v1.1.md\`
2. ghi chú liên kết T4 tối thiểu
3. \`HUB-DOM-CONCEPT-DEVELOPMENT_v1.1.md\`
4. \`HUB-CATALOG-CONCEPT-DEVELOPMENT_v1.1.yaml\`

Hai control Concept được sao chép nguyên byte vào \`runtime/packages/concept-development/\`. Không có body của Creative, Brainstorm, Debate hoặc anti-drift trong runtime T4. Ghi chú T4 không thay đổi semantics của core/Catalog, không mô phỏng Router và không tuyên bố Library retrieval hoặc migration binding.

SHA-256:

| Artifact | SHA-256 |
| --- | --- |
| Hub CI 1.1 | \`7bb946874663627060d28e47674decb07ba99f51acbffb6550db98d65746157b\` |
| Concept core 1.1 | \`b93c4b3045c5ce980fdc3157d01728f3bd650e0cc4e908c8f89fda3f8346a4b0\` |
| Concept local Catalog 1.1 | \`eaf480160e055ac7afc12ee4f8d511d09b6828abd14063d85ca571f5e6f03c07\` |

Runtime core và Catalog có cùng kích thước/hash với exact upstream ACTIVE sources tương ứng.

## Kiểm chứng tĩnh và hồi quy

- \`python -X utf8 -m compileall -q app.py test_app.py test_t3.py test_t4.py\`: PASS.
- \`python -X utf8 -m unittest -q test_app test_t3 test_t4\`: 20/20 PASS sau correction của một test UI; lỗi ban đầu chỉ do mock sai namespace AppTest, không phải runtime failure.
- T4 đọc lại CI/core/Catalog ở mỗi request và payload giữ đúng thứ tự byte.
- T4 thiếu tệp, lỗi quyền, I/O hoặc UTF-8: dừng trước API, không fallback T2/T1/T0.
- T0/T1/T2 không đọc Concept runtime; T3 vẫn chỉ đọc bốn control routing riêng và giữ route records tách khỏi history.
- \`runtime/packages/concept-development/\` chỉ có hai file core/Catalog; không có leaf body.
- Toàn bộ 212 tệp \`upstream/\` byte-identical trước/sau T4.
- \`git diff --exit-code -- upstream test_app.py test_t3.py\`: PASS.
- T5 không bắt đầu.

## Live T4 và đối chứng T1

Mỗi ca chạy trong AppTest session mới qua API thật với \`gpt-5.6-sol\`. Cùng năm prompt được chạy ở T4 và T1. Không có UI/API error hoặc exception.

| Ca | Quan sát T4 | Phân loại |
| --- | --- | --- |
| A — audit thể chế thuế ký ức | Giữ đúng audit; nêu lỗ hổng nhân quả, trade-off và dữ kiện thiếu; không sửa thiết kế hay biến giả định thành fact | PASS trong scope |
| B — phát triển hệ quả + feedback | Tách phần suy ra được khỏi nhánh đề xuất, phát triển hệ quả trực tiếp và vòng phản hồi | PASS trong scope |
| C — cụm tự nhiên “Brainstorm sâu…” | Tạo các nhánh/hệ quả như công việc concept thường; không tuyên bố \`HUB-CAP-BRAINSTORM\` được chọn hoặc áp dụng | PASS cho \`SEMANTIC FIT != LEAF ACTIVATION\` |
| D — span \`/BRAINSTORM ... #\` hợp lệ | Nhận diện đúng span nhưng báo specialized Brainstorm execution không thể thực hiện vì body leaf không được cung cấp; không emulation bằng core | PASS cho selection/block boundary |
| E — \`/CREATIVE ...\` thiếu \`#\` | Báo span chưa hợp lệ vì thiếu terminator; không implicit close, không thực thi Creative | PASS cho malformed-span boundary |

Đối chứng T1 có khác biệt material ở D/E: T1 không có Concept core/Catalog nên đã trực tiếp tạo nội dung brainstorm cho D và xây nghi lễ Creative cho E. Vì vậy việc T4 chặn D/E là hành vi quan sát được của control Concept được nạp, không phải hành vi baseline tự nhiên của cùng API trong các ca này.

Ở C, T4 vẫn tạo nhiều ý tưởng dù không kích hoạt leaf. Điều này phù hợp contract: core có thể làm sufficient ordinary unscoped concept work; natural-language “brainstorm” không tự cấp quyền cho specialized Brainstorm leaf. Live smoke này không chứng minh mọi prompt tự nhiên sẽ luôn phân biệt đúng.

## Giới hạn bằng chứng

\`\`\`text
T4 MANUAL CONCEPT HOST PATH
= VERIFIED

CONCEPT CORE + LOCAL CATALOG BYTE-EXACT RUNTIME COPIES
= VERIFIED

ORDINARY CORE AUDIT / CAUSAL DEVELOPMENT
= SCOPED LIVE PASS

EXPLICIT LEAF DETECTION + BLOCK WITHOUT BODY
= SCOPED LIVE PASS FOR BRAINSTORM

MALFORMED LEAF REJECTION
= SCOPED LIVE PASS FOR CREATIVE

SPECIALIZED LEAF EXECUTION
= NOT RUN

ROUTER-INTEGRATED PACKAGE RETRIEVAL
= NOT RUN

LOCAL LIBRARY/FILESYSTEM BINDING MIGRATION
= NOT STARTED

T5
= NOT STARTED
\`\`\`

---

## T5 — Concept Scoped Leaves (2026-11-04, Asia/Bangkok)

**IMPLEMENTED / STATIC PASS / LIVE MIXED.** Các mục T0–T4 phía trên giữ nguyên như bằng chứng lịch sử; dòng T5 NOT STARTED trước đó mô tả thời điểm kết thúc T4.

Baseline trước T5: repository `<LOCAL_REPO>`, nhánh `main`, HEAD `476cf3a282ddc951181a986e44e3ef7e76a79ae8`. Dirty baseline: `.gitattributes`, `README.md`, `VERIFICATION.md`, `app.py`; untracked `runtime/packages/concept-development/`, `test_t4.py`. Index trống. T4 được giữ tại chỗ; không stage/commit/push/tag/branch hoặc sửa remotes.

### Triển khai và ranh giới

Thêm nhãn UI `T5 - Concept Scoped Leaves`, dùng luồng trả lời `call_model` thông thường. Payload giữ nguyên byte UTF-8 theo thứ tự: CI 1.1 → adapter T5 tiếng Anh tối thiểu → Concept core 1.1 → Concept local Catalog 1.1 → Creative 1.1 → Brainstorm 1.1 → Debate 1.0. Mỗi request đọc lại đúng sáu tệp; không cache. Không có parser span, regex router, leaf detector, state machine hoặc heuristic trong Python. Core/Catalog giữ quyền nhận diện/chọn span.

T5 chọn thủ công `HUB-PKG-CONCEPT-DEVELOPMENT` cho phần yêu cầu hiện tại, với ba leaf khả dụng cục bộ; availability không phải activation. Không nạp anti-drift hoặc package body khác. Các entry anti-drift của Catalog vẫn INACTIVE. Đây không phải retrieval tích hợp Router, không mô phỏng Router và không migration ChatGPT Library resolution.

Creative/Brainstorm có bằng chứng binding Library cũ RESOLVED trong Catalog. Debate vẫn UNRESOLVED/NOT_PERFORMED ở host ChatGPT cũ. Bản Debate local được đối chiếu toàn bộ byte với upstream ACTIVE/1.0 và chỉ là **T5 local test binding only**. Không sửa Catalog, binding lịch sử hoặc nguồn upstream. Local byte verification không chứng minh Library retrieval.

### Kiểm chứng tĩnh

- Trước T5: 20/20 test T0–T4 PASS. Sau T5: `python -X utf8 -m unittest -q test_app test_t3 test_t4 test_t5`: **25/25 PASS**.
- Test T4 chỉ đổi kỳ vọng inventory thư mục từ hai sang năm tệp để phản ánh T5. Kiểm tra payload T4 vẫn giữ nguyên, xác nhận T4 chỉ đọc CI/core/Catalog.
- Ba runtime leaf byte-exact với upstream ACTIVE; core/Catalog của T4 không đổi. Inventory runtime Concept đúng năm tệp.
- Payload T5 so sánh byte đầy đủ và thứ tự đọc chính xác qua hai request, thay nội dung giữa request (cả BOM/CRLF), chứng minh đọc lại, không chuẩn hóa hoặc cache. Input control được chuyển nguyên vẹn tới model; Python không chọn leaf.
- 24 tổ hợp lỗi trên sáu tệp (missing, permission, I/O, invalid UTF-8): client API không được khởi tạo; history, response labels, route records và prompt giữ nguyên; không fallback T4/T2/T1/T0.
- T0–T4 không đọc ba leaf mới. T0/T1/T2/T4/T5 dùng chung history và nhãn UI; T3 vẫn JSON schema inspection, chỉ prompt hiện tại và route records riêng. Quay về T5 không nhận bản ghi T3 vào history.
- `python -X utf8 -m compileall -q app.py test_app.py test_t3.py test_t4.py test_t5.py sessions/run_t5_live.py`: PASS.
- `git diff --check`: PASS. `git diff --exit-code -- upstream test_app.py test_t3.py`: PASS.
- Đối chiếu manifest SHA-256 trước/sau: toàn bộ **212 tệp upstream byte-identical**; `.gitattributes`, `test_app.py`, `test_t3.py`, Technical runtime, Concept core/Catalog giữ nguyên so với baseline T5. Evidence T4 không bị ghi đè. Phần VERIFICATION trước mục T5 giữ nguyên byte.

SHA-256 của runtime và upstream tương ứng (nguồn: `upstream/Central Hub/library_modules/`; runtime: `runtime/packages/concept-development/`):

| Tệp | SHA-256 runtime | SHA-256 upstream |
| --- | --- | --- |
| HUB-DOM-CONCEPT-DEVELOPMENT_v1.1.md | b93c4b3045c5ce980fdc3157d01728f3bd650e0cc4e908c8f89fda3f8346a4b0 | b93c4b3045c5ce980fdc3157d01728f3bd650e0cc4e908c8f89fda3f8346a4b0 |
| HUB-CATALOG-CONCEPT-DEVELOPMENT_v1.1.yaml | eaf480160e055ac7afc12ee4f8d511d09b6828abd14063d85ca571f5e6f03c07 | eaf480160e055ac7afc12ee4f8d511d09b6828abd14063d85ca571f5e6f03c07 |
| HUB-DOM-CREATIVE_v1.1.md | 0430934d81b57743854543c52d9b78100d6209d8415a59c890e89f19296b4052 | 0430934d81b57743854543c52d9b78100d6209d8415a59c890e89f19296b4052 |
| HUB-CAP-BRAINSTORM_v1.1.md | 3758bf748ab11886656f0ea2a73472323301d14e7bf93bca5767079fea824843 | 3758bf748ab11886656f0ea2a73472323301d14e7bf93bca5767079fea824843 |
| HUB-CAP-DEBATE_v1.0.md | 430d1c01892c510e3d0c605654626b69202065a113e1fe4bf4c60da332ab0ddc | 430d1c01892c510e3d0c605654626b69202065a113e1fe4bf4c60da332ab0ddc |

### Live A–H

Chạy qua AppTest UI và API thật, model cấu hình `gpt-5.6-sol`, từ `2026-11-03T18:09:14Z` đến `18:10:49Z` (01:09–01:10 ngày 04/11 giờ local). Mỗi ca một session mới; G có hai lượt trong cùng session. Tổng 10 request: 9 request T5 và một đối chứng T4/A. Không UI/API error hoặc exception. Không thay model, tham số, nguồn hoặc adapter giữa các ca.

Prompt yêu cầu ban đầu bị mất dấu thành `?`; bản khôi phục tiếng Việt sạch UTF-8 lưu nguyên văn ở `sessions/t5_live_prompts.json`. Runner: `sessions/run_t5_live.py`; toàn bộ prompt, lỗi và history trả lời: `sessions/t5_live_results.json`. Chạy lại bằng `python -X utf8 sessions/run_t5_live.py` sẽ gọi API thật và ghi đè kết quả T5, cần sao lưu kết quả hiện tại trước nếu muốn giữ cả hai lần. Các tệp `sessions/` bị Git ignore theo chính sách sẵn có; bằng chứng này chỉ tồn tại local, không có tuyên bố đã commit.

| Ca | Kết quả | Bằng chứng và giới hạn |
| --- | --- | --- |
| A | PASS | Trước span audit cơ chế định giá/trích xuất; trong span đảo premise thành bắt buộc tiếp nhận ký ức, phát triển hệ quả bậc hai và feedback; sau span đánh giá điều kiện sinh học/pháp lý, không mở nhánh mới. T4/A nhận diện span nhưng chặn Brainstorm do thiếu body, không tạo nhánh. |
| B | PARTIAL | Creative tạo cảnh ga tàu; giữa hai span phân tích đơn vị tính, bảo lưu, quyền can thiệp. Debate không chạy: model nói “chưa có liên kết đọc đã được xác minh trong danh mục hiện tại”. Không kiểm chứng được consequential objection hoặc stopping của Debate. |
| C | PASS | Hai nhóm Brainstorm theo thứ tự, phần đầu có đúng hai nhánh phong tỏa ký ức/chuyển quyền sở hữu; giữa là ràng buộc xác minh; phần sau đảo tự nguyện thành tự động thế chấp. Không gộp hai span hoặc buộc nhánh sau phụ thuộc một kết quả cụ thể ở trước. |
| D | PASS | Báo `/DEBATE` xuất hiện trước khi `/CREATIVE` đóng, toàn bộ nhóm không hợp lệ; không dựng nghi lễ hoặc thực thi phản đối. Không có yêu cầu core độc lập để tiếp tục. |
| E | PASS | Phân biệt inline code và câu trích dẫn là dữ liệu; không đổi premise hoặc thêm cảnh. |
| F | PARTIAL | Không chạy Creative, không đóng span ngầm; nhưng đưa ví dụ đã bổ sung `#` dưới nhãn “Cú pháp đúng”. Không tự thực thi bản sửa, song chưa đạt yêu cầu nghiêm ngặt “no syntax repair” ở đầu ra. |
| G | FAILURE | Lượt 1 chặn Debate do Catalog “chưa phân giải”/chưa xác minh Library; lượt 2 làm core, phát triển chuỗi che giấu cảm xúc → định giá kém → giám sát. Không có Debate đã kích hoạt ở lượt 1 nên không thể kết luận no-persistence sau thực thi Debate là PASS. |
| H | PASS | Creative hiện thực nghi lễ đổi màu mắt, chi tiết màu/loại ký ức và hệ quả xã hội; không gọi hoặc tự chọn Brainstorm. Không có bước đổi premise vật chất được nêu rõ, nên nhánh xử lý conditional material change chưa bị thử mạnh bởi ca này. |

### Failures/partials và giới hạn

B/G cho thấy model vẫn ưu tiên yêu cầu Library verification và metadata Debate UNRESOLVED của core/Catalog/leaf hơn khai báo local availability trong adapter. Đây là diễn giải nguyên nhân dựa trên lời từ chối quan sát được, không phải bằng chứng truy cập nội bộ model. Local Debate body byte-exact đã được cung cấp nhưng **specialized Debate execution chưa được quan sát thành công**. Không sửa controls/adapter hoặc lịch sử binding để làm lại kết quả sau failure; cần ủy quyền riêng nếu muốn xử lý xung đột này.

F giữ đúng cổng không thực thi nhưng đưa ra cú pháp đã sửa; ghi PARTIAL thận trọng. Các PASS chỉ thuộc các prompt/lần chạy trên; không chứng minh toàn bộ module, mọi provenance/nesting case, Library binding, Router retrieval hoặc tính ổn định nhiều lần chạy. H chưa chứng minh xử lý mọi material premise change. Không thêm kiểm thử dựa trên khớp câu chữ để biến các giả thuyết hành vi thành PASS.

### Tệp và Git

T5 sửa `app.py`, `README.md`, append `VERIFICATION.md`, chỉnh duy nhất inventory assertion trong `test_t4.py`; thêm `test_t5.py` và ba runtime leaf. Bằng chứng local trong `sessions/`: runner, prompts, results, manifest baseline T5 và bản nội dung append này. `.gitattributes` cùng các thay đổi T4 khác được giữ lại. Git diff so với HEAD chứa cả T4 chưa commit và T5; không được diễn giải toàn bộ diff là riêng T5. Không stage, commit, push, tag, tạo branch hoặc sửa remotes. **STOP: T6 NOT STARTED.**

# Kết quả kiểm chứng T5 — Concept scoped leaves

Ngày kiểm chứng: 2026-11-04 (Asia/Ho_Chi_Minh). Baseline Git vẫn là commit `476cf3a` đã push trước T4. T4 và T5 đều còn là thay đổi local chưa stage/commit/push.

`T5 IMPLEMENTED / STATIC VERIFIED / LIVE PARTIAL WITH REPRODUCED DEBATE BINDING FAILURE`

## Phạm vi triển khai

T5 thêm chế độ `T5 - Concept Scoped Leaves`. Concept package vẫn được chọn thủ công để hiệu chuẩn; T3 Router không thực hiện retrieval/execution trong chế độ này.

Mỗi request T5 đọc lại đúng thứ tự:

1. `HUB_CI_v1.1.md`
2. adapter T5 local calibration tối thiểu
3. `HUB-DOM-CONCEPT-DEVELOPMENT_v1.1.md`
4. `HUB-CATALOG-CONCEPT-DEVELOPMENT_v1.1.yaml`
5. `HUB-DOM-CREATIVE_v1.1.md`
6. `HUB-CAP-BRAINSTORM_v1.1.md`
7. `HUB-CAP-DEBATE_v1.0.md`

Python không phân tích `/CREATIVE`, `/BRAINSTORM`, `/DEBATE`, dấu `#`, nesting, overlap hoặc provenance. Core/Catalog và model giữ toàn bộ semantics nhận diện/chọn span.

Ba leaf runtime là bản sao nguyên byte của nguồn ACTIVE:

| Artifact | SHA-256 |
| --- | --- |
| Concept core 1.1 | `b93c4b3045c5ce980fdc3157d01728f3bd650e0cc4e908c8f89fda3f8346a4b0` |
| Concept Catalog 1.1 | `eaf480160e055ac7afc12ee4f8d511d09b6828abd14063d85ca571f5e6f03c07` |
| Creative 1.1 | `0430934d81b57743854543c52d9b78100d6209d8415a59c890e89f19296b4052` |
| Brainstorm 1.1 | `3758bf748ab11886656f0ea2a73472323301d14e7bf93bca5767079fea824843` |
| Debate 1.0 | `430d1c01892c510e3d0c605654626b69202065a113e1fe4bf4c60da332ab0ddc` |

Creative và Brainstorm có binding ChatGPT Library cũ RESOLVED trong Catalog. Debate vẫn giữ đúng metadata lịch sử `resolution: UNRESOLVED`, `verification: NOT_PERFORMED`. T5 không sửa metadata này và không tuyên bố local copy đã biến thành ChatGPT Library binding.

## Kiểm chứng tĩnh và hồi quy

- `python -X utf8 -m compileall -q app.py test_app.py test_t3.py test_t4.py test_t5.py`: PASS.
- `python -X utf8 -m unittest -q test_app test_t3 test_t4 test_t5`: 25/25 PASS.
- T5 reread CI/core/Catalog/ba leaf mỗi request; không cache.
- Payload giữ nguyên byte và đúng thứ tự nêu trên.
- Mất file, lỗi quyền, I/O hoặc UTF-8 ở bất kỳ một trong sáu file đọc từ disk của T5: dừng trước API, không fallback, không làm đổi history/route records.
- T0–T4 không bắt đầu đọc ba leaf mới. T4 vẫn chỉ đọc CI/core/Catalog dù inventory runtime Concept đã có năm file.
- T3 vẫn là Structured Outputs route inspection riêng, không nhận T5 body.
- Không nạp anti-drift hoặc package khác.
- Toàn bộ 212 file `upstream/` không thay đổi.
- `git diff --check`: PASS.
- Không stage/commit/push T4/T5. T6 chưa bắt đầu.

## Live T5 — A đến H

Các prompt được lưu/đọc bằng UTF-8 sạch. Mỗi case dùng session mới, trừ G cố ý dùng hai lượt trong cùng session. Tất cả request live dùng `gpt-5.6-sol`; không có UI/API error.

| Case | Kết quả quan sát | Phân loại |
| --- | --- | --- |
| A — core → Brainstorm → core trong cùng turn | Phần trước span audit bằng core; span Brainstorm đảo premise sang thuế bắt buộc nhận thêm ký ức, theo second-order/feedback; sau `#` trở lại đánh giá causal bằng core | PASS |
| B — Creative → core → Debate | Creative dựng cảnh hoạt động; phần giữa core audit hoạt động; Debate bị chặn vì Catalog vẫn ghi Debate Library binding UNRESOLVED/NOT_PERFORMED | PARTIAL / REPRODUCED BINDING FAILURE |
| C — hai Brainstorm span tách nhau | Hai span được thực hiện riêng theo thứ tự; phần giữa là ràng buộc core; span thứ hai đảo giả định tự nguyện mà không bị nhập vào span đầu | PASS |
| D — opener lồng/đè | `/DEBATE` xuất hiện trước khi `/CREATIVE` đóng; model từ chối toàn nhóm và không chạy leaf nào | PASS |
| E — control nằm trong code/quote | Cả Brainstorm và Creative được nhận là dữ liệu/literal, không phải directive; không leaf nào chạy | PASS |
| F — Creative thiếu `#` | Không chạy Creative và không tự đóng cuối turn; nhưng phản hồi đưa ra một ví dụ cú pháp đã thêm `#` | PARTIAL |
| G — Debate rồi lượt sau core | Lượt 1 Debate bị chặn bởi cùng metadata UNRESOLVED; lượt 2 chạy core bình thường. Vì Debate chưa từng thực thi, chưa chứng minh được no-persistence sau một Debate thành công | PARTIAL / BLOCKED |
| H — Creative không tự gọi Brainstorm | Creative hiện thực hóa nghi lễ đổi màu mắt; không mở Brainstorm hoặc biến nó thành pipeline; không thấy activation ngoài span | PASS trong scope |

Đối chứng T4 cho case A tiếp tục chặn Brainstorm vì T4 không cung cấp leaf body. T5 cùng prompt đã thực thi Brainstorm thật rồi trở lại core. Đây là bằng chứng scoped rằng việc thêm leaf body local thay đổi đúng phần được cấp phép, không biến Brainstorm thành mode toàn turn.

## Failure quan trọng: Debate

B và G tái hiện cùng một failure:

```text
LOCAL DEBATE BODY
= PRESENT
= BYTE-EXACT ACTIVE/1.0 SOURCE

OLD CHATGPT LIBRARY METADATA
= UNRESOLVED
= NOT_PERFORMED

MODEL RESULT
= REFUSES DEBATE EXECUTION
```

Đây là `REPRODUCED FAILURE` của **host-binding migration path**, không phải bằng chứng Debate logic sai. Core yêu cầu selected leaf phải qua xác minh identity/FULL_FILE dưới binding hiện hành; Catalog vẫn mô tả host ChatGPT cũ. Adapter T5 cố ý không được phép viết lại trạng thái đó, nên model giữ Catalog làm authority và chặn execution.

T5 không sửa failure này. Việc giải quyết cần một bước binding local có thẩm quyền riêng; không được ngầm biến local file presence thành Library verification.

## Giới hạn và trạng thái

```text
T5 HOST PAYLOAD PATH
= VERIFIED

CREATIVE LOCAL SCOPED EXECUTION
= SCOPED LIVE PASS

BRAINSTORM LOCAL SCOPED EXECUTION
= SCOPED LIVE PASS

SPAN ORDER / EXIT / REPEAT
= SCOPED LIVE PASS

NESTED / LITERAL / UNCLOSED CONTROL HANDLING
= PASS EXCEPT F WORDING PARTIAL

DEBATE LOCAL SCOPED EXECUTION
= BLOCKED
= REPRODUCED HOST-BINDING FAILURE

DEBATE NO-PERSISTENCE AFTER SUCCESSFUL EXECUTION
= NOT ESTABLISHED

ROUTER-INTEGRATED LOCAL RETRIEVAL
= NOT RUN

LOCAL LIBRARY/FILESYSTEM BINDING MIGRATION
= NOT STARTED

T6
= NOT STARTED
```

# T6 — Concept + Technical Composition: kiểm chứng tĩnh

Ngày: 2026-11-04. `T6 IMPLEMENTED / STATIC VERIFIED / LIVE NOT RUN`.
Baseline: `main`, HEAD `476cf3a282ddc951181a986e44e3ef7e76a79ae8`; T4/T5 đã có sẵn và cố ý chưa stage/commit. Nội dung phía trên là bằng chứng lịch sử tại thời điểm T6 chưa bắt đầu; mục này ghi trạng thái T6 mới.

T6 thêm lựa chọn `T6 - Concept + Technical Composition` vào đường trả lời thông thường. Mỗi request đọc lại bảy tệp UTF-8, không cache, ghép nguyên byte theo thứ tự:

1. `upstream/Central Hub/HUB_CI_v1.1.md`
2. adapter T6 tối thiểu bằng tiếng Anh
3. `runtime/packages/technical/HUB-DOM-TECHNICAL_v1.0.md`
4. `runtime/packages/concept-development/HUB-DOM-CONCEPT-DEVELOPMENT_v1.1.md`
5. `runtime/packages/concept-development/HUB-CATALOG-CONCEPT-DEVELOPMENT_v1.1.yaml`
6. `runtime/packages/concept-development/HUB-DOM-CREATIVE_v1.1.md`
7. `runtime/packages/concept-development/HUB-CAP-BRAINSTORM_v1.1.md`
8. `runtime/packages/concept-development/HUB-CAP-DEBATE_v1.0.md`

Adapter chỉ thiết lập điều kiện phối hợp thủ công và ranh giới trách nhiệm; không viết lại quy tắc chi tiết của module. Python chỉ nạp tệp, gọi API, dùng history hiện có và xử lý lỗi; không thêm semantic router, classifier, splitter, span parser, detector, authority resolver, dependency solver, state machine hoặc heuristic. Không có framework eval mới.

Kiểm chứng đã thực hiện:

- Baseline T0–T5: `python -X utf8 -m unittest -q test_app test_t3 test_t4 test_t5`: **25/25 PASS**.
- Sau T6: `python -X utf8 -m unittest -q test_app test_t3 test_t4 test_t5 test_t6`: **29/29 PASS**; API được mock, không phát sinh request live.
- Payload T6 được so sánh toàn bộ nội dung và thứ tự qua hai request; thay nội dung cả bảy tệp giữa request, gồm BOM/CRLF, xác nhận đọc lại và không chuẩn hóa byte. Input/history được chuyển nguyên vẹn, kể cả control literal hoặc malformed; test không diễn giải semantics của chúng.
- Theo dõi chính xác read set T6: chỉ bảy tệp nêu trên; không đọc Router, Architecture, Root Catalog, Authoring, AIS, ImageT, anti-drift hoặc package body khác.
- 28 tổ hợp lỗi (missing, permission, I/O, invalid UTF-8 trên từng tệp): dừng trước khởi tạo client API, không fallback; giữ nguyên history, response labels, route records và prompt UI.
- Read set T0–T5 giữ nguyên. T3 tiếp tục Structured Outputs `json_schema`, chỉ prompt hiện tại, route records riêng; chuyển T6 → T3 → T6 không đưa bản ghi T3 vào history thường. Nhãn T6 hiển thị đúng, không gửi vào API.
- `python -X utf8 -m compileall -q app.py test_app.py test_t3.py test_t4.py test_t5.py test_t6.py`: PASS.
- `git diff --check`: PASS.
- Manifest SHA-256 đầu/cuối T6: 223 tệp được bảo vệ không đổi, gồm toàn bộ **212 tệp upstream**, sáu tệp runtime, `.gitattributes` và bốn test T0–T5. Không thêm package body hay tệp runtime mới. Phần VERIFICATION có trước T6 được giữ nguyên byte.

Blocker được giữ nguyên:

- Debate local body vẫn hiện diện và byte-exact; Catalog vẫn `UNRESOLVED / NOT_PERFORMED` cho binding ChatGPT Library cũ. T6 không sửa hoặc vượt qua binding; Debate có thể tiếp tục bị chặn. Failure T5 vẫn là bằng chứng trong phạm vi đã ghi.
- **Authoring cố ý bị loại khỏi T6 do binding host cũ hiện còn `UNRESOLVED / NOT_PERFORMED`**. Không nạp, thêm body, mô phỏng hoặc tuyên bố thực thi Authoring. Theo Architecture, blocker này chỉ chặn công việc phụ thuộc Authoring, không chặn Hub độc lập.
- Đây là hiệu chuẩn phối hợp thủ công, không phải Router-integrated composition/retrieval hoặc local Library binding migration. Chưa kiểm chứng live về phạm vi trách nhiệm trong cùng request/qua lượt, authority bleed, premature convergence hay leaf persistence. Live campaign UTF-8 sẽ do ChatGPT giám sát chạy riêng; Codex không chạy prompt live tiếng Việt hoặc ASCII smoke trong T6.

T6 thay đổi `app.py`, `README.md`, append `VERIFICATION.md`, thêm `test_t6.py`. Diff so với HEAD còn bao gồm T4/T5 có sẵn; không được quy toàn bộ diff cho T6. Không stage, commit, push, tag, tạo branch hoặc thay remotes.

**STOP: T7 NOT STARTED.**

# T6 — kiểm chứng live composition

Phần này cập nhật trạng thái LIVE NOT RUN của mục T6 tĩnh ngay phía trên. Campaign live được chạy sau khi Codex đã dừng, bằng prompt UTF-8 sạch và AppTest qua API thật với gpt-5.6-sol.

T6 LIVE COMPOSITION: SCOPED PASS

Tổng cộng 11 request live:
- 9 request T6: A–F, H một lượt; G hai lượt trong cùng session.
- 1 đối chứng T5/A.
- 1 đối chứng T2/A.
Không có UI error, API error hoặc exception.

| Case | Quan sát | Phân loại |
| --- | --- | --- |
| A — premise hư cấu khóa + audit thể chế + chẩn đoán tải cao | Giữ nguyên premise “sao chép, không xóa”; tách audit thể chế khỏi các giả thuyết kỹ thuật; không xếp hạng nguyên nhân khi chưa có log; không dùng kỹ thuật để sửa canon | PASS về composition boundary |
| B — lỗi kỹ thuật chưa xác nhận → hệ quả thể chế có điều kiện | Giữ cảm biến/bộ đệm/lưu trữ là giả thuyết cạnh tranh; đưa phép kiểm tra phân biệt; chỉ phát triển hệ quả thể chế dưới điều kiện lỗi thật sự được xác nhận; không nâng chẩn đoán thành fact của thế giới | PASS |
| C — Brainstorm span xen chẩn đoán kỹ thuật | Brainstorm tạo hai nhánh đảo premise; sau # chuyển sang đánh giá tải thiết bị, giữ nhiệt/nhiễu là giả thuyết chưa xác định và không chọn nhánh nào làm thiết kế chính thức | PASS |
| D — Creative span rồi audit kỹ thuật | Creative dựng cảnh; sau span phân biệt rõ chi tiết mà cảnh đã thiết lập với cơ chế kỹ thuật chưa có bằng chứng; không viết lại cảnh để “sửa” kỹ thuật | PASS |
| E — chỉ audit chính danh xã hội | Dù Technical body hiện diện, phản hồi chỉ làm Concept work về chấp nhận/phản đối/vòng phản hồi chính trị; không tự mở chẩn đoán máy móc | PASS cho no Technical bleed |
| F — chỉ chẩn đoán máy tính thật | Phản hồi chỉ làm chẩn đoán kỹ thuật và phép kiểm tra phân biệt; không kéo worldbuilding/Concept vào task | PASS cho no Concept bleed |
| G — Brainstorm ở lượt 1, đổi hẳn sang PC diagnosis ở lượt 2 | Lượt 1 thực thi Brainstorm; lượt 2 bỏ hẳn worldbuilding/Brainstorm và làm Technical diagnosis | PASS cho no leaf/package persistence qua lượt |
| H — axiom hư cấu khóa + bottleneck kỹ thuật quy mô thành phố | Ghi rõ axiom là premise hư cấu đã khóa, không dùng vật lý đời thực để bác bỏ; đồng thời tách các nút thể chế khỏi các giả thuyết kỹ thuật chưa có số liệu | PASS mạnh cho authority boundary |

## Đối chứng A: T6 so với T5 và T2

Cùng prompt A được chạy trong session mới ở T6, T5 và T2.

- T6 thực hiện đầy đủ cả audit thể chế và chẩn đoán tải cao, giữ hai loại trạng thái tách biệt.
- T5, dù không nạp Technical, vẫn tự làm được phần lớn chẩn đoán cơ chế tải cao.
- T2, dù không nạp Concept package, vẫn tự làm được phần lớn audit thể chế.

Do đó campaign này không xác lập rằng việc nạp hai package tạo ra một năng lực mà model/Hub CI vốn không có. Nó xác lập điều hẹp hơn nhưng quan trọng cho Central Hub: khi cả hai package cùng hiện diện, model không quan sát thấy authority bleed, package domination hoặc tự biến availability thành global mode trong các ca đã thử.

MULTI-PACKAGE COEXISTENCE = SCOPED LIVE PASS
TECHNICAL → FICTIONAL CANON AUTHORITY BLEED = NOT OBSERVED
CONCEPT → TECHNICAL FACT/DIAGNOSIS OVERRIDE = NOT OBSERVED
LEAF PERSISTENCE ACROSS # = NOT OBSERVED
LEAF / CONCEPT PERSISTENCE ACROSS DOMAIN-SWITCH TURN = NOT OBSERVED
PACKAGE AVAILABILITY → FORCED APPLICABILITY = NOT OBSERVED
ADDED CAPABILITY OF T6 OVER T2/T5 = NOT ESTABLISHED

## Blocker vẫn giữ nguyên

T6 không chạy Debate và không sửa metadata Debate. Failure T5 vẫn giữ nguyên: local Debate body có mặt và byte-exact nhưng old-host Catalog binding vẫn UNRESOLVED / NOT_PERFORMED.

Authoring tiếp tục cố ý không được nạp trong T6 vì Root Catalog/Architecture hiện coi binding Authoring old-host là unresolved. Không có bằng chứng T6 nào nâng Authoring hoặc Debate thành resolved.

T6 STATIC = 29/29 PASS
T6 LIVE = SCOPED PASS A–H
ROUTER-INTEGRATED PACKAGE SELECTION/RETRIEVAL = NOT RUN
LOCAL HOST-BINDING SUCCESSOR = NOT IMPLEMENTED
T7 = NOT STARTED
