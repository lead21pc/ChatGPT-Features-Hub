# Thí nghiệm 2 retry: explicit Concept cache — LIVE PASS

Ngày 2026-11-05, người dùng mở lại M3 sau khi tăng project spend limit. Candidate explicit-cache cũ được áp lại trên current `main`, đồng thời sửa chuỗi lỗi sai đã được ghi nhận trong review lịch sử. Không tạo experiment thứ ba.

## Kết quả live

- W1: 7/7 Responses calls completed, error = null.
- W2: 4/4 Responses calls completed, error = null.
- W2 Concept: `cached_tokens = 6161`, `cache_write_tokens = 0`.
- W1 Concept đã ghi đúng prefix dùng lại: `cache_write_tokens = 6161`.
- Concept leaf selection vẫn chỉ chọn `HUB-CAP-BRAINSTORM` trong cả hai workload, blocker rỗng.
- W1 giữ Authoring GENERIC + BRAINSTORM, không AIS/tools/target execution.
- W2 giữ Technical + Concept + AIS, AIS dùng native web search, không Authoring/target execution.
- Không có retry.

## Chi phí

Theo giá GPT-5.6 Sol hiện hành được dùng trong M3 ($4/M ordinary input, $0.40/M cached input, $5/M 30m cache write, $20/M output; web search $0.01/action):

- W1 token cost: $0.450049.
- W2 token cost: $0.424437.
- W2 web search actions: 4 = $0.04.
- Retry pair estimated total: $0.914486.
- Baseline Concept combined input billing: $0.100224.
- Retry Concept combined input billing: $0.0619934.
- Concept input saving: $0.0382306 = 38.145%.

Không dùng whole-pair delta làm causal savings metric vì W1 bắt đầu với cache chung nguội hơn baseline cũ và output/AIS/search thay đổi ngẫu nhiên. Success gate của experiment là W2 Concept cache reuse + giảm Concept combined input billing + giữ scoped semantics; cả ba đã đạt.

## Disposition

Experiment 2: LIVE PASS / TARGET ACHIEVED.

Promote đúng candidate nhỏ này vào runtime local:
- explicit 30m cache breakpoint/key chỉ cho stable Concept selection prefix;
- không đổi model, reasoning, verbosity, call count, tools hoặc package semantics;
- không thêm prewarm/retry/call merge;
- giữ toàn bộ evidence lịch sử của experiment 1 và lần quota-blocked trước.

M3 hoàn tất ở mức token/cache optimization đã chứng minh. Không chạy experiment thứ ba trong campaign này.
