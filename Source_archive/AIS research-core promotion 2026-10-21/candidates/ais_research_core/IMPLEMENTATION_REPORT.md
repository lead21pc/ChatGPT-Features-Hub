# AIS research core — báo cáo candidate local

Ngày: 2026-10-20. Trạng thái: CANDIDATE, không active, chưa triển khai.

Repository: `<WORKSHOPS_REPO>`.
Branch: `main`. HEAD trước thực hiện: `603bd01af7e5f0a55d34e8a6cb3070f9773dbe15`.
Working tree ban đầu sạch; không có thay đổi staged. Không kiểm tra remote trong tác vụ này.

Phạm vi đọc: hướng dẫn repository và SYSTEM_CONTEXT; Hub CI/Router/Architecture/Catalog; toàn bộ pipeline/router AIS, 28 ca AIS, đặc tả Hub và test/helpers liên quan; Router handoff Revamp; hai tài liệu bổ sung trên ổ D. Phạm vi ghi: bộ candidate này và một tệp kiểm tra trong `Central Hub/tests`. Không ghi vào Revamp hay nguồn phụ thuộc.

## Kết quả đối chiếu và chẩn đoán

ACCEPT WITH LOCAL CORRECTION: ý định mở rộng AIS tương thích với baseline. Sửa cục bộ cách mô tả nguyên nhân: không coi lỗi hồi cứu là lỗi nội bộ AIS đã được xác lập. Giữ nguyên quyền Hub, thêm đúng một stage RESEARCH_STRATEGY và một trường research_strategy trong search_contract hiện có.

- OBSERVED FAILURE / USER_REPORTED: báo cáo hồi cứu phủ nhận search trong khi trace UI cho thấy search đã chạy. Handoff bổ sung ghi các trace “Searched 15 websites” và “Searched 11 websites”. Tác vụ này không trực tiếp xem lại ảnh C.png hay tái hiện runtime.
- SUPPORTED RISK / xác nhận từ tệp: `failures.tool_not_executed` hiện yêu cầu báo chưa thực hiện nhưng không phân biệt rõ trace vắng mặt với bằng chứng không thực thi. Return hiện có actions actually performed và actual source reads, nhưng chưa buộc trạng thái/basis thực thi theo từng hành động. Khoảng thiếu này cho phép báo cáo thiếu căn cứ; chưa đủ để kết luận nó gây ra lỗi runtime đã báo.
- Xác nhận từ tệp: AIS hiện có tám stage, ba mode và kỷ luật nguồn/phạm vi đủ để mở rộng cục bộ; không có stage chiến lược độ sâu/executor/tài nguyên. Đây là phần mở rộng được yêu cầu, không phải bằng chứng rằng toàn bộ AIS đang hỏng.
- Đường liên quan: Hub giao mục tiêu -> AIS khóa phạm vi/nguồn -> nghiên cứu -> kiểm tra support/coverage -> trả Hub. Chỉnh tại hợp đồng nghiên cứu và đầu ra AIS; không chuyển chủ sở hữu global claim state hay tự đánh giá toàn lượt sang AIS.
- Handoff AIS không có tại đường dẫn repository được yêu cầu; đã đọc bản thay thế `<HANDOFF_DIR>/CENTRAL_HUB_AIS_STABILIZATION_CURRENT_REPLACEMENT.md`. Router Revamp chỉ đăng ký REVAMP_SYSTEM_CURRENT; không tự bổ sung entry. Đã đọc `<HANDOFF_DIR>/PROJECT_VERIFICATION_PHILOSOPHY.md` sau khi người dùng cung cấp; không sao chép hai tệp này vào runtime.
- H36 trong repository còn ghi corrected rerun NOT_RUN. Yêu cầu và handoff mới hơn ghi NONE -> NONE -> AIS -> NONE thành công. Giữ đây là kết quả cũ do người dùng báo, không tuyên bố đã tái hiện; không mở lại routing miss hay sửa lịch sử trong tác vụ candidate này.

Tiêu chí chấp nhận: baseline active nguyên byte; đủ 20 tình huống bắt buộc; UNKNOWN khi không quan sát được thực thi; trace trực tiếp ưu tiên hơn hồi cứu; trace trực tiếp mâu thuẫn giữ CONFLICTED; một stage mới; không tạo package/registry/gate độc lập; giữ nguồn đã đọc, support và phạm vi qua fallback; toàn bộ suite đạt. Kế hoạch đã thực hiện: mở rộng cặp AIS trong vùng candidates, thêm đặc tả và kiểm tra tập trung, kiểm tra hồi quy toàn Hub.

## Các tệp mới và lý do

| Tệp tính từ Central Hub | Vai trò cần thiết |
| --- | --- |
| `candidates/ais_research_core/AIS_PIPELINE_v1.1-candidate.md` | Điểm vào candidate; tham chiếu đúng router candidate; mô tả nghiên cứu lặp có đọc nguồn, chiến lược và bằng chứng thực thi. |
| `candidates/ais_research_core/AIS_ROUTER_v1.2-candidate.yaml` | Hợp đồng chi tiết: RESEARCH_STRATEGY; NORMAL/THOROUGH/EXTENSIVE; CHAT_GUIDED/DEEP_RESEARCH/WORK; tài nguyên, transition, fallback và đầu ra quan sát được. |
| `candidates/ais_research_core/RESEARCH_CORE_TEST_CASES.md` | 26 ca, gồm 20 ca yêu cầu; tiêu chí live, ghi trace và điều kiện đánh giá ổn định. |
| `tests/test_ais_research_candidate.py` | Bốn kiểm tra hợp đồng/bảo toàn baseline và 26 fixture đặc tả; dùng parser YAML nghiêm ngặt hiện có. Không phải bộ thực thi AIS. |
| `candidates/ais_research_core/IMPLEMENTATION_REPORT.md` | Ghi phạm vi, căn cứ, kết quả và giới hạn để xét duyệt candidate. Không phải control runtime hay handoff Revamp. |

CHAT_GUIDED giữ vai trò nền tảng mạnh. Hai executor còn lại chỉ là các nhánh trong AIS, cần đường gọi thật và ủy quyền; ưu tiên không chứng minh đã thực thi. Không hard-code quota. UNKNOWN không được đổi thành AVAILABLE. Khi giảm executor, giữ chứng cứ đã hỗ trợ, chỉ lập lại công việc chưa giải quyết và báo phần coverage bị giảm.

Mọi nguồn active, Hub core, Catalog/binding, ImageT, Prompt Authoring và handoff Revamp được giữ nguyên. Cả 28 ca AIS và các tiêu chí chấp nhận cũ giữ nguyên byte; ba mode, mode_resolution và source_policy cũng giữ nguyên trong candidate. Không archive predecessor vì cặp active vẫn được giữ để hoạt động song song; candidate chưa thay thế chúng.

## Kiểm chứng

Thực hiện từ thư mục Central Hub:

```powershell
python -B -m unittest discover -s tests -p test_ais_research_candidate.py -v
python -B -m unittest discover -s tests -v
git -c core.longpaths=true diff --check -- .
```

Kết quả: suite tập trung 30/30 PASS; toàn Hub 104/104 PASS, gồm 74 kiểm tra baseline và 30 kiểm tra mới. STATIC CONTRACT TEST: PASS. SPEC SIMULATION: 26 fixture PASS. Các fixture có sẵn phân loại nhiệm vụ/bằng chứng; không chứng minh model nhận diện đúng ngôn ngữ hay tuân thủ pipeline.

Parser hiện có kiểm toàn bộ YAML ngoài archive, từ chối duplicate/merge keys, anchors, aliases, custom tags và scalar mơ hồ. Kiểm tra mới xác nhận UTF-8 không BOM, LF/EOF/whitespace, đúng tên tham chiếu, một stage bổ sung, không admission trong Catalog, cùng SHA-256 của chín tệp baseline trọng yếu. Không sửa test cũ để đạt PASS. Không có lỗi suite cần phân loại hoặc sửa ngoài phạm vi.

`git diff` tracked và index không có thay đổi. Năm tệp mới để untracked, chưa staged. Vì git diff thông thường không bao gồm untracked, whitespace của các tệp mới còn được kiểm trực tiếp bằng suite. Lệnh Git không bật longpaths gặp đường archive quá dài ngoài phạm vi; lệnh kiểm tra giới hạn Central Hub với `-c core.longpaths=true` đạt, không đổi cấu hình repository.

## Giới hạn và thử live kế tiếp

Candidate sẵn sàng về mặt hợp đồng cho thử live có kiểm soát; chưa đủ bằng chứng để gọi là AIS ổn định trong hội thoại thực tế. CONTROLLED LIVE: NOT_RUN. REAL-CONTEXT STRESS của candidate: NOT_RUN. Không tuyên bố LIVE VERIFIED.

Đường gọi Deep Research, trạng thái quota và khả năng Chat -> Work của Project đích chưa được kiểm chứng trong tác vụ này. Không cần khẳng định capability công khai hiện hành để viết hợp đồng có điều kiện; không dùng forum làm bằng chứng khả dụng. Chỉ đường gọi/transition thật được quan sát tại surface thử mới cho phép thực thi. Nếu chỉ có Project context thì chuẩn bị handoff đủ tám trường, không khẳng định chuyển toàn lịch sử. Không có đường gọi thì fallback được phép hoặc giữ unresolved.

Khi có ủy quyền live riêng: dùng môi trường thử tương thích, admission tường minh cho đúng cặp candidate; binding active hiện tại vẫn trỏ cặp cũ nên không thể coi upload candidate là tự chọn được. Không tự sửa stack hay binding đang dùng. Chạy nhóm quan sát trace/đọc/support trước, rồi chọn lane và fallback theo các ca trong RESEARCH_CORE_TEST_CASES. Ghi đúng model/surface/cặp nguồn, trace, nguồn đã đọc, support và giới hạn. Những đường nền tảng không khả dụng phải giữ UNKNOWN/UNAVAILABLE; fixture mô phỏng không được ghi live PASS. Sau đường chạy chuẩn bị, cần một thử hội thoại thực tế có tích lũy ngữ cảnh trước khi kết luận độ bền.

Không sửa handoff trong tác vụ này. Delta đề xuất cho Revamp nếu được cho phép sau: đã có cặp candidate local và 104 kiểm tra tĩnh đạt; 28 ca cũ còn nguyên; nguyên nhân runtime/chủ sở hữu lỗi hồi cứu vẫn chưa xác lập; live candidate và invocation tại Project đích chưa chạy. Tệp này không tự chấp nhận delta đó.

Không stage, commit, push, tạo branch/worktree, tag/release, triển khai Project, sửa Library hay thay đổi remote. Không bắt đầu milestone kế tiếp.
