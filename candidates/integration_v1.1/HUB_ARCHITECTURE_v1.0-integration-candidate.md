# Central Hub — kiến trúc tích hợp hạ tầng dùng chung v1.0

Module ID: HUB-CORE-ARCH
Runtime role: CORE_ARCHITECTURE
Scope: shared Central Hub topology, module/package identity, Library resolution, composition and common failure behavior
Status: CANDIDATE
Version: 1.0
Responsibility boundary: shared technical architecture only; no global behavior, domain, pipeline or tool authorization ownership

## 1. Trạng thái và quyền sở hữu

Đây là integration contract CANDIDATE, NOT ACTIVE production. Chỉ bộ core có tên chính xác trong CI/Router integration được dùng khi người dùng cài thủ công và ủy quyền live integration trial. Sự hiện diện không kích hoạt. Quyền thử core candidate không cho phép chạy package candidate hoặc tự triển khai. Hub CI/Router v1.0 trong repository giữ nguyên.

Tài liệu chỉ định nghĩa kiến trúc kỹ thuật chung. Hub CI giữ operation/stage/state/truth/action, nhu cầu kiểm chứng, authorization chung và cách giải thích. Hub Router giữ lựa chọn/composition có phạm vi. Package/module giữ hành vi chuyên biệt; pipeline giữ quy trình nội bộ. Tài liệu không sở hữu domain knowledge, phương pháp AIS, generation mechanics ImageT, tool authorization internals, canon/semantic truth hoặc ontology chung của các ngành.

Contract không phải chương trình thực thi, resolver service hay state engine. Không thêm registry, graph engine, scoring, ranking hoặc package manager.

## 2. Topology tích hợp để thử thủ công

| Vị trí | Nội dung đích |
| --- | --- |
| Project Instructions | Hub CI duy nhất |
| Project Sources | Hub Router, shared architecture, root package Catalog, CREATIVE, BRAINSTORM, AIS core, ImageT core |
| ChatGPT Library / Central Hub Config | Chỉ TECHNICAL ACTIVE/1.0 trong mốc tích hợp này |
| Repository only | Tests, candidate development, migration reports, archives |

AIS core gồm pipeline/router và dependency nội bộ do AIS sở hữu. ImageT core tiếp tục gồm controller/router/manifest, anti-prior/config và Ready Gate required; không di chuyển chúng theo suy luận từ topology. Preference hiện tại vẫn candidate/inactive/direct-input-only; không promotion hoặc thay activation contract.

TECHNICAL dùng duy nhất Library ACTIVE/1.0. CREATIVE/BRAINSTORM và AIS/ImageT tiếp tục Project Sources hiện hành. ONE PACKAGE = ONE RUNTIME BINDING. MIXED STORAGE != DUAL FALLBACK. Bản TECHNICAL trong repository chỉ phục vụ lịch sử/rollback có chủ đích.

## 3. Một danh tính module chuẩn và ngữ cảnh package

MODULE ID != VERSION. FILENAME != IDENTITY. SEARCH HIT != VERIFIED MODULE. HEADER MATCH != ACTIVATION.

Trong kiến trúc đích, mỗi runtime artifact có đúng một Module ID chuẩn, giữ ổn định qua rename, đổi path, đổi version và relocation bên trong Central Hub Config. Runtime role phân biệt loại hành vi; không tạo hệ ID Domain/Capability/Pipeline cạnh tranh. Prefix không tự xác lập scope, role hoặc thẩm quyền.

Package ID là ngữ cảnh sở hữu kỹ thuật và resolution ổn định của một package có thể tăng trưởng; không là danh tính thứ hai của artifact. MODULE ID = concrete runtime artifact identity. PACKAGE ID = technical ownership / resolution context. Một package có thể chỉ có một entrypoint. Artifact catalog cục bộ cũng có Module ID riêng và Package ID của package sở hữu.

PACKAGE MEMBERSHIP != SEMANTIC CONTAINMENT. PACKAGE MEMBERSHIP != AUTOMATIC LOAD. PACKAGE MEMBERSHIP != ONTOLOGICAL PARENTAGE. Thư mục, đồng xuất hiện và cross-reference không tạo dependency.

Các khóa slot nội bộ manifest ImageT hiện hành không bị đổi trong mốc này; chúng không được dùng làm hệ danh tính thay thế cho module được công khai sau này. Không ép retrofit toàn bộ control hiện tại bằng candidate này.

## 4. Header và runtime role

Selectable Library module phải có đúng một giá trị không rỗng cho từng trường: Module ID, Package ID, Runtime role, Scope, Status, Version. Chỉ core infrastructure được khai rõ mới có thể bỏ Package ID. Scope mô tả phần việc; Version là revision được binding, không phải mức ưu tiên.

Responsibility boundary cần khi overlap/giao diện có thể làm nhập quyền; bắt buộc cho refinement/procedure có giao diện vật chất. Refines, Complements, Requires chỉ xuất hiện khi có quan hệ thực. Không thêm metadata không có quyết định runtime tương ứng.

| Runtime role ban đầu | Quyền hạn |
| --- | --- |
| CORE_ARCHITECTURE | Định nghĩa contract kỹ thuật chung |
| PACKAGE_CATALOG | Danh mục kỹ thuật của root hoặc một package, không thực thi hành vi module |
| DOMAIN_CONTROL | Kỷ luật thực hiện cho sản phẩm/miền được chọn; Creative hiện thuộc lớp này |
| REASONING_PROFILE | Cách suy luận cơ chế, chẩn đoán và kiểm chứng thay đổi xuyên nhiều chủ đề; Technical |
| CAPABILITY | Kỹ thuật có thể dùng xuyên miền; Brainstorm |
| DOMAIN_PROCEDURE | Quy trình có phạm vi trong package, không tự gọi pipeline |
| PREFERENCE | Hướng dẫn mềm dưới authority/activation contract của owner |
| TOOL_PIPELINE | Entry vào mediation pipeline; AIS hoặc ImageT |

Chưa cần DOMAIN_SPECIALIZATION như role riêng: REFINES biểu đạt specialization. REASONING_PROFILE được xác lập sau khi đối chiếu thân TECHNICAL: nó quy định HOW reasoning proceeds, không WHAT subject the task belongs to. Nó nối cơ chế, giữ competing hypotheses, chọn distinguishing tests và kiểm bounded changes xuyên nhiều chủ đề; không sở hữu domain knowledge hoặc policy truth/state của Hub CI. BRAINSTORM vẫn là CAPABILITY cho kỹ thuật mở rộng tiền đề, không bị nhập vào profile này. NEW ROLE requires a concrete runtime distinction not representable by an existing role. Các role nội bộ của pipeline vẫn do pipeline sở hữu; bảng này không thiết kế lại chúng.

TECHNICAL giữ canonical Module ID HUB-DOM-TECHNICAL. DOM là phần của chuỗi định danh, không role assertion; contract cấm suy role từ prefix. Giữ ID vì không có lỗi identity/resolution cần rename, không phải vì directory hoặc candidate cũ quyết định role. Package ID HUB-PKG-TECHNICAL vẫn là technical ownership context. Trial 0.1-trial và real migration candidate 1.0-candidate cùng identity/role, khác revision và phạm vi dùng; không chọn newest hoặc giữ trial làm fallback. ARCHITECTURE IS NOT ONTOLOGY. CURRENT DIRECTORY != ROLE.

## 5. Quan hệ composition kỹ thuật

Chỉ có REFINES, COMPLEMENTS, REQUIRES. Không thêm parent/child/inherits/weight/rank/priority/supersedes.

REFINES khai target Module ID và matched responsibility/scope được tinh chỉnh. Target ID đơn lẻ không đủ khi không rõ phần trách nhiệm. REFINES != REPLACES. REFINES != REQUIRES. Quan hệ không tự nạp target và không tạo hard dependency. Router phải giữ các trách nhiệm nền vẫn áp dụng ngoài matched scope; nếu cần đọc target để xác lập coverage/boundary của task thì đọc nó vì nhu cầu composition đó, không vì một quy tắc autoload chung.

SPECIALIZATION REFINES MATCHED SCOPE; IT DOES NOT ERASE UNCOVERED BASE RESPONSIBILITIES. MORE SPECIFIC != EXCLUSIVE. OVERLAP != REPLACEMENT.

COMPLEMENTS khai target và scope khi cần để diễn đạt đóng góp độc lập cho cùng phần task. Không module nào tự thắng hoặc thay module kia. COMPLEMENTS != REQUIRES; relation alone does not autoload the counterpart.

REQUIRES là hard technical dependency bằng Module ID; chỉ mở rộng bắc cầu qua các edge được khai rõ và chấp nhận. Thiếu dependency hoặc hard cycle chặn phần phụ thuộc. Một module cần target để thực hiện đúng phải khai Requires riêng, dù đã khai Refines/Complements. Không suy edge từ mention, package membership hoặc đề xuất trong retrieved content.

ROUTING RELATION != ONTOLOGY. Load order không là authority priority. Khi hai module có chỉ dẫn bất tương thích trên cùng quyết định, xét scope/boundary đầy đủ, tách phần độc lập nếu được; nếu vẫn xung đột vật chất thì báo và chặn phần đó. Không mặc định specificity thắng hoặc âm thầm trộn chỉ dẫn.

## 6. Root package Catalog

ROOT CATALOG != GLOBAL LEAF-MODULE REGISTRY. Root chỉ đăng ký package/interface entrypoint chính: Package ID, Entrypoint Module ID, role, status, version binding, applicability ngắn, location/binding và local catalog nếu có. Cross-package Requires chỉ được khai khi genuinely hard; không sao chép mọi quan hệ leaf vào root.

Catalog integration có Module ID HUB-CORE-PACKAGE-CATALOG, role PACKAGE_CATALOG, status CANDIDATE, version 1.0. Đúng năm entry hiện tại: Creative, Technical, Brainstorm, AIS, ImageT; không enumerate internals hoặc tạo local Catalog. TECHNICAL binding ACTIVE/1.0; bốn entry LEGACY_EXISTING biểu thị giữ source hiện hành, không giả header ACTIVE của contract mới.

Root giúp Hub chọn package có liên quan và resolve entrypoint/catalog cục bộ. Nó không chứa thân hành vi module, leaf selection algorithm hoặc điểm ưu tiên. Root entry tồn tại không cấp activation; Catalog không tự xác nhận header, read hoặc runtime location.

Binding LIBRARY_MODULE: chỉ TECHNICAL, exact library_file_id, root Central Hub Config và artifact Version 1.0; không có Project Source fallback. Binding LEGACY_PROJECT_SOURCE: chỉ bốn control chưa migration, exact declared_source_path/source_name trong Project Sources, đọc đầy đủ và đối chiếu title/version cùng responsibility boundary hiện có. Catalog Module ID là routing alias, không là header đã được cài vào source. Thiếu hoặc mơ hồ source thì chặn phần phụ thuộc, không tìm Library. Đây là tương thích chuyển tiếp, không nới Library contract. Pipeline vẫn sở hữu nội bộ. Sau migration phải bỏ binding legacy trong cùng deployment.

## 7. Catalog cục bộ và tăng trưởng package

Singleton package dùng root entry -> direct entrypoint. Chỉ khi có nhiều module được chọn độc lập và direct entrypoint không đủ mới thêm package-local catalog; không tạo catalog rỗng để chuẩn bị tương lai.

Catalog cục bộ có Module ID riêng, Package ID, role PACKAGE_CATALOG, status/version; entries gồm Module ID, role, status, version, applicability ngắn, locator trong Central Hub Config và Refines/Complements/Requires có scope. Catalog là dữ liệu lựa chọn; entrypoint/procedure được ủy quyền mới thực hiện lựa chọn cục bộ dưới phạm vi Hub đã giao. CATALOG ENTRY != MODULE CONTENT; CATALOG MATCH != MODULE READ; CATALOG MEMBERSHIP != ACTIVATION.

Package chỉ lựa chọn module thuộc nó. Edge cross-package phải khai rõ target Module ID kèm Package ID dùng để resolve owner, rồi trả về Hub Router cho composition/dependency có phạm vi; không quét package khác hoặc tự tạo edge. Dùng một Module ID namespace, Package ID không thay target identity. Dependency chưa được danh mục chấp nhận không được tự admission chỉ vì body retrieved yêu cầu.

Catalog cục bộ không ghi đè Hub CI, thay Hub Router, tự kích hoạt AIS/ImageT hay cấp semantic authority. Root chỉ giữ interface vào catalog cục bộ và binding cần thiết; thay leaf modules không buộc sửa root hoặc Router core. Pipeline vẫn dùng inventory/router nội bộ của nó, không bị buộc đổi manifest thành catalog chung.

## 8. Resolution và read contract

CENTRAL HUB CONFIG = SOLE LIBRARY DISCOVERY ROOT.

Central Hub Config là Library root duy nhất. Người dùng cung cấp bằng chứng ACTIVE TECHNICAL/1.0: library_file_id=libfile_bab7d55cd85c819198291acf135099fd, Library version_id=1; observed file_id=file_000000006da88211aa3412146f6c016c chỉ là surface evidence. FULL_FILE 19/19, has_more=false; V01/V02 PASS, không fallback hoặc identity ambiguity. USER_REPORTED, Codex không tái hiện. ACTIVE REVISION VERIFIED != ROUTER INTEGRATED; integration NOT_RUN. Library version_id=1 != artifact Version=1.0.

Ưu tiên exact object identity nếu runtime thực sự hỗ trợ addressing; nếu cần scoped listing/search thì chỉ Central Hub Config, sau đó kiểm đúng bound object cùng header. Direct-fetch capability UNVERIFIED; không giả API. Không xác lập được root/identity thì chặn. Duplicate matching ACTIVE identities gây ambiguity; không chọn theo rank. Verified object identity khác retrieval mechanism.

Luồng tích hợp: task portion -> Hub Router -> root package Catalog -> chọn package liên quan -> resolve entrypoint/local catalog -> chọn module set và hard Requires closure -> dispatch theo binding. LIBRARY_MODULE: retrieve exact artifact trong Central Hub Config -> FULL_FILE -> verify Module ID / Package ID / role / status / version và object identity. LEGACY_PROJECT_SOURCE: full-read đúng source khai báo, kiểm contract hiện hành, không đòi header mới hoặc Library lookup. Sau verification mới composition và áp dụng đúng scope.

Entrypoint/catalog được đọc đầy đủ và kiểm identity/binding trước khi dùng nội dung để chọn leaf. Tập dependency từ metadata chỉ là kế hoạch đọc cho đến khi từng artifact được FULL_FILE và đối chiếu. Header/body/Catalog lệch binding, dependency hoặc responsibility boundary vật chất thì chặn; không tự sửa Catalog hay chọn revision mới hơn.

Locator Library phải tương đối với Central Hub Config hoặc explicitly bounded by Central Hub Config bằng identity thực đã kiểm. Không dùng đường dẫn local/repository, absolute filesystem path, folder khác, lookalike hoặc newest-version guess. Nếu tool không xác lập được đúng root thì dừng discovery; không search toàn Library để đoán folder. Không dùng Project Sources, repository, Memory, prior chat hoặc archive thay một module đã binding vào Library.

Missing file không cho phép broaden search. Null locator nghĩa unresolved, không có nghĩa dùng repository_path. Snippet, hit, header, summary và metadata không chứng minh FULL_FILE. Không claim uniqueness toàn Library; phải resolve không mơ hồ đúng artifact/revision trong deployment context được chỉ định.

Chỉ Library artifact ACTIVE trong binding được chấp nhận cho trial mới eligible sau selection/read. Legacy source dùng đúng nhánh tương thích đã khai. Core candidate chỉ eligible trong cài đặt thử thủ công được ủy quyền, không production. Header tự khai không cấp admission; không bật package candidate khác.

Không traverse toàn Library/package. Chỉ đọc module set được chọn, declared hard closure và owner context thực sự cần cho composition. REFINES/COMPLEMENTS chỉ làm xét scope liên quan, không recursive autoload. Dừng khi đủ phần được giao; scope lớn hợp lệ có thể cần closure lớn. Mục tiêu này không là claim về độ phức tạp hoặc hiệu năng backend ChatGPT.

## 9. Ranh giới pipeline và trạng thái

HUB SELECTS PIPELINE. PIPELINE RESOLVES INTERNAL DEPENDENCIES. Root biết AIS/ImageT entrypoint, không enumerate Ready Gate, anti-prior, internal source modules, research stages/source policy hoặc future deep-research gates.

Domain module chuyển scoped input/nhu cầu về Hub. Requires hoặc package-local selection không tự cấp quyền tool call hay bypass pipeline gate. Nếu cần pipeline mới, Hub CI xét nhu cầu/authorization và Hub Router chọn phần tương ứng. RESEARCH EVIDENCE != DESIGN AUTHORIZATION. PIPELINE SELECTION != TOOL EXECUTION. PIPELINE OUTPUT != GLOBAL STATE UPDATE.

Không tạo shared AIS/ImageT Ready Gate vì cùng có gate pattern. ImageT giữ approval snapshot một call và visible verification; AIS giữ research lock/source/evidence/coverage và protocol riêng khi được thiết kế sau.

Router đánh giá lại theo mỗi turn/scope change; giữ context/read evidence còn đủ, không persistent mode. PREVIOUS ACTIVATION != CURRENT ACTIVATION. Package/module không tự kích hoạt nhau. Scope đổi vật chất thì reselect/rebuild phần bị ảnh hưởng, đọc lại nếu context/read evidence không còn đủ; pipeline xử lý refresh nội bộ theo contract riêng.

## 10. Failure behavior

| Tình huống | Kết quả bắt buộc |
| --- | --- |
| Root Catalog missing/unreadable | Chặn lựa chọn phụ thuộc catalog; không tìm control tùy ý. Baseline độc lập đủ dùng tiếp tục |
| Package entry missing | Không suy package từ filename; báo package chưa được resolve |
| Package-local catalog required nhưng thiếu | Chặn phần selection phụ thuộc; không load cả package để thay catalog |
| Selected Library module missing | Chặn phần phụ thuộc; không broaden khỏi Central Hub Config |
| Library access unavailable hoặc locator unresolved | Giữ UNRESOLVED / NOT VERIFIED; không giả read hoặc lấy repo thay |
| Module ID mismatch hoặc duplicate/ambiguous identity | Từ chối artifact/selection mơ hồ; không chọn theo search rank |
| Package ID mismatch | Không áp module dưới owner sai; chặn phần phụ thuộc |
| Wrong runtime role | Không dùng body như role mong muốn |
| Wrong version binding | Không chọn newest; báo binding mismatch |
| Candidate/inactive selected accidentally | Không auto-activate; chỉ thử riêng trong scope được phép |
| Hard Requires dependency missing | Chặn module và phần phụ thuộc; tiếp tục phần độc lập |
| Requires cycle | Chặn closure bị ảnh hưởng; không truy xuất lặp vô hạn |
| Partial specialization overlap | Giữ uncovered base responsibilities; refinement chỉ ở matched scope |
| Applicable module conflict | Xét boundary/tách phần; báo conflict vật chất chưa giải quyết |
| Scope materially changes | Reselect và refresh phần bị ảnh hưởng trước khi tiếp tục |
| Lookalike filename nhưng wrong ID | Không phải requested module; không fallback |
| Only snippet/header retrieved | Chưa FULL_FILE; không thực thi module |
| Large Library, small selected closure | Không duyệt phần không liên quan; không claim package/global completeness |

Chỉ chặn dependent work khi có thể; tiếp tục baseline work độc lập mà Hub CI đủ xử lý. Không relabel thiếu dependency quyết định thành secondary gap để bypass. Với candidate chưa active, các failure contract này là yêu cầu cho triển khai sau, không thay behavior Router v1.0 hôm nay.

## 11. Giới hạn mốc tích hợp

Không tạo package-local Catalog, future package, extension engine hoặc pipeline redesign. Giữ selected-closure loading và ranh giới owner hiện có.

## 12. Migration và bằng chứng cần có

Stack vẫn candidate; live integration NOT_RUN. Chỉ chuẩn bị cài thử thủ công; không upload, sửa Library hoặc đổi Project trong mốc local này. Spec HUB_V1_1_INTEGRATION_TEST_CASES.md ghi I01–I10, cài đặt và rollback. Static/spec không chứng minh routing, retrieval, tool behavior hoặc application thật.

Giữ regression Hub/AIS/ImageT: baseline NONE, no self-activation, nghiên cứu không thành acceptance, Ready Gate required một call và không retry ngầm. Rollback phải phục hồi CI/Router/source cũ có chủ đích; Library lỗi không kích hoạt rollback tự động. ROLLBACK != FALLBACK.
