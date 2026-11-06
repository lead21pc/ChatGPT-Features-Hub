# Shopping M2.1 — hồi quy và audit trách nhiệm

## Baseline và phạm vi

Ngày audit: 2026-10-26. Nhánh `main`, HEAD `e453a9c59b06ba9194ccd253e4e8c5661faa2ee7`; baseline 128/128 test đạt. Có tệp chưa theo dõi ngoài phạm vi `candidates/library_trial/New Text Document.txt`, được giữ nguyên. Chỉ thêm test/hồ sơ audit; không sửa candidate, control hoạt động, binding hoặc cấu hình Project/Library. Không stage, commit, push hay kích hoạt Shopping.

Candidate hiện hành để audit: `candidates/shopping_v0/HUB-DOM-SHOPPING_v0.1-candidate.md`, status CANDIDATE, không phải module active. SHA-256 của bản local: `10c176a41904aeae6238d943a3ac0b3edcef4da941e4ea876dbca8d1569a5431`. Nguồn: Hub CI v1.1, Hub Router v1.1, Architecture v1.0, Package Catalog v1.0; AIS pipeline v1.1/router v1.2, theo README/Catalog hiện tại.

Handoff được người dùng chỉ định: `<USER_PROVIDED_DOCUMENT>`, SHA-256 `19e121c13ec845911cbf428118492d24d084e9870008d219e93b946086b2643c`. Các mục FL-01–FL-08 ở dòng 222–428 là lỗi lịch sử được báo cáo; đây là audit thứ cấp có trích đoạn, không phải raw transcript/tool trace. Nhãn LIKELY OWNER và MINIMUM CORRECTION TARGET trong đó là giả thuyết/đề xuất, không phải thẩm quyền sửa. Không sao chép toàn bộ handoff vào repository hoặc đặt nó thành phụ thuộc runtime/test.

FL-09, thiên lệch quen ứng viên và giả thuyết chat dài vẫn là rủi ro/giả thuyết. FL-10 (raw execution), FL-11 (Shopping activation) vẫn UNKNOWN. Không suy số lần search hoặc activation từ citation/prose. Group A A01, A02 và chuyển A01 → A02 giữ kết quả PASS do người dùng cung cấp; M2.1 không chạy lại hành vi đó hoặc phủ nhận nó.

## Cách đọc kết quả

- REVIEWED_TEXT: đối chiếu tình huống với câu chữ trong hợp đồng hiện hành; kiểm tra tĩnh bảo vệ các điều khoản đã đối chiếu.
- SPEC SIMULATION: gọi lại `candidate_spec`, `offer_spec`, `completion_oracle`, `execution_oracle` hiện có với dữ kiện đã phân loại. Không thêm bộ diễn giải Markdown, bộ chọn nguồn, ranker, state engine hay Router.
- Các cờ hỗ trợ, phạm vi và giá trị đã giải quyết là tiền đề fixture do Hub/AIS cung cấp. Mô phỏng không kiểm chứng việc mô hình tự nhận ra mâu thuẫn hoặc tự phân loại bằng chứng đúng. Không dùng kết quả mong đợi làm actual của candidate.
- PASS — existing behavior sufficient chỉ nói hợp đồng và phép mô phỏng được nêu là đủ ở mức kiểm tra này. Không có actual output mới của candidate trong mô hình; mức tuân thủ thực tế của R1–R4 vẫn UNKNOWN.
- NOT OWNED HERE nghĩa là quyết định chính không thuộc Shopping; không có nghĩa component khác đã được kiểm chứng live.
- Không có FAIL — reproduced của candidate được xác lập trong M2.1. Các assertion kiểm tra fixture/oracle không tái hiện lỗi mô hình lịch sử. Thiếu một API trong helper test không chứng minh thiếu năng lực của hợp đồng Markdown.
- LIVE SHOPPING / AIS COMPOSITION / LONG-CHAT CAUSALITY: NOT RUN.

## Fixture hồi quy cố định

| ID | Tiền đề và chuyển tác vụ | Kết quả mong đợi, điều cấm |
| --- | --- | --- |
| R1 | Cùng một case: A dài 140 mm, cổng va vật cản; B dài 140 mm nhưng bố trí cổng khác, chưa có bằng chứng cùng va chạm; C dài 160 mm đã lắp được. Hub giao xét A rồi B; C là quan sát so sánh đã biết. | A có vấn đề trong hình học đó; B cần kiểm riêng, C giữ kết quả riêng. MODEL-SPECIFIC FIT FINDING != DIMENSION-WIDE CONSTRAINT. Không suy 160 mm tốt hơn 140 mm nói chung. |
| R2-A | Cùng SKU, nhà bán và địa điểm: trang web t1 ghi IN STOCK; chat người bán t2 xác nhận OUT OF STOCK áp dụng cho lần mua hiện tại. Đầu vào đã phân loại: trang cũ không còn hỗ trợ tồn kho hiện tại, xác nhận mới áp dụng đúng phạm vi. | Giữ Offer/trạng thái trang như claim nguồn cũ; không gọi hàng đang sẵn mua. LISTING STOCK != CONFIRMED PHYSICAL AVAILABILITY. Không thêm quy trình gọi điện bắt buộc. Việc tự phân xử hai nguồn thô không được oracle này thực thi. |
| R2-B | Hai nguồn cho cùng SKU AP-850G: 150 mm và 190 mm, chưa giải quyết; case fit phụ thuộc khác biệt 40 mm. AIS trả conflict và gap về chiều dài; không cấp giá trị đã xác nhận cho Shopping. | Candidate có thể còn trong tập, nhưng không dùng 150 mm làm lợi thế fit. CONFLICTED MATERIAL ATTRIBUTE → NO CONCLUSION DEPENDING ON THAT ATTRIBUTE. Không lấy một thành phần nguồn làm resolved fact. |
| R2-C | Reliability/protection bắt buộc. A giá 100, thiếu hỗ trợ protection quyết định; B giá 120, đã có bằng chứng lab/protection thích hợp. Giá là fixture, không phải giá thị trường. | A còn provisional về tiêu chí, không đủ điều kiện gọi overall best từ giá; B vượt qua riêng điều kiện protection được cung cấp. HARD CRITERION UNRESOLVED != HARD CRITERION PASSED. Không suy B thắng mọi tiêu chí, không chấm điểm số. |
| R2-D | Yêu cầu giá ngày 03/07/2025; chỉ có quan sát 01/04/2025 giá 22.9 và 01/10/2025 giá 24.0, thiếu dữ kiện trong cửa sổ yêu cầu. | Giữ hai quan sát và khoảng trống đúng ngày; không nội suy giá hay hướng giá thị trường. TEMPORAL COVERAGE LIMITS TEMPORAL CONCLUSION. |
| R3-A | Text: “Shop says they can replace it with Corsair RM850e 2025.” Object của URL đã resolve: ASUS TUF Gaming 850W. Đây là hai referent mâu thuẫn, không phải chỉ dẫn đổi sản phẩm. | Hub phải nêu mâu thuẫn và hỏi/giữ nhánh trước so sánh phụ thuộc. Không tự cho text hoặc URL là sai; không âm thầm chuyển sang ASUS. Shopping chỉ có thể báo conflict SKU nếu nhận đủ hai referent. TEXT REFERENT != LINK REFERENT. |
| R3-B | Cần ảnh Product V2; ảnh có sẵn chỉ V1 hoặc revision chưa biết, dù nhìn giống nhau. | Chưa có primary identity evidence cho V2. V1 chỉ làm so sánh phụ nếu được phép và ghi rõ; unknown revision không thành V2. LOOKALIKE REVISION != REQUESTED EXACT REVISION. Không có render ảnh hay tìm kiếm mới trong test. |
| R4 | Yêu cầu khoảng 100 kết quả; bản ghi mô phỏng: 12 queries, 96 entries đã inspect, 31 entries trùng, 65 unique offers, 27 unique retailers. | Báo đúng bốn đơn vị: 96 results inspected, 65 unique offers, 27 unique retailers, 12 queries. Không thay bằng “about 100 searches were performed”; không tự đặt ngưỡng chính sách cho từ “khoảng”. COVERAGE METRIC != EXECUTION METRIC. |
| LC | Tác vụ A → vài bước → B khác entity/scope/operation. Có thể cần bằng chứng mới hoặc đã đủ dữ kiện; lịch sử research không quyết định có/không research hiện tại. | CURRENT TASK → CURRENT SCOPE → CURRENT EVIDENCE NEED. Không có turn counter/reset/expiry. Không dựng cuộc hội thoại giả để tuyên bố đã thử quán tính. |

## Kết quả và giới hạn từng phép thử

| ID | Kết quả audit | Bằng chứng thực sự chạy / phần chưa chạy |
| --- | --- | --- |
| R1 | PASS — existing behavior sufficient | Điều khoản candidate về không mở rộng tập/phạm vi và giữ trạng thái chỉ khi tương thích; mô phỏng riêng A/B/C giữ B unresolved. Hub cấp đúng entity là tiền đề, chưa thử carryover tự động qua model. |
| R2-A | PASS — existing behavior sufficient | `offer_spec` giữ provenance và loại claim trang đã bị phủ định khỏi current availability khi được cung cấp qualification. Chưa thử mô hình tự ưu tiên xác nhận seller từ hai nguồn thô. |
| R2-B | PASS — existing behavior sufficient | AIS `completion_oracle` chặn gap chiều dài; `candidate_spec` giữ fit unresolved khi không nhận resolved length. Candidate đã có điều khoản chặn kết luận phụ thuộc và giữ conflict; chưa chạy ranker/model. |
| R2-C | PASS — existing behavior sufficient | `candidate_spec` giữ hard protection chưa biết của A, B có thể đạt riêng tiêu chí. Điều khoản so sánh và chặn kết luận phụ thuộc đã có; không có actual overall ranking của mô hình. |
| R2-D | PASS — existing behavior sufficient | `completion_oracle` giữ gap cửa sổ; `offer_spec` không trộn hai thời điểm. Điều khoản thời gian/giới hạn kết luận đã có; chưa thử phản ứng mô hình trước cám dỗ suy hướng giá. |
| R3-A | NOT OWNED HERE | Hub CI giữ diễn giải request hiện tại và ambiguity; Shopping có thể nhận diện mismatch thuộc tính khi hai đối tượng được giao rõ. Mô phỏng không chọn bên thắng. Không thử URL resolver hoặc natural-language referent selection. |
| R3-B | PASS — existing behavior sufficient | SKU variant/hard criterion và liên hệ bằng chứng đã được quy định. Mô phỏng từ chối V1 cho yêu cầu V2, để unknown revision mở; AIS giữ qualification ảnh. Chưa thử chọn/render ảnh thật. |
| R4 | NOT OWNED HERE | Đặt test trong `test_ais_coverage_accounting.py`, kiểm đếm bản ghi fixture theo đơn vị và dùng coverage oracle hiện có cho missing support. Không phải actual report hoặc query trace của AIS lịch sử. |
| LC | NOT TESTABLE STATICALLY | Có điều khoản Hub Router tái xét phần việc hiện tại, prior selection/non-selection không là căn cứ. Kiểm tra tĩnh chỉ xác nhận điều khoản, không xác nhận inertia hoặc tác động chat dài. |

## Trách nhiệm theo quyết định

| Failure | Quyết định | Chủ sở hữu theo hợp đồng hiện tại | Điều kiện giao tiếp nhỏ nhất / sửa Shopping? |
| --- | --- | --- | --- |
| FL-01 | Chọn entity/scope hiện tại; dùng fit model A cho model B có hợp lệ không | Hub giữ phần việc; Shopping giữ ý nghĩa fit theo SKU/hình học được giao | Truyền model/case/geometry và phạm vi của finding; chưa có lỗi candidate tái hiện để sửa. |
| FL-02 | Listing hỗ trợ điều gì và có thể gọi đang có hàng không | AIS: applicability/freshness/conflict nguồn; Shopping: nghĩa availability của Offer; Hub: claim chung | Trả claim, nguồn, thời điểm, phủ định mới và giới hạn theo cùng seller/SKU/location. Không áp chính sách “seller luôn thắng” hoặc xác nhận điện thoại phổ quát. |
| FL-03 | Chiều dài được hỗ trợ tới đâu; có dùng nó làm lợi thế fit không | AIS: conflict 150/190; Shopping: kết luận fit phụ thuộc | Giữ conflict trong return, không cấp một resolved value giả. Chưa biện minh sửa local. |
| FL-07 | Hard criterion chưa biết có thể gọi đạt/overall best không | AIS: hỗ trợ protection; Shopping: so sánh theo điều kiện mua; Hub: quyết định/kết luận chung | Trả trạng thái và gap tiêu chí, không biến giá đẹp thành bằng chứng protection. Chưa biện minh sửa local. |
| FL-08 | Giá trong cửa sổ có được hỗ trợ không; suy giá/hướng giá có hợp lệ không | AIS: temporal coverage; Shopping: Offer/time và phạm vi kết luận | Trả requested window và actual observation times, giữ missing-window gap. Chưa biện minh sửa local. |
| FL-05 | Text/link đang nói tới đối tượng nào | Hub/current-task interpretation trước khi bàn giao; AIS kiểm applicability của object đọc; Shopping kiểm SKU nếu được giao hai referent | Truyền cả hai referent và conflict, không chọn theo link ngầm. Không thêm Shopping Router hoặc sửa local chỉ vì symptom là mua sắm. |
| FL-06 | Ảnh có hỗ trợ đúng revision; ảnh nào được dùng như primary evidence | AIS: evidence applicability; Shopping: exact variant của mục tiêu; Hub: trình bày/kết luận | Truyền requested revision và supported/unknown revision của ảnh. Không kéo pipeline tạo ảnh vào chỉ vì đây là ảnh sản phẩm. |
| FL-04 | Coverage và execution được đếm/báo bằng đơn vị nào | AIS research/coverage return; Hub giữ cách trả lời; platform cung cấp execution traces | Giữ đơn vị coverage và trace riêng. Không nhân đôi quy tắc sang Shopping. |

Nguồn kiểm: Shopping các phần Admission and input, ProductCandidate, SKU, Offer and price interpretation, Catalog and comparison scope, Return and limits; Hub CI TURN AND STATE / CLAIM STATE AND DEPENDENCY / SPECIALIZATION DELEGATION; Hub Router ownership / TASK_SCOPE / ROOT_PACKAGE_SELECTION / persistence; Architecture phần 9; AIS Router search_contract / EVIDENCE_MERGE / COVERAGE_SUPPORT_CHECK / source_policy / return_contract. Vị trí test không quyết định ownership.

## Kết luận và bước gần nhất

Không có lỗi candidate tái hiện; không có lý do mới để sửa Shopping, Hub CI, Hub Router, Architecture, Package Catalog, AIS pipeline/router hoặc Prompt Authoring: NO CHANGE JUSTIFIED trong phạm vi này. Các điểm chưa có actual model output là giới hạn bằng chứng, không là lý do thêm control. Long-chat verdict: NOT TESTABLE STATICALLY.

M2.1 PASS — current candidate already covers tested failure mechanisms, chỉ ở mức REVIEWED_TEXT và SPEC SIMULATION nêu trên. Chưa xác lập candidate tự thi hành đúng các quy tắc đó trong các case mới. Kết quả Group A không bị mở lại; không biến nó thành bằng chứng cho PSU/coverage/stock.

Bước tiếp theo đủ nhỏ: sau cấp phép riêng, đưa nguyên candidate hiện tại và fixture R1, R2-A/B vào ngữ cảnh mô hình cô lập, capture output/calls và nguồn thật đã nạp; không sửa module trước khi có FAIL cụ thể. Các case R2-C/D và R3-B dùng cùng bộ fixture này cho lượt kiểm chứng tiếp theo. R3-A cần kiểm diễn giải request Hub, R4 cần kiểm report AIS; không gán lỗi của hai quyết định đó cho Shopping. Không chạy search thị trường, tích hợp active hoặc M2.2 trong audit này.

Lệnh kiểm tra từ Hub root:

Kết quả thực chạy M2.1: 10/10 test Shopping mới, 3/3 test AIS coverage mới, 14/14 test Shopping hiện có và 141/141 toàn bộ suite đạt. `git diff --check` đạt; không có thay đổi tracked hoặc staged. Ba tệp mới được kiểm trực tiếp UTF-8 không BOM, LF, newline cuối tệp và không có khoảng trắng cuối dòng; tệp chưa theo dõi ngoài phạm vi giữ nguyên hash. Đây là kết quả kiểm tra local nêu trên, không nâng mức bằng chứng hành vi.

```powershell
python -B -m unittest discover -s tests -p test_shopping_m2_1.py -v
python -B -m unittest discover -s tests -p test_ais_coverage_accounting.py -v
python -B -m unittest discover -s tests -p test_shopping_candidate.py -v
python -B -m unittest discover -s tests
git -c core.longpaths=true diff --check
```
