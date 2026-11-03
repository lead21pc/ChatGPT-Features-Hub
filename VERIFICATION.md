# Kết quả kiểm chứng Giai đoạn 1

Ngày kiểm chứng: 2026-11-03 (Asia/Bangkok).

`STATIC / LOCAL APP VERIFIED`

`LIVE API VERIFIED: NOT RUN`

Chưa đạt tiêu chí PASS toàn bộ Giai đoạn 1 vì môi trường không có API key. Chưa xác minh quyền truy cập `gpt-5.6-sol`, quota hay response thật.

Đã kiểm tra bằng Python 3.11.9, openai 2.38.0, streamlit 1.58.0:

- Import SDK/app và biên dịch Python: đạt.
- Đọc config thật; từ chối config thiếu, JSON lỗi, sai kiểu hoặc model rỗng: đạt.
- Streamlit AppTest: tiêu đề, model, prompt rỗng, key rỗng và không thêm lượt thất bại vào lịch sử: đạt.
- SDK thật với HTTP transport mô phỏng, không gửi ra mạng: payload đúng model, chỉ có user/assistant, `store=False`, response hiển thị trong UI và hai lượt hội thoại đúng thứ tự: đạt.
- HTTP mô phỏng 401/429/404/500, mất kết nối, timeout, response rỗng/chưa hoàn tất; không retry, không thay lịch sử khi lỗi, đọc lại key khi gửi: đạt.
- Server Streamlit thật tại loopback: trang HTTP 200 và health `ok`; đã dừng server sau kiểm tra: đạt.
- So sánh SHA-256 toàn bộ 212 tệp và toàn bộ đường dẫn thư mục giữa nguồn và bản sao: khớp. Bao gồm cả cache có sẵn trong nguồn; không chạy test hoặc sửa nội dung bản sao.
- `git diff --check` cho các file app/tài liệu mới: đạt. Kiểm tra toàn bản sao báo whitespace có sẵn (gồm CRLF và các dòng trong patch nguồn); giữ nguyên theo yêu cầu sao chép byte-exact, không sửa để làm sạch kiểm tra này.

Baseline workspace: chưa có app và chưa thuộc repo nào. Đã tạo repo Git local tại thư mục này, branch `main`, chưa có HEAD/commit; không có remote. Các file mới có đánh dấu intent-to-add để xem diff, chưa stage nội dung hoặc commit. `config.json` được bỏ qua. Repo nguồn có working tree sạch, branch `main`, HEAD `b3f470a46c87c4bfad68d74bf031f78d7abc87b4` khi sao chép. Không sửa repo nguồn.

Để hoàn tất live verification: điền key vào `config.json`, chạy lệnh trong README, bấm Send với `Chỉ trả lời: T0 OK`; xác nhận response hiện bên dưới rồi kiểm tra câu hỏi tiếp nối. Chỉ ghi live PASS sau khi đường Streamlit → config → OpenAI API → GPT-5.6 Sol → response hiển thị thực sự thành công.
