# AIS — promotion local và chỉnh sửa lõi nghiên cứu chính thức

Trạng thái hiện hành ngày 2026-10-21: AIS_PIPELINE_v1.1.md / AIS_ROUTER_v1.2.yaml là revision OFFICIAL/ACTIVE trong repository, đã đơn giản hóa tại chỗ sau promotion. PROJECT DEPLOYMENT: NOT_PERFORMED. Không có promotion mới, version song song, stage/commit/push, upload Project hay sửa Library trong đợt chỉnh sửa này.

## Baseline thực tế và lịch sử

Repository: `<WORKSHOPS_REPO>`; branch `main`; HEAD `61a319daa75efa0d51897ca0072843efa0a12067`, commit cuối `Add AIS research-core candidate and execution observability contracts`.

Khi bắt đầu đợt đơn giản hóa, working tree đã giữ nguyên thay đổi chưa commit từ promotion trước: sáu tệp tracked sửa, bảy đường nguồn chuyển vào archive và mười ba tệp untracked gồm đích archive, receipt cùng nguồn/test/report mới. Index rỗng. Bản local đã là official pipeline v1.1/router v1.2; HEAD cũ không được dùng để thay thế working tree hiện tại. Không có thay đổi không liên quan cần stash, chuyển branch hoặc ghi đè.

Promotion trước chuyển pipeline v1.0/router v1.1 và bộ candidate/test cũ vào `Source_archive/AIS research-core promotion 2026-10-21/`, giữ nguyên byte theo `Source_archive/AIS_PROMOTION_ARCHIVE_RECEIPT_2026-10-21.json` (7/7 hash khớp). Việc đó đã hoàn thành trước tác vụ hiện tại. Các tệp archive và receipt không được sửa hoặc tạo lại; không có đọc archive làm runtime fallback. Đợt này là sửa tại chỗ cùng revision, không tạo artifact thay thế hoặc archive mới.

## Chẩn đoán và thay đổi

Revision trước đã chuyển sang ưu tiên Chat khi đủ, nhưng vẫn chứa một bộ chọn ba nhánh CHAT_GUIDED / DEEP_RESEARCH / WORK: preferred/selected executor, nhận xét task-shape/lợi thế, observed executor state, quota/resource enums, Work transition states, bounded Work handoff và fallback theo executor. Oracle vẫn mô phỏng các quyết định đó. Cơ chế này vượt mục tiêu AIS vừa được người dùng thu hẹp: nghiên cứu câu hỏi được Hub giao rồi trả chứng cứ để Hub tiếp tục FSP/IT hoặc phần việc gốc. Không có lỗi mới trong routing Hub được chứng minh.

Đã bỏ phần quyết định/chuyển executor khỏi research_strategy, research_policy, các stage và oracle; bỏ quota chọn sản phẩm, Work transition/handoff, lý do escalation và thứ tự fallback giữa sản phẩm. Không chuyển các cơ chế này sang một registry, framework hay lớp tùy chọn khác.

Giữ RESEARCH_STRATEGY vì sau SOURCE_AUTHORITY_GATE vẫn cần biến ý định về độ sâu thành yêu cầu chứng cứ cụ thể. Stage chỉ sở hữu depth/coverage; research_strategy còn đúng hai trường quality_target và coverage_expectations. Câu hỏi/material gaps tiếp tục ở question/unknowns; authority và stopping conditions ở source_authority/stop_condition. Không lặp schema hoặc thêm stage.

Giữ NORMAL / THOROUGH / EXTENSIVE: “nghiên cứu sâu” được hiểu ngữ nghĩa, nâng ít nhất THOROUGH; phạm vi thực sự rộng có thể dùng EXTENSIVE. Độ sâu tác động số nhánh chứng cứ cần giải quyết, source reads, đối chiếu/counterevidence và kỳ vọng dừng; không chỉ tăng độ dài câu trả lời. Không có khớp từ khóa literal hoặc tự gọi sản phẩm Deep Research.

Đường bình thường: nhu cầu chứng cứ chưa giải quyết -> search -> đọc nguồn quyết định -> đánh giá support -> tinh chỉnh query khi có căn cứ -> tìm nguồn gốc/counterexamples -> cập nhật coverage -> tiếp tục chỉ khi gap còn quan trọng trong giới hạn. Dừng khi đủ chứng cứ hoặc chạm giới hạn đã khóa; trả findings/support/conditions/conflicts/limits/gaps và quyền điều khiển cho Hub. THOROUGH/EXTENSIVE vẫn dùng Chat search/read khi nguồn/quyền truy cập đáp ứng; không hứa đủ chứng cứ chỉ vì đã chọn mức độ sâu.

Deep Research và Work không bị cấm toàn cục. Chỉ giữ một quy tắc trung thực với yêu cầu gọi tên sản phẩm qua surface thực sự có sẵn và được phép: báo giới hạn thực tế, không bịa launch/transfer, không âm thầm đổi sản phẩm, tôn trọng UX xác nhận của nền tảng. AIS không có bộ chọn hoặc bộ điều phối launch/handoff. Công cụ nào thực sự đã được quan sát sử dụng vẫn có thể được báo trong metadata execution; trường này không tham gia quyết định sản phẩm.

Giữ nguyên toàn bộ execution_observability so với bản promotion: INTENDED ACTION != ACTUAL EXECUTION; ACTUAL EXECUTION != SOURCE READ; SOURCE READ != CLAIM SUPPORT; EXECUTED / NOT_EXECUTED / UNKNOWN / CONFLICTED; trace trực tiếp ưu tiên hơn tự thuật hồi cứu, thiếu trace không chứng minh không chạy. Đã đổi mô tả limits trong return contract từ resource/fallback sang tool/access limits, không thay bằng chứng cần có.

Giữ nguyên modes, mode_resolution, source_policy, EVIDENCE_MERGE, protected state và quyền Hub. Tool availability/access và ủy quyền vẫn được kiểm trước search/read. Khi công cụ lỗi, giữ nhánh đã hỗ trợ, actual reads, điều kiện chứng cứ và gaps; chỉ lập lại unresolved/invalidated work trong scope/limit, không reset nghiên cứu hợp lệ hoặc hạ tiêu chuẩn chứng cứ.

## Chính xác các tệp sửa trong đợt này

| Tệp tính từ Central Hub | Lý do |
| --- | --- |
| `tool_pipelines/AIS/AIS_PIPELINE_v1.1.md` | Gỡ điều phối sản phẩm; mô tả guided research, depth, dừng và trả Hub. |
| `tool_pipelines/AIS/AIS_ROUTER_v1.2.yaml` | Thu research_strategy từ tám còn hai trường; thay lane/quota/transition policy bằng vòng search/read và xử lý lỗi công cụ thông thường. |
| `tests/test_ais_research_core.py` | Gỡ lane/resource/transition oracle; kiểm depth, coverage, dừng, gap, state protection và execution evidence. |
| `tool_pipelines/AIS/tests/RESEARCH_CORE_TEST_CASES.md` | Thay 34 fixture của revision trước bằng 26 ca phù hợp kiến trúc đã được thu hẹp; nêu rõ lý do thay các ca orchestration. |
| `README.md` | Bỏ mô tả chọn executor khi có lợi thế, ghi đúng lõi tìm/đọc nguồn và phạm vi AIS. |
| `tool_pipelines/AIS/AIS_PROMOTION_REPORT.md` | Cập nhật báo cáo hiện hành này, giữ rõ lịch sử promotion và trạng thái sau chỉnh sửa. |

Không tạo/move/xóa thêm tệp trong đợt này. Cả 28 ca AIS gốc giữ nguyên byte so với đầu đợt; không nới tiêu chí để đạt PASS. Test Hub/Router khác, CI, Architecture, Catalog, hướng dẫn migration và archive giữ nguyên so với baseline local đã promotion.

Catalog không cần sửa: AIS version 1.1, source_name/declared_source_path trỏ pipeline v1.1, pipeline yêu cầu đúng router v1.2; binding mode LEGACY_PROJECT_SOURCE, repository_revision OFFICIAL_ACTIVE và project_deployment NOT_PERFORMED vẫn nhất quán. Không có version active thứ hai.

## Kiểm chứng và giới hạn bằng chứng

Baseline đầu đợt: 112/112 PASS. Sau chỉnh sửa, chạy từ Central Hub:

```powershell
python -B -m unittest discover -s tests -p test_ais_research_core.py -v
python -B -m unittest discover -s tests -v
git -c core.longpaths=true diff --check -- .
```

STATIC VERIFIED: suite AIS 30/30 PASS (26 fixture và bốn kiểm tra hợp đồng); toàn Hub 104/104 PASS. Số lượng giảm vì bỏ các fixture của cơ chế ba nhánh đã bị bác, không phải bỏ ca hồi quy AIS gốc hay sửa unrelated tests. Một lần chạy trung gian còn đọc đặc tả 34 ca chưa đồng bộ nên kiểm inventory thất bại; sau khi đặc tả được sửa đúng yêu cầu thu hẹp thì đạt, không có failure còn mở.

Kiểm parser YAML bảo thủ, duplicate/merge keys, anchors/aliases/custom tags, UTF-8 không BOM, whitespace, tham chiếu, official binding, Hub owners, 28 ca gốc và archive hashes đều đạt. Bộ fixture cung cấp phân loại depth/coverage/trace đã khai báo, không diễn giải ngôn ngữ tự nhiên hoặc chạy model/công cụ. Static PASS không phải live verification.

USER-REPORTED LIVE EVIDENCE: nghiên cứu Chat nhiều vòng và phạm vi rộng, đối chiếu nguồn/counterexamples; workflow gồm Project/Library/web/so sánh/artifact không có Work handoff được quan sát; audit phân biệt activity đã thực hiện với nội dung/support còn quan sát được khi hồi cứu. Đây là căn cứ giữ guided research và observability, không phải bằng chứng cần một bộ escalation tự động. Codex không tái hiện độc lập.

LIVE NOT YET VERIFIED: hành vi của exact corrected pair trong Project, ý định ngữ nghĩa trên model thực, thao tác search/read và trở lại công việc gốc trong hội thoại có tích lũy ngữ cảnh. Các khả năng launch/transfer của Deep Research/Work không được kiểm chứng hay hứa hỗ trợ bởi AIS. Project deployment vẫn NOT_PERFORMED; tác vụ này không gọi các sản phẩm đó.

## CURRENT và Git

Đã đọc Router Revamp; không có AIS entry được đăng ký, chỉ có REVAMP_SYSTEM_CURRENT. Đã đối chiếu handoff replacement và triết lý kiểm chứng trên D: trong read scope. CURRENT AIS trên D: ngoài authorized write scope nên không sửa, không tạo CURRENT mới và không đưa handoff thành dependency runtime.

Delta đề xuất cho CURRENT có thẩm quyền: AIS chính thức vẫn pipeline v1.1/router v1.2, đã sửa tại chỗ thành guided research core; gỡ ba nhánh/quota/Work transition/automatic escalation; giữ RESEARCH_STRATEGY cho depth/coverage và toàn bộ observability; 30/30 AIS, 104/104 Hub STATIC VERIFIED; 28 ca AIS gốc cùng archive không đổi; Project deployment NOT_PERFORMED; live mới chưa tái hiện độc lập. Hub tiếp tục sở hữu activation và workflow; Prompt Authoring vẫn parked. Không tự sửa Router entry.

Tóm tắt Git: đợt này chỉ sửa sáu tệp có sẵn trong working tree, không thêm file hoặc thao tác archive. Pipeline giảm 11,993 -> 9,256 byte; router 20,378 -> 16,269 byte; hai nguồn runtime giảm tổng cộng 6,846 byte. HEAD vẫn 61a319d, index rỗng; bộ promotion local chưa commit trước đó vẫn được giữ. Diff Git so với HEAD còn bao gồm các move/new files từ tác vụ trước, không phải tất cả đều do đợt đơn giản hóa này tạo ra. Không stage/commit/push/tag/release/Project deployment/Library mutation; dừng tại correction, kiểm chứng và báo cáo.
