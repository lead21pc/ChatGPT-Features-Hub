# Hub Router v1.1 — đặc tả candidate và mô phỏng

Status: CANDIDATE / NOT ACTIVE / DO NOT DEPLOY
Role: NON_RUNTIME_NORMATIVE_ORACLE
Target: HUB_ROUTER_v1.1-candidate.yaml
Evidence: STATIC / SPEC SIMULATION; LIVE ROUTING: NOT_RUN; LIVE LIBRARY RETRIEVAL: NOT_RUN

## Phạm vi và cách đọc bằng chứng

Router candidate dùng architecture v0.1 và root package Catalog v0.1, không thay Router active v1.0. Các nguồn active, headers, catalog và Library không được migration/promotion bởi đặc tả này. H01–H35, AIS và ImageT regressions hiện hành giữ nguyên.

Oracle trong tests/test_hub_router_candidate.py chỉ xử lý fixture trong bộ nhớ. Fixture khai trước semantic matches bằng tập scope; oracle không hiểu ý định từ ngôn ngữ tự nhiên và không chạy YAML như chương trình. Các identity/header/read records tổng hợp là dữ liệu kiểm contract, không phải file runtime hay Library locator. SPEC_FIXTURE_READ != LIVE FULL_FILE READ.

Đối chiếu current-route dùng bản chiếu metadata test-only từ năm entrypoint hiện hữu. Status ACTIVE trong bản chiếu fixture không đổi status CANDIDATE trong Catalog thật. CURRENT ACTIVE FILE != FUTURE MODULE ID CONTRACT. Những control chưa có header mới không bị sửa; metadata stand-in chỉ chứng minh route có thể biểu diễn.

Sau reconciliation, TECHNICAL giữ HUB-DOM-TECHNICAL / HUB-PKG-TECHNICAL, role REASONING_PROFILE. Catalog nay chuẩn bị expectation ACTIVE / 1.0 cho promotion-ready artifact chưa deployed; parity vẫn kiểm được cùng kiểu nhu cầu với TECHNICAL active v1.0, không sửa source active. DOM không được suy thành domain role. Kết quả live trial 0.1-trial và real candidate 1.0-candidate được ghi riêng theo báo cáo người dùng; không chứng minh ACTIVE revision, các mô phỏng A–M hoặc Router candidate đã live verified.

Mọi output oracle ghi runtime_ready=false, live_library_retrieval=NOT_RUN. Planned module set khác spec-verified set; thiếu read/dependency/conflict có thể chặn một root mà vẫn giữ root độc lập. Runtime Library locator còn UNRESOLVED và Project Sources chưa được xác minh thì vẫn báo runtime blocker dù fixture có identity/read record hợp lệ.

## Các ca bắt buộc

| ID | Fixture / input | Kết quả bắt buộc |
| --- | --- | --- |
| A | Singleton TECHNICAL, task cần cơ chế | Entry TECHNICAL trực tiếp; giữ role DOMAIN_CONTROL; không local catalog bắt buộc |
| B | CREATIVE + BRAINSTORM cùng task | Giữ hai module/role độc lập, không một winner |
| C | SYNTHETIC_REFINEMENT_A refine base tại X; task X+Y | A chỉ áp X; base vẫn áp Y; refinement không xóa base |
| D | A refine B, task chỉ cần phần độc lập của A | B không tự load; không tạo Requires giả |
| E | A Requires B; B Requires C | Closure A,B,C; ghi hai direct edges |
| F | A Requires B thiếu; một root độc lập khác hợp lệ | Chặn A và phần phụ thuộc; root độc lập tiếp tục |
| G | A Requires B; B Requires A | Phát hiện cycle; chặn các root phụ thuộc, không lặp vô hạn |
| H | A Complements B | A không tự nạp B; nếu B independently matches thì giữ cả hai, không dominance |
| I | Candidate package/module semantically matches | Không auto-select như ACTIVE; explicit active request bị chặn |
| J | Package lớn có local catalog, root chỉ một entry | Router/root không enumerate leaf IDs; owner giữ local inventory |
| K | Package có 24 leaf fixtures rồi tăng lên 40 | Router và root giữ nguyên bytes/data; chỉ leaf liên quan và hard closure có spec read requests |
| L | Domain + AIS | Hub chọn pipeline entrypoint độc lập; oracle không đọc AIS internals |
| M | Turn/scope mới không cần module trước | Tập mới không giữ activation cũ; task baseline trả tập rỗng |

## Parity và lỗi bổ sung

Kiểm baseline NONE; từng entrypoint trong năm entrypoint hiện tại; combination domain/capability/pipeline, nhiều task portions và reassessment. Package selection xét interface; singleton/growing dùng cùng thuật toán dispatch. Chuyển sang growing có thể cập nhật local_catalog interface metadata, nhưng thêm leaf sau đó không thay root/Router.

Kiểm root missing/unreadable, unknown package, missing entrypoint, required local catalog thiếu, leaf unresolved, duplicate identity trong fixture deployment context, wrong Module ID/Package ID/role/version/status, header/snippet thay FULL_FILE, same-scope conflict và unsupported cross-package relation. Requires đến pipeline không tự activate pipeline; Hub phải chọn pipeline độc lập. Cross-package target phải có owner Package ID và declaration được chấp nhận.

REFINES và COMPLEMENTS chỉ tạo nhu cầu xét scope, không dependency traversal. Base context có thể cần đọc nếu coverage/boundary không xác lập được, nhưng fixture có coverage rõ không phải tải target chỉ vì relation tồn tại. Quan hệ mơ hồ hoặc không được chấp nhận chặn phần phụ thuộc; không suy hierarchy.

## Boundary Library và pipeline

CENTRAL HUB CONFIG = SOLE LIBRARY DISCOVERY ROOT. Không có Library search/call trong oracle. Null locator không đổi thành repository_path, Project Sources, Memory, archive, prior chat hoặc lookalike. Kiểm fixture root sai/locator không resolve và Library unavailable bằng blocker, không gọi retrieval thật.

AIS/ImageT là opaque entrypoints; không nạp modes/stages, manifest slots hoặc gate internals qua generic Router. Pipeline sở hữu dependency nội bộ và authorization riêng. Không chạy image/research tool trong tests.

## Chạy và nghiệm thu

Từ Central Hub chạy `python -B -m unittest discover -s tests -v`. PASS chỉ xác nhận từng thuộc tính tĩnh hoặc kết quả oracle được assert. Không suy chất lượng semantic selection bằng model, runtime performance, deployment hoặc Library retrieval từ kết quả này.

Thử live sau này cần ủy quyền riêng, binding/header được migration và locator thật đã resolve bên trong Central Hub Config. Ghi inputs, versions, nguồn thực đọc, output/calls quan sát được và giới hạn. STATIC / SPEC PASS != LIVE ROUTING VERIFIED. Chưa thực hiện live trial trong mốc này.
