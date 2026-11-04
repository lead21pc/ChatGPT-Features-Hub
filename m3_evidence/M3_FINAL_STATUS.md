# Trạng thái cuối M3: CLOSED

Quyết định người dùng ngày 2026-11-05: đóng M3 và workstream Central Hub local/API. Đây là quyết định chấp nhận một backup path hoạt động, không phải xác nhận experiment tối ưu thành công.

- **CENTRAL HUB LOCAL/API: BACKUP. FUNCTIONAL STATUS: VERIFIED + LIVE VERIFIED**, dựa trên static verification, live API verification M1/M2 và các workload đã chạy trong phạm vi bằng chứng hiện có. Không dùng làm runtime chính cần tiếp tục tối ưu chi phí.
- **M3: CLOSED. TOKEN/CACHE OPTIMIZATION: CLOSED / NO FURTHER WORK PLANNED.** Không yêu cầu API cost thấp hơn subscription. Không có retry mặc định hoặc experiment bổ sung; chỉ mở lại khi người dùng yêu cầu rõ ràng.
- Experiment 1: **FAILED TARGET**; đã live-run nhưng Concept W2 không có cache reuse như mục tiêu. Báo cáo và số liệu gốc trong [REPORT.md](REPORT.md) giữ nguyên.
- Experiment 2 explicit cache: **STATIC VERIFIED / LIVE NOT ESTABLISHED / CLOSED WITHOUT PROMOTION**. Live attempt bị chặn ngay root W1 bởi `429 project_spend_limit_exceeded`, trước Concept call. Không có bằng chứng live xác nhận Concept explicit-cache path, không có claim cache hit/savings hoặc live PASS.
- Runtime giữ nguyên baseline đã restore `8f5487ca8b124edb339192a9704b5d74157bcf00`, branch `main`. Không áp lại `explicit_candidate_runtime.patch`, không sửa pipeline/runtime để tối ưu token. Toàn bộ evidence, patch và runner được giữ làm lịch sử, không phải runtime active.
- **M4: NOT STARTED.** Wrap-up không gọi API live; chỉ kiểm chứng local/static. Không stage, commit hoặc push trong lượt đóng này.

Trạng thái `NOT COMPLETE` trong các báo cáo experiment là kết quả lịch sử trước quyết định đóng mục tiêu tối ưu, không phải chỉ dẫn tiếp tục công việc. [EXPERIMENT_2_REVIEW.md](EXPERIMENT_2_REVIEW.md) vẫn giữ nguyên giới hạn bằng chứng và lỗi live gốc.

## Hồ sơ trước quyết định đóng — M3 NOT COMPLETE

Thí nghiệm 1 thất bại vì W2 Concept không có cache reuse; bằng chứng gốc được giữ nguyên. Thí nghiệm 2 đã qua kiểm tra tĩnh nhưng live bị chặn ngay tại root W1 bởi `429 project_spend_limit_exceeded`, chưa tới Concept. Không retry hoặc chạy W2/thí nghiệm thứ ba.

Không có số đo cache hit/write, ngữ nghĩa M2 hoặc chi phí live của thí nghiệm 2. Runtime đã được khôi phục; toàn bộ 270 tracked files khớp baseline bytes đã lưu, tracked diff và index rỗng. HEAD/ref local origin/main cùng `8f5487ca8b124edb339192a9704b5d74157bcf00`, branch main; không xác minh được remote trực tiếp vì thiếu credentials.

Kiểm tra cuối: local 117/117, Authoring upstream 33/33, compileall 65 file, diff check, quét API key và bảo toàn thí nghiệm 1 đều PASS. Chỉ còn `m3_evidence/` untracked. Không stage/commit/push hoặc triển khai M4.

Chi tiết và giới hạn: [EXPERIMENT_2_REVIEW.md](EXPERIMENT_2_REVIEW.md). Usage baseline và trạng thái không có usage mới: [explicit_metrics.json](explicit_metrics.json). Lỗi live nguyên bản: [explicit_workload_1.json](explicit_workload_1.json).
