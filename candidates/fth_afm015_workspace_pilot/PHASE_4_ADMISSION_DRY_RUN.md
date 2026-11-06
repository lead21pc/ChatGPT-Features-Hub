# AFM-015 — Phase 4 round-trip dry run

`PHASE_4_FTH_ROUND_TRIP_DRY_RUN_PASS` — `NO_ADMISSION_PERFORMED`. [Patch đề xuất](PHASE_4_AFM015_PROPOSED.patch) là `NON_AUTHORITATIVE_PROPOSED_PATCH`, không phải FTH source. `PATCHABLE != ACCEPTED`; `DRY-RUN PASS != ADMISSION`.

## Baseline và fixture

Preflight repository root `<WORKSHOPS_REPO>`, branch `main`, HEAD `bad3cf55ecd2a58bb0ee47d51154c93cf13ff9f3`; `origin/main` cục bộ và remote main cùng SHA, working tree và index sạch. AFM-015 source và snapshot byte-equal: 6.022 byte, SHA-256 `8d14eb73c4587db297d46c9804f9d262dc605513a93d13ed3c2b6f0eb58d27d5`. Đoạn AF-HN-OPEN-006–009 của envelope khớp current `92`: `PHASE_4_BASELINE_VALID`.

Fixtures chỉ được chọn để kiểm coverage, không là tác giả chấp nhận chất liệu. P1 = [Phase 3 A2](PHASE_3_SEMANTIC_RECONCILIATION.md), P2 = B1, N1 = C-A; output nguyên văn và provenance Phase 2 ở [PHASE_2_RUNTIME_OUTPUTS.md](PHASE_2_RUNTIME_OUTPUTS.md). Không rerun A/B/C.

## Vị trí và hiệu ứng dự kiến

| Fixture | Vị trí đề xuất | Hiệu ứng nếu sau này được chấp nhận | Giới hạn và owner |
| --- | --- | --- | --- |
| P1 / A2 | §5.5, sau qualifier về phục sức chức vụ/phẩm cấp/nghi lễ | Lịch sử cá nhân hoặc chuyển giao một món trang phục không tự xóa/chuyển nguồn gốc văn hóa của nó. | AFM-015: không chốt tập quán tặng/thừa kế, bảo tồn, ý nghĩa xã hội hay quyền với mọi phục sức; AF-HN-OPEN-007 vẫn OPEN. |
| P2 / B1 | §5.7, sau chuẩn chung và các qualifier | Văn bản chung có thể kèm bản dịch/giải thích bằng ngôn ngữ vùng để hỗ trợ người dùng. | AFM-015 cho giao diện ngôn ngữ; chuẩn tiếng Trung hiện đại, qualifier về dân và văn kiện địa phương giữ nguyên. Giá trị pháp lý, phạm vi, quy trình dịch, dạng chữ và vai trò vẫn chưa xác lập; AF-HN-OPEN-008 vẫn OPEN. |

Nếu tác giả sau này chấp nhận đúng P2, phần -008 có thể được thu hẹp chỉ ở khả năng tồn tại lớp dịch/giải thích hỗ trợ cho văn bản chung; không từ đó suy nghĩa vụ áp dụng, phạm vi tài liệu, giá trị pháp lý, quy trình hay nhân sự. Ghi nhận narrowing này trong xử lý OPEN sau quyết định riêng; `92` không được sửa trong dry run.

## Negative fixture N1

C-A gồm địa vị tự trị hành chính, quyền lực lãnh thổ, hội đồng/chính quyền liên vùng, quyền ràng buộc và hệ quả ngân sách/tư pháp/bổ nhiệm. Những phần đó không có trong patch AFM-015. `ROUTE TO AFM-012 / AF-HN-OPEN-006 IF PURSUED`. Loại khỏi patch theo owner không đồng nghĩa bác ý tưởng tương lai.

## Kiểm tra và kết quả

- `git apply --check` với patch trên working tree: PASS; không áp patch vào CURRENT.
- Dựng candidate trong bộ nhớ từ unified diff: hai câu chèn, không xóa dòng; toàn bộ nội dung baseline giữ nguyên theo thứ tự. Đối chiếu ngữ nghĩa với AFM-015, `92`, Phase 3 và ranh giới owner: PASS cho P1/P2/N1 trong phạm vi fixture.
- Không có nội dung tự trị/cơ quan chính quyền được thêm; -007 và -008 chưa được giải quyết. Không có thay đổi FTH CURRENT, `92` hay control Hub; kiểm hash/trạng thái sau dry run.
- FTH `build_consolidation.py --check`: PASS, 17 current modules / 21 current hashes; kiểm cấu trúc/hash, không chứng minh canon hay runtime.
- Patch có thể kiểm tra và bỏ đi mà không cần migration; đây là khả năng kỹ thuật/semantic bounded, không là quyết định P1 hoặc P2 nên được nhập. C-A không bị bác như ý tưởng tương lai. Admission đòi hỏi quyết định riêng của tác giả.
