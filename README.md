# ChatGPT Features Hub

**Một workspace ChatGPT đa dụng để chẩn đoán kỹ thuật, phát triển ý tưởng, soạn prompt, nghiên cứu, xử lý ảnh và hỗ trợ quyết định mua sắm.**

[Cách Hub xử lý công việc](#cách-hub-xử-lý-công-việc) · [Các gói hiện hành](#các-gói-hiện-hành) · [Soạn prompt](#soạn-prompt-với-authoring) · [Chọn điểm bắt đầu](#chọn-điểm-bắt-đầu) · [Trạng thái kiểm chứng](#trạng-thái-kiểm-chứng)

## Hub được xây dựng để làm gì

Central Hub là dự án cá nhân phát triển qua sử dụng thực tế, từ việc ghi nhận lỗi hành vi của mô hình đến điều chỉnh Custom Instructions, kiểm tra hồi quy và thử nghiệm từng revision. **ChatGPT Web / Project + Library** là môi trường chính. Các hợp đồng hiện hành nằm trong [Central Hub/](<Central Hub/README.md>).

## Cách Hub xử lý công việc

Hub giữ mục tiêu của yêu cầu hiện tại và giao từng phần việc cho gói phù hợp. Một lượt giải thích hoặc trao đổi thông thường có thể chỉ cần Hub CI. Khi nhiều gói cùng tham gia, mỗi gói đóng góp trong phạm vi được giao và Hub tổng hợp kết quả.

```text
Yêu cầu hiện tại
  ↓
Hub CI · thao tác, trạng thái và quyền hành động
  ↓
Router + Catalog · phạm vi, lựa chọn gói và xác minh nguồn
  ↓
Gói được chọn · mô-đun nội bộ hoặc pipeline theo phạm vi
  ↓
Hub tổng hợp kết quả
```

[Hub CI 1.1](<Central Hub/HUB_CI_v1.1.md>) là Custom Instructions của Project. [Router 1.1](<Central Hub/HUB_ROUTER_v1.1.yaml>) dùng [Architecture 1.10](<Central Hub/HUB_ARCHITECTURE_v1.10.md>) và [Package Catalog 1.10](<Central Hub/HUB_PACKAGE_CATALOG_v1.10.yaml>) để xác định gói, kiểm tra binding và phân công theo phạm vi. Gói tự phân giải mô-đun nội bộ theo Catalog của mình. ChatGPT thực hiện truy xuất và gọi công cụ khi có đủ điều kiện.

## Các gói hiện hành

| Gói | Vai trò trong yêu cầu |
| --- | --- |
| **Technical** | Giải thích cơ chế, phân biệt giả thuyết và thiết kế phép kiểm tra để xác định nguyên nhân hoặc kiểm chứng một thay đổi kỹ thuật. |
| [**Concept Development**](<Central Hub/library_modules/HUB-DOM-CONCEPT-DEVELOPMENT_v1.1.md>) | Phát triển và kiểm tra ý tưởng. Creative mở rộng bên trong tiền đề, Brainstorm phát triển các nhánh và Debate phản biện đề xuất. |
| [**Authoring**](<Central Hub/library_modules/HUB-CAP-AUTHORING_v0.7.md>) | Chuyển yêu cầu thành prompt tự chứa cho đích được chọn. |
| [**AIS**](<Central Hub/tool_pipelines/AIS/AIS_PIPELINE_v1.1.md>) | Tìm, đọc và đánh giá bằng chứng bên ngoài để Hub sử dụng trong phần việc cần nghiên cứu. |
| [**ImageT**](<Central Hub/tool_pipelines/ImageT/IMAGE_CONTROLLER_v1.2.md>) | Phân tích ảnh và chuẩn bị hoặc thực hiện thao tác ảnh theo quyền và điều kiện kiểm tra của pipeline. |
| [**Shopping**](<Central Hub/library_modules/HUB-DOM-SHOPPING_v1.0.md>) | So sánh phương án mua theo yêu cầu, SKU, offer, giá và độ phủ bằng chứng. Hub chọn AIS độc lập khi cần nghiên cứu bên ngoài. |

## Soạn prompt với Authoring

Dùng `/AUTHOR` với đích được chọn, sau đó mô tả yêu cầu bằng ngôn ngữ thông thường. Authoring tạo prompt và kết thúc ở đó.

```text
/AUTHOR CODEX
Soạn prompt để Codex chẩn đoán vì sao ứng dụng chậm khi mở tệp lớn.
Yêu cầu đo trước khi đề xuất thay đổi.
```

Thêm `ISOLATED` khi muốn giới hạn nguồn nội dung cho lượt soạn prompt hiện tại. Các đích, preset và điều kiện kích hoạt nằm trong [hợp đồng Authoring 0.7](<Central Hub/library_modules/HUB-CAP-AUTHORING_v0.7.md>).

## Chọn điểm bắt đầu

| Bạn muốn | Điểm vào |
| --- | --- |
| Đọc hoặc đánh giá bộ ChatGPT Project + Library | [Mục lục Central Hub](<Central Hub/README.md>) |
| Xem các điều kiện chọn gói và truy xuất | [Architecture](<Central Hub/HUB_ARCHITECTURE_v1.10.md>) và [Package Catalog](<Central Hub/HUB_PACKAGE_CATALOG_v1.10.yaml>) |
| Đối chiếu promotion và kết quả theo revision | [Hồ sơ runtime](<Central Hub/RUNTIME_EVIDENCE_CHANGELOG.md>) và [kiểm thử Hub](<Central Hub/tests/>) |
| Thử bản dự phòng Python/Responses API | [Hướng dẫn Local/API](legacy/README.md) |
| Tìm snapshot 1.9 hoặc bằng chứng M2/M3 | [Hồ sơ kiểm thử Local/API](legacy/README.md) và [VERIFICATION.md](VERIFICATION.md) |

## Trạng thái kiểm chứng

Bộ nguồn hiện hành dùng CI/Router 1.1 và Architecture/Catalog 1.10. Nguồn được tách từ thư mục Central Hub của ChatGPT Creative Workshops tại commit `e310b451`. Các kiểm tra tĩnh và mô phỏng Local/API trên bộ 1.10 đã chạy. Các lượt live Responses API trước đó giữ phạm vi theo workload và revision đã ghi. Trạng thái Library, Project và định tuyến Shopping live được theo dõi riêng trong [hồ sơ Shopping 1.0](<Central Hub/SHOPPING_PROMOTION.md>).

<details>
<summary>Bản dự phòng Local/API</summary>

Entry point Python và binding local vẫn ở gốc repository và trong `runtime/`. Runtime đọc control hiện hành từ `Central Hub/`. Streamlit mặc định chạy ở `127.0.0.1`. MCP cung cấp kiểm tra chỉ đọc qua stdio. Shopping và ImageT chưa có binding local.

Chạy kiểm thử Local/API từ gốc repository bằng `python -X utf8 -B -m unittest discover -s legacy/tests`. Snapshot 1.9, log và bằng chứng M2/M3 nằm trong [legacy/](legacy/).

</details>
