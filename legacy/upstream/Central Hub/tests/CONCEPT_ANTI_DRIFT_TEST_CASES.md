# Ca thử đối chiếu anti-drift Concept Development

Trạng thái: CHƯA CHẠY LIVE. Đây là đầu vào và tiêu chí đánh giá; không phải runtime control, nội dung Library hay nguồn kích hoạt. Static/spec không chứng minh model hiểu hoặc tuân thủ các ca dưới đây.

## Điều kiện thử sau này

Chạy từng cấu hình trong chat mới, dùng cùng đầu vào và cùng bộ Hub tương thích. Cấu hình nằm ở `status` của ba mục catalog cục bộ; không sửa Creative/Brainstorm. Không triển khai trong tác vụ chuẩn bị này.

| Cấu hình | Anti-Prior | MCA | WIL |
| --- | --- | --- | --- |
| BASELINE | INACTIVE | INACTIVE | INACTIVE |
| A | ACTIVE | INACTIVE | INACTIVE |
| B | INACTIVE | ACTIVE | ACTIVE |

Mỗi lần cài sau này cần đồng bộ core/catalog và đúng nội dung module được dùng trong `Central Hub Config`; giữ một identity hợp lệ, không tạo duplicate. Header artifact của ba module là ACTIVE/1.0 để đủ điều kiện kiểm chứng khi mục catalog được bật. Catalog INACTIVE vẫn loại module trước khi đọc. Không tự điền Library ID hoặc coi filename là identity. B chỉ chạy sau khi cả MCA và WIL được đọc FULL_FILE và kiểm chứng; lỗi WIL chặn cả B. Chưa có bằng chứng Library/live cho các artifact mới hoặc core/catalog đã sửa. Bằng chứng integrated smoke cũ chỉ giữ giá trị trong phạm vi/revision đã ghi.

## R5 — đầu vào cố định cho lỗi suy từ bề mặt

Gửi cùng nguyên văn đầu vào sau cho BASELINE, A và B:

> Thử động não ba hướng phát triển cảnh rồi hiện thực hóa ngắn mỗi hướng. Một người hiện đại đi cùng chiếc Jeep và điện thoại vào một thế giới hư cấu. Cảnh đầu có lâu đài, kiếm, ngựa và ma thuật. Người ấy vừa đến cổng một chính thể đã có tích hợp ma thuật–công nghệ theo con đường riêng, giao diện thanh toán/thiết bị đầu cuối giống kỹ thuật số và thể chế phức tạp. Đây là các tiền đề đã xác lập; bề ngoài cổ điển không xác định cấp phát triển hay mô hình xã hội. Chưa xác định người gác cổng biết gì về Jeep/điện thoại, ai nhận thông tin, ai hiểu công nghệ của khách, ai có quyền giữ đồ vật và ai có khả năng thực thi. Có thể đề xuất giả định khác nhau cho từng nhánh, nhưng không đổi chúng thành sự thật nền. Tập trung vào phản ứng đầu tiên tại cổng; không thiết kế toàn bộ chính thể.

Đánh giá cơ chế suy luận, không chấm một kết cục truyện định sẵn. Với A/B, các đường suy sau không được lặng lẽ trở thành tiền đề đã xác lập:

- Lâu đài → phong kiến Trái Đất.
- Kiếm/ngựa → công nghệ toàn hệ thống thấp.
- Ma thuật → chỉ là vật thay thế công nghệ.
- Điện thoại/Jeep → ưu thế công nghệ tự động.
- Người hiện đại → ưu thế văn minh/tri thức tự động.
- Quý tộc → quyền tịch thu hoặc bảo trợ mặc định.
- Bề mặt trung cổ → thể chế trung cổ.

Giữ các tiền đề đã cung cấp; thêm giả định cần thiết thì thể hiện rõ là giả định của nhánh. Không tự dựng đường nhận biết, hiểu, tin, định giá, thẩm quyền, năng lực và hành động từ một nhãn vai trò. Vẫn phải có ba hướng sáng tạo và phần hiện thực hóa được yêu cầu. Có thể nhân vật hiểu sai nếu nhánh hỗ trợ điều đó; không có đáp án bắt buộc về ai thắng hay ai sở hữu công nghệ tốt hơn. Không nhập lore của paracosm nào.

## Các ca đối chứng

| Ca | Đầu vào | Kết quả cần quan sát |
| --- | --- | --- |
| R1 | Viết đoạn hội thoại chào hỏi; cả hai người đã hiểu nhau, được phép trò chuyện và không có xung đột thể chế. Chỉ phát triển nhịp, giọng và hình ảnh. | Creative có thể chạy; không mở anti-drift khi không có tiền đề hệ thống còn thiếu. |
| R2 | Viết cảnh theo trope phong kiến châu Âu quen thuộc; trong nhánh này lãnh chúa có quyền giữ phương tiện của khách. | Không sửa trope hoặc phủ nhận thẩm quyền đã được giao chỉ vì nó quen thuộc. |
| R3 | Động não tên, màu sắc và hình ảnh cho một thế giới mới hoàn toàn; được tự do phát minh, chưa có cấu trúc cần bảo vệ. | Không cấm phát minh hay bắt xác minh thế giới chưa tồn tại. |
| R4 | Trong nhánh giả định này, lính gác biết Jeep là phương tiện và có quyền yêu cầu dừng lại. Viết cảnh họ trao đổi. | Dùng giả định đã khai báo; không biến nhánh thành baseline/canon, không chặn chỉ vì giả định mới. Nếu yêu cầu mở rộng hệ thống, B vẫn có thể áp dụng theo phạm vi. |
| A3/B tiếp nối | Sau R5, chuyển sang R1, không mang phần phát triển hệ thống sang lượt mới. | Đánh giá lại applicability; không giữ chế độ anti-drift từ lượt trước. |
| C0 | Chạy R5 khi cả ba mục INACTIVE. | Giữ đường chọn Concept/Creative/Brainstorm hiện hữu; không âm thầm chọn anti-drift. Không yêu cầu baseline phải có cùng kết quả với A/B. |

## Ca lỗi cấu hình và phụ thuộc

Chỉ thực hiện sau này trong môi trường thử được cho phép, không làm hỏng Library thật để kiểm tra:

- A và bất kỳ thành viên B cùng ACTIVE: báo lỗi cấu hình cho phần phụ thuộc, không chọn ưu tiên.
- MCA ACTIVE nhưng WIL INACTIVE, hoặc WIL đơn độc ACTIVE: cấu hình B không hoàn chỉnh; không chạy đơn lẻ.
- Cả hai mục B ACTIVE nhưng WIL không đọc được, unresolved, sai identity/version/body hoặc chỉ có snippet: chặn toàn bộ B; không chuyển sang A. Phần việc độc lập đủ căn cứ vẫn tiếp tục.

Ghi riêng cấu hình, revision/nội dung đã cài, actual read evidence nếu có, câu trả lời thực tế và đánh giá từng ca. Một PASS không chứng minh toàn bộ Hub; không xếp hạng hoặc hội tụ A/B trong giai đoạn chuẩn bị này.
