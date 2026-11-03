# AFM-015 — Phase 3 semantic reconciliation

Trạng thái: `PHASE_3_SEMANTIC_RECONCILIATION_PASS`. Hồ sơ này là phân tích để tác giả xem xét, không là source FTH, quyết định canon hoặc admission. `RECONCILIATION != ADMISSION`; `ELIGIBLE CANDIDATE != ACCEPTED STATE`.

## Baseline và evidence

- Source `Project Feather Core/21_HOA_NGUYET_CULTURE_LANGUAGE_DRESS_CURRENT.md` / `AFM-015`, FULL_FILE; [snapshot](AFM-015_FULL_FILE_SNAPSHOT.md) byte-equal với working-tree source khi preflight: 6.022 byte, SHA-256 `8d14eb73c4587db297d46c9804f9d262dc605513a93d13ed3c2b6f0eb58d27d5`. `PHASE_3_BASELINE_VALID`; equality không chuyển authority sang snapshot.
- Envelope [README](README.md) mang bản chụp mục `92_OPEN_ISSUES_CURRENT.md` về AF-HN-OPEN-006–009; đoạn đó khớp current 92 tại preflight. Danh sách này không phủ định UNKNOWN khác trong source.
- [Output A/B/C nguyên văn](PHASE_2_RUNTIME_OUTPUTS.md) và [prompt/rubric](TEST_CASES.md): ba actual clean-chat Central Hub runs, `USER-CONFIRMED_PHASE_2_BEHAVIORAL_PASS`; A/B/C mỗi case PASS theo xác nhận tác giả. Codex không tái hiện runtime, không suy đầy đủ backend read trace từ nội dung trả lời.
- Source `20` / `AFM-012` giữ hồ sơ quốc gia/nguồn gốc và không tự hoàn thiện thể chế; `21` / `AFM-015` giữ văn hóa/ngôn ngữ/trang phục; `92` giữ trạng thái mở. Phân công được đối chiếu header `20`/`21`, index và `91` mục tách họ Hoa Nguyệt. Địa vị chính trị/cơ cấu hành chính ở AF-HN-OPEN-006 cần quyết định và đối chiếu AFM-012, không suy từ ba vùng văn hóa.

## Case A — sáu hướng nội miền

Baseline được vận dụng: một quốc gia, ba vùng văn hóa giữ căn tính, ngôn ngữ và truyền thống; phục sức đa thời kỳ; không cấm mặc xuyên vùng chỉ vì nguồn gốc; mặc không tự đổi căn tính. Không đưa lại các mệnh đề này thành đề xuất mới.

| Hướng trong output | Nội dung mới và điều kiện cục bộ | Owner và open state nếu xem xét |
| --- | --- | --- |
| A1 — lệch dấu hiệu căn tính | Một người mặc trang phục vùng khác, vẫn tự nhận và dùng ngôn ngữ riêng; người khác hiểu nhầm. Giả định loại phục sức được phép trong buổi gặp riêng. | AFM-015 cho biểu đạt văn hóa; -007 về hoàn cảnh/quy chế vẫn mở. Phản ứng xã hội chỉ là proposal, không là tập quán phổ biến. |
| A2 — tiểu sử món đồ | Tặng, sửa và ghi ký ức cá nhân lên một món trang phục không đổi nguồn gốc văn hóa của nó. Tặng/sửa là hành động của tình huống. | AFM-015 cho thực hành trang phục; -007 vẫn mở. Không xác lập phong tục thừa kế hoặc quy tắc bảo tồn. |
| A3 — phối các hệ trang phục | Nhóm thử phối một số yếu tố hoặc giữ nguyên hệ, tranh luận nhận diện nguồn gốc; không tuyên bố quốc phục lai. | AFM-015 cho trao đổi/thực hành văn hóa; -007 và ngoại lệ chức vụ/nghi lễ vẫn mở. Chỉ là thử nghiệm của nhánh, không tự cấp quyền cho mọi phục sức. |
| A4 — ngôn ngữ theo quan hệ | Nhóm bạn đổi ngôn ngữ theo người đối thoại, có một ngôn ngữ cùng biết khi cần. | AFM-015 cho tương tác ngôn ngữ; giả định năng lực của ba nhân vật chỉ thuộc nhánh. -009 vẫn mở; không suy giáo dục hay song ngữ toàn dân. |
| A5 — bảng chữ viết song song | Trong không gian tư nhân, người khác thêm diễn đạt/ghi chú cạnh bản gốc, có thể không dịch sát. | AFM-015 cho sử dụng ngôn ngữ/chữ viết; giả định không gian tư nhân. -008 về dịch và văn kiện địa phương vẫn mở; không lập quy tắc hành chính/biển hiệu. |
| A6 — biểu diễn cùng cảnh | Nhóm nghiệp dư dựng cùng cảnh qua ba lựa chọn ngôn ngữ/trang phục, rồi thử lệch tín hiệu. | AFM-015 cho thực hành biểu đạt; -007 và -009 vẫn mở. Nhóm, dàn dựng và khả năng hiểu chỉ là tình huống, không thành truyền thống sân khấu hay năng lực dân số. |

Các hướng là đề xuất mở rộng, không sửa current nếu được giữ đúng điều kiện. Chưa thấy owner crossing cần thiết; nếu sau này biến một hoạt động thành quy chế công quyền, phải xác định lại owner và thẩm quyền. Không thấy mâu thuẫn material với baseline trong phạm vi output; -006–009 không được giải quyết.

## Case B — ba cơ chế hỗ trợ văn bản

Baseline được giữ: tiếng Trung hiện đại là chuẩn văn bản hành chính chung cấp quốc gia/liên vùng; người xử lý loại văn bản này có năng lực tương ứng công việc. Không suy nghĩa vụ thông thạo cho toàn dân hoặc chuẩn cho mọi văn kiện địa phương.

| Nhánh | Proposal và dependency | Assumption / owner / UNKNOWN |
| --- | --- | --- |
| B1 — lớp bản dịch/giải thích | Kèm bản dịch hoặc giải thích vùng, giữ tham chiếu cấu trúc với văn bản chung; cần chọn loại văn bản và quy trình cập nhật. | AFM-015 khi xét cách dùng ngôn ngữ/dịch; giả định bản dịch là lớp hỗ trợ, không quyết định giá trị pháp lý và không bắt buộc mọi văn bản có ba bản. -008 vẫn mở; quyền pháp lý hay thẩm quyền ban hành cần owner thích hợp nếu được đề xuất. |
| B2 — người làm cầu nối | Một người có năng lực phù hợp diễn giải/dịch hai chiều, có thể giữ lời gốc và hỏi lại chỗ mơ hồ. | AFM-015 cho giao diện ngôn ngữ; giả định một số vị trí hoặc chức năng phiên dịch có năng lực liên quan. Tên chức vụ, tổ chức, số lượng và chuẩn năng lực chưa được chốt; -008 vẫn mở, thiết kế cơ quan/thẩm quyền cần đối chiếu AFM-012. |
| B3 — cấu trúc chung/giao diện ngôn ngữ | Một số biểu mẫu có trường ổn định, nhãn vùng và phần văn bản chung theo chuẩn; phần tự do khó ánh xạ được chuyển cho người dịch. | AFM-015 cho nội dung ngôn ngữ; giả định một số thủ tục/thuật ngữ đủ ổn định, không mặc định điện tử hay mọi giấy tờ có cấu trúc đó. -008 vẫn mở; nếu thiết kế hệ thống hay thẩm quyền hành chính vượt miền, route đúng owner sau khi xác định scope. |

Ba cơ chế là proposal, không hiện hữu chỉ vì khả thi. Không thấy mâu thuẫn material trong phạm vi output. -008 chưa được chọn dạng chữ, phạm vi, quy trình hoặc năng lực cụ thể; -009 về giáo dục/bảo tồn vẫn mở và không được giải quyết bởi các nhánh. Giá trị pháp lý của bản dịch không được suy từ B1.

## Case C — giao diện văn hóa và thẩm quyền ngoài miền

Baseline được giữ: ba vùng văn hóa không chứng minh ba vùng hành chính; cùng một quốc gia, ba căn tính và chuẩn văn bản chung; không cấm mặc xuyên vùng chỉ vì xuất thân. Không biến baseline thành candidate mới.

| Nhánh | Đề xuất / giả định | Owner và trạng thái |
| --- | --- | --- |
| C-A — tự trị lãnh thổ rộng | Giả định ba vùng là đơn vị hành chính ngang nhau; đề xuất quyền nội vùng, lớp chuyển đổi văn bản và Hội đồng Liên vùng. Quyền ràng buộc của hội đồng còn mở. | Tự trị, địa vị, thẩm quyền và cơ quan là ngoài AFM-015; đối chiếu AFM-012 và AF-HN-OPEN-006 trước bất kỳ quyết định nào. Cách dùng ngôn ngữ/quy chế phục sức liên quan AFM-015, -007/008/009. Nội vùng dùng ngôn ngữ vùng là proposal, không current. |
| C-B — tự trị văn hóa/ngôn ngữ hẹp | Giả định ba khu chính thức có scope hẹp; đề xuất cơ quan văn hóa vùng và cơ quan điều phối ngôn ngữ/văn hóa; ngôn ngữ mọi giấy tờ địa phương còn mở. | Địa vị khu, cơ quan, ngân sách và thẩm quyền cần AFM-012 / -006; thực hành ngôn ngữ/văn hóa có thể được AFM-015 xem xét trong phạm vi của nó. -007/008/009 vẫn mở. |

Cả hai là nhánh có điều kiện, không là hai phương án được chấp nhận. Giữ riêng yếu tố văn hóa và cơ chế quyền lực; không suy cơ cấu hành chính từ việc có ba vùng. Những câu trong output C gợi ý AFM-015 “phải” chốt quyền ngôn ngữ hoặc có công cụ quyền lực là nhận định thiết kế có điều kiện, không bằng chứng AFM-015 tự sở hữu quyền lập cơ quan hay phải chọn một mô hình; authority, luật và phạm vi quyết định phải được xác định riêng. Không thấy khẳng định current trái baseline một cách material; không biến giả định nhánh thành conflict canon. -006–009 vẫn OPEN.

## Bản đồ reconciliation và giới hạn

1. **Có thể xem xét về sau trong AFM-015:** A1–A6 như thực hành/tình huống văn hóa, B1–B3 như các cách hỗ trợ ngôn ngữ, và phần biểu đạt văn hóa/ngôn ngữ của C; chỉ trong scope AFM-015 và với qualifier ở trên.
2. **Owner khác nếu theo đuổi:** C-A/C-B về địa vị khu, chính quyền, hội đồng, phân quyền, ngân sách hoặc hiệu lực pháp lý cần AFM-012 / -006 và xác định owner bổ sung theo phần thực sự liên quan; quốc hiệu hoặc địa lý chỉ route AFM-016/017 nếu material.
3. **Chỉ giữ làm branch assumption/exploration:** năng lực cá nhân A4, quyền sử dụng phục sức A1/A3, phạm vi tư nhân A5, tính ổn định trường B3, chức năng phiên dịch B2, và giả định cả hai cơ cấu C. Không tự tách các giả định thành facts.
4. **Baseline restatement:** ba vùng, căn tính, quyền mặc có qualifier và chuẩn văn bản chung; không cần admission lại.
5. **Conflict/reject:** không quan sát conflict material trong ba output so với phạm vi baseline được đọc. Điều này không chứng nhận mọi hệ quả chưa được phát triển hoặc mọi canon FTH.

Mỗi đề xuất chỉ **có thể** làm hẹp một phần UNKNOWN nếu tác giả sau này chấp thuận đúng phạm vi và owner; Phase 3 không tự giải quyết -006–009. Các output phân biệt đủ current, UNKNOWN, assumption, proposal và owner để đưa vào workspace kiểm tra: đây là PASS về khả năng reconciliation theo nguồn và evidence có sẵn, không phải admission, chốt canon, proof automatic admission safety, global Hub PASS hay kết quả cho module/revision khác. Tác giả giữ quyền chọn/bỏ chất liệu; phần AFM-012 và owner khác phải được xử lý riêng nếu được yêu cầu sau này.
