# Central Hub Local — phương án backup

Quyết định đóng workstream ngày 2026-11-05: Central Hub local/API được giữ làm **BACKUP**, functional status **VERIFIED + LIVE VERIFIED** theo bằng chứng M1/M2 và các workload đã chạy. **M3 CLOSED**; không tiếp tục tối ưu chi phí/token/cache, không có kế hoạch retry mặc định và **M4 NOT STARTED**. Một backup path hoạt động và đã kiểm chứng là mục tiêu hoàn tất; API không cần rẻ hơn subscription để được coi là thành công. Chỉ mở lại M3 khi người dùng yêu cầu rõ ràng.

Experiment 1 đã live-run nhưng không đạt mục tiêu cache reuse. Experiment 2 explicit cache đạt static verification, nhưng live attempt bị chặn tại root bởi `429 project_spend_limit_exceeded`, trước Concept call: **LIVE NOT ESTABLISHED / CLOSED WITHOUT PROMOTION**. Runtime giữ baseline đã restore `8f5487ca8b124edb339192a9704b5d74157bcf00`; không áp lại patch candidate. Xem [trạng thái M3 cuối](m3_evidence/M3_FINAL_STATUS.md) và [VERIFICATION.md](VERIFICATION.md); toàn bộ `m3_evidence/` được giữ làm lịch sử.

Checkpoint M2 ngày 2026-11-05: Authoring **0.7 ACTIVE trong runtime local**, Architecture/Catalog 1.9; CI/Router 1.1. Binding v0.2/v0.3 dùng bản 0.7 byte-exact. Exact `/AUTHOR <OUTPUT_TARGET> ISOLATED` hoặc `/AUTHOR <OUTPUT_TARGET> P<n> ISOLATED` giới hạn nguồn task material cho lượt hiện tại; không có suffix thì giữ hành vi 0.6. Không xóa lịch sử, không lưu chế độ và không cấp quyền chạy target. Contributor + ISOLATED không kích hoạt. Các mô tả phiên bản trong hồ sơ T0–T9 bên dưới giữ bối cảnh kiểm chứng lịch sử; xem [VERIFICATION.md](VERIFICATION.md) và [bằng chứng 0.7](m2_evidence/authoring_0_7/) cho kết quả hiện tại. Tại checkpoint M2 này chưa bắt đầu M3/M4; quyết định đóng M3 hiện tại nằm ở đầu tài liệu.

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

4. Mở [giao diện local](http://127.0.0.1:8501), nhập prompt rồi bấm **Send**. Mặc định là **Central Hub - Local Runtime**: Hub → Root Router → tập package được chọn → phản hồi. Chỉ gửi khi muốn chạy API thật; M1 được kiểm chứng bằng static/mock, không tự chạy chiến dịch live.

Lịch sử chỉ giữ trong Streamlit session, không ghi xuống `sessions/`. Khi tải lại trang hoặc khởi động lại app, lịch sử có thể mất. Lượt lỗi không được thêm vào lịch sử; prompt vẫn còn để gửi lại. Nếu thiếu key, hết quota, mất mạng hoặc không có quyền truy cập model, giao diện hiển thị lỗi; đó chưa phải live PASS.

Chọn **Chế độ** trước khi gửi:

- **Central Hub - Local Runtime** (mặc định): `m1.call_runtime(config, messages)` chọn root một lần bằng chính CI/Router/Architecture/Catalog hiện hành, kiểm tra identity/version/source rồi dùng inventory binding v0.3 sẵn có. Không chọn package thì dùng Hub baseline. Technical/Concept dùng lại truy xuất/hash và chọn leaf của T7 qua T8; Authoring dùng nguyên admission, contributor và quy tắc kết thúc ở prompt artifact của T8. AIS dùng lại kiểm tra Catalog, truy xuất cặp pipeline/router và kiểm tra bằng chứng `web_search_call` của T9, với native Responses `web_search`. Hub nhận bằng chứng AIS và giữ quyền diễn đạt kết luận/trạng thái. Khi Technical/Concept được root chọn độc lập cùng Authoring, kết quả theo phạm vi được chuyển cho Authoring để làm căn cứ; thân control không được đưa vào pha Authoring cuối. Việc soạn prompt cho AIS/ImageT không tự chạy target. Chọn root ImageT gây lỗi `local-runtime unavailable`, không đọc body, không mô phỏng hoặc fallback. Lỗi root/package/binding/tool chặn lượt, giữ history và prompt; M1 hiện dừng cả lượt khi có blocker. Hàm trả `(answer, trace)`; UI chỉ hiện phản hồi hoặc lỗi. Các chế độ T0–T9 bên dưới vẫn là đường chẩn đoán/hiệu chuẩn.
- **T0 - Raw API**: API thuần như Giai đoạn 1, không nạp CI, không gửi `instructions`.
- **T1 - Hub CI**: cùng model, tham số và lịch sử như T0; mỗi request đọc nguyên nội dung UTF-8 của `upstream/Central Hub/HUB_CI_v1.1.md` vào trường `instructions` của Responses API. Không sửa CI, không nạp Router hoặc module nào khác. Nếu không đọc được CI, ứng dụng báo lỗi và không gửi request, không chuyển sang T0.
- **T2 - Hub CI + Technical**: mỗi request đọc nguyên CI trên và `runtime/packages/technical/HUB-DOM-TECHNICAL_v1.0.md`, ghép vào `instructions` theo thứ tự CI → ghi chú liên kết kiểm thử cục bộ → Technical. Ghi chú chỉ xác định Technical được chọn thủ công cho phần yêu cầu/nhiệm vụ hiện tại vì Router vắng mặt; không thay đổi ngữ nghĩa Technical. Bản runtime sao chép byte-exact từ nguồn ACTIVE v1.0 tại `upstream/Central Hub/candidates/promotion/HUB-DOM-TECHNICAL_v1.0.md`. Thiếu hoặc không đọc được một trong hai control sẽ báo lỗi trước API, không chuyển sang T1/T0. Đây là phép thử một module chọn thủ công; không nạp Router, Architecture, Root Catalog hay package khác.

- **T3 - Hub Routing Inspect**: chỉ mô phỏng `eligibility.simulation` của Router, thực hiện `TASK_SCOPE` và `ROOT_PACKAGE_SELECTION`. Mỗi request đọc nguyên bốn control hiện hành trong `upstream/Central Hub/`: `HUB_CI_v1.1.md`, `HUB_ROUTER_v1.1.yaml`, `HUB_ARCHITECTURE_v1.8.md`, `HUB_PACKAGE_CATALOG_v1.8.yaml`, kèm adapter tiếng Anh tối thiểu. Model chọn package theo ngữ nghĩa; Python chỉ yêu cầu, phân tích và kiểm tra cấu trúc bản ghi qua Responses API Structured Outputs (`text.format`, `json_schema`, `strict=true`, `store=False`). UI hiển thị JSON có nhãn T3; `selected_packages: []` là NONE. Thiếu hoặc không đọc được bất kỳ control nào sẽ báo lỗi trước API, không chuyển chế độ hoặc dùng nguồn thay thế. T3 dừng trước truy xuất/thực thi package, không đọc package body, không giải quyết Library/filesystem binding và không gọi công cụ.

- **T4 - Hub CI + Concept Core**: hiệu chuẩn chọn thủ công `HUB-PKG-CONCEPT-DEVELOPMENT` cho phần yêu cầu/nhiệm vụ hiện tại, không chạy Router. Mỗi request đọc lại CI → ghi chú T4 tối thiểu bằng tiếng Anh → core 1.1 → Catalog cục bộ 1.1 vào `instructions`, qua `call_model` để trả lời thông thường. Hai tệp trong `runtime/packages/concept-development/` là bản sao nguyên byte của nguồn ACTIVE cùng tên trong `upstream/Central Hub/library_modules/`. Catalog là metadata lựa chọn bắt buộc của core; không cung cấp thân leaf. Span hợp lệ có thể được nhận diện nhưng thực thi chuyên biệt bị chặn; cụm từ tự nhiên không kích hoạt leaf. Công việc concept thông thường đủ dữ kiện tiếp tục qua core. Thiếu tệp, lỗi đọc hoặc UTF-8 ở CI/core/Catalog sẽ dừng trước API, không chuyển chế độ. Đây không phải thực thi package tích hợp Router, truy xuất Library hay migration binding cục bộ. Không nạp Creative, Brainstorm, Debate, anti-drift hoặc package khác.

- **T5 - Concept Scoped Leaves**: chọn thủ công Concept package, dùng `call_model` trả lời thông thường. Mỗi request đọc lại CI → adapter hiệu chuẩn cục bộ → core 1.1 → Catalog cục bộ 1.1 → Creative 1.1 → Brainstorm 1.1 → Debate 1.0. Core/Catalog nhận diện và chọn span; Python chỉ nạp nội dung, không phân tích control. Ba leaf khả dụng tại local chỉ thực thi trong span hợp lệ được chọn, không duy trì qua terminator hoặc lượt sau. Không nạp anti-drift hay package body khác. Thiếu/lỗi đọc/UTF-8 ở bất kỳ tệp bắt buộc nào sẽ dừng trước API, giữ history, không fallback. Đây là calibration package chọn thủ công, không tích hợp retrieval Router và không migration ChatGPT Library. Debate được kiểm tra byte-exact với upstream ACTIVE cho **T5 local test binding only**; binding ChatGPT Library cũ vẫn UNRESOLVED. Kết quả live có PARTIAL/FAILURE; xem `VERIFICATION.md`.

- **T6 - Concept + Technical Composition**: hiệu chuẩn phối hợp thủ công Technical 1.0 và Concept Development 1.1. Mỗi request đọc lại nguyên byte CI → adapter T6 tiếng Anh tối thiểu → Technical → Concept core → Catalog cục bộ → Creative → Brainstorm → Debate. Mỗi package chỉ đóng góp trong trách nhiệm hiện có; Python không chia phạm vi, chọn package hay phân tích span. Thiếu/lỗi đọc/UTF-8 ở bất kỳ tệp bắt buộc nào sẽ dừng trước API, giữ history và route records, không fallback. Binding cũ giữ nguyên: Debate có thể tiếp tục bị chặn; Authoring cố ý không được nạp vì binding cũ UNRESOLVED/NOT_PERFORMED, không mô phỏng Authoring. Không tích hợp retrieval Router hoặc migration binding Library. T6 đã qua 29/29 kiểm thử tĩnh và live composition A–H đạt trong phạm vi đã thử; xem VERIFICATION.md. Kết quả live không chứng minh T6 tạo năng lực mới so với T2/T5, chỉ chứng minh ranh giới phối hợp trong campaign hiện tại.

- **T7 - Router Local Retrieval**: model chọn root package qua Structured Outputs từ CI 1.1, Router 1.1, Architecture 1.8, Root Catalog 1.8 và manifest local được đọc lại mỗi request. Python kiểm tra identity, đường dẫn trong `runtime/` và SHA-256 trước khi dùng nội dung. Nếu chọn Concept, model đọc core + Catalog để chọn leaf trước khi Python nạp riêng leaf đó. Payload cuối theo thứ tự CI → ghi chú T7 → Technical nếu được chọn → core + Catalog Concept nếu được chọn → leaf được chọn theo thứ tự manifest. Không chọn package thì chỉ dùng CI và ghi chú T7. `call_t7(config, messages)` trả `(answer, trace)` cho kiểm chứng nội bộ; UI thường chỉ hiển thị phản hồi và nhãn chế độ.

`runtime/HUB_LOCAL_BINDINGS_v0.1.json` là chủ sở hữu binding local duy nhất của T7, chỉ bind Technical và năm artifact Concept. JSON phục vụ khả năng đọc bằng thư viện chuẩn Python, tránh thêm PyYAML; đây không phải lựa chọn kiến trúc mới. Binding kế nhiệm chỉ đổi nơi lưu/truy xuất sang `LOCAL_RUNTIME_FILE`, không xác minh ChatGPT Library hoặc sửa metadata nguồn cũ. Authoring/AIS/ImageT chưa có binding, không nạp body hoặc mô phỏng; phần độc lập đủ dữ kiện vẫn có thể tiếp tục. Lỗi control/config dừng trước API; lỗi artifact đã chọn chặn phần phụ thuộc, không fallback hoặc đổi chế độ. T7 đã qua 47/47 kiểm thử tĩnh và live A–I đạt trong phạm vi đã thử. Debate được chọn, hash-verify, truy xuất và thực thi thành công qua LOCAL_RUNTIME_FILE; điều này giải quyết failure host-binding T5 trên đường T7 local, không thay đổi trạng thái ChatGPT Library cũ.

T3 chỉ gửi prompt hiện tại, không gửi lịch sử T0/T1/T2/T4/T5/T6/T7 hoặc các bản ghi T3 trước đó. Các bản ghi T3 được giữ riêng trong session, không đưa vào lịch sử trả lời thông thường. Phản hồi lỗi, bị từ chối, chưa hoàn tất, thiếu văn bản hoặc JSON sai cấu trúc không tạo bản ghi mới; prompt và bản ghi thành công trước đó vẫn còn. Dùng **session mới cho mỗi ca so sánh T3 sạch**. Khi kiểm tra thủ công, chọn T3, gửi `Giải thích RAM và SSD khác nhau thế nào.` rồi xác nhận bản ghi có nhãn T3 và NONE; dùng session mới cho yêu cầu chẩn đoán nguyên nhân máy khựng để kiểm tra lựa chọn Technical.

Với T0/T1/T2/T4/T5/T6/T7/T8/T9, chế độ hiện ở phía trên và cạnh từng phản hồi. Đổi chế độ giữ nguyên lịch sử chung giữa chín chế độ này, kể cả phản hồi từ chế độ trước; nhãn chế độ không gửi vào API. Để so sánh A/B T0/T1/T2/T4/T5/T6/T7 với lịch sử trống, mở session mới cho mỗi phép thử. Kiểm tra T1 bằng hai prompt tương tự bước 4, thay `T0 OK` bằng `T1 OK`. Với T2, dùng session mới, chọn T2 và hỏi chẩn đoán máy khựng khi mở nhiều tab nhưng chưa có log; hỏi tiếp nguyên nhân nào chắc chắn nhất. Kiểm tra phản hồi có giữ nguyên nhân chưa xác định, phân biệt triệu chứng/giả thuyết và đưa phép kiểm tra phân biệt có giới hạn.

`upstream/Central Hub/` là bản sao tham chiếu nguyên trạng từ `<WORKSHOPS_REPO>\Central Hub`, repo nguồn tại HEAD `b3f470a46c87c4bfad68d74bf031f78d7abc87b4`, working tree sạch khi sao chép. T0 không đọc thư mục này; T1 và T2 chỉ đọc đúng `HUB_CI_v1.1.md` từ upstream khi chạy. Technical trong T2 được đọc từ bản runtime riêng, không đọc nguồn promotion. Ứng dụng không ghi vào bản sao.

Ứng dụng dùng [Responses API](https://developers.openai.com/api/docs/quickstart) và model [GPT-5.6 Sol](https://developers.openai.com/api/docs/models/gpt-5.6-sol). T3 dùng [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs?api-mode=responses). Quyền truy cập model phụ thuộc tài khoản API thực tế.

- **T8 - Authoring Lifecycle**: dùng riêng `runtime/HUB_LOCAL_BINDINGS_v0.2.json` gồm Technical + Concept như v0.1 và Authoring 0.6. Mỗi lượt đọc lại controls và manifest; root model không nhận inventory leaf hoặc manifest thô. Sau root selection, host xác minh hash/UTF-8 Authoring và model quyết định admission hiện tại qua Structured Outputs. Python không phân tích `/AUTHOR`. Inactive chỉ dùng Hub CI ở pha cuối; activation không duy trì qua lượt hay clarification/reauthor.

T8 active tạo một prompt rồi dừng; target AIS/IMAGET/CODEX/WORK/GENERIC và preset không cấp phép thực thi target. Với CREATIVE/BRAINSTORM, Concept owner phân giải theo core/Catalog chính xác; chỉ leaf được chọn và xác minh mới được đọc, thực thi thành contribution có scope/provenance/protected constraints. Nhãn contributor không bỏ qua gate Concept. Contributor lỗi chặn prompt phối hợp, không thay bằng single-target tương đương. Pha Authoring cuối nhận contribution thực tế, không nhận lại raw Concept/leaf controls; nội dung sinh ra không tự trở thành canon/design được chấp nhận.

`from t8 import call_t8`; `call_t8(config, messages)` trả `(answer, trace)` với root/retrieval, admission target/preset/contributor, contributor retrieval và blockers. UI dùng lịch sử thường và nhãn T8; T3 vẫn tách riêng. T7 chỉ dùng v0.1 và không có Authoring binding. Metadata ChatGPT Library cũ vẫn `UNRESOLVED / NOT_PERFORMED`; v0.2 là binding kế nhiệm local riêng, không sửa upstream.

T8 static/mock sau correction đạt 23/23; full T0–T8 đạt 70/70. Live campaign dùng 3/4 user requests rồi dừng đúng cost policy: single-target/preset và no-persistence PASS; contributor path lộ sequencing failure, đã sửa cục bộ và kiểm static/mock nhưng chưa live-reverify. Không chạy request thứ 4. Xem VERIFICATION.md.

- **T9 - AIS Local Execution**: mỗi lượt đọc lại Hub CI 1.1, Router 1.1, Architecture/Catalog 1.8 và manifest v0.3. Root model chọn scope bằng Structured Outputs; chỉ AIS được chọn mới được đọc cặp pipeline 1.1/router 1.2 và xác minh SHA-256. Không chọn AIS thì không đọc AIS, không có web_search và trả lời bằng Hub CI baseline. Các package khác chỉ được giữ scope, không được thực thi trong T9.

Executor là [native OpenAI Responses API web_search](https://developers.openai.com/api/docs/guides/tools-web-search), với `tool_choice="required"` và `include=["web_search_call.action.sources"]`. AIS trả evidence artifact về pha Hub cuối không có tools; Hub giữ câu trả lời và claim/state. `from t9 import call_t9`; hàm trả `(answer, trace)`, UI chỉ hiện câu trả lời và nhãn chế độ.

v0.3 giữ nguyên các entries v0.2, chỉ thêm AIS. v0.1/v0.2 và metadata Project Sources cũ giữ nguyên; local binding không tuyên bố Project deployment. ImageT: **OUT OF SCOPE / REMOVED FROM THIS MIGRATION** theo quyết định người dùng.

T9 hiện đã qua 15/15 kiểm thử tập trung và 85/85 full suite. Live dùng đúng **1 user request** có lực phân biệt cao: Root chọn AIS, local pipeline/router được SHA-256 verify, native `web_search` tạo `web_search_call` hoàn tất, source/citation URL được capture và evidence quay về Hub với blocker rỗng. Negative-control live không chạy vì static đã phủ đường no-AIS và không tạo thêm bằng chứng đáng kể.

ImageT đã được loại khỏi migration này theo quyết định người dùng; không có T10/ImageT trong kế hoạch hiện tại. Xem `VERIFICATION.md` để phân biệt checkpoint tĩnh cũ, incident mock/concurrent-write và PASS live cuối.
