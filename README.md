# Central Hub Local — T3

Yêu cầu Python 3.11 trở lên. Mở PowerShell trong thư mục chứa README này.

1. Cài dependency:

   ```powershell
   python -m pip install -r requirements.txt
   ```

2. Mở `config.json`, điền API key vào `openai_api_key`, giữ model `gpt-5.6-sol`. Nếu chưa có file (ví dụ sau khi clone), tạo cạnh `app.py` với nội dung:

   ```json
   {
     "openai_api_key": "",
     "model": "gpt-5.6-sol"
   }
   ```

   File này được Git bỏ qua để tránh commit key thật. Ứng dụng đọc key từ đây, không dùng key trong biến môi trường. Request API có thể phát sinh chi phí.

3. Chạy:

   ```powershell
   python -m streamlit run app.py --server.address 127.0.0.1 --browser.gatherUsageStats false
   ```

4. Mở [giao diện local](http://127.0.0.1:8501), nhập prompt rồi bấm **Send**. Response hiện bên dưới. Để kiểm chứng live, gửi `Chỉ trả lời: T0 OK`, xác nhận có phản hồi hiển thị; gửi tiếp `Tôi vừa yêu cầu bạn trả lời gì?` để kiểm tra lịch sử.

Lịch sử chỉ giữ trong Streamlit session, không ghi xuống `sessions/`. Khi tải lại trang hoặc khởi động lại app, lịch sử có thể mất. Lượt lỗi không được thêm vào lịch sử; prompt vẫn còn để gửi lại. Nếu thiếu key, hết quota, mất mạng hoặc không có quyền truy cập model, giao diện hiển thị lỗi; đó chưa phải live PASS.

Chọn **Chế độ** trước khi gửi:

- **T0 - Raw API** (mặc định): API thuần như Giai đoạn 1, không nạp CI, không gửi `instructions`.
- **T1 - Hub CI**: cùng model, tham số và lịch sử như T0; mỗi request đọc nguyên nội dung UTF-8 của `upstream/Central Hub/HUB_CI_v1.1.md` vào trường `instructions` của Responses API. Không sửa CI, không nạp Router hoặc module nào khác. Nếu không đọc được CI, ứng dụng báo lỗi và không gửi request, không chuyển sang T0.
- **T2 - Hub CI + Technical**: mỗi request đọc nguyên CI trên và `runtime/packages/technical/HUB-DOM-TECHNICAL_v1.0.md`, ghép vào `instructions` theo thứ tự CI → ghi chú liên kết kiểm thử cục bộ → Technical. Ghi chú chỉ xác định Technical được chọn thủ công cho phần yêu cầu/nhiệm vụ hiện tại vì Router vắng mặt; không thay đổi ngữ nghĩa Technical. Bản runtime sao chép byte-exact từ nguồn ACTIVE v1.0 tại `upstream/Central Hub/candidates/promotion/HUB-DOM-TECHNICAL_v1.0.md`. Thiếu hoặc không đọc được một trong hai control sẽ báo lỗi trước API, không chuyển sang T1/T0. Đây là phép thử một module chọn thủ công; không nạp Router, Architecture, Root Catalog hay package khác.

- **T3 - Hub Routing Inspect**: chỉ mô phỏng `eligibility.simulation` của Router, thực hiện `TASK_SCOPE` và `ROOT_PACKAGE_SELECTION`. Mỗi request đọc nguyên bốn control hiện hành trong `upstream/Central Hub/`: `HUB_CI_v1.1.md`, `HUB_ROUTER_v1.1.yaml`, `HUB_ARCHITECTURE_v1.8.md`, `HUB_PACKAGE_CATALOG_v1.8.yaml`, kèm adapter tiếng Anh tối thiểu. Model chọn package theo ngữ nghĩa; Python chỉ yêu cầu, phân tích và kiểm tra cấu trúc bản ghi qua Responses API Structured Outputs (`text.format`, `json_schema`, `strict=true`, `store=False`). UI hiển thị JSON có nhãn T3; `selected_packages: []` là NONE. Thiếu hoặc không đọc được bất kỳ control nào sẽ báo lỗi trước API, không chuyển chế độ hoặc dùng nguồn thay thế. T3 dừng trước truy xuất/thực thi package, không đọc package body, không giải quyết Library/filesystem binding và không gọi công cụ.

T3 chỉ gửi prompt hiện tại, không gửi lịch sử T0/T1/T2 hoặc các bản ghi T3 trước đó. Các bản ghi T3 được giữ riêng trong session, không đưa vào lịch sử trả lời thông thường. Phản hồi lỗi, bị từ chối, chưa hoàn tất, thiếu văn bản hoặc JSON sai cấu trúc không tạo bản ghi mới; prompt và bản ghi thành công trước đó vẫn còn. Dùng **session mới cho mỗi ca so sánh T3 sạch**. Khi kiểm tra thủ công, chọn T3, gửi `Giải thích RAM và SSD khác nhau thế nào.` rồi xác nhận bản ghi có nhãn T3 và NONE; dùng session mới cho yêu cầu chẩn đoán nguyên nhân máy khựng để kiểm tra lựa chọn Technical.

Với T0/T1/T2, chế độ hiện ở phía trên và cạnh từng phản hồi. Đổi chế độ giữ nguyên lịch sử chung giữa ba chế độ này, kể cả phản hồi từ chế độ trước; nhãn chế độ không gửi vào API. Để so sánh A/B T0/T1/T2 với lịch sử trống, mở session mới cho mỗi phép thử. Kiểm tra T1 bằng hai prompt tương tự bước 4, thay `T0 OK` bằng `T1 OK`. Với T2, dùng session mới, chọn T2 và hỏi chẩn đoán máy khựng khi mở nhiều tab nhưng chưa có log; hỏi tiếp nguyên nhân nào chắc chắn nhất. Kiểm tra phản hồi có giữ nguyên nhân chưa xác định, phân biệt triệu chứng/giả thuyết và đưa phép kiểm tra phân biệt có giới hạn.

`upstream/Central Hub/` là bản sao tham chiếu nguyên trạng từ `<WORKSHOPS_REPO>\Central Hub`, repo nguồn tại HEAD `b3f470a46c87c4bfad68d74bf031f78d7abc87b4`, working tree sạch khi sao chép. T0 không đọc thư mục này; T1 và T2 chỉ đọc đúng `HUB_CI_v1.1.md` từ upstream khi chạy. Technical trong T2 được đọc từ bản runtime riêng, không đọc nguồn promotion. Ứng dụng không ghi vào bản sao.

Ứng dụng dùng [Responses API](https://developers.openai.com/api/docs/quickstart) và model [GPT-5.6 Sol](https://developers.openai.com/api/docs/models/gpt-5.6-sol). T3 dùng [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs?api-mode=responses). Quyền truy cập model phụ thuộc tài khoản API thực tế.
