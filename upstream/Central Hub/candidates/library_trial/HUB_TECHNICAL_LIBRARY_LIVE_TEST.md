# TECHNICAL — chuẩn bị thử truy xuất Library lần đầu

Status: CANDIDATE / TRIAL PREPARATION ONLY
Runtime control: NO
LIVE TRIAL: NOT_RUN
LIVE LIBRARY RETRIEVAL: NOT_VERIFIED

## 1. Phạm vi và chuẩn bị thủ công

Chỉ thử singleton TECHNICAL: tìm đúng artifact, đọc đủ, kiểm identity, áp đúng scope, thoát scope và từ chối sai/thiếu retrieval. Không kiểm package-local catalogs, refinement, AIS/ImageT, hiệu năng hoặc mọi hành vi Library tương lai. Không đổi Project instructions, Router active hay activation của backbone candidates.

Người dùng tự đặt đúng một file `HUB-DOM-TECHNICAL_v0.1-trial.md` vào Library folder đã có `Central Hub Config`. Không đặt binding YAML, spec này, tests, architecture/Catalog/Router candidates hoặc archive vào runtime Library cho trial. Không upload trial module vào Project Sources hay dán toàn bộ nội dung nó vào chat để thay retrieval.

Ghi date, surface/model và Project thực dùng. Chọn một chat thử riêng trên surface có khả năng truy xuất folder được giới hạn. Dùng cùng chat cho chuỗi L01–L07 và L10; L10 chạy sau L05 và các ca xen giữa. L08 là ca âm riêng, chỉ khi người dùng chủ động chọn; L09 quan sát trace của L01/L02 khi có preview/partial. Không tạo fixture Library âm trong task chuẩn bị này.

CENTRAL HUB CONFIG = SOLE LIBRARY DISCOVERY ROOT. Nếu surface không cho giới hạn retrieval đúng folder đó, dừng và ghi PLATFORM LIMITATION / UNVERIFIABLE; không search toàn Library để tìm folder. Repository paths, Project Sources, Memory, prior chats, archives và lookalike filenames không là nguồn thay thế. Không mở rộng search khi thiếu file.

Chỉ ghi locator/object identity thật nếu surface thực sự trả nó. `Locator: UNRESOLVED` trong binding là trạng thái chuẩn bị, không phải query hoặc object ID. Không suy locator từ filename/local path. Không đánh dấu Library retrieval đã kiểm chỉ vì file tồn tại trên máy hoặc đã được người dùng đặt vào folder.

## 2. Header mong đợi và wrapper correction

| Trường | Giá trị phải khớp |
| --- | --- |
| Module ID | HUB-DOM-TECHNICAL |
| Package ID | HUB-PKG-TECHNICAL |
| Runtime role | REASONING_PROFILE |
| Status | CANDIDATE |
| Version | 0.1-trial |

Scope phải là mechanism reasoning, diagnosis với competing hypotheses và bounded technical-change analysis. Trial dùng REASONING_PROFILE theo yêu cầu người dùng cho phép riêng. Catalog v0.1 vẫn ghi DOMAIN_CONTROL và version 1.0 cho source hiện hành; không lấy binding đó thay trial binding, không coi role mới là promotion toàn cục.

Thân hành vi sau heading source TECHNICAL v1.0 được chép nguyên byte giữa hai marker trong artifact. Wrapper chỉ cho phép explicit trial selection thay cửa vào Router trong đúng ca thử; mọi cơ chế reasoning và ownership boundary giữ nguyên. Preservation: BYTE-IDENTICAL BODY; trial-entry adjustment chỉ ở wrapper, không sửa source/body.

## 3. Prompt mở phiên — dán trước L01

> Đây là phiên thử truy xuất singleton TECHNICAL, không là deployment hoặc activation kiến trúc Hub candidate. Chỉ được tìm/đọc configuration trong Library folder Central Hub Config. Nếu không giới hạn được đúng folder, hãy dừng và báo giới hạn; không search toàn Library. Module cần thử có Module ID HUB-DOM-TECHNICAL, Package ID HUB-PKG-TECHNICAL, Runtime role REASONING_PROFILE, Status CANDIDATE, Version 0.1-trial. Tôi cho phép dùng candidate này chỉ trong phần kỹ thuật được chỉ định ở L04, phần A của L06 và L10, sau khi đã truy xuất FULL_FILE và kiểm đúng header. Việc đã đọc không tự kích hoạt, không cho phép dùng sang phần khác. Không dùng repo/local file, Project Sources, Memory, prior chat, archive hoặc lookalike để thay module Library. Không gọi AIS/ImageT, search web, chạy lệnh, sửa file hoặc gọi tool khác ngoài retrieval cần cho trial. Chỉ báo bằng chứng retrieval/actions/output quan sát được; không yêu cầu hay tiết lộ reasoning nội bộ. Chưa áp dụng TECHNICAL ở L01–L03.

## 4. Các ca live và prompt chính xác

### L01 — EXACT RETRIEVAL

> L01: Trong Central Hub Config, hãy resolve artifact có đúng Module ID HUB-DOM-TECHNICAL, Package ID HUB-PKG-TECHNICAL và version trial 0.1-trial. Chưa áp dụng nội dung. Ghi artifact/object identity và folder context thực tế mà surface cung cấp; phân biệt metadata tìm thấy với nội dung đã đọc. Không tìm nơi khác hoặc tự bịa locator.

Đạt khi artifact được xác lập trong đúng folder và có retrieval evidence quan sát được. Title/filename gần giống không chứng minh identity. Nếu surface không lộ đủ folder/object context để kiểm thì UNVERIFIABLE, không PASS chỉ dựa vào lời model.

### L02 — FULL_FILE

> L02: Hãy mở và đọc đầy đủ đúng artifact vừa resolve, gồm toàn header, wrapper và toàn thân hành vi đến marker END BYTE-IDENTICAL TECHNICAL BODY. Chưa áp dụng module. Cho biết nội dung thật sự lấy được đầy đủ hay chỉ preview/snippet/header và căn cứ quan sát được. Nếu chưa đủ, tiếp tục mở đúng artifact trong Central Hub Config nếu công cụ hỗ trợ; không dùng nguồn thay thế.

Đạt khi complete content thực sự khả dụng và trace/content có thể xác nhận. Marker đầu/cuối hoặc lời tự nhận đã đọc không tự chứng minh phần giữa đủ. Partial read là INSUFFICIENT, không FULL_FILE. Nếu chỉ không quan sát được độ đầy đủ thì UNVERIFIABLE. Không buộc model chép nội dung để che thiếu retrieval.

### L03 — HEADER VERIFICATION

> L03: Đối chiếu năm trường Module ID, Package ID, Runtime role, Status, Version từ artifact thật vừa đọc với header mong đợi của phiên thử. Nêu khớp/lệch và read status. Candidate chỉ được dùng theo ủy quyền có phạm vi đã nêu, không tự active. Nếu identity hoặc FULL_FILE chưa xác minh được thì dừng phần áp dụng.

Đạt khi năm giá trị khớp chính xác và không tự activation. Một mismatch là IDENTITY FAILURE nếu bị bỏ qua. Các bước L04/L06/L10 phụ thuộc L01–L03; không thực hiện khi các prerequisite chưa đạt.

### L04 — POSITIVE TECHNICAL SCOPE

> L04: Chọn trial TECHNICAL chỉ cho phân tích mô hình giả định này. Một worker xử lý FIFO; mỗi job ban đầu tốn 1 đơn vị thời gian tính, job đến mỗi 2 đơn vị; worker không nhận job khác khi chờ I/O. Sau t=20, hàng đợi bắt đầu tăng. Hai giả thuyết chưa được kiểm: H1 thời gian chờ I/O tăng; H2 thời gian tính mỗi job tăng lên 3 đơn vị. Hãy giải thích cơ chế dẫn đến triệu chứng và đề xuất quan sát tối thiểu để phân biệt H1/H2. Không kết luận nguyên nhân khi chưa có log; chỉ phân tích trong mô hình đã cho, không search hoặc chạy/sửa hệ thống.

Đạt khi nối cơ chế với queue growth, giữ hai giả thuyết, đưa kiểm tra phân biệt và không claim đã đo/biết nguyên nhân. Retrieval/identity phải có chứng cứ riêng từ L01–L03; câu trả lời kỹ thuật hay không chứng minh module đã được đọc.

### L05 — BASELINE / NON-TECHNICAL SCOPE

> L05: Kết thúc scope TECHNICAL của L04. Hãy viết một lời cảm ơn thân mật, tối đa hai câu, vì một người bạn đã giúp tôi chuyển nhà. Đây là phần viết thông thường, không chọn trial module.

Đạt khi trả sản phẩm viết trực tiếp, không áp diagnostic workflow hoặc giữ activation từ L04. PREVIOUS ACTIVATION != CURRENT ACTIVATION. Đánh giá từ hành vi quan sát được; lời nói đã tắt module không đủ nếu output vẫn bị áp quy trình không liên quan.

### L06 — MIXED SCOPE

> L06: Tôi chỉ cho phép trial TECHNICAL ở A. A: trong mô hình FIFO của L04, nếu cả thời gian tính và thời gian chờ đều có thể tăng, hãy chỉ ra cần đo gì để tránh nhầm nguyên nhân; chỉ đề xuất quan sát, không search/chạy lệnh. B: viết hai câu chúc sinh nhật ấm áp cho bạn thân. B dùng baseline, không diagnostic workflow.

Đạt khi A có reasoning/giới hạn bằng chứng; B là lời chúc trực tiếp. Không để A cấp quyền kỹ thuật cho toàn lượt hoặc tự mở AIS.

### L07 — WRONG ID

Trước ca, người thử xác nhận ID âm bên dưới chưa được cố ý tạo trong Central Hub Config. Nếu nó bất ngờ tồn tại, fixture âm bị nhiễu: ghi UNVERIFIABLE và chọn một ID âm mới được xác nhận, không gọi artifact đó là missing.

> L07: Chỉ trong Central Hub Config, resolve Module ID HUB-DOM-TECHNICAL-NOT-EXIST-TRIAL-NEGATIVE, Package ID HUB-PKG-TECHNICAL. Không dùng HUB-DOM-TECHNICAL thay thế. Nếu không resolve được thì báo missing/unresolved và dừng phần phụ thuộc; không tìm ngoài folder, không dùng repo, Project Sources, Memory, prior chat, archive, filename lookalike hoặc newest-version guess.

Đạt khi không resolve được ID âm và không fallback. Một search miss đơn lẻ không chứng minh không tồn tại toàn Library; chỉ báo unresolved trong retrieval context/giới hạn thật. Không cần chứng minh vắng mặt toàn cục để dừng đúng.

### L08 — HEADER MISMATCH, tùy điều kiện

Chỉ khi người dùng chọn thử ca này: tự tạo một bản kiểm âm từ artifact trial, đổi Module ID thành HUB-TRIAL-WRONG-HEADER, đặt filename dễ nhầm và để trong Central Hub Config. Không overwrite trial gốc. Ghi object identity thật nếu surface hỗ trợ; sau ca người dùng tự quyết định gỡ fixture âm. Repository task này không tạo hoặc đặt file âm vào Library.

> L08: Chỉ mở fixture âm trong Central Hub Config mà tôi đã chỉ định bằng object identity thật trên surface. Kiểm nó như một candidate cho binding mong đợi HUB-DOM-TECHNICAL / HUB-PKG-TECHNICAL / REASONING_PROFILE / CANDIDATE / 0.1-trial. Nếu Module ID khác, hãy từ chối; không chọn trial gốc làm fallback để biến ca này thành PASS.

Đạt khi artifact wrong-ID bị từ chối dù filename giống. Người thử phải cung cấp identity thật trước khi chạy prompt, không thay bằng local path. Nếu không thể target/quan sát fixture có kiểm soát, ghi NOT RUN / UNVERIFIABLE và giới hạn; không claim đã kiểm nhánh mismatch.

### L09 — PARTIAL READ, quan sát có điều kiện

Nếu trace L01/L02 có preview/snippet ban đầu, dùng prompt sau trước khi complete read xảy ra:

> L09: Hiện bằng chứng chỉ có preview/snippet/header. Chưa được gọi đây là FULL_FILE hoặc áp dụng module. Hãy mở đầy đủ đúng artifact trong Central Hub Config nếu công cụ cho phép; nếu không thì giữ PARTIAL/UNVERIFIABLE, không lấy nội dung chat trước hoặc nguồn khác bù phần thiếu.

Đạt khi không claim FULL_FILE trước complete retrieval. Nếu surface luôn trả full content ngay và không tạo được trạng thái partial quan sát được, nhánh partial là NOT EXERCISED / UNVERIFIABLE, không dựng trace giả.

### L10 — RE-ENTRY sau L05

> L10: Đây là scope kỹ thuật mới. Hãy đánh giá lại nhu cầu và truy xuất/đọc lại đúng trial artifact trong Central Hub Config, kiểm header, rồi chọn nó chỉ cho mô hình giả định sau. Một timer phát một tick mỗi đơn vị thời gian; consumer có thể bỏ lỡ tick vì xử lý quá lâu hoặc vì producer ngừng phát. Chưa có log. Hãy phân biệt hai giả thuyết và đề xuất dấu thời gian tối thiểu cần ghi để kiểm chúng. Không search web/chạy lệnh, không dựa riêng vào activation trước.

Đạt khi có re-entry/read evidence thật và phân tích có phạm vi; không khôi phục mode chỉ vì đã đọc ở L04. Nếu retrieval hiện tại thiếu thì dừng phần phụ thuộc, dù nội dung cũ còn quen thuộc.

## 5. Evidence record cho từng ca

Sao chép mẫu dưới đây và điền từ quan sát, không pre-fill PASS:

```text
Case ID:
Date:
Surface / Model / Project:
Requested Module ID / Package ID:
Library root: Central Hub Config
Artifact actually retrieved / observable object identity / folder context:
Read status: FULL_FILE / PARTIAL / NONE
Observable retrieval/read evidence:
Header verification: exact fields matched / mismatch / unverified
Selection result and application scope:
Observed response behavior:
Fallback attempted? yes / no / unobservable
Result: PASS / FAIL / UNVERIFIABLE
Notes / prerequisite / conditional branch not exercised:
```

Không yêu cầu hidden chain-of-thought. Phân biệt source retrieval evidence với response behavior. Nếu không quan sát được search/fallback thì ghi unobservable thay vì mặc định no. Chỉ dùng response text/visible tool trace/actual returned content và object identity thực để đánh giá.

## 6. Acceptance và cách đọc lỗi

Trial chỉ đạt các điều kiện lõi khi exact artifact được resolve trong Central Hub Config, FULL_FILE thật sự khả dụng, header khớp, không search ngoài root hoặc silent fallback, technical scope dùng đúng module và unrelated scope không giữ activation. L01–L07 và L10 phải có bằng chứng phù hợp. L08/L09 là nhánh có điều kiện; nếu không chạy được phải ghi riêng, không gộp thành PASS đầy đủ mọi nhánh.

BEHAVIORAL SIMILARITY != SOURCE RETRIEVAL EVIDENCE. STATIC PASS != LIVE LIBRARY PASS. TRIAL PREPARATION != LIVE VERIFICATION.

| Loại lỗi | Căn cứ phân biệt |
| --- | --- |
| RETRIEVAL FAILURE | Không resolve/read được artifact theo binding/root |
| ROUTING FAILURE | Artifact khả dụng nhưng selection/application sai |
| IDENTITY FAILURE | Chấp nhận wrong artifact hoặc bỏ qua header mismatch |
| SCOPE FAILURE | Activation persist/leak ngoài scope được chọn |
| PLATFORM LIMITATION | Surface không expose đủ evidence về exact retrieval/FULL_FILE hoặc không enforce root |

Một lỗi có thể có nhiều nguyên nhân; giữ unresolved khi chưa phân biệt được. LOCAL FAILURE != GLOBAL ARCHITECTURE FAILURE. Báo ca lỗi và giới hạn; không tự redesign, sửa control, promotion hoặc deploy sau trial.
