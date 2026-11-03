# Authorize Integrity Search (AIS)

**Trạng thái: candidate / thiết kế local v0.1, chưa được chấp nhận hoặc triển khai.**

AIS là package hướng dẫn cho một ChatGPT Project chuyên tìm kiếm, kiểm chứng và nghiên cứu. AIS tham gia hệ quản trị và vòng phản hồi của repo hiện tại. Đây không phải repo riêng, sản phẩm search công khai, SaaS hay search engine tổng quát.

## Các file

- [AIS CI v0.1](./Authorize%20Integrity%20Search%20CI/AIS_CI_v0.1.md): hành vi nền, cửa vào router, ranh giới thao tác và chứng cứ.
- [AIS Router v0.1](./Authorize%20Integrity%20Search%20Modules/AIS_SOURCE_ROUTER_v0.1.yaml): mode, contract tạm, nguồn, thực thi và hợp nhất chứng cứ.
- [Route test cases](./tests/ROUTE_TEST_CASES.md): tình huống khai báo và tiêu chí quan sát; chưa phải kết quả runtime.

## Runtime dự kiến và giới hạn

```text
ChatGPT Project -> AIS CI -> AIS Router
                               |-> DIRECT -> reasoning -> response
                               |-> Work/platform-native research
                                   -> evidence -> reasoning -> response
```

Ưu tiên subscription và hạ tầng native OpenAI. Đây là tiền đề lựa chọn triển khai; không bảo đảm tài khoản có mọi công cụ, quyền đọc nguồn hoặc giới hạn cần thiết. CI/router chỉ điều khiển hành vi chuẩn bị, đánh giá và trả lời; Work/platform sở hữu thực thi. YAML không tự khởi chạy Work.

Theo [Projects and chats — OpenAI](https://learn.chatgpt.com/docs/projects), Project có thể chứa chat dùng Chat hoặc Work; ChatGPT Project không tự đọc thư mục máy tính. Tài liệu này được đọc ngày 2026-10-15, chỉ hỗ trợ ranh giới tổ chức đó, không chứng minh AIS đã hoạt động. Khi thử runtime sau này, cần chủ động đặt CI trong Project instructions và cung cấp đúng router vào Project Sources; đường dẫn repo không thay nguồn runtime. **Task hiện tại không thực hiện các bước này.**

Memory và sự quen thuộc từ prior chat không là source of truth, evidence, authority, runtime state bắt buộc hoặc fallback. Một claim chỉ có Memory vẫn chưa xác minh. Contract và theo dõi chứng cứ chỉ cần tồn tại trong thao tác; không cần database, cache hay file state.

## Inspection và lựa chọn DNA

Đã đọc trực tiếp các file sau trong working tree trước khi thiết kế. Các liên kết dưới đây phục vụ truy nguyên thiết kế, **không là dependency hoặc authority runtime của AIS**:

| Nguồn đã đọc | Kết luận dùng cho thiết kế |
| --- | --- |
| [Global CI v8.9](../llm-controls/global-instructions/ChatGPT%20Plus%2B%20Era/chatgpt%20v8.9.txt) | Design parent: grounding -> chức năng lượt nói -> không tăng mức xác nhận; giữ state, kiểm chứng claim phụ thuộc và product/runtime thay đổi. AIS viết lại đủ quy tắc cần dùng, không yêu cầu load Global CI. |
| [FTH CI v3.4 candidate](../Project%20Feather%20Core/Project%20Feather%20Core%20CI/candidates/FTH_CI_version_v3.4.md) | Giữ entry do CI sở hữu, route trước conclusion, findings không mở task và chỉ block phần phụ thuộc. Candidate không chứng minh active deployment. |
| [FTH Router v5.0](../Project%20Feather%20Core/Anti-Drift%20Source/FTH_Anti_Drift_Source_Router_v5.0.yaml) | Giữ read != hit, metadata != authority, bounded partial và reroute. Local router khai báo CI 3.3/base 8.8; không đổi khai báo này sang candidate 3.4. |
| [ImageT v1.0.0](../Image%20Transcendent/Image%20Transcendent%20CI/ImageT_v1.0.0.md), [router](../Image%20Transcendent/Image%20Transcendent%20Modules/IMAGE_SOURCE_ROUTER.yaml), [manifest](../Image%20Transcendent/Image%20Transcendent%20Modules/manifest.yaml) | Manifest trong checkout chỉ định baseline 1.0.0, router 2.0.0-yaml-candidate; không suy live state. Giữ operation lock, bảo vệ field ngoài delta, không claim tool chưa chạy; listing/applicability không tự activation. |
| [SYSTEM_CONTEXT](../SYSTEM_CONTEXT.md), [README repo](../README.md) | Đặt AIS vào control/feedback loop hiện có; nguồn repo, quyết định tác giả và runtime là các lớp chứng cứ khác nhau. |

Không mang sang AIS canon, ontology, Library FTH, Module ID, closure graph, bootstrap index/open issues, authoring pipeline hay overlay chuyên lore. Không mang manifest/version selection, image template, visual priority, anatomy/topology, Ready Gate hay chấm ảnh của Image Transcendent. Các primitive đó giải quyết domain khác.

```text
SHARED CONTROL DNA != SHARED DOMAIN
LINEAGE != RUNTIME DEPENDENCY
SIMILAR ROUTING != IDENTICAL ROUTER
```

## Phần riêng của search

Bốn mode tách theo chức năng: DIRECT không cần nguồn ngoài; VERIFY kiểm claim xác định; RESEARCH giải câu hỏi cần thông tin ngoài; EXPLORE mở option space. Brainstorm không cần nguồn ngoài vẫn DIRECT. Task hỗn hợp tách phần, không thêm taxonomy. Mode là cách định tuyến chứng cứ, không thay operation/stage của người dùng.

Giữ bảy stage nhỏ theo thứ tự khai báo trong router. DIRECT bỏ qua các stage tìm kiếm. Contract tạm khóa câu hỏi, known/unknowns, authority, allowed/protected update scope và điều kiện dừng. Policy nguồn nằm ngay router vì chưa có trách nhiệm riêng buộc tách file: freshness, primary/direct support, corroboration, conflict, injection và thiếu decisive evidence.

CI và router v0.1 được viết bằng tiếng Anh gọn; AIS vẫn trả lời bằng tiếng Việt trừ khi có yêu cầu khác. Khi câu hỏi hoặc đích kiểm chứng thay đổi đáng kể, phải định tuyến lại và thay contract bị ảnh hưởng dù phạm vi không rộng hơn; chỉ refine query cho cùng câu hỏi thì giữ contract.

## Vai trò trong quản trị và phản hồi

AIS trả kết quả có nguồn và giới hạn cho tác giả đánh giá; không tự cập nhật control, requirement, canon hoặc project khác. Vòng phản hồi dùng cùng mô hình repo: sử dụng thật -> quan sát lỗi -> phân tích nguyên nhân -> đề xuất có phạm vi -> tác giả đánh giá -> thay đổi được cho phép -> kiểm tra cấu trúc và thử runtime -> giữ/sửa/rollback. Đây là quy trình có quyết định người dùng, không phải automation hoặc quyền sửa ngầm.

Repo/local files != live Project deployment. Local package != accepted design hoặc active runtime. Output nghiên cứu và test cấu trúc không tự promotion. Baseline Git lúc bắt đầu: repo cha `CI Versioning Audit & Changelog`, branch `main`, HEAD `68e693e927b5f7d1f61cde881ef53f0b17b75268`; dirty state ngoài AIS được giữ nguyên. Task này không stage, commit, push, tạo branch/tag, sửa remote hoặc deploy.

## Độ phức tạp và bước thử tiếp theo

`LOW DENSITY -> TEST -> ADD COMPLEXITY ONLY WHERE FAILURE REMAINS`.

Chưa có failure hiện tại cần manifest, registry, validator framework, overlay, resolver, catalog hoặc source-ranking engine. Chưa cần control/config thứ năm. Không thêm Brave, OpenAI API, MCP riêng, backend, database, cache service, agent framework hay external provider. Chỉ xem xét integration khi thử native runtime chứng minh một concrete gap và người dùng cho phép; không có integration chờ sẵn.

Những câu hỏi cần thử thật: CI/router có được đọc và tuân thủ trong Project + Work không; công cụ có mở được nội dung quyết định và trả nguồn đủ để đánh giá support không; bốn mode, scope lock, contract, conflict và partial có giữ đúng qua nhiều bước/lượt chat không. Dùng quy trình trong test cases để ghi nhận, không coi việc có file là đã pass.
