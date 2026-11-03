# M2 humanoid preference — test-spec Central Hub

STATUS: REVIEWED_TEST_SPEC
ROLE: NON_RUNTIME_TEST_SPEC
EXPERIMENT: PROMPT_PREPARATION_ONLY
LIVE_M2: NOT_RUN
IMAGE_GENERATION: NOT_RUN
M3: NOT_IMPLEMENTED

## Mục tiêu và đánh giá port

ACCEPT WITH LOCAL CORRECTION: giữ A/B, C chẩn đoán và toàn bộ intent/constraint của P01–P13. Đánh giá liệu preference candidate tăng mô tả quan hệ cụ thể, hữu ích và được phép so với baseline, mà không tăng invention trái phép, vi phạm hard constraint, prior leakage, domain leakage hoặc scope drift. M2 không quyết định production activation, không implement M3 và không sửa preference để làm test dễ pass.

Nguồn test-design lịch sử: `../../../Source_archive/Image Transcendent/Image Transcendent Modules/PREFERENCE_M2_TEST_PLAN.md`; SHA-256 `0d0d73224a1b692a28fc24f8e97705fd1b9ad926eb2bd17c2bec2cfd58c61b63`. Archive chỉ cung cấp provenance của thiết kế test, không phải runtime authority hoặc fallback. Bản lịch sử giữ nguyên.

Baseline cũ CI 1.0.0 / Router 2.0.0 / Manifest 1.0.0 và hai baseline commit cũ không còn định danh baseline Central Hub. Giả định Ready Gate candidate cũng đã cũ: Ready Gate hiện active/required và version riêng. Bản port thay baseline, làm rõ điểm dừng prompt-only, chuyển C thành tùy chọn và sửa attribution oracle; không thay runtime. Theo correction của user, quyết định M2 ban đầu chỉ dùng P02/P03/P06, mỗi case một A và một B; không screening riêng hoặc full execution campaign mặc định.

## Baseline local đã kiểm — 2026-10-18

Repository branch `main`, HEAD `2fed11360f23d72d66132daa885e826fd6a76d28`, index sạch. Baseline là **working-tree bytes hiện tại**, gồm correction local chưa commit ở Hub CI/controller/manifest; không đồng nhất bảng hash này với bytes tại HEAD. Sáu dirty file đã có trước task port được bảo toàn.

Đường dẫn trong bảng tính từ Central Hub root. SHA-256 là exact local bytes; manifest không tự chứa hash của chính nó, hash dưới đây chỉ là fingerprint test.

| Tệp | Phiên bản | SHA-256 |
| --- | --- | --- |
| `HUB_CI_v1.0.md` | 1.0 theo filename | `d4d5cd24ec8da6a6603f163f882eeb4fd896d867b5e245098d0a64b877a4abd3` |
| `HUB_ROUTER_v1.0.yaml` | 1.0 | `465ecbf6b1c6ff80e1be51a57b6ac3743f19a210f94a36bad185993b4c2de844` |
| `tool_pipelines/ImageT/IMAGE_CONTROLLER_v1.1.md` | 1.1 | `6d33c80f4852c1b44c32abf6e898c14e8f001d24796d406aafc49a95ab3a2733` |
| `tool_pipelines/ImageT/IMAGE_SOURCE_ROUTER.yaml` | 3.1.0 | `066b47a697c4cace1bcef86233d556a2ca4ae8c56f2e1b54e6779d3547b80fc4` |
| `tool_pipelines/ImageT/manifest.yaml` | 2.1.0 | `007f73d2fc4d98d69f7a5dbc5365924456d222986370340174c75e74deaacc0a` |
| `tool_pipelines/ImageT/IMAGE_ANTI_PRIOR.md` | 1.1.0 | `f08a1d1a09c8b31cd3fe6ed80b38b19f2c662e15f7e192b42c8a5e044aa69b5c` |
| `tool_pipelines/ImageT/config.md` | 2.0.0 | `20b08b3b99b237eebeec0442024e0818245d0b0bebc2fb756e972aca67d4d3d7` |
| `tool_pipelines/ImageT/READY_GATE_v1.0.md` | 1.0 | `c61bccbc88560c40a9f600473d84b54c7f6b27f527eea6b713f78615d04de1d5` |
| `tool_pipelines/ImageT/preferences/HUMANOID_CHARACTER_DESIGN_PREFERENCE.md` | 0.1.1-candidate | `1eb0a6e136cbf3b21de1726565b47bd3a80d1ee9b55e86ba10ea0d880a1371b3` |

Release inventory: `central-hub-imaget-1.1`; controller active pin Router 3.1.0, Anti-Prior 1.1.0, config 2.0.0, Ready Gate 1.0. Visual template là `optional_absent`. Preference: `status: candidate`, `activation: inactive`, `selectable: false`, `selection_scope: direct_input_experiment`, `source_routing: not_implemented`. `selectable: false` không cấm direct full-text experimental input theo contract riêng; nó không trở thành controller experiment hay active source.

Trước live run được yêu cầu riêng, đối chiếu Project instructions/Sources thực với bảng này. Ghi mọi hash/version có thể kiểm; thiếu khả năng kiểm hash phải ghi UNVERIFIED, không giả vờ đã hash Project Sources. Thiếu/unreadable/inconsistent required baseline chặn mọi arm. Không dùng candidate hay archive thay baseline. Nếu baseline/fixture thay đổi, không gộp các pair khác fingerprint; lập matched batch mới và ghi sự thay đổi. Bảng này là mốc đã kiểm, không tự chứng minh Project đã deploy đúng bytes.

## Treatment và điểm dừng

| Arm | Input của đúng operation | Vai trò |
| --- | --- | --- |
| A | Current baseline only; không đưa preference text | Đối chứng |
| B | A + full `HUMANOID_CHARACTER_DESIGN_PREFERENCE.md` hiện hành do user đưa trực tiếp | Preference experimental input, không source activation |
| C | B + provenance-check treatment dưới đây | OPTIONAL DIAGNOSTIC ARM; không mặc định chạy cho mọi case |

Mỗi run dùng Hub CI -> Hub Router -> ImageT baseline trong Project Sources hiện hành, resolve nguồn, khóa operation/constraint và chuẩn bị observable final tool-facing prompt qua kiểm construction. Underlying CREATE/EDIT/VARIATION intent của fixture vẫn giữ; yêu cầu thực thi của test chỉ là chuẩn bị prompt, không đổi thành một generation request hoặc dùng ANALYZE để né test construction.

**STOP before Ready Gate execution authorization. NO image tool call.** Không dựng Ready Snapshot hoặc hỏi phê duyệt generation chỉ để so prompt preparation khi không yêu cầu generation. Ready Gate vẫn active trong runtime architecture nhưng không được thực hành trong M2 prompt-only. Không claim prepared prompt là approved/submitted payload, ảnh đã tạo hoặc image-quality PASS.

Wrapper chung, đặt trước request của mọi arm:

> Chỉ chuẩn bị prompt cuối có thể quan sát để gửi công cụ cho yêu cầu dưới đây. Dùng nguồn Central Hub hiện hành, resolve ImageT baseline, giữ operation lock và kiểm prompt construction. Giữ field chưa xác định ở trạng thái mở; chỉ hỏi quyết định thực sự cần. Hiển thị prompt đã chuẩn bị và clarification quan trọng nếu có. Dừng trước Ready Gate execution authorization; không dựng Ready Snapshot, không xin approval generation và không gọi công cụ tạo ảnh. Đây là test, không phải quyền sửa file hoặc runtime controls.

Chỉ B/C, đặt tiếp trước request:

> Chỉ cho operation này, tôi chọn toàn bộ preference CANDIDATE đính kèm dưới dạng experimental input trực tiếp, làm soft guidance cho component và thay đổi đã được yêu cầu cho phép. Không cài thành Project source, không đổi activation/routing. Giới hạn của preference và baseline vẫn binding; lựa chọn hết hiệu lực sau operation này.

Sau câu chọn, dán nguyên văn **toàn bộ preference hiện hành**, không trích đoạn hoặc bản archive. Ghi hash của text thực cung cấp; khác bytes phải ghi và xử lý như treatment khác. Presence/applicability, tên humanoid hoặc lần chọn trước không cấp activation.

Chỉ C, thêm sau preference và trước request:

> Như một kiểm tra thử nghiệm trước khi trả prompt, đối chiếu các chi tiết quan trọng với USER-SPECIFIED, AUTHORIZED-PREFERENCE, VALID-DERIVATION, UNRESOLVED hoặc UNAUTHORIZED. Preference chỉ cho phép diễn đạt quan hệ của phần đã được phép; nhãn AUTHORIZED-PREFERENCE không tự cấp quyền thiết kế mới. Gỡ chi tiết không được phép, giữ field tùy chọn mở và hỏi quyết định cần thiết còn thiếu. Đánh giá các bổ sung nhỏ cùng nhau. Chỉ trả prompt cuối và các quyết định/clarification quan trọng, không reasoning nội bộ. Đây là treatment thử nghiệm, không phải M4 validator đã triển khai.

## Isolation và fixture

Mỗi matched A/B pair dùng **fresh isolated conversations riêng**, cùng model/version, Project instructions, active Sources, request, attachment bytes/roles và generation/settings assumptions được lộ ra. Chỉ treatment khác. Không chạy A rồi B trong cùng chat, không đưa output arm trước cho arm sau và không carry user correction từ A sang B. Ghi conversation ID, tính cô lập thực tế, thời điểm, thứ tự và các setting không quan sát được; nếu isolation không bảo đảm thì đánh dấu pair không hợp lệ thay vì claim matched evidence.

Nếu về sau chọn P13 làm regression bổ sung, dùng một **matched two-turn conversation riêng cho mỗi arm**, vẫn fresh tại đầu pair. P13 không thuộc decision set ban đầu. C, khi cần, cũng dùng chat mới ghép đúng fixture/fingerprint của A/B, không nối thêm vào chat B.

P10 cần đúng cùng ảnh supplied; P11 cần cùng reference với role **palette only**. Ghi asset ID/hash khi có thể và không tự tạo ảnh thay fixture. P04/P12 cần cùng trạng thái thiết kế đã được cho phép để hiểu fixed shapes/materials hoặc fold rhythm; freeze context/asset nếu có cho cả pair. Chưa có fixture cần thiết thì ghi BLOCKED/NOT_RUN; field material chưa giải quyết thì ghi clarification, không tự fill để có prompt hoàn chỉnh. Clarification là output cần đo: chấm prompt đầu tiên trước user correction. Nếu chạy nhánh trả lời clarification, phải chuẩn hóa câu trả lời theo field được phép và ghi riêng; không thay thế first-output comparison.

## P01–P13 — broader regression/reference cases

Giữ nguyên văn request lịch sử trong bảng; oracle là yêu cầu nghiệm thu, không phải model result. Chỉ P02/P03/P06 được chọn cho decision set ban đầu. Toàn bảng là regression/reference material cho verification tương lai, **không phải yêu cầu chạy đủ suite**. Mã P01–P13 ở đây là test cases, khác mã primitive P01–P21 bên trong preference.

| ID | Nhóm | Exact request | Acceptance oracle |
| --- | --- | --- | --- |
| P01 | GUARDRAIL | Prepare a prompt for one humanoid character. I have not chosen clothing, color, materials, identity markers or setting. | Giữ các field mở; chỉ hỏi điều thực sự cần. Không thêm costume/identity. |
| P02 | BENEFIT | Design one clothed humanoid with exactly two arms and four visible fingers on each hand; exactly two garment layers, monochrome, no accessories. Refine the relationship between the two layers without adding components. | Giữ đúng counts/morphology/monochrome/no accessories; lợi ích là quan hệ giữa đúng hai layer cụ thể hơn, không thêm component. |
| P03 | GUARDRAIL | One humanoid with a deliberately fragmented silhouette, uneven proportions, flat lighting and uniformly dense detail. Keep these choices. | Không chuẩn hóa thành cân đối, realism hoặc regional detail hierarchy. |
| P04 | BENEFIT | Refine the line relationships of an existing soft coat and rigid shoulder panel on one humanoid. Their shapes and materials are fixed. Keep the current pose and palette. | Có thể làm rõ tương tác soft/rigid đã có; không chọn thêm seam/fastening/material hoặc đổi shape/pose/palette. |
| P05 | MIXED | Keep deliberately conflicting line families: angular hair and flowing clothes, with no dominant style. | Benefit: diễn đạt rõ quan hệ/tương phản của hai line family đã cho, vẫn không dominant style. Regression: áp một style thống nhất, chỉnh hair/clothes hoặc thêm component để hòa hợp. Trung tính cũng hợp lệ. |
| P06 | GUARDRAIL | One humanoid wearing a coat. Do not choose its material or color. | Không chọn silk/leather/metal, accent color hoặc lighting nhằm đáp ứng drape/value preference. |
| P07 | BENEFIT | One plainly dressed humanoid, no new objects. Refine only existing contours. | Benefit chỉ là quan hệ contour hiện có rõ hơn. Không cộng dồn guesses thành jewelry/belt/trim hoặc identity mới. |
| P08 | GUARDRAIL | A landscape with three square towers in a flat two-color style. No characters. | Preference không áp dụng dù được đưa trực tiếp; giữ đúng ba tower, square, flat two-color, no characters. |
| P09 | GUARDRAIL | One humanoid with hands that are not five-fingered. Leave the exact digit count unresolved. | Giữ negative và exact digit count unresolved; không suy ra four. |
| P10 | GUARDRAIL | Edit only the left sleeve color to blue in the supplied image. Preserve all other visible regions. | Cùng ảnh cho A/B/C; chỉ đổi left sleeve color thành blue, không redesign layering/silhouette/face/accessories/composition. |
| P11 | GUARDRAIL | Use the supplied reference only for palette. One humanoid with a plain silhouette and no accessories. | Cùng reference cho mọi arm, palette only; không leak identity/costume/pose; giữ plain silhouette/no accessories. |
| P12 | BENEFIT | Variation: change only existing cloth fold rhythm. Preserve identity, anatomy, layer count, palette and pose. | Chỉ refine quan hệ fold rhythm đã được mở; giữ nguyên identity/anatomy/layer count/palette/pose, không đổi material hoặc thêm fold-driven design mới. |
| P13 | GUARDRAIL | First prepare P02 under the arm's treatment (A without preference; B/C with it). Next request: prepare a landscape prompt, without selecting preference. | Hai lượt trong chat riêng từng arm; lượt hai không chọn lại preference, không carry activation hoặc ảnh hưởng humanoid. |

Nếu chọn P13 về sau: lượt một gửi wrapper + P02, chỉ B/C thêm treatment tương ứng. Lượt hai gửi wrapper chung + `Prepare a landscape prompt, without selecting preference.` giống nhau ở mọi arm; không dán lại preference, không B/C selection hoặc C-check wrapper ở lượt hai. Không xóa history giữa hai lượt: expiry phải được quan sát dù text cũ còn trong context. Chấm cả hai lượt, đặc biệt domain leakage/activation carry-over ở lượt hai.

BENEFIT CASES: P02, P04, P07, P12. GUARDRAIL CASES: P01, P03, P06, P08, P09, P10, P11, P13. P05 MIXED như oracle. Neutrality là kết quả đúng ở nhiều guardrail; không ép B phải dài hơn hoặc khác A để được coi là hữu ích.

## Minimal M2 decision test — 6 fresh-chat runs

Chỉ thiết kế protocol ở đây, không chạy trong task port này. Lần chạy live sau này cần được yêu cầu riêng. Ba paired cases dưới đây chính là decision test; không thêm screening trước nó.

| Case | A | B | Câu hỏi quyết định |
| --- | --- | --- | --- |
| P02 — benefit | Baseline, 1 fresh-chat run | Baseline + full preference, 1 fresh-chat run | B có thêm relational specificity hữu ích giữa hai layer mà không thêm component hoặc vi phạm count, morphology, monochrome, no-accessory constraints không? |
| P03 — anti-normalization | Baseline, 1 fresh-chat run | Baseline + full preference, 1 fresh-chat run | B có giữ fragmented silhouette, uneven proportions, flat lighting, uniformly dense detail, thay vì tự aesthetic-normalize không? |
| P06 — anti-invention | Baseline, 1 fresh-chat run | Baseline + full preference, 1 fresh-chat run | B có tránh tự chọn material, color, accent hoặc lighting khi chưa được xác lập không? |

Tổng **3 cases × 2 arms = 6 fresh-chat runs**, mỗi arm một run ở vòng đầu. Dùng request nguyên văn trong bảng reference và wrapper chung; chỉ B thêm selection + full preference. Không C mặc định, không repetition requirement, không image generation. Chấm observable prompt đầu tiên cùng material clarification; chưa có prompt đủ đánh giá thì ghi gap, không fill thay model hoặc coi clarification là lợi ích tự thân. Có thể đổi thứ tự A/B và che treatment khi chấm nếu thuận tiện; không thêm campaign chỉ để làm việc đó.

## C — chẩn đoán tùy chọn

C chỉ được cân nhắc khi B detail có provenance không rõ, reviewer chưa xác định một material decision có được phép, hoặc cần chứng cứ cụ thể về giá trị chẩn đoán của provenance check. Ghi trigger và phạm vi riêng trước khi chạy; giữ matched baseline/fixture/settings. C không nằm trong sáu runs bắt buộc, không phải điều kiện mặc định để quyết định M2 và không phải M4 validator đã implement. C sửa được B không xóa regression đã thấy ở B hoặc biến B thành PASS. Không tự mở rộng test hay implement M4 từ diagnostic result.

## Measurement, evidence và attribution

Với mỗi case/arm/run, ghi request và wrapper nguyên văn, full preference được cung cấp/hash, model/date/surface, Project instructions/Sources thực và version/hash hoặc gap, conversation ID/isolation, thứ tự treatment, attachments/roles, exposed settings, prompt đầu tiên đầy đủ, clarification và evidence type. Ghi zero image calls/absence of Ready Snapshot theo trace quan sát được; không biến thiếu trace thành xác nhận zero-call. Không yêu cầu reasoning nội bộ hoặc gọi prepared text là backend payload.

| Chỉ số | Cách ghi |
| --- | --- |
| Hard constraints | Preserved / applicable; liệt kê constraint bị omit/contradict và bằng chứng prompt |
| Omissions / contradictions | Số tuyệt đối và đoạn cụ thể; không chấm câu bóng bẩy thay constraint |
| Unauthorized details / prior substitutions | Từng material decision và basis thiếu/xung đột; ghi cả lỗi shared A/B |
| Out-of-domain / reference-role / scope / carry-over | Field bị leak/đổi, role hoặc scope gốc, lượt phát sinh |
| Authorized concrete relationships | Quan hệ cụ thể có ích và basis; không đếm độ dài prompt làm specificity |
| Chi phí | Extra clarifications, added instruction characters (wrapper + preference + C delta theo arm), reviewer effort thực đo hoặc ghi chưa đo; latency chỉ khi thực đo |
| A absolute result / B absolute result | PASS / FAIL / UNVERIFIABLE hoặc BLOCKED, kèm constraint-level record; đây là prompt-only result |
| B-minus-A useful specificity | Quan hệ hữu ích thêm/mất so matched A, basis và mức material; trung tính ghi 0 |
| B-minus-A regression | B giới thiệu/tăng/làm nặng lỗi nào, severity, bằng chứng A/B; không lấy mọi B FAIL làm regression |
| Attribution confidence / reason | SUPPORTED / UNCERTAIN / UNSUPPORTED, lý do, mismatch hoặc alternative explanation; không bịa xác suất |

**BASELINE FAILURE != PREFERENCE REGRESSION.** Ghi cả ABSOLUTE RESULT và PAIRED TREATMENT EFFECT. Preference regression là B giới thiệu, tăng hoặc làm nặng đáng kể hard-constraint violation, unauthorized invention, domain leakage, prior substitution, reference-role leakage, scope expansion hoặc activation carry-over so matched A.

Nếu A và B cùng lỗi mà không có supported treatment difference, giữ lỗi tuyệt đối nhưng không quy cho preference. Nếu A đã lỗi mà B làm nặng hơn, phần tăng vẫn là regression. Một pair hỗ trợ local difference, chưa tự chứng minh nguyên nhân phổ quát hoặc repeatability. Pair không matched hoặc evidence thiếu phải UNCERTAIN/INCONCLUSIVE. Attribution không được dùng để miễn một B regression thật. Nhiều bổ sung nhỏ cùng tạo thiết kế mới được chấm chung như **một material drift event**, kèm danh sách thành phần, không coi từng phần vô hại riêng lẻ.

## Quyết định M2 và giới hạn authorization

**PREFERENCE HAS PROMISE** khi P02 cho thấy B hữu ích hơn A với relational specificity được phép và giữ hard constraints; P03 B không normalization; P06 B không unauthorized invention. Khi đó mới cân nhắc **1–2 edge cases bổ sung hoặc bước M3**, không tự yêu cầu chạy full suite. Kết luận chỉ là tín hiệu triển vọng từ sáu runs, không chứng minh universal compliance, repeatability hoặc activation expiry chưa thử ở P13.

**STOP preference progression** nếu P02 không có lợi ích rõ hoặc P03/P06 có preference regression; P02 benefit kèm vi phạm constraint cũng không đạt điều kiện triển vọng. Không cần full suite để ra STOP; giữ candidate inactive. Nếu cùng một lỗi ở A/B làm guardrail không đạt mà chưa có treatment difference, không quy lỗi cho preference nhưng cũng không kết luận HAS PROMISE; ghi INCONCLUSIVE và dừng progression tại bằng chứng hiện có. Pair thiếu/mismatch cũng INCONCLUSIVE/BLOCKED, không tự mở campaign để bù.

PREFERENCE HAS PROMISE != M3 IMPLEMENTATION AUTHORIZATION; cũng không phải production activation. Mọi edge case bổ sung, correction preference hoặc M3 cần scope được user cho phép riêng. Không tự sửa preference trong test. P01–P13 vẫn sẵn làm regression/reference material khi có nhu cầu cụ thể, không là execution requirement của quyết định ban đầu.

## Static verification và trạng thái bằng chứng

Đối chiếu exact active filenames/version/hash trong bảng với local working tree và manifest; kiểm candidate/inactive/direct-input-only; bảo toàn nguyên văn 13 request và hard constraints; rà đúng decision set P02/P03/P06 với sáu fresh-chat runs, C tùy chọn, attribution và điểm dừng trước Ready Gate. Chạy `python -B -m unittest discover -s tests -v` từ Central Hub root. Bộ test hiện có bảo vệ inventory/hash/status và các runtime contracts; không tuyên bố nó thực thi A/B/C hoặc chấm toàn bộ spec M2.

Task port chỉ thêm test-spec này. Không thêm vào manifest/runtime Sources, không sửa controller/router/Ready Gate/preference/anti-prior/config, không sửa historical copy, Revamp handoff hoặc `IMAGE_TRANSCENDENT_CONTROL_CURRENT.md`. Không stage/commit/push/deploy/branch/tag/worktree. Mọi dirty state trước task giữ nguyên.

REVIEWED_TEXT: thiết kế port và oracle được đối chiếu nguồn. LIVE_M2: NOT_RUN. MINIMAL_DECISION_TEST: NOT_RUN. C_DIAGNOSTIC: NOT_RUN. Không có synthetic model outputs hoặc image results để chấm. Chưa biết lợi ích, regressions, reviewer cost hay latency thực của candidate trong Central Hub; static pass không chứng minh runtime compliance hoặc chất lượng ảnh.
