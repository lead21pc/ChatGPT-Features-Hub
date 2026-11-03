# Pilot AFM-015: bản làm việc tại Central Hub

Trạng thái: `HISTORICAL / WORKFLOW-FEASIBILITY EVIDENCE`; `NON_AUTHORITATIVE_WORKING_COPY`.
Mục đích ban đầu: Central Hub brainstorm pilot, Phase 2.
Ngày chuẩn bị: 2026-10-25 (Asia/Bangkok).
Chỉ là artifact thử nghiệm cục bộ: không active, không runtime source, không fallback source, không canon authority. Không phải module/control Hub, không đăng ký trong Catalog và không sửa Library binding.

Pilot được giữ làm bằng chứng lịch sử về khả năng dùng material FTH có phạm vi để làm việc ngoài FTH, giữ kết quả không có authority và đưa về đối chiếu/review. `AFM-015 != ACTIVE BRIDGE ARCHITECTURE`; `AFM-015 PASS != FORMAL BRIDGE REQUIRED`. Các kết quả đã ghi không xác lập nhu cầu về transport layer hoặc gate FTH riêng trong Hub.

Workflow hiện tại do người dùng xác nhận: người dùng cung cấp context cần thiết cho Hub, Hub dùng capability hiện có theo task, rồi người dùng đưa working output về project để stack thật của project review. Việc chuyển context không chuyển authority; FTH giữ quyền nguồn, anti-drift, reconciliation và admission. Đây là cách người dùng đang làm việc, không phải protocol chuyển giao bắt buộc trong Hub core.

Mọi stack/version, binding, source/open-state snapshot và hướng dẫn chạy bên dưới là `BASELINE AT THE TIME OF THE PILOT`, không khai báo phiên bản active hoặc deployment hiện tại. Giữ cả bảy tệp tại chỗ để bảo toàn provenance, đầu vào, output và kết quả; các hướng dẫn/nhãn chuẩn bị cũ là hồ sơ thử nghiệm, không là yêu cầu tiếp tục bridge.

## Nguồn và provenance

- Repository: `lead21pc/chatgpt-ci-worldbuilding`.
- Source module: `AFM-015`.
- Source path từ repository root: `Project Feather Core/21_HOA_NGUYET_CULTURE_LANGUAGE_DRESS_CURRENT.md`.
- Source commit: `ad3823b4b2ae3e8756c5691b663eda2901b122f3`, branch `main`.
- Source Git blob: `9a4bfd58f7624851fa2cc5f3ecb3bc6e379e7ebc`.
- Source SHA-256: `8d14eb73c4587db297d46c9804f9d262dc605513a93d13ed3c2b6f0eb58d27d5`.
- Source size: `6022` byte.
- [AFM-015_FULL_FILE_SNAPSHOT.md](AFM-015_FULL_FILE_SNAPSHOT.md) giữ toàn bộ source nguyên byte, gồm header, qualifier, UNKNOWN và provenance; không phải bản tóm tắt.
- Header `Module ID: AFM-015`, `Runtime role: CURRENT_SOURCE` bên trong snapshot là trích nguyên header của nguồn tại commit trên. Chúng không cấp role, admission hoặc authority cho bản sao trong thư mục này. Không sửa snapshot để giả một module mới.
- Source current tiếp tục ở FTH. Snapshot chỉ ghi nhận baseline của thử nghiệm, không tự cập nhật theo FTH và không được dùng thay source current trong tác vụ FTH sau này. Nếu source thay đổi, đối chiếu độ lệch trước khi tái dùng; không âm thầm gọi bản chụp cũ là current.
- Quyền tạo: yêu cầu Phase 2 của tác giả trong lượt này. Chỉ chuẩn bị đầu vào và đặc tả; không nhập canon hoặc merge ngược FTH.

`CURRENT_SOURCE != WORKING COPY`
`WORKING COPY != CANDIDATE CANON`
`PROPOSAL != ADMISSION`
`FULL_FILE REMAINS THE BASELINE`
`NODE_OR_FULL IS OUT OF SCOPE`

## Baseline lịch sử khi chuẩn bị pilot

Repository root là `<WORKSHOPS_REPO>`; branch `main`, HEAD như trên. Working tree và staging sạch tại preflight; HEAD so với `origin/main` cục bộ là `0 / 0`. HEAD đã khác mốc Phase 1 `fabaab45029e6dad946889faccb4b174549a3479`; phép `git diff --name-only` giữa hai commit không ghi nhận thay đổi dưới FTH hoặc Central Hub. Truy vấn remote trực tiếp thất bại với `schannel: AcquireCredentialsHandle failed: SEC_E_NO_CREDENTIALS`; chưa xác nhận GitHub hiện tại.

Tại preflight pilot, FTH repository dùng CI 3.4, Source Router 5.0, Authoring Pipeline 1.1. Pipeline 1.0 còn là bản rollback; candidate không tự active. Nguồn AFM-015, open state và quyết định tách miền được đọc lại từ working tree tại thời điểm đó, không dùng Memory, prior-chat hoặc archive làm fallback.

Tại preflight 2026-10-25, Central Hub repository dùng CI 1.1, Router 1.1, Architecture 1.0 và root Catalog 1.0, với năm entry CREATIVE, TECHNICAL, BRAINSTORM, AIS, ImageT. Đây là baseline lịch sử, đã được thay bằng baseline tại lần reconciliation pilot dưới đây. Thư mục `Central Hub/candidates/` đã chứa các thử nghiệm Markdown theo nhóm; pilot dùng lại cách đặt này.

## Baseline Hub và snapshot tại lần reconciliation pilot

Preflight reconciliation: branch `main`, HEAD `866a38dfedbe60caba00afa0372412b05f9ff419`; `origin/main` và remote main được quan sát cùng SHA. Tại lần kiểm đó, snapshot vẫn bằng source AFM-015 trong working tree từng byte: `6022` byte, SHA-256 `8d14eb73c4587db297d46c9804f9d262dc605513a93d13ed3c2b6f0eb58d27d5`. `SNAPSHOT BASELINE STILL CURRENT FOR THIS PILOT`; snapshot không được tạo lại.

Tại baseline reconciliation pilot, Hub dùng CI 1.1, Router 1.1, Architecture 1.1 và root Catalog 1.1. Root có TECHNICAL, `HUB-PKG-CONCEPT-DEVELOPMENT`, AIS và ImageT. Concept Development sở hữu entrypoint `HUB-DOM-CONCEPT-DEVELOPMENT` 1.0 / `DOMAIN_CONTROL` và package-local catalog `HUB-CATALOG-CONCEPT-DEVELOPMENT` 1.0 / `PACKAGE_CATALOG`; `HUB-CAP-BRAINSTORM` 1.1 / `CAPABILITY` và `HUB-DOM-CREATIVE` 1.1 / `DOMAIN_CONTROL` là hai leaf được chọn độc lập, không phải root package riêng.

Bốn object concept được ChatGPT quan sát/người dùng cung cấp evidence trong `Central Hub Config`: root-scoped listing không thấy duplicate cho bốn identity trong phạm vi kiểm, FULL_FILE identity/content và Library/repository bytes khớp; Catalog ghi binding `RESOLVED`. `locator` và `library_version_id` vẫn `null`; surface ID chỉ là evidence/debug. Không suy direct fetch hay complete Hub runtime retrieval trace từ evidence này.

Một integrated Central Hub runtime smoke ngày 2026-10-27 đã được người dùng xác nhận PASS cho một đường thực thi có AIS, TECHNICAL, Concept Development, BRAINSTORM và CREATIVE, theo đúng revision và giới hạn trong `Central Hub/RUNTIME_EVIDENCE_CHANGELOG.md`. Đây không phải global Hub PASS, không xác minh từng retrieval trace và không chứng minh hành vi pilot AFM-015. Toàn bộ C01–C12 live chưa chạy và không là prerequisite của pilot này trừ khi chính test AFM-015 cho thấy dependency cụ thể.

## Trạng thái nguồn tại baseline pilot phải bảo vệ

Các dòng dưới là nhắc phạm vi từ snapshot, không thay thế FULL_FILE hoặc có authority độc lập:

- Một quốc gia thống nhất, ba vùng văn hóa Hoa/Nhật/Việt; nhãn vùng chưa là tên riêng chính thức.
- Mỗi vùng giữ ngôn ngữ, truyền thống và căn tính riêng; giao lưu không bắt buộc đồng hóa.
- Trang phục đa thời kỳ: hệ Hanfu; Kimono/Yukata và phục sức lịch đại; áo dài và cổ phục Việt. Không thu mỗi vùng thành một bộ duy nhất.
- Không cấm mặc trang phục vùng khác chỉ vì nguồn gốc; không tự cấp quyền với mọi phục sức chức vụ, phẩm cấp, nghi lễ và không đổi căn tính người mặc.
- Ngôn ngữ/hệ chữ hiện đại: tiếng Trung/chữ Hán hiện đại; tiếng Nhật/Kanji-Hiragana-Katakana; tiếng Việt/Quốc ngữ. Di sản Hán/Nôm không bị phủ định; chữ cổ không tự thành chuẩn hành chính bắt buộc.
- Tiếng Trung hiện đại là chuẩn văn bản hành chính chung cấp quốc gia/liên vùng; quan chức cần năng lực tương ứng công việc. Không suy mọi văn kiện địa phương dùng tiếng Trung hoặc mọi dân phải thông thạo.

Tên cảm hứng không nhập lịch sử thật hoặc cơ chế truyền văn hóa xuyên thế giới. Trang phục truyền thống không điều khiển Undi; thêm vùng Việt không tự đổi Undi. Chuẩn ngôn ngữ không tự quyết định luật dùng quốc hiệu. Bảo tồn cổ văn tự nguyện chưa là chính sách hay nguyên tắc thứ tám.

## UNKNOWN/open state mang theo

Đoạn đính kèm nguyên nội dung từ `Project Feather Core/92_OPEN_ISSUES_CURRENT.md` tại baseline pilot, mục “Hoa Nguyệt — bảy nguyên tắc nền, các mục mở 2026-10-10”. Đây là bản chụp state/định tuyến, không là quyền giải quyết các mục mở. Dùng nó cùng UNKNOWN tại snapshot; không dùng danh sách này làm bằng chứng rằng không còn UNKNOWN khác.

<!-- BEGIN OPEN STATE SNAPSHOT -->
## Hoa Nguyệt — bảy nguyên tắc nền, các mục mở 2026-10-10

`20` §5.2 / `AFM-012` giữ nguồn gốc ba quốc gia tiền thân; `21_HOA_NGUYET_CULTURE_LANGUAGE_DRESS_CURRENT.md` §5 / `AFM-015` giữ ba vùng văn hóa Hoa/Nhật/Việt, căn tính riêng, trang phục đa thời kỳ/quyền mặc xuyên vùng theo nguồn gốc, hệ chữ hiện đại theo vùng và tiếng Trung hiện đại cho văn bản hành chính chung. AF-HN-OPEN-006 thuộc hồ sơ nguồn gốc `20` và giao diện vùng `21`; AF-HN-OPEN-007–009 thuộc `21`. Các nhãn Hoa/Nhật/Việt chưa là tên vùng chính thức. Không suy quyền hành chính từng vùng hoặc cơ chế truyền văn hóa xuyên thế giới.

| ID | Trạng thái | Phạm vi còn mở |
| --- | --- | --- |
| AF-HN-OPEN-006 | UNKNOWN / OPEN | Tên riêng ba vùng/ba quốc gia tiền thân, thời điểm/nguyên nhân/phương thức hợp nhất, địa vị chính trị sau hợp nhất, cơ cấu hành chính; quan hệ thời gian/nhân quả với dark foundation, Lục Kì Nhân và quốc hiệu kép chưa xác lập. |
| AF-HN-OPEN-007 | UNKNOWN / OPEN | Danh mục/niên đại/hoàn cảnh dùng/quy chế trang phục theo vùng qua các thời kỳ; ngoại lệ phục sức chức vụ, phẩm cấp, nghi lễ. Không cấm theo nguồn gốc không tự thành quyền mặc mọi phục sức. |
| AF-HN-OPEN-008 | UNKNOWN / OPEN | Dạng Hán tự phồn thể/giản thể, phạm vi chính xác của chuẩn văn bản cấp quốc gia/liên vùng, quy tắc văn kiện địa phương, quy trình dịch và năng lực tương ứng từng công việc quan chức. Không suy nghĩa vụ thông thạo cho toàn dân. |
| AF-HN-OPEN-009 | UNKNOWN / OPEN | Giáo dục ngôn ngữ và quy định triển khai/bảo tồn di sản chữ viết. Hướng học/bảo tồn cổ văn và văn học truyền thống tự nguyện trong ghi chú nguồn chưa được nhập thành chính sách hoặc nguyên tắc thứ tám. |
<!-- END OPEN STATE SNAPSHOT -->

Chỉ tên vùng/giao diện văn hóa của -006 liên quan trực tiếp AFM-015; nguồn gốc, hợp nhất, địa vị chính trị/cơ cấu hành chính không được nhập vào authority của AFM-015. Các phần này được mang theo như trạng thái chưa xác lập để tránh suy diễn. Không mang câu trả lời của owner khác vào local truth.

## Ranh giới owner

Đường dẫn dưới đây tương đối với repository root, chỉ là pointer phục vụ chuẩn bị/đối chiếu, không là locator Library hoặc hard dependency. Bảng này không sao chép controlling lore ngoài miền.

| Owner | Khi câu hỏi vượt AFM-015 | Pointer current |
| --- | --- | --- |
| AFM-012 | Hồ sơ nền, nguồn gốc/hợp nhất; cơ cấu hành chính và địa vị chính trị đang mở tại AF-HN-OPEN-006 | `Project Feather Core/20_HOA_NGUYET_NATIONAL_CANON_CURRENT.md` |
| AFM-016 | Quốc hiệu, biểu tượng, luật dùng tên trong văn kiện | `Project Feather Core/22_HOA_NGUYET_STATE_IDENTITY_SYMBOLS_CURRENT.md` |
| AFM-003 | Undie/Undi và thiết kế trang phục nghề | `Project Feather Core/13_UNDIE_SYSTEM_CURRENT.md` |
| AFM-013 | Ý định phía AetherFire, gồm ý định chiếm dụng quốc phục | `Project Feather Core/10_AETHERFIRE_NATIONAL_CANON_CURRENT.md` |
| AFM-017 | Địa lý, giao thương, đối ngoại phía Hoa Nguyệt | `Project Feather Core/23_HOA_NGUYET_GEOGRAPHY_TRADE_RELATIONS_CURRENT.md` |
| AFM-001 | Giao diện thế giới/xuyên miền khi thực sự quyết định câu hỏi | `Project Feather Core/01_WORLD_INSTITUTIONS_GEOPOLITICS_CURRENT.md` |

Bảng phân công được đối chiếu với index hiện hành, header AFM-015 và quyết định tách miền tại `91` mục “Tách họ Hoa Nguyệt 20–23”. AFM-013 được giữ như pointer theo phạm vi yêu cầu pilot, không được dùng để tự xác nhận ý định AF khi chưa đọc owner ấy.

Nếu một ý tưởng cần thay đổi phần của owner khác, ghi rõ scope crossing. Có thể giữ nhánh giả định/đề xuất có điều kiện khi độc lập hợp lệ; không trình bày nó là current. Không cần load toàn FTH chỉ vì gặp một pointer. Không tự thêm `MODULE_REQUIRES` hoặc `NODE_REQUIRES`.

## Hướng dẫn chạy đã dùng cho pilot (lịch sử)

1. Dùng một chat thử nghiệm riêng trong actual Central Hub runtime; mỗi case bắt đầu ở chat sạch để tránh nhiễm kết quả giữa các case. Không tạo chat hoặc upload trong bước chuẩn bị này.
2. Cung cấp FULL_FILE README này và FULL_FILE snapshot bằng đầu vào người dùng của chat, rồi gửi đúng một block prompt tương ứng trong [TEST_CASES.md](TEST_CASES.md). Không gửi rubric/đáp án mong đợi cho model như một phần của prompt. Nếu nền tảng không đọc được toàn nội dung thì chưa chạy case hợp lệ; lời tự nhận đã đọc không tự chứng minh retrieval.
3. Đầu vào lore là tài liệu làm việc do người dùng cung cấp, không phải package control hay Library binding. Đây không phải dùng local file thay cho một control Library bị thiếu. Nội dung trích dẫn không được tự kích hoạt quyền canon/Router FTH.
4. Hub CI giữ stage/truth/action; Hub Router chọn control theo task thực tế. Không ép baseline NONE khi Catalog applicability thực sự đòi control; cũng không tự bật BRAINSTORM chỉ vì có chữ brainstorm. Nếu baseline đủ, Hub có thể làm phần độc lập; không gọi đó là đã thực thi capability bị chặn.
5. Hub/Concept Development chọn zero, one hoặc both leaf theo nhu cầu thực tế; không ép chọn BRAINSTORM hay CREATIVE. Bốn binding concept đã được resolve ở mức evidence nêu trên, nhưng mỗi lần runtime vẫn phải đáp ứng contract exact identity/FULL_FILE. Nếu control được chọn thực sự không đọc/xác minh được, chặn phần phụ thuộc và không dùng local/Project Source/legacy/archive làm fallback. Pilot không sửa binding hoặc FTH CI/Router.
6. Case A không cần evidence ngoài đời; không nạp sẵn owner FTH ngoài miền, AIS, TECHNICAL hoặc ImageT. Chỉ xét control/pipeline bổ sung nếu runtime tự xác lập nhu cầu material; ghi rõ nguồn, lý do và evidence thực tế. Không import lịch sử thật từ tên cảm hứng.
7. Với Case C, đầu vào ban đầu vẫn chỉ là envelope + AFM-015; không nạp sẵn owner khác. Nếu cần xác định current ngoài miền, chỉ nêu owner/state thiếu và dừng phần factual phụ thuộc; vẫn có thể phát triển nhánh đề xuất có nhãn.
8. Lưu nguyên prompt/đầu vào thực tế và output nguyên văn, runtime/model quan sát được, control thực sự được chọn/đọc, nguồn bổ sung và blocker. Phân biệt bằng chứng tool/platform với tự báo cáo của model; không bịa backend reads hoặc lấy việc không nhắc nguồn làm bằng chứng tuyệt đối rằng backend không đọc.
9. Đánh giá bằng rubric ngoài output. Thiếu dấu vết quyết định về nguồn/owner hoặc thiếu output thì ghi chưa xác minh, không tự PASS. Blocker nạp control không tự chứng minh module lore thiếu closure.

Nếu source hoặc Hub stack đã đổi trước lần chạy, ghi baseline thực tế và phần lệch; không giả baseline cũ vẫn current. Không tự cập nhật control hoặc snapshot trong lúc chấm để làm case đạt.

## Tiêu chí kết quả brainstorm của pilot (lịch sử)

Khi material, kết quả cần phân biệt bằng prose thông thường:

- Baseline current được giữ, theo mục snapshot liên quan.
- Assumptions dùng riêng cho từng nhánh; không làm điều kiện thật của thế giới.
- Proposed additions/changes và khác biệt thực chất giữa các hướng.
- Owner-boundary crossings: phần nào vượt miền và owner/state còn thiếu.
- Câu hỏi còn mở; UNKNOWN nền vẫn mở dù nhánh có giả định.
- Chứng cứ ngoài nếu có AIS trong một lần chạy được cho phép riêng, giữ nguyên mức hỗ trợ và giới hạn; ba case chuẩn không cần AIS.
- Mục nào sẽ cần đối chiếu/reconciliation/admission FTH về sau. Không thực hiện thủ tục admission ở đây.

CURRENT/UNKNOWN/ASSUMPTION/PROPOSAL là nhãn dùng khi cần rõ trạng thái, không là schema hoặc primitive mới. Không cần đủ mọi trường khi không material. Không chọn nhánh cuối hoặc gọi canonization thay tác giả.

## Kết quả đã ghi nhận

- Đặc tả: xem TEST_CASES.md; expected behavior là tiêu chí, không phải quan sát model.
- `PHASE_2_BEHAVIORAL_PASS`: người dùng xác nhận cả A/B/C PASS sau ba actual clean-chat Central Hub run; `USER-CONFIRMED_PHASE_2_BEHAVIORAL_PASS`, Codex không tái hiện độc lập. [Output nguyên văn](PHASE_2_RUNTIME_OUTPUTS.md) là evidence, không là runtime control hoặc FTH source.
- `PHASE_3_SEMANTIC_RECONCILIATION_PASS`: [đối chiếu semantic](PHASE_3_SEMANTIC_RECONCILIATION.md) đã chuẩn bị được theo baseline và owner/state. PASS chỉ xác nhận khả năng đưa material vào workspace kiểm tra, không phải admission hay chấp nhận canon.
- `PHASE_4_FTH_ROUND_TRIP_DRY_RUN_PASS` / `NO_ADMISSION_PERFORMED`: [patch đề xuất không có authority](PHASE_4_AFM015_PROPOSED.patch) đã được kiểm tra khả năng áp dụng và ranh giới theo [báo cáo dry run](PHASE_4_ADMISSION_DRY_RUN.md); P1/P2 chưa được chấp nhận, C-A được route sang AFM-012 nếu tiếp tục.
- Integrated runtime smoke có `USER_CONFIRMED_LIVE_PASS` đúng scope ở trên. Codex không tái hiện độc lập các behavioral PASS đã được người dùng xác nhận; complete internal retrieval traces không được xác minh độc lập. Giới hạn này không hạ trạng thái A/B/C PASS đã ghi. Không coi full C01–C12 live là prerequisite của Case A.
- A/B/C là kết quả đã được tác giả xác nhận, không suy toàn bộ C01–C12, global Hub hay các module FTH khác đã PASS. Các UNKNOWN và owner crossings tiếp tục được giữ trong hồ sơ Phase 3.
- Không đổi current FTH/Hub, không stage/commit/push/deploy và không thực hiện admission trong đợt reconciliation này.

## Kiểm chứng cục bộ đã thực hiện

Kết quả ngày 2026-10-25; đây là chứng cứ repository/static, không phải output của Hub.

- `LOCAL_ARTIFACT_PASS`: kiểm tra trực tiếp 21 điều kiện về byte/hash, provenance, bản chụp open state, ba prompt/rubric, UTF-8/whitespace, không admission vào Catalog và phạm vi Git.
- AFM-015 source và snapshot bằng nhau nguyên `6022` byte, SHA-256 `8d14eb73c4587db297d46c9804f9d262dc605513a93d13ed3c2b6f0eb58d27d5`.
- 46 file baseline được băm trước khi tạo artifact và so sánh lại: root Markdown FTH, direct-child controls FTH, root files Hub và Library-module artifacts local đều không đổi. Không đọc archive làm current fallback.
- Đoạn AF-HN-OPEN-006–009 trong envelope khớp nguyên nội dung section hiện hành của `92`; UNKNOWN và qualifier trong source giữ bằng snapshot nguyên byte.
- `STATIC_SPEC_PASS`: đã đọc lại cả ba file từ disk; đối chiếu scope A nội miền, B sát UNKNOWN và C vượt owner; mỗi case có prompt, expected behavior và PASS/FAIL riêng. Case B cho phép giả định cục bộ có nhãn, chỉ coi việc trình bày nó như current fact là lỗi. Đây là review nội dung đặc tả, không phải thực thi semantic test trên model.
- Từ thư mục FTH: `python -B -X utf8 build_consolidation.py --check` → PASS: 17 current modules, 21 current hashes, archive not accessed, read-only.
- Từ thư mục Central Hub: `python -B -X utf8 -m unittest discover -s tests -p test_hub_contracts.py -q` → 32 tests, OK. Bộ test hiện có kiểm contract/static và có đối chiếu lịch sử riêng; không dùng archive làm runtime fallback. Không chạy toàn suite hoặc thêm framework.
- Git: branch/HEAD không đổi; tracked diff và staged diff rỗng; chỉ có ba file untracked trong thư mục pilot này. Không stage/commit/push/deploy hoặc sửa binding.
- Tại thời điểm kiểm tra 2026-10-25: `BEHAVIORAL_NOT_RUN` và `LIVE_NOT_VERIFIED`; chưa có output A/B/C hay evidence runtime cho pilot. Kết quả integrated smoke sau đó được ghi riêng ở baseline hiện hành và không chứng minh hành vi giữ boundary của pilot.
