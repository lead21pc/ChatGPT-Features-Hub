# User Profile dùng chung — candidate 0.1

`HUB-USER-PROFILE` cung cấp ngữ cảnh do người dùng khai báo cho phần việc cụ thể. Người dùng sở hữu dữ liệu. Shopping là bên tiêu thụ được khai báo. Tài nguyên nằm ngoài danh mục gói gốc và không mang vai trò runtime. Hub giữ quyền chọn gói, xét phạm vi và xác minh đầu vào. Gói tiêu thụ giữ trách nhiệm diễn giải và đánh giá chứng cứ. Hồ sơ chỉ chứa dữ liệu và siêu dữ liệu truy cập. Định tuyến, xếp hạng, suy luận y tế, thao tác công cụ, bộ nhớ và trạng thái mô hình nằm ngoài trách nhiệm của hồ sơ.

## Sở hữu và chỉnh sửa

`customizable: true` nghĩa là người dùng có thể tự chỉnh sửa nội dung thủ công.

```text
PROFILE READABLE != PROFILE WRITABLE
USER-PROVIDED DATA != MODEL-PERSISTED STATE
MODEL INFERENCE != PROFILE FACT
CHAT CONTEXT != PROFILE UPDATE AUTHORIZATION
CUSTOMIZABLE != MODEL-MUTABLE
PROFILE MUTATION BY MODEL: NEVER
```

Mô hình bị cấm ghi, nối thêm, xóa, suy ra rồi lưu, chuẩn hóa tại chỗ, hợp nhất dữ liệu từ chat hoặc tự làm mới giá trị cũ. Quyền ghi file thông thường, quyền sửa repository và yêu cầu sửa hồ sơ trong chat đều không cấp quyền đột biến hồ sơ. Khi thấy một giá trị cần xem lại, mô hình trả chênh lệch hoặc đề xuất cho người dùng tự chỉnh sửa.

## Hai object theo phạm vi đọc

- `BASICS` gộp ngữ cảnh chung và sở thích vì chúng có cùng phạm vi đọc trong candidate. Chỉ lưu dữ liệu ít nhạy cảm phục vụ so sánh hoặc lọc khi có nhu cầu.
- `HEALTH_CONSTRAINTS` chỉ chứa các chất hoặc thành phần người dùng khai báo cần tránh để đánh giá tương thích sản phẩm. Bệnh sử, chẩn đoán và danh mục thuốc nằm ngoài candidate.

Template công khai là một tài liệu YAML chứa hai mẫu object rỗng. Khi tạo dữ liệu thực, người dùng lưu từng object riêng, không dùng tài liệu mẫu làm object gộp. Đọc `FULL_FILE` trên object gộp sẽ đưa dữ liệu sức khỏe vào ngữ cảnh ngay cả khi chỉ cần sở thích. Repository công khai chỉ lưu schema, hợp đồng truy cập, template và fixture tổng hợp. Giá trị thật cùng tham chiếu riêng do người dùng giữ ngoài repository. Việc tách nơi lưu không dựa vào `.gitignore`.

## Điều kiện đọc và sử dụng

Hub chọn gói cho tác vụ hiện tại. Gói nêu phần cần đọc và mục đích. Hub kiểm tra quyền theo bộ ba gói, phần và mục đích, đồng thời xác nhận nhu cầu thực tế trước khi phần tương ứng được cung cấp. Thiếu quyền mặc định là `DENY`. Có quyền nhưng thiếu nhu cầu thì bỏ qua đọc. Dữ liệu tường minh của lượt hiện tại đã đủ thì bỏ qua đọc. Consumer chỉ nhận phần đã được phép và giữ nguồn gốc do người dùng khai báo.

```text
ACCESS DECLARATION != AUTOMATIC LOAD
MODULE HAS ACCESS != MODULE NEEDS DATA THIS TURN
ACCESS != AUTHORITY
PROFILE VALUE != CURRENT REQUIREMENT
PROFILE PREFERENCE != HARD CONSTRAINT
HEALTH FACT != MEDICAL CONCLUSION
```

So giá đơn thuần không yêu cầu `HEALTH_CONSTRAINTS`. Đánh giá tương thích có thể cần phần này nếu kết quả phụ thuộc vào ràng buộc đã khai báo. Khi cần AIS, Hub chỉ chuyển tiêu chí sản phẩm tối thiểu để xác minh. Hồ sơ và nguồn gốc cá nhân của ràng buộc không đi theo yêu cầu tìm kiếm.

Giá trị chưa biết giữ `UNKNOWN`. Phát biểu tường minh hiện tại thắng khi có xung đột trong tác vụ, và nội dung đã lưu giữ nguyên. Thiếu phần được phép chỉ giữ phần cá nhân hóa phụ thuộc ở trạng thái chưa giải quyết. Phần so sánh độc lập tiếp tục khi đủ dữ liệu. Candidate không dùng Memory, chat cũ, file tương tự hoặc suy luận để điền phần còn thiếu.

## Giới hạn kiểm chứng

Candidate dùng đầu vào được cung cấp riêng theo phần và fixture tổng hợp. Hợp đồng Hub hiện hành chưa định nghĩa truy xuất tài nguyên phi module từ Library. Phân giải đúng object, `FULL_FILE` và kiểm soát phạm vi truy xuất cần được xác minh riêng trước khi dùng dữ liệu riêng tư. Các khai báo ở đây mô tả hành vi kỳ vọng, chưa thiết lập quyền truy cập ở cấp nền tảng.

Một consumer Health tương lai có thể được biểu diễn trong fixture riêng dưới cùng định danh tài nguyên. Candidate không cấp quyền Health, đăng ký gói Health hay cung cấp thủ tục y tế. Kết quả `STATIC / SPEC ONLY` chỉ xác nhận artifact và kỳ vọng fixture, không xác nhận hành vi mô hình, Library, quyền riêng tư, dấu vết đọc, định tuyến Hub hoặc hành vi Health.
