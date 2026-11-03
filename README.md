# Central Hub Local — Giai đoạn 1

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

`upstream/Central Hub/` là bản sao tham chiếu nguyên trạng từ `<WORKSHOPS_REPO>\Central Hub`, repo nguồn tại HEAD `b3f470a46c87c4bfad68d74bf031f78d7abc87b4`, working tree sạch khi sao chép. Ứng dụng không đọc hay thực thi thư mục này; không nạp Hub CI hoặc module nào.

Ứng dụng dùng [Responses API](https://developers.openai.com/api/docs/quickstart) và model [GPT-5.6 Sol](https://developers.openai.com/api/docs/models/gpt-5.6-sol). Quyền truy cập model phụ thuộc tài khoản API thực tế.
