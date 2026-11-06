# Kết quả kiểm chứng Giai đoạn 1

> Các đường dẫn máy trong hồ sơ và log đính kèm đã được thay bằng ký hiệu trung tính. Kết quả kỹ thuật, revision, workload và phạm vi kiểm chứng giữ nguyên. Các PASS lịch sử không xác nhận live cho nguồn 1.10.


## Closeout GPT-6.1 Sol — 2026-11-05

**GPT-6.1 Sol = LIVE VERIFIED CANDIDATE FOR TESTED CENTRAL HUB W1/W2 SCOPE**; không phải replacement đã kiểm chứng toàn cục cho mọi đường Central Hub.

- Review lại evidence local đã có: W1 **7/7 completed, semantic PASS** trong phạm vi Authoring + Concept; W2 **4/4 completed, semantic PASS** trong phạm vi Technical + Concept + AIS. Không chạy lại live trong closeout.
- Explicit Concept cache: W1 write **6161**, W2 cached **6161**; blocker rỗng, không target execution trong phạm vi thử.
- Config local được ignore và toàn bộ response xác nhận `gpt-6.1-sol`: đây là model hiện cấu hình/ưu tiên cho thử nghiệm và runtime local, không phải quyết định kiến trúc MCP/kênh tương lai.
- Theo snapshot giá lưu cùng phép thử: tổng pair **$0.5063505 ≈ $0.506351**, gồm web search; so với GPT-5.6 Sol M3 retry **$0.914486**, thấp hơn **44,63% trên đúng hai workload**. Không suy rộng tiết kiệm hoặc quy toàn bộ chênh lệch cho model/cache.
- AIS **evidence-source compliance PASS**, **search-discovery boundary PARTIAL**: discovery có nguồn ngoài Tauri; evidence/citations sử dụng nguồn Tauri chính thức. Không kết luận AIS thất bại toàn cục.
- Tương thích model trong phạm vi đã thử không chứng minh khả năng chuyển model cho toàn hệ thống. Giữ nguyên mọi provenance GPT-5.6 Sol lịch sử, gồm hồ sơ M3 bên dưới. **M4 NOT STARTED**; không triển khai MCP.

Review, hash raw evidence, phép tính và kiểm chứng closeout: [GPT61_W1_W2_REVIEW.md](m3_evidence/GPT61_W1_W2_REVIEW.md). Raw sessions/config giữ local và được ignore, không commit key.

## M3 explicit-cache completion — 2026-11-05

- **CENTRAL HUB LOCAL/API: BACKUP — VERIFIED + LIVE VERIFIED.**
- Người dùng mở lại M3 sau khi tăng project spend limit; không mở M4.
- Experiment 1 giữ nguyên **FAILED TARGET**.
- Experiment 2 explicit Concept cache: **STATIC VERIFIED + LIVE VERIFIED / TARGET ACHIEVED**. Retry W1 hoàn tất 7/7 Responses calls; W2 hoàn tất 4/4; không retry.
- W1 Concept ghi 6.161 cache-write tokens cho stable prefix; W2 Concept đọc lại 6.161 cached tokens.
- Concept combined input billing giảm từ **$0.100224** baseline xuống **$0.0619934**, tiết kiệm **$0.0382306 / 38.145%** tại đúng bucket được tối ưu.
- Retry pair token cost là **$0.874486**; 4 web-search actions thêm **$0.04**, tổng ước tính **$0.914486**. Không dùng whole-pair delta làm causal savings vì W1 cache warmth, output và AIS/search thay đổi giữa các lần chạy.
- Scoped M2 semantics giữ nguyên trong live retry: W1 Authoring GENERIC + BRAINSTORM, W2 Technical + Concept + AIS; Concept chỉ chọn Brainstorm, blocker rỗng, không target execution.
- Candidate explicit 30m Concept breakpoint/key được promote local. Không thêm prewarm, retry, call merge, model/reasoning/verbosity change hoặc experiment thứ ba.
- Candidate lịch sử có chuỗi lỗi T7 sai ở nhánh Concept validation; promotion sửa wording này thành lỗi T8/Concept phù hợp mà không đổi validation/failure behavior.
- **M3 TOKEN/CACHE OPTIMIZATION: COMPLETE FOR ACCEPTED SCOPE. M4: NOT STARTED.**

Bằng chứng: [M3_FINAL_STATUS.md](m3_evidence/M3_FINAL_STATUS.md), [EXPERIMENT_2_RETRY_REVIEW.md](m3_evidence/EXPERIMENT_2_RETRY_REVIEW.md), [explicit_retry_metrics.json](m3_evidence/explicit_retry_metrics.json), [explicit_retry_workload_1.json](m3_evidence/explicit_retry_workload_1.json), [explicit_retry_workload_2.json](m3_evidence/explicit_retry_workload_2.json).

Các file review trước retry vẫn là bằng chứng lịch sử của checkpoint quota-blocked; các claim `M3 NOT COMPLETE` / `LIVE NOT ESTABLISHED` trong chúng không phải trạng thái hiện hành sau retry.

## M2 — Authoring 0.7 source isolation, 2026-11-05

Checkpoint trước mutation: repo `<LOCAL_REPO>`, branch `main`, worktree/index sạch, `HEAD=origin/main=c619a5a6895cf0d9aa67a92ebb46f36a8bb9e228` (`Complete local runtime M1 and M2 acceptance`). Người dùng đã cho phép candidate live, promotion có điều kiện, stage, commit và push trong M2. Không tạo branch/tag; không bắt đầu M3/M4.

### CANDIDATE LIVE PASS

Chạy trước mọi active mutation, đúng I1 và I3 từ `ISOLATION_TEST_CASES.json`; mỗi ca một Responses API call, `max_retries=0`, không tools. Controls gồm nguyên Hub CI 1.1, candidate Catalog 1.9-candidate và Authoring 0.7-candidate. Prior chat/project context nằm trong lịch sử nền; current request giữ nguyên và không chứa canary. Không gửi reference_output, required, forbidden hoặc expected checks cho model.

- I1: prompt so sánh cedar/ash chỉ dùng số đo được cung cấp, giữ chưa chọn phương án, không bịa số đo; không GOLD/CANARY_LEDGER/CANARY_PROJECT.
- I3: một yêu cầu làm rõ nguồn quyết định kiến trúc bằng cách cung cấp hoặc định danh duy nhất tài liệu truy cập được, đặc biệt giao diện lưu trữ; không CANARY_POSTGRES/CANARY_FILES và không đoán quyết định.

Bằng chứng đầy đủ: [candidate_I1.json](m2_evidence/authoring_0_7/candidate_I1.json), [candidate_I3.json](m2_evidence/authoring_0_7/candidate_I3.json). Có toàn payload/response, hash controls/input/output, model, SDK, versions, thời gian và semantic review; không dùng khớp câu chữ đáp án mẫu để chấm output tiếng Việt.

### Promotion và STATIC/SPEC PASS

Authoring ACTIVE/0.7 giữ nguyên module/package/runtime role. Body giống candidate đã thử live; bỏ mục source isolation mới thì phần hành vi kế thừa giống nguyên 0.6. Catalog 1.9 thêm đúng cú pháp isolated; Architecture 1.9 và pin Router cần cập nhật vì hợp đồng yêu cầu exact stack pins. CI và thuật toán Router không đổi. Không thêm context engine, registry, parser hoặc Router axis.

Binding v0.2 (T8 diagnostic) và v0.3 (M1 runtime) cùng đổi sang module 0.7 byte-exact; hash shared-package pin của T9 được cập nhật. Không đổi AIS entries. `ADMISSION_SCHEMA` có `isolated:boolean`; model sở hữu lexical admission, Python chỉ kiểm tra kiểu/tổ hợp và truyền trace/handoff. inactive hoặc contributor != NONE buộc isolated=false; preset P1/P2/P3 được đi cùng isolated. Không strip history ở Python.

- Full Central-Hub-Local: **117/117 PASS**, `socket.socket.connect` bị chặn toàn cục.
- Focused upstream candidate + m1 + m2 + m4 + isolation: **33/33 PASS**, gồm isolation **8/8**. Tests lịch sử 0.6/1.8 dùng snapshot archive; active equivalents nằm trong `test_authoring_07.py`. Candidate source/fixtures không sửa.
- Compile toàn bộ **59 file Python**: PASS. `git diff --check`: PASS.
- Static/mock phủ exact activation, preset+isolated, malformed/unsupported forms, no-suffix false, no persistence sau clarification/reauthor, impossible combinations, genuine blockers, giữ history, source-boundary handoff và no-target execution. Các ca này không chứng minh model tuân thủ mọi dạng cú pháp trong live.
- Đối chiếu toàn bộ 208 file upstream tại checkpoint với allowlist promotion cụ thể: PASS; ImageT, candidate và package ngoài Authoring không đổi. Các predecessor bị thay thế được archive byte-exact, có receipt/hash. Test cũ “mọi upstream file giống HEAD” được thay bằng kiểm tra baseline cố định để cho phép đúng promotion đã duyệt, vẫn kiểm mọi file ngoài scope.

Chi tiết: [static_summary.json](m2_evidence/authoring_0_7/static_summary.json), [local_static.txt](m2_evidence/authoring_0_7/local_static.txt), [focused_upstream.txt](m2_evidence/authoring_0_7/focused_upstream.txt). Các mismatch static ban đầu do kỳ vọng revision cũ đã được sửa trong phạm vi; log ban đầu giữ riêng, không phải kết quả nghiệm thu cuối.

Giới hạn mirror-wide upstream được người dùng cung cấp trước: thiếu original git-history objects và Project Feather files. Đây là giới hạn môi trường mirror, tách khỏi Authoring 0.7. Không chạy lại toàn suite upstream trong lượt promotion; không suy full upstream PASS từ focused PASS.

### ACTIVE LOCAL RUNTIME LIVE PASS

Chỉ chạy sau static gate PASS, dùng đúng current turn do người dùng chỉ định. Lịch sử nền chứa `CANARY_ACTIVE_PRIOR` và quyết định giả định đã chấp nhận cloud notebooks, loại giấy. Không xóa lịch sử ở bất kỳ pha nào.

Đúng **một top-level request**, **3 Responses API calls**, tất cả completed, `max_retries=0`, không tools và không target execution. Root chỉ chọn HUB-PKG-AUTHORING; admission/handoff ghi `isolated=true`; trace `authoring_isolated=true`, target GENERIC, preset/contributor NONE; blocker rỗng. Module runtime được đọc và SHA-256 verified. Prompt cuối chỉ so sánh giấy/văn bản thuần túy, giữ cả hai chưa quyết định, không nhập canary hoặc quyết định cũ. Không thực thi so sánh thay cho việc tạo prompt.

Bằng chứng: [active_runtime.json](m2_evidence/authoring_0_7/active_runtime.json), có đầy đủ inputs/outputs của cả ba pha, hashes, versions và trace. Tổng phần Authoring 0.7 trong lượt này: **5 Responses API calls**, gồm hai candidate cases và một active top-level request; **0 retry**, không live attempt bổ sung.

`STATIC/SPEC PASS != CANDIDATE LIVE PASS != ACTIVE LOCAL RUNTIME LIVE PASS`. Kết quả chỉ xác minh phạm vi đã chạy, không chứng minh ChatGPT Library installation/retrieval hoặc Project deployment. Các bằng chứng M1/M2 trước đây được giữ nguyên. Commit/push promotion được thực hiện sau khi kiểm tra staged snapshot; hash commit và trạng thái remote được báo ở kết quả tác vụ.

---

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


# T7 — Router Local Retrieval: kiểm chứng tĩnh

Ngày: 2026-11-04. Baseline: `main` sạch tại `8f402ebcb6845f0a8f0b0d080824c0ada94a85fc`.

`T7 IMPLEMENTED / STATIC VERIFIED / LIVE NOT RUN`

T7 thêm luồng trả lời thường gồm ba pha model: chọn root qua Structured Outputs từ nguyên nội dung CI 1.1 / Router 1.1 / Architecture 1.8 / Root Catalog 1.8 / manifest local; chọn leaf qua Structured Outputs chỉ khi Concept đã được chọn và interface đã đọc đủ; trả lời từ các artifact đã chọn và xác minh. Mọi pha dùng cùng model/config, toàn bộ history thường hiện tại, `store=False`, không retry. Python không phân loại prompt, chia task, phân tích control span hoặc quyết định applicability.

Manifest duy nhất `runtime/HUB_LOCAL_BINDINGS_v0.1.json` khai báo `LOCAL_RUNTIME_FILE`, Technical 1.0 và năm artifact Concept: core/Catalog/Creative/Brainstorm 1.1, Debate 1.0. Mỗi artifact khai báo identity/role/version, đường dẫn tương đối và SHA-256. JSON được dùng để consumer Python đọc bằng thư viện chuẩn, tránh thêm PyYAML; không phải thay đổi sở thích kiến trúc hay package manager.

Binding kế nhiệm local chỉ đổi binding lưu trữ/truy xuất. Metadata ChatGPT Library cũ được giữ nguyên, không viết lại hoặc tuyên bố đã xác minh Library. Failure Debate của T5 vẫn là bằng chứng lịch sử trong đúng phạm vi T5; T7 dự kiến được thử live riêng để xác định binding kế nhiệm local có giải quyết việc truy xuất/thực thi Debate hay không. Kiểm thử tĩnh chỉ chứng minh body Debate được chọn, hash-verify và chuyển vào payload dù Catalog vẫn giữ `UNRESOLVED / NOT_PERFORMED`; chưa chứng minh model thực thi Debate thành công.

Authoring/AIS/ImageT vẫn chưa có binding T7. Chọn các package đó tạo blocker phần chuyên biệt và không đọc body/fallback/mô phỏng; các phần Technical, Concept hoặc baseline độc lập vẫn có thể tiếp tục. Thiếu/sai control hoặc config dừng trước API. Lỗi tệp đã chọn, UTF-8, SHA-256 hoặc đường dẫn thoát runtime chặn phần phụ thuộc; core/Catalog lỗi chặn lựa chọn leaf phụ thuộc. Kết quả Structured Outputs sai cấu trúc dừng lượt, không đoán/thử lại. Lượt thất bại toàn bộ không thay đổi history, nhãn hoặc bản ghi T3.

Bằng chứng tĩnh:

- 29 kiểm thử T0–T6 giữ nguyên; thêm 18 kiểm thử T7 bằng HTTP transport giả lập, không chi API credit.
- `python -X utf8 -m unittest -q test_app test_t3 test_t4 test_t5 test_t6 test_t7`: **47/47 PASS**.
- `python -X utf8 -m compileall -q app.py test_app.py test_t3.py test_t4.py test_t5.py test_t6.py test_t7.py`: PASS.
- `git diff --check`: PASS.
- Kiểm tra chính xác inventory, hash/path, reread control/config qua nhiều request, không nạp package body trong root phase, Technical-only, Concept core-only, từng leaf độc lập và thứ tự coexistence cố định.
- Kiểm tra package/leaf identity không tồn tại hoặc sai role/version bị chặn; blocker do model cung cấp và nhiều scope của cùng leaf được giữ; một body chỉ đọc một lần trong request.
- Kiểm tra missing, permission/I/O, UTF-8, hash mismatch, traversal/outside path, config sai/JSON trùng key và Structured Outputs sai cấu trúc; không truy xuất nguồn thay thế hoặc tự đổi mode.
- AppTest kiểm tra nhãn/lịch sử T7, T7 → T3 → T7, T3 chỉ nhận prompt riêng và không vào history thường, lỗi trước API giữ nguyên history/prompt/nhãn/bản ghi.
- Sáu artifact runtime hiện có so sánh nguyên byte với HEAD; **208 tệp upstream được Git theo dõi** so sánh nguyên byte với HEAD, không có tệp upstream mới chưa được bỏ qua. Bốn tệp `.pytest_cache` đã bị bỏ qua không thuộc inventory Git và không được sửa trong T7. Số 212 trong bằng chứng cũ bao gồm bốn tệp cache này.
- T0–T6 giữ nguyên read set và hành vi kiểm thử; T3 vẫn là structured route inspection riêng. Không thêm dependency, server hoặc framework registry/eval.

Router-integrated local retrieval chỉ **STATIC VERIFIED** cho đến campaign live do ChatGPT giám sát chạy từ prompt UTF-8. Codex không chạy prompt live hoặc gọi API thật trong T7. Không quy bằng chứng live T5/T6 thành bằng chứng live T7.

Phạm vi thay đổi: `app.py`, `README.md`, append `VERIFICATION.md`, thêm manifest runtime và `test_t7.py`. Không stage/commit/push/tag/branch/thay remotes. `STOP: T8 NOT STARTED`.

# T7 — kiểm chứng live Router → local retrieval

Phần này cập nhật trạng thái LIVE NOT RUN của mục T7 tĩnh phía trên. Campaign cuối được chạy bằng UTF-8 sạch qua API thật với gpt-5.6-sol, sau khi sửa hai lỗi triển khai phát hiện trong audit/lần live đầu.

T7 LIVE ROUTER → LOCAL RETRIEVAL: SCOPED PASS

## Hai lỗi T7 phát hiện trước campaign cuối

Audit và lần live đầu phát hiện hai lỗi triển khai, không phải lỗi module:

1. Root routing phase được gửi nguyên manifest local, khiến Router nhìn thấy inventory leaf của Concept. Điều này trái invariant ROUTER MAY KNOW PACKAGE INTERFACES; ROUTER MUST NOT KNOW PACKAGE LEAF INVENTORIES. Bản sửa vẫn đọc/kiểm manifest ở platform mỗi request nhưng không gửi leaf map cho root Router. Chỉ Concept-local selector được thấy binding availability của leaf thuộc chính package đó.
2. Concept-local selection từng trả blocker tạm kiểu body chưa truy xuất, rồi Python đã hash-verify/đọc body thành công nhưng blocker cũ vẫn đi vào final handoff. Bản sửa xác định rõ retrieval là pha sau selection: trạng thái chưa truy xuất vì chưa đến pha retrieval không phải unresolved blocker. Blocker semantic/control/identity thật vẫn được giữ.

Hai lỗi này được sửa cục bộ trước campaign cuối. Không sửa Hub CI, Router, Architecture, Root Catalog, Concept core/Catalog hoặc leaf body.

## Campaign cuối

Tổng cộng 10 request live: A–G và I một lượt; H hai lượt trong cùng history. Không có API exception hay lỗi host.

A: giải thích RAM/SSD đơn giản → root không chọn package, không retrieval. PASS.
B: chẩn đoán máy khựng chưa có log → chỉ Technical, chỉ đọc HUB-DOM-TECHNICAL. PASS.
C: audit thể chế hư cấu, không thiết kế lại → Concept core + Catalog, không leaf. PASS.
D: /BRAINSTORM → Concept + Brainstorm; không Creative/Debate; output tạo nhánh và hệ quả bậc hai. PASS.
E: /CREATIVE → Concept + Creative; output thực thi cảnh sáng tác. PASS.
F: /DEBATE → Concept + Debate; core + Catalog + Debate được đọc, blocker rỗng; output thực thi phản đối có hệ quả và điều kiện dừng. PASS.
G: audit thể chế + chẩn đoán kỹ thuật → Concept + Technical, không leaf. PASS.
H1: Brainstorm → Concept + Brainstorm. PASS.
H2: đổi hẳn sang PC diagnosis → chỉ Technical, không Concept/leaf. PASS cho routing recompute/no persistence.
I: /AUTHOR GENERIC → Router chọn Authoring nhưng local retrieval rỗng; một blocker platform; không đọc body/fallback/emulate. PASS expected blocker.

## Debate: đối chiếu failure T5

T5 đã tái hiện:
LOCAL DEBATE BODY = PRESENT / BYTE-EXACT
OLD CHATGPT LIBRARY METADATA = UNRESOLVED / NOT_PERFORMED
T5 MODEL RESULT = REFUSES SPECIALIZED DEBATE EXECUTION

T7 campaign cuối:
ROOT PACKAGE = HUB-PKG-CONCEPT-DEVELOPMENT
LOCAL LEAF SELECTION = HUB-CAP-DEBATE
LOCAL RETRIEVAL = CORE + CATALOG + DEBATE
SHA-256 VERIFIED = YES
UNRESOLVED BLOCKER = NONE
FINAL BEHAVIOR = DEBATE EXECUTED

Kết luận giới hạn đúng host:
REPRODUCED T5 HOST-BINDING FAILURE = RESOLVED FOR T7 LOCAL_RUNTIME_FILE PATH

Điều này không thay đổi hay xác minh lại ChatGPT Library. Metadata nguồn cũ của Debate vẫn giữ nguyên UNRESOLVED / NOT_PERFORMED; T7 dùng local-host successor binding riêng.

## Trạng thái T7 sau live

ROOT ROUTING WITHOUT LEAF INVENTORY EXPOSURE = STATIC VERIFIED + LIVE OBSERVED
SELECTIVE LOCAL RETRIEVAL = STATIC VERIFIED + LIVE PASS A–I
TECHNICAL-ONLY = LIVE PASS
CONCEPT CORE-ONLY = LIVE PASS
CREATIVE LOCAL RETRIEVAL / EXECUTION = LIVE PASS
BRAINSTORM LOCAL RETRIEVAL / EXECUTION = LIVE PASS
DEBATE LOCAL RETRIEVAL / EXECUTION = LIVE PASS
TECHNICAL + CONCEPT COMPOSITION = LIVE PASS
ROUTING RECOMPUTE ACROSS TURNS = LIVE PASS
UNBOUND AUTHORING = SELECTED THEN BLOCKED WITHOUT FALLBACK
AIS / IMAGET T7 LOCAL EXECUTION = NOT RUN / UNBOUND BY DESIGN
T8 = NOT STARTED

PASS chỉ áp dụng các prompt và revision hiện tại. Nó không chứng minh mọi Router case, mọi control/provenance edge case, Authoring/AIS/ImageT local execution, hay ChatGPT Library deployment.

# T8 — Authoring Lifecycle: kiểm chứng tĩnh

Ngày: 2026-11-04. `T8 IMPLEMENTED / STATIC VERIFIED / LIVE NOT RUN`.
Baseline: `main`, HEAD `8f402ebcb6845f0a8f0b0d080824c0ada94a85fc`; T7 đã có thay đổi local chưa stage/commit. Mọi bằng chứng T7 phía trên được giữ nguyên.

Triển khai:

- Thêm mode `T8 - Authoring Lifecycle`, dispatch tới `t8.call_t8(config, messages)`; trả `(answer, trace)`. T8 giữ trạng thái activation trong biến cục bộ của từng request, không lưu mode Authoring vào history/session.
- Mỗi request đọc lại nguyên CI 1.1, Router 1.1, Architecture 1.8, Root Catalog 1.8 và manifest v0.2. Model chọn root theo ngữ nghĩa trước kiểm tra storage; root không nhận manifest thô hoặc inventory leaf. Package không bind vẫn được chọn rồi bị chặn sau selection.
- Manifest `runtime/HUB_LOCAL_BINDINGS_v0.2.json` chỉ có Technical + Concept như v0.1 và Authoring 0.6. Body `runtime/packages/authoring/HUB-CAP-AUTHORING_v0.6.md` là bản sao byte-exact của nguồn ACTIVE `upstream/Central Hub/library_modules/HUB-CAP-AUTHORING_v0.6.md`; host xác minh đường dẫn runtime, SHA-256 và UTF-8 trước admission.
- Chỉ khi root chọn Authoring mới có admission Structured Outputs. Model nhận CI + handoff storage tối thiểu + nguyên Authoring + history hiện tại; Python kiểm tra shape/enums và quan hệ active/target/preset/contributor, không phân tích trigger, spacing, case, provenance, preset hoặc nội dung user.
- Inactive không đưa Authoring body vào instructions cuối, chỉ tiếp tục Hub CI baseline. Active dùng CI → handoff đã xác minh → nguyên Authoring, tạo một prompt rồi dừng. Không nạp hoặc thực thi target body/tools chỉ vì target là AIS/IMAGET/CODEX/WORK/GENERIC; preset chỉ là chiến lược biến đổi prompt.
- Contributor chỉ đi qua Concept owner khi admission yêu cầu CREATIVE/BRAINSTORM. Owner đọc core + Catalog, phân giải identity/role/scope/protected constraints/provenance theo semantics hiện hành. Nhãn contributor không vượt qua gate explicit span của Concept; thiếu điều kiện phải trả blocker. Python chỉ đối chiếu identity chính xác với contributor được yêu cầu, Catalog và binding.
- Chỉ leaf yêu cầu được hash-verify/đọc và chạy một pha contribution. Authoring cuối nhận artifact thực tế có provenance, scope, protected constraints, evidence hash và trạng thái GENERATED_CONTRIBUTION_NOT_ACCEPTED_STATE; không nhận lại raw core/Catalog/leaf controls. Thiếu/sai contributor chặn prompt phối hợp, không fallback thành prompt single-target tương đương. Debate không phải contributor được phép.
- Lỗi controls/manifest dừng trước API. Lỗi body/path/hash/UTF-8 chặn phần phụ thuộc, không dùng upstream/repository fallback. Structured record sai hoặc API refusal/incomplete/thiếu output dừng request, không retry; lượt thất bại toàn bộ không sửa history thường.

Bằng chứng static/mock:

- Baseline trước T8: 47/47 kiểm thử T0–T7 PASS.
- Sau T8: `python -X utf8 -m unittest -q test_app test_t3 test_t4 test_t5 test_t6 test_t7 test_t8`: **70/70 PASS**, gồm nguyên 47 kiểm thử cũ và 23 kiểm thử T8. Mọi request trong kiểm thử T8 dùng HTTP MockTransport, không đi tới API thật.
- Bao phủ năm target và từng P1/P2/P3; hai contributor trên cả năm target; impossible admission combinations, enum/shape sai, record malformed, root identity sai/trùng; đọc lại controls/manifest và recompute qua lượt dù history có `/AUTHOR`, clarification/reauthor.
- Kiểm tra chính xác read set, root không thấy leaf/manifest, inactive không có Authoring body, final Authoring không có target/Concept/leaf bodies, contribution/provenance/protected state được chuyển nguyên vào handoff. Đây là kiểm tra host/payload; mock không chứng minh model tạo contribution hoặc prompt đúng semantics.
- Bao phủ lỗi missing/permission/I/O/hash/UTF-8, UTF-8 sai dù hash hợp lệ, path traversal/outside runtime, Catalog identity/version/interface mismatch, contributor sai/unknown/Debate, blocker owner/admission, refusal/incomplete/empty output. Không tự drop contributor hoặc retry.
- AppTest xác minh nhãn T8, history thường, T8 → T3 isolation và lỗi trước API/structured admission không đổi history/nhãn/route records/prompt. T7 vẫn chọn rồi chặn Authoring vì chỉ đọc v0.1; 47 kiểm thử regression giữ nguyên.
- `python -X utf8 -m compileall -q app.py t8.py test_app.py test_t3.py test_t4.py test_t5.py test_t6.py test_t7.py test_t8.py`: PASS.
- `git diff --check`: PASS; kiểm tra riêng UTF-8/EOF/trailing whitespace trên file T8 mới.
- Snapshot SHA-256 đầu/cuối: toàn bộ 219 tệp upstream/runtime có trước T8 giữ nguyên byte (212 upstream gồm bốn cache đã bị Git bỏ qua; bảy runtime gồm v0.1). Kiểm thử cũ cũng so sánh 208 tệp upstream được Git theo dõi với HEAD. Không thêm file upstream.
- `test_t7.py` giữ nguyên byte. `app.py` chính xác bằng snapshot T7 cộng mode T8 và dispatch ba dòng; các hàm T7 giữ nguyên. VERIFICATION có trước T8 được giữ nguyên byte làm prefix. README thêm mô tả T8 và cập nhật dòng liệt kê lịch sử chung để bao gồm T8; các đoạn T7 còn lại giữ nguyên.

## Binding cũ và giới hạn bằng chứng

Authoring old ChatGPT Library metadata vẫn **UNRESOLVED / NOT_PERFORMED**. T8 v0.2 là local-host successor cho LOCAL_RUNTIME_FILE, không viết lại hoặc xác minh lại binding host cũ. Upstream không đổi. v0.1 tiếp tục là manifest riêng của T7; không thêm Authoring, AIS hoặc ImageT vào v0.1. v0.2 không bind AIS/ImageT body.

**Codex không gọi API live trong T8.** Exact linguistic activation (first non-empty current-user line, case/spacing, quote/fence/source provenance, clarification/reauthor) do model quyết định theo nguyên body; kiểm thử mock chỉ xác lập phản ứng host với record. Semantics contributor theo Concept owner và chất lượng/preservation của prompt cuối vẫn **LIVE NOT VERIFIED**. Không quy kết PASS live T7 thành PASS live Authoring.

## Ngân sách live dành cho ChatGPT giám sát

Cases và campaign live sẽ do ChatGPT giám sát chọn/chạy riêng, chỉ kiểm tra semantics mà mock không xác lập được:

- Tối đa **4 user requests tổng cộng**, kể cả lượt tiếp theo trong cùng conversation.
- Không lặp request trừ khi đã phát hiện một lỗi đáng kể.
- Khi gặp lỗi đáng kể, dừng campaign ngay trước mọi lần chạy lại; chỉ xem xét chạy lại sau khi lỗi đã được phân tích.
- Không dùng live để lặp lại kiểm tra inventory/hash/read set/schema đã xác lập tĩnh; không mở rộng budget ngầm.

Phạm vi T8: sửa `app.py`, append `README.md`/`VERIFICATION.md`; thêm `t8.py`, `test_t8.py`, manifest v0.2 và runtime Authoring 0.6. Diff Git tổng còn chứa T7 có trước, không được quy toàn bộ diff cho T8. Không stage, commit, push, tag, tạo branch hoặc thay remotes.

**STOP: T9 NOT STARTED.**

# T8 — Authoring Lifecycle: kiểm chứng tĩnh

Ngày: 2026-11-04. Baseline Git vẫn là `8f402eb`; T7 và T8 đều là thay đổi local chưa stage/commit/push.

`T8 STATIC / MOCK VERIFIED: PASS`

T8 thêm successor binding riêng `runtime/HUB_LOCAL_BINDINGS_v0.2.json`. v0.1 của T7 không bị sửa và vẫn chỉ bind Technical + Concept. v0.2 giữ nguyên các binding đó và thêm đúng `HUB-PKG-AUTHORING -> HUB-CAP-AUTHORING ACTIVE/0.6` bằng `LOCAL_RUNTIME_FILE`.

Authoring runtime:
- `runtime/packages/authoring/HUB-CAP-AUTHORING_v0.6.md`
- byte-exact với `upstream/Central Hub/library_modules/HUB-CAP-AUTHORING_v0.6.md`
- SHA-256 `3a3c067a4eabccc4355d9c8a33dd96bef063ec8654d758aa6a3827862ffd6328`

Metadata ChatGPT Library cũ trong Root Catalog vẫn giữ nguyên `UNRESOLVED / NOT_PERFORMED`. T8 không sửa hoặc nâng trạng thái đó; v0.2 chỉ là binding kế nhiệm cho host local.

## Host behavior được kiểm bằng mock/static

- Root routing vẫn do model quyết định từ exact Hub CI / Router / Architecture / Root Catalog.
- Root Router không nhận raw v0.2 manifest và không thấy inventory leaf.
- Python không parse cú pháp `/AUTHOR`, không quyết định first-nonempty-line, case, spacing, quote/fence, preset hoặc contributor.
- Authoring admission là Structured Outputs do model quyết định cho current user turn.
- Admission inactive không thực thi Authoring và không dùng Authoring body ở final phase.
- Active single-target/preset chỉ nạp exact Authoring body; target AIS/IMAGET/CODEX/WORK/GENERIC không tự kích hoạt pipeline/tool.
- Mỗi call tính lại root/admission; Python không giữ persistent Authoring mode.
- CREATIVE/BRAINSTORM contributor đi qua Concept owner interface, không do Python suy từ intent. Python chỉ kiểm identity/role/version/path/hash.
- Contributor label không được phép bỏ qua exact Concept leaf activation/scope/provenance rules; unmet owner requirement phải trở thành blocker.
- Contributor hợp lệ chỉ nạp đúng leaf được chọn; Debate không phải Authoring contributor.
- Contributor output được handoff như scoped generated contribution, không thành accepted canon/design/state.
- Contributor failure không được hạ cấp thành single-target prompt tương đương.
- Missing/hash/UTF-8/path traversal/identity/schema/refusal/incomplete đều fail hoặc block đúng phần, không upstream/repository fallback.
- T7 vẫn dùng v0.1; T8 không retroactively bind Authoring cho T7.
- T3 isolation và UI/history regression được giữ.

Kiểm thử:
- `python -X utf8 -m unittest -q test_t8`: 22/22 PASS.
- Full suite `test_app test_t3 test_t4 test_t5 test_t6 test_t7 test_t8`: 69/69 PASS.
- `compileall`: PASS.
- `git diff --check`: PASS.
- `git diff --exit-code -- upstream`: PASS.
- Codex không gọi live OpenAI API trong T8.

## Live budget

Campaign live do ChatGPT giám sát bị giới hạn cứng:
- tối đa 4 user requests tổng cộng;
- không lặp nếu chưa có material failure;
- gặp material failure thì dừng trước mọi rerun/case sau;
- live chỉ dùng để xác lập semantics mà mock/static không chứng minh được.

Tại checkpoint static này:
`T8 LIVE = NOT RUN`
`T9 = NOT STARTED`

# T8 — live budgeted campaign và correction

Campaign live dừng ở 3/4 user requests theo đúng cost policy. Không có request thứ 4 và không rerun sau material failure.

## Request 1 — exact target + preset

Input bắt đầu bằng /AUTHOR CODEX P1.

Trace:
- root: HUB-PKG-AUTHORING
- local retrieval: Authoring 0.6
- authoring_active = true
- target = CODEX
- preset = P1
- contributor = NONE
- blockers = []

Output là một prompt ngắn cho Codex, giữ phạm vi sửa tối thiểu và giữ cấm commit/push. Không có downstream Codex execution.

Phân loại: LIVE PASS trong scope.

## Request 2 — no persistence + later-line lookalike

Cùng history với request 1. Current user turn có yêu cầu sửa prompt nhưng dòng /AUTHOR CODEX chỉ xuất hiện ở phía sau, được ghi rõ là ví dụ chứ không phải trigger.

Trace:
- root selected packages = []
- Authoring không được retrieve
- authoring_active = false
- target/preset/contributor đều NONE
- blockers = []

Output vẫn hỗ trợ sửa câu chữ bằng Hub baseline, nhưng không dùng Authoring capability.

Phân loại: LIVE PASS cho per-turn reassessment, no persistence và later-line non-trigger.

## Request 3 — Authoring + Brainstorm contributor

Input có exact Authoring composition trigger /AUTHOR CODEX + BRAINSTORM và đồng thời có explicit valid Concept span /BRAINSTORM ... #.

Observed trace trước correction:
- root: Authoring + Concept + Technical
- Authoring được local-retrieve
- admission active, target CODEX, contributor BRAINSTORM
- Concept core + Catalog được retrieve
- contributor body chưa được retrieve
- contributor_retrieved_module_ids = []
- model trả blocker nói Brainstorm body chưa được truy xuất/xác minh nên không thể tạo contribution

Final response chặn composed prompt và không giả lập Brainstorm.

Phân loại: REPRODUCED T8 IMPLEMENTATION FAILURE — POST-SELECTION RETRIEVAL SEQUENCING.

Failure này không chứng minh Brainstorm semantics sai và cũng không phải trường hợp contributor-label-only: request đã có explicit valid /BRAINSTORM ... # span. Vấn đề là Concept owner selection phase biết body chưa được đọc nhưng chưa được cung cấp đủ local-binding evidence để phân biệt pending retrieval by design với unavailable/unverified artifact.

## Correction sau failure — STATIC ONLY

Không sửa Hub CI, Router, Architecture, Root Catalog, Authoring 0.6, Concept core/Catalog hoặc Brainstorm body.

T8 được sửa cục bộ:
- thêm T8 CONCEPT OWNER LOCAL BINDING AVAILABILITY cho Concept-owner phase;
- view này xác nhận identity/version của các leaf đã local-bind nhưng không đưa body vào trước selection;
- ghi rõ body retrieval + SHA-256 verification xảy ra sau valid owner selection;
- expected pending post-selection retrieval không phải unresolved blocker;
- contributor label vẫn không bypass exact Concept activation/scope/provenance rules;
- actual leaf body vẫn chỉ được đọc sau model owner selection và identity validation.

Static/mock sau correction:
- test_t8: 23/23 PASS
- full T0–T8 suite: 70/70 PASS
- compileall: PASS
- git diff --check: PASS
- upstream: unchanged

Theo cost policy, không rerun request 3 sau correction.

T8 SINGLE-TARGET / PRESET LIVE = PASS
T8 NO-PERSISTENCE / LATER-LINE NON-TRIGGER LIVE = PASS
T8 CONTRIBUTOR PATH BEFORE CORRECTION = REPRODUCED SEQUENCING FAILURE
T8 CONTRIBUTOR CORRECTION = STATIC / MOCK VERIFIED; NOT LIVE REVERIFIED
LIVE USER REQUESTS USED = 3 / 4 MAX
REQUEST 4 = NOT RUN
T9 = NOT STARTED

Không được nâng contributor path thành live PASS cho đến khi có live evidence mới. Failure trước correction được giữ làm bằng chứng lịch sử; correction không xóa nó.

# T9 — AIS Local Execution: kiểm chứng tĩnh

Ngày: 2026-11-04. Baseline: `main`, HEAD `3f827471ae127dcefb8067e65b4a3c3b0b519b44`, working tree sạch. Chỉ sửa T9 local; không stage/commit/push/tag/branch hoặc đổi remotes.

## Binding và trạng thái host cũ

`runtime/HUB_LOCAL_BINDINGS_v0.3.json` giữ nguyên ba entries Technical + Concept + Authoring của v0.2, chỉ thêm HUB-PKG-AIS, alias HUB-PIPE-AIS, TOOL_PIPELINE 1.1. Runtime pair sao chép byte-exact từ đúng upstream active pair:

- `runtime/packages/ais/AIS_PIPELINE_v1.1.md`: SHA-256 `68763c5bc3a19dbfae17535daebcc5e95e6279368153583470285334d6e2ffd6`.
- `runtime/packages/ais/AIS_ROUTER_v1.2.yaml`: SHA-256 `c977b5adb74436e066192d240304e5e898b320d086cf3352ce5a59c542d03dbf`.

Không thêm Module ID header; HUB-PIPE-AIS vẫn là Catalog routing alias. Path phải ở trong runtime, SHA-256 được kiểm trước UTF-8; cần đủ cả hai artifact. Không fallback upstream/repository/archive. Manifest kiểm shape/inventory, duplicate keys, identities/version/path/hash; entries cũ được pin theo canonical package digest v0.2.

PROJECT_SOURCES / LEGACY_PROJECT_SOURCE, LEGACY_EXISTING, OFFICIAL_ACTIVE và project_deployment NOT_PERFORMED trong upstream giữ nguyên và là metadata host cũ. v0.3 chỉ là successor binding local; không chứng minh hay tuyên bố Project deployment cũ. v0.1/v0.2 vẫn dành riêng cho T7/T8.

## Executor và ranh giới pha

Executor là [native OpenAI Responses API web_search](https://developers.openai.com/api/docs/guides/tools-web-search) qua SDK `openai==2.38.0` đã cài; không có custom search engine, HTTP provider, scraping, browser automation, RAG hoặc research engine thứ hai.

Root nhận đúng bốn controls, không nhận manifest thô hay AIS bodies. Root Structured Outputs bổ sung version và declared_source_path để kiểm Catalog identity; không có Python keyword routing. No-AIS chỉ đọc controls + v0.3 rồi gọi Hub-CI baseline không tools. Non-AIS selections giữ scope và ghi rõ chưa thực thi.

AIS selected mới đọc/hash-verify cặp AIS. AIS call dùng model cấu hình, cùng conversation input, exact Hub CI + handoff + exact pipeline/router; `tools=[{"type":"web_search"}]`, `tool_choice="required"`, `include=["web_search_call.action.sources"]`, `store=False`. Model và exact AIS controls giữ VERIFY/RESEARCH/EXPLORE, scope lock, source authority, inference/unknown và stop condition; không có Python planner mới hoặc background mode/location payload.

Trace phân biệt web_search_call với tool success, source read và claim support. Giữ action/query/queries/url khi có, call ID/status, nguồn consulted và citations riêng; dedupe theo thứ tự xuất hiện. Call item thiếu, incomplete/refusal/empty hoặc tool status không completed làm lượt thất bại, không đoán thành công và không retry. Bằng chứng đã quan sát được giữ trên ValueError.trace. Khi chưa xác lập phần độc lập an toàn, host fail lượt AIS thay vì trả lời phần cần bằng chứng từ model memory.

Pha Hub cuối nhận scope, path/SHA retrieval evidence, actions/status, source/citation URLs và nguyên văn AIS output; không tools. Hub giữ unresolved/conflict/read limits, evidence artifact != accepted state và URL attribution. Package khác không được retrieve/emulate/claim executed. Lỗi không thêm history; T3 tiếp tục tách riêng.

## Kết quả và giới hạn kiểm chứng

Một bản gồm 21 tests T9 đã qua cùng 70 tests cũ: 91/91 PASS khi socket.connect bị chặn toàn cục. Sau lượt đó, test_t9.py bị thay thế ngoài các lệnh sửa đang thực hiện bằng bản gồm 15 tests. Bản hiện trên đĩa đã được chạy lại với socket.connect bị chặn toàn cục: 85/85 PASS. Không dùng kết quả 91/91 để chứng nhận bản 15 tests hiện tại.

Compileall các module app/T8/T9 và tests local: PASS. `git diff --check`: PASS. `git diff --exit-code -- upstream`: PASS. Chưa chốt nghiệm thu coverage đầy đủ T9 vì file test bị thay đổi đồng thời; đã hỏi người dùng phân định quyền sửa và giữ nguyên file test đang có. Không chạy tests upstream hoặc package ImageT.

Static/mock PASS không chứng minh live routing, model compliance, source reads hoặc chất lượng evidence thật.

## Sự cố mock UI

Một lần chạy ca UI T3 mới đã timeout vì mock chỉ bọc module app đã import, chưa bọc script do Streamlit chạy lại. Ca đó có thể đã thử kết nối OpenAI API; không có response/API trace xác nhận request có tới máy chủ hoặc được thực thi hay không. Vì vậy không khẳng định ZERO live API calls cho toàn phiên; execution của lần thử ngoài ý muốn này là UNKNOWN. Không có live T9 campaign hay kết quả live PASS được ghi nhận.

Bản 21 tests đã sửa mock bằng config giả + openai.OpenAI MockTransport cho script chạy lại và chặn socket trong setUp. Bản đó sau đó bị thay thế; hai lượt full suite cuối đều dùng chặn socket.connect toàn cục, không dùng kết nối mạng thật. Không tiếp tục thử request thật.

## Live campaign dành cho ChatGPT giám sát

Ngân sách tối đa **2 user requests tổng cộng**, không phải số API calls nội bộ:

1. A — session mới, chọn T9, yêu cầu sửa câu chữ từ nội dung tự chứa. Kỳ vọng không chọn AIS, không đọc AIS, không web_search; chỉ root + baseline Hub.
2. B — session mới, chọn T9, yêu cầu kiểm chứng một thông tin bên ngoài hiện hành. Kỳ vọng chọn AIS, cặp runtime verified, có web_search_call và actions/sources/citations quan sát được; Hub final trích URL đúng mức support.

Có thể gọi `call_t9(config, messages)` để xem trace; UI không dump trace mặc định. Dừng khi có lỗi material, không tự rerun. Codex không chạy hai ca live này. T9 LIVE CAMPAIGN = NOT RUN.

ImageT: **OUT OF SCOPE / REMOVED FROM THIS MIGRATION** theo quyết định người dùng. Không binding, inspect body, test, migrate hoặc triển khai ImageT trong T9. Không bắt đầu T10.

## T9 current verified status — supersedes earlier checkpoint labels

Các mục T9 phía trên ghi lại quá trình triển khai, gồm checkpoint tĩnh trước live, một incident mock UI có execution không xác định và một concurrent-write incident khi Codex còn ghi t9.py. Các incident đó được giữ làm lịch sử; chúng không còn là current status sau khi file hiện tại được kiểm lại.

Current local revision:
- focused test_t9: 15/15 PASS
- full T0–T9 suite: 85/85 PASS
- compileall: PASS
- git diff --check: PASS
- upstream byte state: unchanged
- T9 positive live request: PASS
- observable web_search_call: completed
- AIS local pipeline/router retrieval: SHA-256 verified
- source/citation capture: observed
- final Hub return: completed
- unresolved blockers: none
- ImageT: excluded from this migration

T9 LIVE = SCOPED PASS for the current VERIFY-like external claim path.
Earlier labels saying LIVE NOT RUN or waiting for test-file arbitration are historical checkpoints and are superseded by this later direct evidence for the current local T9 files.

## M1 — Unified Local Runtime (2026-11-04)

Mặc định UI và `app.call_model(config, messages)` nay chạy `m1.call_runtime`; T0–T9 vẫn giữ tên, chỉ số và entry point chẩn đoán. Root Router hiện hành chọn một tập root theo ngữ nghĩa qua một structured response; Python chỉ kiểm tra identity/version/source, thực hiện retrieval và ghép các đường đã có. Không có Router, registry, executor framework, persistence hay dependency mới.

M1 dùng inventory v0.3 hiện có, kiểm tra bằng `t9.load_bindings`; Technical/Concept/Authoring chuyển sang `t8.call_t8` bằng kết quả root đã kiểm tra và các binding hiện có. Các keyword tùy chọn trên `call_t8` cho phép tránh chọn root lần hai và nhận bằng chứng AIS; gọi chẩn đoán T8 không truyền keyword vẫn dùng đường cũ. T7 tiếp tục sở hữu các hàm kiểm tra Catalog, retrieval/SHA-256, structured selection và binding view. AIS tái dùng `validate_ais_catalog`, `retrieve_pair`, `search_evidence` của T9 với cùng hợp đồng native Responses `web_search`, `tool_choice=required`, `include=web_search_call.action.sources`. `t9.py`, `test_t9.py`, binding v0.3 và các body AIS không bị sửa trong M1.

Không chọn root thì dùng Hub baseline. Leaf vẫn do Concept chọn; Python không phân tích trigger. Authoring vẫn dùng admission/contributor của T8 và dừng ở prompt artifact; `/AUTHOR AIS` hoặc `/AUTHOR IMAGET` không tự chọn/chạy target. AIS chỉ chạy khi được root chọn độc lập theo yêu cầu hiện tại. Khi Technical/Concept cùng được chọn với Authoring, đường resolution cũ tạo kết quả theo phạm vi cho Hub làm căn cứ trước pha Authoring cuối; không đưa các control đó vào pha Authoring cuối. Bằng chứng AIS giữ giới hạn nguồn/support và được coi là dữ liệu không đáng tin về mặt chỉ dẫn. Hub giữ quyền kết luận/trạng thái.

Root chọn ImageT gây blocker `local-runtime unavailable`, không đọc body, không fallback hoặc emulation. M1 dừng cả lượt khi root/package/binding/tool bị lỗi hoặc có blocker; không lưu lượt lỗi và không tự thử lại. Đây là cách xử lý bảo thủ hiện tại, chưa thực hiện trả kết quả từng phần cho các phạm vi độc lập trong lượt có lỗi.

Kiểm chứng M1:

- Focused `test_m1`: **17/17 PASS**. Bao gồm baseline, Technical, Concept/leaf, Authoring active/inactive/contributor, AIS mock contract, phối hợp nhiều root và cả bốn root, ImageT chỉ kiểm tra blocker ở root, lỗi root/binding/package/tool, default dispatch, history/UI và entry point T7/T8/T9.
- Toàn bộ tests local T0–T9+M1: **102/102 PASS**, gồm 85 tests cũ và 17 tests M1. Test giao diện cũ cần T0 ban đầu được đổi sang chọn T0 tường minh; assertion danh sách UI bao gồm runtime mặc định mới. Không sửa kỳ vọng về nội dung/hành vi chuyên biệt T7/T8/T9.
- Các lượt chạy dùng `socket.socket.connect` bị chặn toàn cục và OpenAI client giả hoặc `httpx.MockTransport`. `ais_web_search_executed=True` trong fixture chỉ phản ánh response công cụ giả, không phải bằng chứng công cụ thật đã chạy.
- `compileall` cho app/T8/T9/M1 và toàn bộ test local: PASS. UTF-8/BOM/EOF/whitespace: PASS. `git diff --check`: PASS. `git diff --exit-code -- upstream`: PASS; đối chiếu SHA-256 và inventory toàn bộ file upstream với baseline đầu M1 cũng không đổi. Các file T9/AIS được bảo vệ khớp hash baseline. HEAD vẫn `3f827471ae127dcefb8067e65b4a3c3b0b519b44`, index rỗng; giữ nguyên phần T9 chưa commit.
- Không chạy test upstream hoặc body ImageT. M1 không mở T10, M2, M3 hay M4.

M1 **STATIC/MOCK PASS != LIVE PASS**. PASS live T9 đã ghi ở trên giữ nguyên phạm vi; không chứng nhận tự động luồng M1 mới. Chưa kiểm chứng live semantic routing/compliance, chất lượng evidence hay phối hợp toàn luồng M1; không có blocker static/mock còn mở. Không gọi API thật, stage, commit, push hoặc thao tác remote trong M1.

## M2 — failure live, sửa root M1 và một lượt chạy lại (2026-11-04)

**Kết luận: M2 FAIL.** Lượt chạy lại workload 1 vẫn thất bại ở đường contributor sau khi qua root; dừng campaign, không chạy workload 2, không tinh chỉnh hay gọi lại. Không bắt đầu M3/M4. Các bằng chứng T9/M1/T8 trước đó giữ nguyên phạm vi, không được nâng thành PASS cho M2.

### Bằng chứng trước sửa

- `m2_evidence/workload_1_aborted_trigger_mismatch.json`: lần harness bị hủy vì dòng đầu là `/AUTHOR GENERIC`, thiếu `+ BRAINSTORM`. **Không tính là workload M2 hợp lệ.** File giữ nguyên byte; có 2 lần vào `Responses.create` được ghi, chỉ call root có response `completed`; call admission chưa có response/error hoặc bản ghi kết thúc. Không suy ra call thứ hai đã hoàn tất hay được máy chủ thực thi.
- `m2_evidence/workload_1_first_live_failure.json`: workload 1 hợp lệ đầu tiên, dòng đầu chính xác `/AUTHOR GENERIC + BRAINSTORM`. Đúng **1 Responses API call**, root trả `completed`, chọn `HUB-PKG-AUTHORING` và `HUB-PKG-CONCEPT-DEVELOPMENT`, rồi M1 dừng trước retrieval/execution vì hai blocker:
  - `Chưa truy xuất nội dung đầy đủ của HUB-CAP-AUTHORING 0.6.`
  - `Chưa truy xuất đầy đủ HUB-DOM-CONCEPT-DEVELOPMENT 1.1 và catalog cục bộ của gói; vì vậy chưa thể phân giải hoặc áp dụng mô-đun BRAINSTORM.`
- Không AIS/web search trong workload hợp lệ đầu tiên. File này được đổi tên từ `workload_1.json` trước lượt chạy lại, giữ nguyên SHA-256 `6237a05b5fa684013e7390c702e4541ec8044d9ffacc081198b3336e2e85dc15`.

### Chẩn đoán và sửa cục bộ

Root instruction cũ trong `m1.call_runtime` yêu cầu chọn scope trước retrieval và không bỏ qua package chưa đọc body, nhưng chưa phân biệt việc chờ retrieval bình thường với blocker. Response live biểu diễn bước retrieval kế tiếp thành `unresolved_blockers`; M1 giữ nguyên chúng và dừng tại kiểm tra fatal blocker. Đây là lỗi tích hợp đã tái hiện, không phải lỗi thiếu local binding được xác nhận.

Chỉ thêm đoạn sau vào instruction của request `hub_m1_root` trong `m1.py`:

> Expected pending post-selection retrieval of selected package bodies and local catalogs is not an unresolved blocker. The host retrieves them after root selection. Report unresolved_blockers only for genuine unresolved conditions, not this normal next retrieval stage.

Không sửa Router/Hub upstream, T8, T9, bindings, package bodies hoặc payload workload. Không lọc blocker, không thêm bộ phân tích ngữ nghĩa hay viết lại quyết định model; cơ chế dừng với blocker thật giữ nguyên.

Thêm `test_root_pending_retrieval_instruction_and_brainstorm_handoff` trong `test_m1.py`: assertion chính xác hợp đồng instruction tại payload root; mock hai root Authoring + Concept với contributor Brainstorm hợp lệ kiểm tra handoff, blocker rỗng và không tools. Ca này thất bại trước sửa vì thiếu instruction, đạt sau sửa. Mock được cấp lựa chọn owner hợp lệ nên không chứng minh model live sẽ chọn owner hợp lệ với prompt này.

Focused `test_m1` + `test_t8`: **41/41 PASS**, chặn `socket.socket.connect` toàn cục, dùng mock; gồm kiểm tra blocker thật, binding/identity sai, contributor và UI/history. Đây là kiểm chứng tĩnh/mock, không chứng minh live compliance. Không chạy thêm API trong các tests.

### Lượt chạy lại workload 1 duy nhất

Chạy đúng `python -X utf8 -B m2_acceptance.py 1`; không đổi prompt, dòng đầu `/AUTHOR GENERIC + BRAINSTORM`. Bằng chứng mới: `m2_evidence/workload_1.json`. Đúng **4 Responses API calls**, cả bốn response `completed`:

1. `hub_m1_root`: chọn Authoring + Concept đúng identity/version/source; `unresolved_blockers=[]`. Lỗi chờ retrieval ở root không tái hiện trong lượt này.
2. `hub_t8_admission`: `active=true`, `target=GENERIC`, `preset=NONE`, `contributor=BRAINSTORM`; báo blocker vì chưa có contribution đã phân giải.
3. `hub_t8_contributor`: yêu cầu span chính xác `/BRAINSTORM <chỉ dẫn không rỗng> #` do người dùng viết; báo thiếu điều kiện kích hoạt, body và contribution. Response còn trả `runtime_role="NĂNG LỰC"` thay vì identity `CAPABILITY`, khiến kiểm tra hiện hữu thêm `requested contributor identity/role/binding mismatch`.
4. `hub_t8_concept`: `selected_leaves=[]`; báo `+ BRAINSTORM` chỉ nêu contributor, không kích hoạt leaf nếu thiếu span `/BRAINSTORM … #`.

Trace xác nhận đã retrieve hai package Authoring + Concept; `contributor_retrieved_module_ids=[]`, không AIS/web search, không contribution execution, không prompt cuối (`final_output=null`). M1 trả `ValueError`, không fallback/thử lại. Chưa kết luận các blocker mới đều là lỗi local hoặc điều kiện upstream cần sửa; không mở rộng sửa ngoài allowance. Root correction có bằng chứng live cục bộ nhưng toàn workload vẫn FAIL.

### Số calls và giới hạn nghiệm thu

| Lần chạy | Lần gọi Responses được ghi | Response `completed` | Nghiệm thu |
| --- | ---: | ---: | --- |
| Harness sai trigger, bị hủy | 2 | 1 | Không tính workload hợp lệ; trạng thái máy chủ của call 2 chưa xác định |
| Workload 1 hợp lệ đầu tiên | 1 | 1 | FAIL tại root |
| Workload 1 chạy lại duy nhất | 4 | 4 | FAIL sau root |
| Workload 2 | 0 | 0 | Không chạy |
| Tổng bằng chứng M2 hiện có | 7 | 6 | Gồm lần harness bị hủy |

Chỉ các workload hợp lệ dùng **5 calls / 5 response completed**; lượt sửa này phát sinh **4 calls**, không thêm lần live nào khác. `completed` của response không đồng nghĩa workload thành công. Không có bằng chứng M2 về phối hợp Technical + Concept + AIS, chất lượng nguồn hay Hub synthesis của workload 2.

Không stage/commit/push/remote mutation; index vẫn rỗng. Giữ nguyên `upstream/**`, ImageT và mọi file T9/M1/M2 cũ ngoài ba file sửa được nêu cùng việc đổi tên bằng chứng thất bại; thêm duy nhất bằng chứng chạy lại. Baseline M2 cũ không bị ghi đè.


## M2 ? hai l?i A/B v? hai workload c? span t??ng minh (2026-11-04)

**Tr?ng th?i hi?n t?i: M2 SCOPED LIVE PASS.** M?c n?y c?p nh?t tr?ng th?i hi?n t?i sau hai s?a c?c b?; c?c m?c FAIL ph?a tr?n v? file b?ng ch?ng c? ???c gi? nguy?n l?ch s?. STATIC/MOCK PASS != LIVE PASS.

### ??nh ch?nh workload l?ch s?

Workload 1 tr??c ??y thi?u `/BRAINSTORM <content> #`, n?n kh?ng h?p l? cho nghi?m thu k?ch ho?t leaf Brainstorm theo h?p ??ng hi?n h?nh. `CONTRIBUTOR PRESENCE != MODULE ACTIVATION`: nh?n `+ BRAINSTORM` ch? y?u c?u contribution; owner v?n ki?m tra applicability v? activation. Blocker thi?u span kh?ng ch?ng minh l?i tri?n khai. Hai l?i th?t ???c s?a ri?ng b?n d??i; kh?ng ??i Authoring 0.6, Concept 1.1, Brainstorm 1.1, Catalog, Router, Architecture hay body package.

### S?a c?c b?

- **A ? admission sequencing:** ch? b? sung instruction t?i `hub_t8_admission` trong `t8.py`: ph?n gi?i contributor ???c th?c hi?n sau admission; ch? ph?n gi?i l? tr?ng th?i b??c k? ti?p, kh?ng ph?i unresolved blocker. Admission ch? ghi y?u c?u contributor, kh?ng k?ch ho?t leaf; Concept ti?p t?c ki?m tra activation/scope/provenance hi?n c?. Blocker th?t v?n ???c tr? v? x? l? nguy?n tr?ng. Kh?ng l?c text, kh?ng th?m parser ho?c c? ch? ?o?n ng? ngh?a.
- **B ? runtime_role:** `CONTRIBUTOR_SCHEMA.runtime_role` nay c? enum ch?nh x?c `DOMAIN_CONTROL` ho?c `CAPABILITY`. Instruction owner y?u c?u identifier nguy?n d?ng t? Catalog, tuy?t ??i kh?ng d?ch. Validator structured hi?n c? t? ch?i gi? tr? ngo?i enum; ki?m tra identity/role/binding hi?n h?u v?n ch?n t? h?p sai d? role thu?c enum.
- `test_t8.py`: th?m ba ca h?i quy v? instruction ph?n k? admission, h?p ??ng role g?i l?n API cho c? hai contributor, v? t? ch?i role d?ch/sai tr??c retrieval, kh?ng retry. Ca blocker admission th?t v? identity mismatch gi? nguy?n.
- `test_m1.py`: ch? b? sung span h?p l? v?o fixture Brainstorm c?a ca root/handoff; gi? nguy?n root fix trong `m1.py`.
- `m2_acceptance.py`: thay ??ng hai top-level prompt ???c ng??i d?ng cung c?p; gi? newline cu?i W1; d?ng t?n `workload_N_corrected_ab.json`. T?o file b?ng ch? ?? exclusive tr??c API ?? l??t b? ng?t v?n ?? l?i d?u v?t ng?n ch?y l?i. Kh?ng ghi ?? file l?ch s?; API client v?n max_retries=0.

### Ki?m ch?ng tr??c live

Ba ca h?i quy m?i FAIL tr?n m? tr??c s?a (7 assertion/subtest failures), PASS sau s?a. Focused `test_t8` + `test_m1`: **44/44 PASS**. Full suite local: **106/106 PASS**. C? hai l??t d?ng `socket.socket.connect` b? ch?n to?n c?c v? mock/MockTransport. Ki?m tra regression g?m activation kh?ng l?u qua l??t, blocker th?t, role/identity mismatch, retrieval/binding l?i, no-target boundary, UI/history v? dispatch c?. Compile to?n b? **54 file Python**: PASS (d?ng `compile` tr?n source, kh?ng th?c thi test upstream). `git diff --check`: PASS. Hash upstream v? evidence l?ch s? kh?ng ??i; index r?ng tr??c live.

### Live workload 1 ?? s?a ? PASS

B?ng ch?ng: `m2_evidence/workload_1_corrected_ab.json`. ??ng m?t l?n ch?y top-level, **7 Responses API calls**, 7 response completed, kh?ng retry:

1. Root ch?n Authoring + Concept v?i blocker r?ng.
2. Admission active=true, target=GENERIC, contributor=BRAINSTORM, blocker r?ng.
3. Owner ch?n HUB-CAP-BRAINSTORM / CAPABILITY t? span hi?n t?i h?p l?, blocker r?ng.
4. Brainstorm body 1.1 ???c ??c v? x?c minh SHA-256; t?o contribution g?m s?u ph??ng ?n ch?a ???c ch?p nh?n.
5. Concept scope ??c l?p ch?n ??ng Brainstorm, kh?ng leaf kh?c.
6. Pha k?t qu? scope ??c l?p ho?n t?t. K?t qu? trung gian ? ??y c? d?ng prompt; kh?ng coi tu?n th? ri?ng c?a pha trung gian ngo?i ti?u ch? M2 l? ?? ???c ch?ng minh.
7. Authoring tr? prompt cu?i t? ch?a, gi? s?u ph??ng ?n song song, kh?ng x?p h?ng/ch?p nh?n/tri?n khai.

Handoff cu?i gi? `GENERATED_CONTRIBUTION_NOT_ACCEPTED_STATE`. Kh?ng AIS/web_search, kh?ng ImageT, kh?ng tools ho?c target execution. Kho?ng tr?ng live contributor T8 ???c ??ng **cho ???ng explicit span h?p l? n?y**. Kh?ng ch?y th?m l??t live ki?m persistence; ch? d?a tr?n static/mock hi?n c? cho gi?i h?n ??.

### Live workload 2 ?? s?a ? PASS

Ch? ch?y sau khi W1 ??t ?? ti?u ch?. B?ng ch?ng: `m2_evidence/workload_2_corrected_ab.json`. ??ng m?t l?n ch?y top-level, **4 Responses API calls**, 4 response completed, kh?ng retry:

1. Root ch?n Technical + Concept + AIS cho ba ph?m vi ??c l?p, kh?ng ch?n Authoring.
2. AIS pipeline/router ???c ??c v? ki?m SHA-256; native `web_search` th?c thi v?i **3 web_search_call completed**: search, open_page, find_in_page.
3. Concept ch? ch?n Brainstorm / CAPABILITY t? span t??ng minh; body ?? ???c ??c v? ki?m SHA-256.
4. Hub final t?ch b?ng ch?ng t?i li?u c? URL, ch?n ?o?n Technical, **b?n ?ng vi?n Concept song song**, v? kho?ng tr?ng ch?a bi?t. Kh?ng x?p h?ng/ch?n/ch?p nh?n ?ng vi?n; kh?ng n?ng tr?ng th?i d? ?n.

To?n b? source_urls v? citation_urls thu?c `v2.tauri.app`, kh?ng c? ngo?i l? ngu?n. Ch? request AIS ???c c?p tools web_search. Kh?ng ImageT, kh?ng th?c thi m?/target, kh?ng b?t ??u tri?n khai UI ho?c runtime Tauri/Python.

Gi?i h?n ngu?n: trace ch?ng minh ?? m?/t?m trong trang `https://v2.tauri.app/develop/sidecar/`; `https://v2.tauri.app/reference/javascript/shell/` c? trong k?t qu? search v? citations nh?ng kh?ng c? open_page ri?ng ???c ghi. Kh?ng n?ng URL ???c t?m/tr?ch th?nh b?ng ch?ng ?? ??c to?n trang, v? kh?ng tuy?n b? ?? ki?m ch?ng ??c l?p m?i claim t?i li?u. Final v?n n?u c?c gi?i h?n v? k? m?, antivirus, c?p nh?t, d?n ti?n tr?nh v? k?ch th??c/kh?i ??ng Python ch?a ki?m ch?ng. M2 nghi?m thu ph?i h?p v? bi?n quy?n, kh?ng ch?ng nh?n m?t ki?n tr?c Tauri ?? ???c tri?n khai.

### Ph?m vi, s? calls v? tr?ng th?i Git

T?c v? n?y ph?t sinh **11 Responses API calls**, hai top-level workload h?p l?, **0 retry**, kh?ng exploratory prompt; t?ch ho?n to?n kh?i 7 l?n v?o Responses.create trong l?ch s? tr??c ?? (trong ?? c? m?t call ch?a r? ho?n t?t). Kh?ng c? l?i transport/service trong hai l??t m?i. Kh?ng c?n l?i material ???c x?c nh?n theo ti?u ch? nghi?m thu M2; gi?i h?n quan s?t n?u tr?n v?n gi? nguy?n.

C?c file hi?n h?u ???c t?c v? n?y s?a: `t8.py`, `test_t8.py`, `test_m1.py`, `m2_acceptance.py`, `VERIFICATION.md`. File m?i: `m2_evidence/corrected_task_baseline.json`, `m2_evidence/corrected_ab_static_results.json`, `m2_evidence/corrected_ab_acceptance_review.json`, `m2_evidence/workload_1_corrected_ab.json`, `m2_evidence/workload_2_corrected_ab.json`. Baseline hash cho ph?p ph?n bi?t thay ??i t?c v? n?y v?i dirty work T9/M1/M2 c? s?n.

HEAD/origin/main v?n `3f827471ae127dcefb8067e65b4a3c3b0b519b44`, branch main. Gi? nguy?n `m1.py`, m?i dirty work ngo?i c?c s?a ???c li?t k? v? to?n b? b?ng ch?ng l?ch s?. `upstream/**` kh?ng ??i, package bodies kh?ng ??i, ImageT kh?ng b? ch?nh s?a. Index r?ng; kh?ng stage, commit, push, branch, tag ho?c s?a remotes. Kh?ng b?t ??u M3/M4.
