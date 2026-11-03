# Kết quả kiểm chứng Giai đoạn 1

Ngày kiểm chứng: 2026-11-03 (Asia/Bangkok).

`STATIC / LOCAL APP VERIFIED`

`USER-PROVIDED LIVE API VERIFIED`

Giai đoạn 1 đạt PASS theo xác nhận của người dùng ngày 2026-11-03: hai prompt kiểm thử live đã PASS trên đường Streamlit → config → OpenAI API → GPT-5.6 Sol → response hiển thị, với Central Hub chưa tham gia. Đây là bằng chứng do người dùng cung cấp; Codex chưa trực tiếp tái hiện live API call.

Đã kiểm tra bằng Python 3.11.9, openai 2.38.0, streamlit 1.58.0:

- Import SDK/app và biên dịch Python: đạt.
- Đọc config thật; từ chối config thiếu, JSON lỗi, sai kiểu hoặc model rỗng: đạt.
- Streamlit AppTest: tiêu đề, model, prompt rỗng, key rỗng và không thêm lượt thất bại vào lịch sử: đạt.
- SDK thật với HTTP transport mô phỏng, không gửi ra mạng: payload đúng model, chỉ có user/assistant, `store=False`, response hiển thị trong UI và hai lượt hội thoại đúng thứ tự: đạt.
- HTTP mô phỏng 401/429/404/500, mất kết nối, timeout, response rỗng/chưa hoàn tất; không retry, không thay lịch sử khi lỗi, đọc lại key khi gửi: đạt.
- Server Streamlit thật tại loopback: trang HTTP 200 và health `ok`; đã dừng server sau kiểm tra: đạt.
- So sánh SHA-256 toàn bộ 212 tệp và toàn bộ đường dẫn thư mục giữa nguồn và bản sao: khớp. Bao gồm cả cache có sẵn trong nguồn; không chạy test hoặc sửa nội dung bản sao.
- `git diff --check` cho các file app/tài liệu mới: đạt. Kiểm tra toàn bản sao báo whitespace có sẵn (gồm CRLF và các dòng trong patch nguồn); giữ nguyên theo yêu cầu sao chép byte-exact, không sửa để làm sạch kiểm tra này.

Baseline tại thời điểm kiểm chứng local ban đầu: workspace chưa có app và chưa thuộc repo nào. Đã tạo repo Git local, branch `main`, lúc đó chưa có HEAD/commit hoặc remote. Các file mới có đánh dấu intent-to-add để xem diff, lúc đó chưa stage nội dung hoặc commit. `config.json` được bỏ qua. Repo nguồn có working tree sạch, branch `main`, HEAD `b3f470a46c87c4bfad68d74bf031f78d7abc87b4` khi sao chép. Không sửa repo nguồn.

Lịch sử bằng chứng: lần kiểm chứng local ban đầu ghi `LIVE API VERIFIED: NOT RUN` vì môi trường Codex thiếu API key. Xác nhận hai prompt live đã PASS từ người dùng thay thế trạng thái live trước đó; kết quả local và mô phỏng bên trên vẫn giữ nguyên phạm vi bằng chứng.
