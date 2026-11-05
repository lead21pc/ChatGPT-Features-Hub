# GPT-6.1 Sol — closeout W1/W2, 2026-11-05

**GPT-6.1 Sol = LIVE VERIFIED CANDIDATE FOR TESTED CENTRAL HUB W1/W2 SCOPE**

Không phải replacement đã kiểm chứng toàn cục cho mọi đường Central Hub. Model hiện cấu hình/ưu tiên cho thử nghiệm và runtime local là `gpt-6.1-sol`: đã đọc riêng model string trong `config.json` được Git ignore; cả 11 response trong evidence cũng ghi model này. `app.read_config()` đọc model từ config, request dùng `config["model"]`; không cần sửa code/config. Closeout chỉ review evidence live đã có, không gọi lại API. **M3 COMPLETE FOR ACCEPTED SCOPE; M4 NOT STARTED.** Không triển khai MCP hoặc redesign.

## Nguồn và provenance

Baseline: repo `Central-Hub-Local`, branch `main`, HEAD `13dd18bbacf899ea9d1bb745357587731f5f8207`; index/worktree sạch, config/session được ignore. Hai raw session ghi cùng HEAD, snapshot hash tracked source trước/sau không đổi và khớp nội dung local trước closeout.

| Raw evidence local, không commit | Thời gian UTC | SHA-256 |
| --- | --- | --- |
| `sessions/gpt61_explicit_workload_1.json` | 2026-11-05 14:56:01–14:58:17 | `ac2ad3866fc686644c28ea1206c2734b21d6fb1753b0ae12740841d76068957d` |
| `sessions/gpt61_explicit_workload_2.json` | 2026-11-05 14:58:45–15:01:05 | `451b6334bebe607279fb61cea104b1bdc4e818fc59efd8d77eb3c49246502e02` |

Review này lưu kết luận và số liệu từ raw session, không thay thế khả năng kiểm tra lại toàn payload/response khi thiếu raw local. Đối chiếu lịch sử với [explicit_retry_metrics.json](explicit_retry_metrics.json), [EXPERIMENT_2_RETRY_REVIEW.md](EXPERIMENT_2_RETRY_REVIEW.md) và [M3_FINAL_STATUS.md](M3_FINAL_STATUS.md). Giữ nguyên các file đó; các phát biểu không đổi model trong promotion M3 mô tả campaign GPT-5.6 Sol lịch sử.

## Kết quả đã đối chiếu

- **W1: 7/7 Responses calls completed, semantic PASS trong tested Authoring + Concept scope.** Root chọn Authoring + Concept; admission GENERIC + BRAINSTORM active, không isolated. Contributor và Concept selection chỉ chọn `HUB-CAP-BRAINSTORM` từ span tường minh. Prompt cuối giữ sáu hướng song song, chưa xếp hạng/chấp nhận; dừng ở prompt cho model khác, không chạy target. Không AIS/tools.
- **W2: 4/4 Responses calls completed, semantic PASS trong tested Technical + Concept + AIS scope.** Root chọn đúng ba package, không Authoring. Concept chỉ chọn Brainstorm. Hub final tách bằng chứng tài liệu, ba ứng viên kiến trúc song song và chẩn đoán Technical; không chọn/chấp nhận ứng viên hoặc khẳng định tích hợp đã chạy.
- Cả hai: `error=null`, `max_retries=0`; blocker rỗng ở root, admission/contributor/Concept khi có và trace cuối. Chỉ request AIS có tools `web_search`; không target execution trong record đã thử. Nhắc tới M4 trong prompt không mở M4.
- **Explicit Concept cache vẫn hoạt động:** W1 `hub_t8_concept` ghi `cache_write_tokens=6161`; W2 cùng pha đọc `cached_tokens=6161`, write=0.
- **AIS evidence-source compliance PASS; search-discovery boundary PARTIAL.** Các citation AIS thuộc bốn trang `v2.tauri.app`: `/develop/sidecar/`, `/reference/config/`, `/reference/javascript/shell/`, `/plugin/shell/`; Hub final dùng nguồn Tauri chính thức. Các open-page action được ghi chỉ tới sidecar và JavaScript shell; không suy ra đã mở riêng hoặc đọc toàn bộ mọi trang được trích.
- Discovery query ghi `site.v2.tauri.app ...`, không phải giới hạn domain tuyệt đối; `source_urls` có cả Reddit, mirror và nguồn ngoài Tauri. Đây là tập discovery, không đồng nghĩa các nguồn đó được dùng làm evidence. Không nâng thành strict discovery-boundary PASS hoặc global AIS failure.

Semantic PASS là kết luận review đầu ra trong hai workload này, không được suy ra chỉ từ response `completed`. Không chứng minh mọi đường T0–T9, activation/persistence, mọi tổ hợp package hoặc toàn hệ thống chuyển model thành công. Ưu tiên model hiện tại không quyết định kiến trúc MCP/kênh tương lai.

## Chi phí ước tính trong phép thử

Dùng snapshot giá lưu trong cả hai raw session: provenance `User-supplied official-doc snapshot; evidence only`. GPT-6.1 Sol: ordinary input $2/M, cached input $0.10/M, 30m cache write $2.50/M, output $10/M, web search $0.01/action. Đây là bảng giá dùng cho phép thử, không phải xác minh giá hiện hành độc lập trong closeout hay hóa đơn thực tế.

Tính mỗi call: `ordinary = input_tokens - cached_tokens - cache_write_tokens`; chi phí token = `(ordinary*2 + cached*0.10 + write*2.50 + output*10)/1_000_000`, rồi cộng web-search actions. Search content đã nằm trong input usage khi provider báo, không cộng ước lượng riêng.

| Workload | Token cost USD | Web-search actions / USD | Tổng USD |
| --- | ---: | ---: | ---: |
| W1 | 0.2434720 | 0 / 0 | 0.2434720 |
| W2 | 0.2128785 | 5 / 0.05 | 0.2628785 |
| Pair | 0.4563505 | 5 / 0.05 | **0.5063505 ≈ 0.506351** |

W2 ghi một search và bốn open-page actions completed. GPT-5.6 Sol M3 retry pair lịch sử là **$0.914486**, gồm bốn web-search actions. Chênh lệch pair **$0.4081355**, tương đương **44.6300% thấp hơn trên đúng hai workload** theo các bảng giá tương ứng. Cache warmth, output và AIS/search usage khác nhau; không phải so sánh chỉ thay model, không phân bổ toàn bộ chênh lệch cho model/cache và không tuyên bố tiết kiệm phổ quát. Provenance và kết quả GPT-5.6 Sol vẫn giữ nguyên.

## Kiểm chứng closeout ngoại tuyến

- Full local suite: **119/119 PASS** qua `unittest.defaultTestLoader.discover('.', pattern='test_*.py')`.
- Focused upstream Authoring: **33/33 PASS**, dùng đúng năm suite như M3: `test_authoring_isolation`, `test_authoring_candidate`, `test_authoring_m1`, `test_authoring_m2`, `test_authoring_m4`. Tên suite cuối là kiểm thử upstream hiện có, không phải mở milestone M4 local.
- Cả hai lượt chặn `socket.socket.connect`, `connect_ex`, `socket.create_connection` toàn cục; request dùng mock/MockTransport. Static PASS không tạo thêm live evidence.
- Compile **45 file Python được Git theo dõi** bằng `compile(source, path, 'exec')`: PASS, không thực thi harness live.
- Diff/whitespace, đối chiếu bảo toàn lịch sử và quét exact configured key trên toàn bộ staged files được kiểm tra trước local commit. Chỉ README, phần status mới đầu VERIFICATION và review này thuộc phạm vi ghi; raw sessions/config không stage.

Không push, deploy, tạo branch/tag hoặc chạy thêm live API trong closeout.
