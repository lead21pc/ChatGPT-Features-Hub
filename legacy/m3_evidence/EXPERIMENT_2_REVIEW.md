# Thí nghiệm 2: chưa đo được cache vì hết hạn mức dự án

**M3 NOT COMPLETE.** W1 chạy đúng một lần nhưng call root đầu tiên bị API từ chối với HTTP 429, `code=project_spend_limit_exceeded`, `type=insufficient_quota`. Chưa gọi Concept, chưa kiểm chứng breakpoint ở provider. Không retry, không chạy W2, không có thí nghiệm thứ ba. Lỗi này không chứng minh request explicit cache hợp lệ hay không hợp lệ ở provider.

## Baseline và phạm vi

Trước sửa: branch `main`, HEAD và ref local `origin/main` đều là `8f5487ca8b124edb339192a9704b5d74157bcf00`; tracked diff và index rỗng; chỉ `m3_evidence/` untracked. Kiểm tra remote trực tiếp không thành công: Schannel báo `SEC_E_NO_CREDENTIALS`; thử OpenSSL không đọc được GitHub Username. Vì vậy không tuyên bố đã xác minh SHA remote trực tiếp trong lượt này.

Đã giữ nguyên mọi file thí nghiệm 1, gồm hai `baseline_current_workload_*`, hai `post_workload_*`, metrics và báo cáo thất bại. Manifest SHA-256: `explicit_preserved_manifest.json`.

## Candidate đã kiểm tra rồi hoàn tác

Chỉ runtime `t8.py` từng được sửa: thêm helper riêng `concept_selection`, được gọi duy nhất cho `hub_t8_concept`. Hub CI, binding view, Concept core/catalog nguyên văn vẫn ở `instructions`; một developer message ổn định chỉ đánh dấu breakpoint, nói rõ không đổi authority/semantics; developer message kế tiếp chứa nguyên handoff và imperative cũ. Toàn bộ hội thoại theo sau giữ nguyên role/content/order. Key cố định `central-hub:t8-concept:v1`; root options explicit/30m qua `extra_body`. Schema và validator lựa chọn leaf giữ nguyên hành vi, kể cả từ chối/incomplete/sai kiểu và kiểm tra identity sau selection.

`test_m1.py` và `test_t8.py` chỉ cập nhật assertion cho hai developer messages mới của Concept; thêm hai tests tập trung. Không đổi `m1.py`, `app.py`, `t9.py`, `m2_acceptance.py`, upstream, package bodies, ImageT, model config hoặc dependencies. Python production không phân tích trigger.

Candidate đã hoàn tác, chỉ còn làm bằng chứng trong `explicit_candidate_runtime.patch` và `explicit_candidate_test_m3.py`. Đây không phải implementation đang hoạt động.

Kiểm tra artifact cuối phát hiện một sai sót thông báo lỗi trong candidate đã hoàn tác: nhánh từ chối structured output dùng nhầm chuỗi lỗi manifest T7 khi sao chép thông báo từ `app.py`. Các điều kiện validation và hành vi dừng vẫn được kiểm thử, nhưng chưa kiểm thử tính chính xác của chuỗi lỗi này. Giữ patch đúng như candidate thực tế để bảo toàn bằng chứng; không sửa lại hoặc chạy thí nghiệm mới. Runtime đã khôi phục không có sai sót được thêm này.

## Kiểm chứng tĩnh trước live

- Local **119/119 PASS**, chặn toàn cục `socket.socket.connect`.
- Authoring upstream tập trung **33/33 PASS**, chặn socket; không tuyên bố upstream toàn bộ PASS.
- JSON request thật qua SDK 2.38.0 và `httpx.MockTransport`: breakpoint được giữ trong input_text, options được serialize ra root, không còn field `extra_body` trên wire; đúng key, schema, stable prefix, handoff và hội thoại.
- So sánh mocks với `t8.py` tại HEAD: mọi request ngoài Concept bằng nhau toàn bộ JSON; kết quả/trace bằng nhau; M2 giữ **7/4 calls**, tools chỉ ở AIS, không đổi package semantics.
- Handoff giữ nguyên toàn bộ selected packages, verified artifacts, contribution, trạng thái chưa được chấp nhận, scoped output và AIS evidence nơi áp dụng. Prefix/schema/key của hai workload mock bằng nhau.
- `compileall` **65 file PASS**, pycache đặt trong thư mục tạm; `git diff --check` PASS; quét exact configured API key trong evidence PASS.

Log và metadata: `explicit_static_local.txt`, `explicit_static_upstream_authoring.txt`, `explicit_static_checks.json`. STATIC/MOCK PASS không phải LIVE PASS.

## Lượt live duy nhất

Runner `run_explicit.py` tái sử dụng observer thí nghiệm 1, thêm ghi JSON đã serialize ở `httpx.Client.send`, không ghi headers hay API key. Bằng chứng: `explicit_workload_1.json`.

| Chỉ số | W1 | W2 |
|---|---:|---|
| Top-level attempts | 1 | Không chạy |
| Responses attempts | 1, tại root | Không chạy |
| Responses completed | 0 | Không chạy |
| Concept attempts | 0 | Không chạy |
| Retry | 0 | Không chạy |
| Usage/cached_tokens/cache_write_tokens | Không được trả về | Không có |
| M2 semantic acceptance | Chưa kiểm chứng | Chưa kiểm chứng |

Không coi usage vắng mặt là 0 token, 0 USD hay cache miss. Chưa có cặp W1/W2 để so key/prefix/thời gian/cache write ở provider. Không được kết luận savings hay regression ngữ nghĩa từ lỗi quota này.

## Chi phí và tiêu chí thành công

Tính theo bucket provider: ordinary = input − cached − cache_write; giá USD/triệu token ordinary=4, cached=0,40, write 30m=5, output=20. Cache write là một bucket thay thế, không cộng thêm phí trên cùng token. Web search tách riêng 0,01 USD/tool call. [Giá model chính thức](https://developers.openai.com/api/docs/models/gpt-5.6-sol), [cơ chế và giá cache chính thức](https://developers.openai.com/api/docs/guides/prompt-caching).

| Concept baseline_current | Input | Ordinary | Cached | Cache write | Output | Input USD | Token USD gồm output |
|---|---:|---:|---:|---:|---:|---:|---:|
| W1 | 9.331 | 3 | 0 | 9.328 | 273 | 0,046652 | 0,052112 |
| W2 | 10.715 | 3 | 0 | 10.712 | 274 | 0,053572 | 0,059052 |
| Cặp | 20.046 | 6 | 0 | 20.040 | 547 | **0,100224** | **0,111164** |

Toàn cặp baseline_current: **0,8712832 USD** token, **0,05 USD** cho 5 web search calls, tổng **0,9212832 USD**, 11 Responses calls. Đây là ước tính theo usage, không phải hóa đơn được xác nhận.

Thí nghiệm 2 không có usage, không có Concept hit/write hay chi phí cặp để đối chiếu. Chưa đạt tiêu chí cached_tokens W2 > 0 và giảm Concept combined input billing. Không quy biến thiên output/search ngẫu nhiên thành tiết kiệm nhân quả.

## Khôi phục và kiểm tra cuối

Đã khôi phục ba tracked files từng sửa bằng bytes từ đúng HEAD. Tất cả **270 tracked files** khớp SHA-256 của baseline_current đã lưu. Có 10 file M2 vốn dùng CRLF trong working tree nên khác bytes blob Git nhưng được Git chuẩn hóa thành diff rỗng; chúng vẫn khớp baseline đã lưu, không bị sửa. Không tự đổi line endings của các file được bảo vệ. Chi tiết: `explicit_restoration.json`.

Sau khôi phục: local **117/117 PASS**, Authoring upstream **33/33 PASS**, socket bị chặn; `compileall` **65 file PASS**, `git diff --check` PASS; tracked diff/index rỗng, chỉ `m3_evidence/` untracked. Quét khóa API và kiểm tra manifest thí nghiệm 1 PASS. Logs: `explicit_final_local.txt`, `explicit_final_upstream_authoring.txt`, `explicit_final_checks.json`.

README/VERIFICATION không đổi vì M3 chưa thành công. Không stage, commit, push, tag, branch, deploy hoặc sửa remotes; không bắt đầu M4/frontend. Không sửa global memory.
