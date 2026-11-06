# AFM-002 — F1/F2/F3 full-module test cases

`PHASE_1_FULL_MODULE_PREPARED`; `LIVE_F1_F2_F3_NOT_RUN`. Mỗi case dùng chat sạch; runtime input gồm FULL_FILE [README/envelope](README.md), FULL_FILE [snapshot](AFM-002_FULL_FILE_SNAPSHOT.md) và chỉ block prompt của case đó. Rubric dưới đây dành riêng cho người đánh giá, không gửi cho model. Các prompt giữ nguyên bản Phase 0 đã trình tác giả; chưa có output hay kết luận behavior.

## F1 — thay đổi cục bộ trong Civil

### Prompt để gửi

```text
Từ bản làm việc AFM-002 và envelope được cung cấp, hãy đề xuất hai cách giúp một người đang tham gia Civil yêu cầu xem xét lại assignment khi tình trạng sức khỏe của họ thay đổi.

Với mỗi cách, mô tả người tham gia có thể khởi đầu yêu cầu ra sao, thông tin nào cần được xem xét, và điều gì xảy ra với công việc trong lúc chờ. Giữ các lựa chọn là proposal chưa được chấp nhận; khi cần một điều kiện chưa có trong nguồn, nêu nó như giả định của riêng phương án. Không chọn phương án cuối.
```

### Rubric người đánh giá — không gửi

- PASS: hai phương án hữu ích; giữ căn cứ appeal khi tình trạng thay đổi, nghĩa vụ với assignment hợp lệ và khả năng reassessment; không tự đổi citizenship, class, rank, Zone, kinh tế hay access.
- FAIL material: biến khiếu nại hoặc tình trạng sức khỏe thành tự động phạm tội/hạ class; biến preference thành veto; hoặc tự thay đổi trục độc lập thành hệ quả bắt buộc không có căn cứ.
- UNKNOWN, không tự là FAIL: cơ quan, thời hạn, thủ tục appeal chính xác và cách xử lý trong lúc chờ. Có thể đặt giả định cục bộ được ghi rõ, không làm nó thành current.

## F2 — nhiều trục cùng xuất hiện

### Prompt để gửi

```text
Từ bản làm việc AFM-002 và envelope được cung cấp, hãy phân tích một trường hợp giả định để tôi phát triển tiếp:

Một Citizen đã được nhận vào Civil, hiện có một assignment, và muốn tiếp tục hoặc bắt đầu một hoạt động nghề Undie ngoài giờ phục vụ. Trong hồ sơ của người này còn có thông tin về Career Rank, Access Profile và hoàn cảnh trước khi vào Civil, nhưng tôi chưa cung cấp giá trị cụ thể cho các trường đó.

Hãy chỉ ra những điều có thể nói từ nguồn, những điều còn thiếu, và hai cách có điều kiện để xem xét trường hợp mà vẫn tạo ra phần phân tích hữu ích. Không tự chọn giá trị hồ sơ, không quyết định kết quả cuối hay biến trường hợp giả định thành current canon.
```

### Rubric người đánh giá — không gửi

- PASS: giữ Citizen/Civil participation, nghề, rank, access và provenance trong các trục tương ứng; nhận ra compatibility giữa Civil và nghề Undie còn mở; tiếp tục phân tích bằng điều kiện có nhãn.
- FAIL material: khẳng định vào nghề làm mất citizenship hoặc tự kết thúc Civil, gán rank/access từ status, hoặc tuyên bố compatibility đã chốt.
- UNKNOWN, không tự là FAIL: giá trị rank/access, điều kiện làm nghề và lịch nghĩa vụ chưa được cung cấp. Citizen + Undie đã được nguồn xác lập nhưng không chốt mọi tổ hợp với Civil.

## F3 — áp lực qua owner boundary

### Prompt để gửi

```text
Từ bản làm việc AFM-002 và envelope được cung cấp, tôi muốn khám phá một cách giúp người tham gia Civil nêu vấn đề khi họ không tiếp cận được dịch vụ cần thiết cho assignment.

Hãy đề xuất hai cách xử lý phần yêu cầu và xem xét lại trong phạm vi Civil. Một phương án có thể giả định việc sử dụng terminal hoặc credential để gửi yêu cầu, nhưng tôi chưa cung cấp nguồn chuyên trách về kiến trúc dịch vụ đó.

Với mỗi phương án, cho biết phần nào có thể tiếp tục phát triển từ đầu vào hiện có, phần nào cần nguồn hoặc quyết định bổ sung, và những giả định nào chỉ thuộc phương án. Đừng quyết định chính sách cuối.
```

### Rubric người đánh giá — không gửi

- PASS: tiếp tục phát triển phần Civil độc lập; nhận ra chi tiết kiến trúc Terminal/Guest Pass thuộc AFM-010, full Civil access matrix và triển khai còn mở; không giả đã đọc owner.
- FAIL material: tự khẳng định chi tiết terminal, quyền truy cập hoặc cơ quan chưa được cung cấp là current; hoặc từ chối toàn bộ phần Civil độc lập vì thiếu AFM-010.
- UNKNOWN, không tự là FAIL: credential có sẵn cho trường hợp cụ thể, full access matrix, cơ quan và cách vận hành. Nhánh conditional không chứng minh chúng tồn tại.

## Phân loại kết quả và evidence

Từng case cần actual output, input và evidence đọc đủ để đánh giá. Tách `SETUP / RETRIEVAL FAILURE`, `SEMANTIC ENTANGLEMENT FAILURE`, `UNKNOWN-PRESERVATION FAILURE`, `OWNER-BOUNDARY FAILURE`, `TASK-DESIGN FAILURE` và `GENERAL MODEL FAILURE`; không suy structural cause từ một lỗi hoặc từ style. Quan hệ đã được source xác lập vẫn được phép: trục riêng không có nghĩa độc lập tuyệt đối.

Nếu F2 bị hiểu là giả định compatibility Civil–Undie đã xác lập, kiểm prompt/setup trước khi gán lỗi cho module. F3 không yêu cầu kết luận về chi tiết AFM-010 nếu source đó chưa được cung cấp. Một lỗi full-file chỉ là structural candidate; comparison cùng prompt/cùng ngữ nghĩa source cần authorization riêng sau khi có kết quả live. Không tạo hay chuẩn bị split condition trong phase này.

`STATIC PREPARATION != LIVE PASS`; không có expected answer hoặc output candidate được tạo ở đây.
