# Trạng thái cuối M3: COMPLETE

Ngày 2026-11-05, người dùng mở lại M3 sau khi project spend limit được tăng để tiếp tục đúng thí nghiệm explicit cache đã bị quota chặn trước đó.

- **CENTRAL HUB LOCAL/API: BACKUP. FUNCTIONAL STATUS: VERIFIED + LIVE VERIFIED.**
- **M3 TOKEN/CACHE OPTIMIZATION: COMPLETE FOR ACCEPTED SCOPE.**
- Experiment 1 giữ nguyên **FAILED TARGET**: stable-prefix reorder không tạo Concept cache reuse.
- Experiment 2 explicit cache: **STATIC VERIFIED + LIVE VERIFIED / TARGET ACHIEVED** sau retry được người dùng cho phép. W1 7/7 call và W2 4/4 call hoàn tất, không retry.
- W1 Concept ghi 6.161 cache-write tokens cho stable prefix; W2 Concept đọc lại đúng 6.161 cached tokens.
- Baseline Concept combined input billing: **$0.100224**. Retry: **$0.0619934**. Giảm **$0.0382306 / 38.145%** tại đúng bucket Concept input được tối ưu.
- Tổng retry pair ước tính **$0.914486**, gồm token + 4 web-search actions. Không dùng whole-pair delta làm causal savings vì cache warmth/output/AIS/search khác nhau giữa các lần chạy.
- Scoped semantics giữ nguyên: W1 Authoring GENERIC + BRAINSTORM; W2 Technical + Concept + AIS; Concept chỉ chọn Brainstorm, blocker rỗng; không target execution.
- Candidate explicit Concept cache hiện được promote vào runtime local. Không thêm prewarm, retry, call merge, model/reasoning/verbosity change hoặc experiment thứ ba.
- Sai chuỗi lỗi T7 trong candidate lịch sử được sửa thành lỗi Concept/T8 phù hợp trước promotion; validation/failure behavior không đổi.
- **M4: NOT STARTED.**

Bằng chứng mới:
- [EXPERIMENT_2_RETRY_REVIEW.md](EXPERIMENT_2_RETRY_REVIEW.md)
- [explicit_retry_metrics.json](explicit_retry_metrics.json)
- [explicit_retry_workload_1.json](explicit_retry_workload_1.json)
- [explicit_retry_workload_2.json](explicit_retry_workload_2.json)

Hồ sơ quota-blocked trước đó và experiment 1 được giữ nguyên làm lịch sử. Các claim `LIVE NOT ESTABLISHED`, `M3 NOT COMPLETE` hoặc `CLOSED WITHOUT PROMOTION` trong file review cũ chỉ mô tả checkpoint trước retry này, không phải trạng thái M3 hiện hành.

Promotion chỉ local cho đến khi Git state cuối được kiểm chứng. Không push hoặc deploy chỉ từ status file này.
