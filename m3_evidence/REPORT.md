# M3 — chưa đạt, đã khôi phục runtime

**M3 FAIL / chưa hoàn tất.** Baseline và post đều đạt ranh giới ngữ nghĩa M2, nhưng kiểm tra cache trọng tâm không đạt và chi phí token của cặp tăng 0,206133%. Đã khôi phục byte-exact `m1.py` và `t8.py` về `8f5487ca8b124edb339192a9704b5d74157bcf00`. Mọi tracked source khớp SHA-256 baseline. Chỉ `m3_evidence/` còn mới để parent review.

Baseline đã xác minh: `main` sạch, HEAD=origin/main đúng SHA trên; Authoring 0.7, Architecture/Catalog 1.9, CI/Router 1.1. Mỗi checkpoint chạy nguyên `m2_acceptance.PROMPTS[1]` rồi `[2]`, mỗi workload một lần, `max_retries=0`. Tổng: 4 top-level attempts, 22 Responses calls, không rerun. Không stage/commit/push, branch/tag/remote/deploy hoặc M4/frontend. README và VERIFICATION không đổi vì cổng thành công không đạt.

## Thử nghiệm đã hoàn tác

- A: riêng `hub_t8_concept`, đưa binding/core/catalog ổn định lên trước verified handoff; imperative vẫn sau handoff.
- B: khi AIS không được chọn, truyền `ais_evidence=None`; giữ root selection/scopes trong local route và trace M1 trả về.
- Không làm C: chưa chứng minh contribution không liên quan; hợp đồng Concept cho phép dùng ngữ cảnh/kết quả trước khi liên quan. Giữ contribution ở mọi pha vốn nhận nó và giữ contribution/scoped output trong final Authoring.
- Không làm D: giữ nguyên toàn bộ AIS evidence khi được chọn và đường chuyển vào final Hub. Không sửa request AIS, model, reasoning, verbosity, tools, số calls hoặc semantics.

Patch và tests nằm trong [candidate_runtime.patch](candidate_runtime.patch) và [candidate_test_m3.py](candidate_test_m3.py); đây là bằng chứng, không phải triển khai đang hoạt động.

## Payload và cache

Baseline W1 Concept nhận contribution 6.459 byte và AIS route/trace 1.973 byte dù AIS không được chọn; final còn có scoped output 4.421 byte. Baseline W2 Concept nhận AIS evidence 13.572 byte. Đây là kích thước JSON UTF-8 theo field, không phải tokens.

Lịch sử M2 ghi root cached=12.544 nhưng Concept W2 cache miss. Baseline hiện tại tái hiện: W1 Concept write=9.328/cached=0; W2 write=10.712/cached=0; root cả hai cached=12.679. Handoff thay đổi đứng trước stable Concept bodies là nguyên nhân cục bộ được đưa ra kiểm tra, chưa phải chẩn đoán nguyên nhân phía provider.

Sau sửa, prefix Concept trước handoff khớp chính xác **30.301 byte**, schema và model giống nhau. W1 bắt đầu `2026-11-04T17:40:16.901769Z`, W2 `2026-11-04T17:41:21.437851Z`, khoảng 65 giây. W1 write=9.122/cached=0; W2 write=10.279/cached=0. Prefix văn bản giống nhau không chứng minh provider tái sử dụng cache; nguyên nhân phía provider vẫn UNKNOWN.

## Usage và giá

Snapshot do tác vụ cung cấp, chỉ dùng làm bằng chứng: gpt-5.6-sol standard short-context, USD/triệu token: ordinary=4; cached=0,40; cache-write 30m=5; output=20. Phí web_search=0,01 USD/tool call, tách riêng. Search content dùng provider input usage nơi được báo cáo; không cộng thêm ước tính token trùng. Đây không phải hóa đơn đã xác nhận.

Ordinary = input − cached − cache_write. Input thô đã bao gồm các bucket; không cộng lần nữa. Cache-write là field thực provider trả về.

| Checkpoint | Input | Ordinary | Cached | Cache-write | Output | Tổng tokens | Token USD | Responses | web_search_call |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Baseline W1 | 68.707 | 21 | 12.679 | 56.007 | 4.783 | 73.490 | 0,3808506 | 7 | 0 |
| Baseline W2 | 86.532 | 39.784 | 12.679 | 34.069 | 7.794 | 94.326 | 0,4904326 | 4 | 5 |
| Post W1 | 66.978 | 21 | 12.813 | 54.144 | 5.236 | 72.214 | 0,3806492 | 7 | 0 |
| Post W2 | 87.960 | 42.126 | 12.840 | 32.994 | 7.691 | 95.651 | 0,4924300 | 4 | 5 |
| **Baseline pair** | **155.239** | **39.805** | **25.358** | **90.076** | **12.577** | **167.816** | **0,8712832** | **11** | **5** |
| **Post pair** | **154.938** | **42.147** | **25.653** | **87.138** | **12.927** | **167.865** | **0,8730792** | **11** | **5** |

Cặp baseline→post: raw input −301; ordinary +2.342; cached +295; write −2.938; output +350. Input cost riêng giảm 0,005204 USD, nhưng output cost tăng 0,007 USD; token cost tổng tăng **0,001796 USD**. Phí web_search mỗi cặp 0,05 USD; tổng ước tính gồm công cụ: **0,9212832→0,9230792 USD**.

Ít raw input hơn không đồng nghĩa tổng chi phí thấp hơn. Một cặp mỗi checkpoint chịu biến thiên output/search và cache đã ấm từ trước; không thể quy toàn bộ chênh lệch cho hai sửa đổi.

[metrics.json](metrics.json) chứa bucket, giá, call count theo từng pha và delta. Nhãn pha văn bản được phân biệt từ imperative thành contribution_execution, independent_scope_execution, final_authoring và final_hub; không đổi request. Tái tính offline bằng `python -X utf8 -B m3_evidence/summarize.py`.

## Nghiệm thu và kiểm chứng

Baseline và post đều **M2 SCOPED SEMANTIC PASS**:

- W1: root Authoring+Concept; GENERIC/BRAINSTORM admission; Brainstorm/CAPABILITY owner và verified retrieval; final có contribution/scoped output và là prompt tự chứa yêu cầu sáu phương án song song. Không chấp nhận, target execution, tools, AIS, ImageT hoặc blocker.
- W2: độc lập Technical+Concept+AIS, chỉ leaf Brainstorm; final tách bằng chứng chính thức, chẩn đoán, ứng viên và khoảng trống. Baseline có bốn ứng viên, post có ba; không xếp hạng/chấp nhận/triển khai. Chỉ AIS có tools, full AIS evidence tới final Hub.
- Candidate: toàn bộ `test_*.py` root **119/119 PASS**, chặn `socket.socket.connect` toàn cục. Hai tests mới: `test_no_ais_keeps_root_selection_and_final_authoring_contribution`, `test_concept_stable_prefix_across_different_handoffs_and_full_ais_final`. Context còn ở pha cần thiết, controls trước handoff/imperative sau handoff và AIS evidence đầy đủ; không chứng minh provider cache.
- Focused upstream: `test_authoring_isolation`, `test_authoring_candidate`, `test_authoring_m1`, `test_authoring_m2`, `test_authoring_m4`: **33/33 PASS**, chặn socket toàn cục. Không tuyên bố mirror-wide upstream PASS.
- Sau hoàn tác: tests root **117/117 PASS**, chặn socket toàn cục. Tests candidate trong evidence không tham gia suite runtime đã khôi phục.
- `compileall` **62 file PASS**, pycache vào thư mục tạm rồi xóa; `git diff --check` PASS; tracked diff/index rỗng. SHA-256 mọi tracked source khớp baseline. Chỉ `m1.py`/`t8.py` từng đổi trong post. ImageT, candidates, upstream, package bodies, app.py, t9.py và m2_acceptance.py không đổi.
- Quét exact configured API key trong evidence PASS, không in key. Logs: [static_local.txt](static_local.txt), [static_upstream_authoring.txt](static_upstream_authoring.txt), [restored_local.txt](restored_local.txt); metadata: [final_checks.json](final_checks.json).

STATIC/MOCK PASS khác LIVE semantic PASS, và cả hai khác tối ưu hóa thành công. Contribution trung gian W1 có dạng prompt ở cả hai checkpoint, tương tự giới hạn M2 lịch sử; không chứng minh độc lập sáu ứng viên đầy đủ ở pha đó. Trace chỉ chứng minh search/open/find thực tế; URL search/citation không chứng minh đọc toàn trang. Không kiểm chứng độc lập từng claim Tauri. Chi tiết trong [acceptance_review.json](acceptance_review.json).

Runner chỉ quan sát, lưu payload, response.usage, tools, trace, final, thời gian UTC và source hashes trong bốn JSON workload; không phải production control.

## Hotspot còn mở

AIS baseline: 51.393 input / 39.775 ordinary / 11.618 write / 0 cached / 2.753 output; post: 53.733 / 42.117 / 11.616 / 0 / 2.302. Giữ nguyên semantics; chưa đủ bằng chứng để cắt context an toàn.

**FUTURE IF NEEDED:** xác minh vì sao prefix cùng pha giống nhau vẫn không được provider tái sử dụng trước khi chọn sửa đổi khác. Chưa triển khai cache key, TTL, prewarm, breakpoints, model split, response chaining, schema redesign hoặc call merging. Không chạy thêm API trong campaign này.

Trạng thái cuối: `?? m3_evidence/`; tracked files/index sạch, HEAD/origin/main giữ baseline.
