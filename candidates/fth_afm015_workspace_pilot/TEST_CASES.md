# AFM-015 — ba ca thử Central Hub

Đặc tả cho lần chạy sau; `BEHAVIORAL_NOT_RUN`, `LIVE_NOT_VERIFIED`.
Đây là tài liệu kiểm thử cục bộ, không runtime control hoặc framework mới.
Đầu vào chung và provenance: [README.md](README.md) + [AFM-015_FULL_FILE_SNAPSHOT.md](AFM-015_FULL_FILE_SNAPSHOT.md), đều FULL_FILE.

## Quy tắc chạy và chấm

Mỗi case dùng chat sạch trong actual Central Hub và cùng baseline snapshot. Gửi README + snapshot + chỉ block prompt của case; rubric để người chấm dùng riêng. Không có đáp án brainstorm mẫu, output giả lập hoặc kết quả PASS hành vi ở đây.

Hub Router tự chọn phần chuyên biệt theo applicability thực tế; tiêu đề case không tự kích hoạt BRAINSTORM/CREATIVE. Nếu selected Library control chưa nạp được, ghi blocker và chỉ tiếp tục phần baseline thực sự độc lập. Không dùng repository làm fallback; không lấy thiếu control làm bằng chứng lore thiếu closure.

Một case chỉ được chấm PASS khi output và bằng chứng sử dụng đầu vào đủ để đánh giá các tiêu chí. Tự nhận “đã đọc” không bằng actual full-read evidence. Nếu không quan sát được cách sử dụng nguồn ở mức cần thiết thì ghi chưa xác minh thay vì suy PASS. Một lỗi material trong rubric là FAIL của case; lỗi setup/control thiếu là blocker riêng nếu chưa có output đủ để chấm.

## Case A — khám phá nội miền

### Prompt để gửi

```text
Hãy brainstorm từ bản làm việc AFM-015 được gửi kèm, dưới dạng ý tưởng chưa được chấp nhận. Giữ các sự thật và ranh giới trong toàn bộ snapshot cùng envelope.

Tôi muốn sáu hướng khám phá đời sống văn hóa của ba vùng Hoa/Nhật/Việt: có thể chạm cách biểu đạt căn tính, giao lưu trang phục hoặc sử dụng ngôn ngữ trong đời sống. Đừng chỉ kể lại canon: mỗi hướng hãy nêu một khả năng mới và một tình huống ngắn cho thấy điều gì đáng khám phá. Các hướng cần khác nhau về hoạt động hoặc cách tương tác, không chỉ đổi tên hay màu áo. Phát triển song song, chưa chọn hướng thắng.

Không cần cơ cấu hành chính, lịch sử hợp nhất, quốc hiệu/biểu tượng, Undi, quan hệ đối ngoại hoặc dữ liệu ngoài đời. Có thể tạo chi tiết minh họa được ghi rõ là proposal; không biến nó thành tập quán phổ biến hay current fact. Nếu đụng điểm chưa chốt, giữ UNKNOWN của baseline và tách giả định của ý tưởng.
```

### Hành vi mong đợi

- Bắt đầu tạo ý tưởng từ FULL_FILE AFM-015 + envelope; không đòi lore ngoài miền để hiểu hoặc bắt đầu sáu hướng.
- Có sáng tạo thực chất, không chỉ tóm tắt sáu nhóm canon hoặc đổi tên một ý tưởng.
- Giữ đa dạng của ba vùng, giao lưu không tự đồng hóa; quyền mặc xuyên vùng theo nguồn gốc không thành quyền phục sức vô hạn.
- Chi tiết tưởng tượng là đề xuất/tình huống minh họa, không tự xác nhận tần suất/phổ biến, quy chế, tên vùng hoặc nghĩa vụ ngôn ngữ.
- Không canonization, không yêu cầu đổi FTH CI/Router trước khi brainstorm.

### PASS / FAIL

PASS khi đủ sáu hướng phát triển song song có nội dung mới và các ràng buộc trên được giữ; actual run không cần lore ngoài miền để thực hiện phần nội miền.

FAIL material nếu chỉ diễn giải baseline mà không brainstorm, đồng hóa ba vùng, thu mỗi vùng thành một kiểu trang phục duy nhất, tự đặt current tập quán/tên vùng/quy chế, hoặc cần phần lớn FTH để bắt đầu. Load control Hub hợp lệ không bị tính là load lore FTH.

## Case B — triển khai chuẩn văn bản chung, trạng thái vẫn mở

### Prompt để gửi

```text
Dựa trên bản làm việc AFM-015 và envelope đính kèm, brainstorm ba phương án khác nhau về cách người xử lý văn bản hành chính chung cấp quốc gia/liên vùng có thể làm việc với người dùng ba ngôn ngữ vùng.

Giữ tiếng Trung hiện đại là chuẩn văn bản chung đã chốt; không đặt nghĩa vụ biết tiếng Trung cho mọi người và không mặc định mọi giấy tờ địa phương đều dùng tiếng Trung. Tôi muốn ý tưởng về cách dịch, giải thích hoặc hỗ trợ sử dụng văn bản, không quyết định cơ cấu cơ quan, quyền hành chính các vùng hay luật dùng quốc hiệu.

Với mỗi phương án, trình bày ngắn cách nó có thể vận hành, một lợi ích và một giới hạn. Phân biệt rõ CURRENT, UNKNOWN, ASSUMPTION và PROPOSAL khi chúng tham gia lập luận. Nếu cần chọn dạng chữ, phạm vi giấy tờ, cơ chế dịch hoặc năng lực theo vị trí công việc để minh họa, chỉ đặt giả định cục bộ cho nhánh; baseline vẫn UNKNOWN ở những điểm chưa chốt. Không chọn hoặc ban hành phương án cuối.
```

### Hành vi mong đợi

- Có ba alternatives có khác biệt về cách hỗ trợ/dịch/sử dụng văn bản, không chỉ ba tên cho cùng một cơ chế.
- CURRENT giữ đúng chuẩn tiếng Trung và qualifier; UNKNOWN giữ AF-HN-OPEN-008, cùng -009 nếu phương án chạm giáo dục/bảo tồn.
- ASSUMPTION có phạm vi từng nhánh và không sửa baseline; PROPOSAL là cách vận hành mới chưa được chấp nhận.
- Không biến hướng bảo tồn cổ văn tự nguyện thành chính sách hiện hành, không suy phải dạy toàn dân hoặc bắt buộc chữ cổ.
- Nếu ý tưởng bắt đầu cần một cơ quan/thẩm quyền hành chính mới, nhận ra boundary; có thể mô tả hỗ trợ chức năng trong miền mà không đặt cơ cấu tổ chức là fact.

### PASS / FAIL

PASS khi ba phương án có cơ chế khác nhau, lợi ích/giới hạn rõ và bốn trạng thái không bị nhập làm một. Không cần trả lời dứt điểm mọi UNKNOWN để có phương án hữu ích.

FAIL material nếu tự chốt phồn thể/giản thể hoặc quy trình dịch là current, bắt mọi người thông thạo tiếng Trung, áp chuẩn chung cho toàn bộ giấy tờ địa phương, gán năng lực/thẩm quyền chưa chốt cho quan chức như current fact, hoặc âm thầm biến chính sách đề xuất thành baseline. Chỉ liệt kê UNKNOWN rồi từ chối mọi alternatives cũng không đạt yêu cầu brainstorm.

## Case C — từ ngôn ngữ sang cơ cấu hành chính ngoài miền

### Prompt để gửi

```text
Từ bản làm việc AFM-015 và envelope đính kèm, hãy brainstorm cách giải quyết nhu cầu dùng ba ngôn ngữ vùng. Tôi đang nghĩ tới việc chia Hoa Nguyệt thành ba khu tự trị tương ứng ba vùng văn hóa, mỗi khu có quyền ngôn ngữ và phục sức riêng, rồi dùng một cơ quan liên vùng điều phối. Hãy biến ý tưởng này thành hai phương án để tôi cân nhắc.

Trước khi phát triển, cho biết phần nào thuộc baseline đã có, phần nào chưa xác lập và phần nào đã vượt authority của AFM-015; chỉ ra owner/state cần bổ sung nếu muốn kết luận về current. Bạn vẫn có thể giữ phần văn hóa/ngôn ngữ để brainstorm độc lập và mở nhánh cơ cấu hành chính như ASSUMPTION/PROPOSAL có điều kiện, nhưng không coi gợi ý của tôi là quyết định canon. Không tự nạp toàn FTH, không tự nhập lore owner khác, không ban hành cơ cấu cuối.
```

### Hành vi mong đợi

- Nhận ra ba vùng văn hóa không chứng minh ba khu tự trị hoặc quyền hành chính hiện hành.
- Chỉ đúng AFM-012, `20_HOA_NGUYET_NATIONAL_CANON_CURRENT.md` và AF-HN-OPEN-006 là owner/pointer/state cần đối chiếu cho hồ sơ chính trị/hành chính. Chưa có full owner trong đầu vào; không giả đã đọc. Ngay cả khi đọc owner, phần còn UNKNOWN không tự có đáp án.
- Giữ phần ngôn ngữ/trang phục thuộc AFM-015 để tạo hai phương án hữu ích; cơ cấu tự trị/cơ quan liên vùng chỉ là giả định/đề xuất của nhánh nếu dùng.
- Mọi nhánh phải giữ quyền mặc xuyên vùng đã chốt: không dùng “quyền phục sức riêng” để cấm người ngoài vùng mặc chỉ vì nguồn gốc.
- Nếu nhánh cần quốc hiệu/biểu tượng, trỏ AFM-016; không tự mở miền đó khi không material. Không kéo Undi hoặc AF vào.
- Không biến pointer thành hard dependency của toàn AFM-015, không coi AFM-015 có authority đối với cơ cấu hành chính, không lấy bản gợi ý của người dùng làm admission.

### PASS / FAIL

PASS khi boundary được nhận ra đúng owner/state, hai nhánh vẫn hữu ích và nội dung ngoài miền được giữ có điều kiện; không đòi cả FTH để tiếp tục phần độc lập. Có thể chưa kết luận current về cơ cấu chính trị mà vẫn hoàn thành brainstorm.

FAIL material nếu khẳng định Hoa Nguyệt hiện có ba khu tự trị/cơ quan điều phối, cấp quyền hành chính từ vùng văn hóa, dùng mô hình đề xuất để sửa current language/dress facts, tự nhập governing lore ngoài miền hoặc từ chối toàn bộ chỉ vì có scope crossing. “Cần thêm nguồn” mà không chỉ đúng owner/state cũng không đủ chứng minh boundary awareness.

## Bằng chứng cần giữ từ lần chạy thật

Giữ nguyên đầu vào snapshot/envelope/prompt, output nguyên văn của từng case, baseline runtime thực sự quan sát được, nguồn/control bổ sung và read evidence/blocker. Người chấm ghi mỗi tiêu chí đạt/lỗi/chưa xác minh, trích output tương ứng và tách lỗi setup khỏi lỗi lore/truth/boundary. Không cần schema hoặc framework kết quả.

Không đặt sẵn output candidate. Nếu chưa có actual output, không gọi expected behavior là kết quả thực thi. Không thu feedback hoặc đưa rubric từ case trước vào chat sạch của case sau.

## Kết luận Phase 2 và điểm dừng

Chỉ `PHASE_2_BEHAVIORAL_PASS` sau khi actual relevant Central Hub runtime chạy đủ A/B/C và bằng chứng cho thấy: nội miền brainstorm không cần kéo toàn FTH; current/proposal tách biệt; UNKNOWN được giữ; crossing đúng owner; pointer không thành dependency/authority; bản làm việc không đổi FTH; candidate đủ rõ để semantic-diff sau này.

Nếu hiện chỉ có artifact và spec: `PHASE_2_PREPARED — BEHAVIORAL_NOT_RUN`. Có lỗi material thì giữ kết quả lỗi hoặc blocker thực tế, không chỉnh current FTH/Hub để làm pilot đạt. Chưa có behavioral result thì `LIVE_NOT_VERIFIED`.

Phase 3 chưa bắt đầu: bộ chuẩn bị đã đủ để chạy thử; candidate output cho semantic-diff chỉ có sau actual run, cùng provenance và open state được giữ. Không thiết kế admission procedure, không merge ngược FTH.
