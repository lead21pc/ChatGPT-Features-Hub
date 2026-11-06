# AetherFire — Status, Civil & Labor Current Canon

> Module ID: `AFM-002`
> Runtime role: `CURRENT_SOURCE`
> Domain / Scope: Status ontology, Citizen, Civil, Yellow, POW, Criminal, Civil entry/allocation/lifecycle, labor, and cross-status transitions.
> Authority boundary: Controls legal/civic status ontology and Civil/labor interfaces within the AetherFire national scope; does not establish one universal legal regime for every country.
> Cross-domain owner boundary: AF national profile by `AFM-013`; detailed Undie professional identity, entry/exit, mobility, work/access, and Undi are controlled by `AFM-003`; shared Terminal/Guest Pass service architecture by `AFM-010` without replacing this module's status and economic-namespace authority.
> Load mode: `FULL_FILE`

> **Domain:** status ontology, social hierarchy, Citizen/Civil/Yellow/POW/Criminal, Civil entry/allocation/lifecycle, cross-status transitions and shared economic/access namespaces.  
> Cơ sở Civil 2026-10-05 trong Part II kiểm soát xét tuyển, phân công, quyền lợi, hoàn thành và rời hệ. Bản đồ định nghĩa giữ các trục độc lập; phần chưa chốt vẫn `UNKNOWN / UNRESOLVED`.
> **Retcon — 2026-10-05:** Civil là chế độ phục vụ tự nguyện ở đầu vào, không Slave/punishment/caste; citizenship là trục riêng. Undie là nghề do `13` kiểm soát. POW/Criminal/Yellow, Career Rank ngoài phạm vi và namespace kinh tế độc lập không tự bị xóa.

## Part I — Resolved status and ontology map

### Guest-service interface — accepted 2026-10-03

`02_TECHNOLOGY_AND_PUBLIC_SERVICE_INFRASTRUCTURE_CURRENT.md` controls the removable terminal and Guest Pass functional model. Guest Pass is a temporary credential/access/service profile, not a legal status, class, Citizen/Civil conversion, or immigration/residency entitlement. Device Deposit, Guest Wallet and Access Profile remain separate objects; a terminal is not an account or access authority.

Guest Wallet có biến tài chính riêng. Kiến trúc Credit Score/Line và bare `credit` phụ thuộc cơ chế Undie cũ đã bị supersede theo retcon 2026-10-05; AF-OPEN-008 và các unknown triển khai ví vẫn mở. Không dùng ví khách để phục hồi các biến cũ. Guest access, legal recognition and recovery/exit after device loss/return are not inferred from existing Civil or Undie rules; AF-TECH-001 records these unknowns.

### AetherFire — Current Status & Ontology Map

> Chỉ gồm ontology hiện hành đã resolve trong cụm Citizen–Civil–Undie. Mọi khoảng trống được ghi `UNKNOWN`; file này không tạo canon mới.
>
> **Truth-status rule:** `ABSENCE OF CANON ≠ CANONICAL NEGATION`; `NOT ESTABLISHED ≠ FALSE`; hai trục độc lập không tự cho biết các giá trị của chúng có thể kết hợp hoặc ánh xạ thế nào.

#### 1. STATUS

**Definition:** trạng thái pháp lý/civic đang chi phối subject; không đồng nhất với class, job, rank, zone hay economic variable.

**Known values trong phạm vi:**

- `Citizen` — citizen status.
- `Civil` — tham gia chế độ phục vụ lao động; không thuộc Slave, không hạ class. Citizenship/tình trạng nhập cư trước và sau service là trục riêng; tên pháp lý cuối cùng còn UNKNOWN.
- `Yellow` — trạng thái kỷ luật tạm thời của Citizen, một tuần ở lần đầu rồi trở lại Citizen. Undi không còn là dấu địa vị/trừng phạt mặc định; trang phục của Yellow cần xác nhận riêng.
- `POW` — public status; backend dùng Slave security category nhưng không kéo POW vào Civil/Criminal/Undie ontology.
- `Slave` — Civil và Undie bị loại khỏi phạm vi này. Criminal vẫn là lớp Slave; POW giữ backend security category riêng, không nhập vào Criminal/Civil.

**Known transitions:**

```text
eligible applicant [không chỉ Citizen]
→ tự nguyện đăng ký + xét tuyển + khả năng tiếp nhận hợp lệ
→ được nhận vào Civil
→ phân công phù hợp bắt buộc
→ hoàn thành thời gian tối thiểu + nghĩa vụ đủ chuẩn
→ rời Civil + gói hoàn thành / tuyến pháp lý theo đầu vào

rời sớm hợp pháp → có thể mất quyền lợi hoàn thành chưa kiếm được
citizenship / residency → không tự đổi chỉ vì tham gia Civil

Citizen → first offense → Yellow → 1 tuần → Citizen
repeat Yellow-rule offense → outcome UNKNOWN [Yellow→Red/Undie đã nghỉ hưu; không tự giữ quota ×2]

death-sentence exposure → plea → Criminal Slave
```

**UNKNOWN:** tái phạm Yellow; eligibility, thời hạn/công thức Civil, thủ tục exit, giới hạn quyền lực và exact immigration pathway. Quyền rời sớm Civil và hôn nhân/tài sản/liên lạc được chốt ở Part II, không còn wholly UNKNOWN. Gia nhập Undie không tạo conversion hoặc White→Citizen.

#### 1A. SOCIAL HIERARCHY / CIVIC STANDING

Social hierarchy là trục riêng với legal status và class.

```text
Hoàng gia > Quý tộc > Sĩ quan quân đội = POW > Thượng lưu > Trung lưu > Trí thức > Citizen > Criminal
```

Civil không phải bậc thấp/caste và không được công quyền đối xử kém Citizen; không đặt mọi người tham gia Civil (gồm người nhập cư) vào một citizenship/social tier chỉ từ service. Không suy mọi quyền chính trị/nhập cư/nghĩa vụ giống Citizen. Undie không là bậc cố định; Purple/Hazel cũ không dùng được.

#### 2. CLASS / COLOR

##### Class

- `Civil` — chế độ phục vụ, không class Slave hoặc tầng người thấp hơn.
- `Undie` — căn tính/hệ sinh thái nghề nghiệp, không nằm trong trường class Slave.
- `Criminal` — lớp Slave riêng. Không dùng Undie nghề nghiệp làm bậc pháp lý/xã hội đối chiếu.

##### Color / visual-functional labels

- `Brown` — dấu status bắt buộc/jumpsuit đồng nhất cho Civil đã bị supersede. Trang phục nghề/an toàn Civil cụ thể chưa chốt; không cấm màu Brown nói chung hoặc chốt penal Brown.
- `Black` — màu nhận dạng của Criminal; `Criminal` mới là class.
- `Red`, `Scarlet`, `Pink`, `Gray`, `Purple`, `Hazel`, `White` — mã kiến trúc Undie cũ đã nghỉ hưu; chỉ tái dùng qua quyết định canon riêng.

**Relations:** Citizen có thể đồng thời hành nghề Undie. Yellow là trạng thái kỷ luật độc lập; Undi là họ đồng phục nghề theo ngữ cảnh, không xác lập Yellow/Slave hoặc White→Citizen.

**UNKNOWN:** sự tồn tại của một penal class Brown ngoài nguồn hiện hành; ma trận quyền/mobility Criminal. Không tiếp tục hỏi full color/rank graph như thể nó còn là kiến trúc Undie hiện tại.

#### 3. JOB / LABOR REGIME

##### Civil

- Tự nguyện tham gia ở đầu vào, xét tuyển không tự động; hệ phải thực sự bảo đảm sinh hoạt/phân công/triển khai.
- Được nhận rồi phải làm assignment và tới địa điểm hợp lệ theo năng lực/thể lực/điều kiện; preference không phải veto.
- Assignment sai, tình trạng đổi hoặc trái chuẩn/không an toàn → có căn cứ khiếu nại, đánh giá lại/phân công lại.
- Upkeep tách tiền công; không giữ người bằng nợ upkeep hoặc tự chuyển failure thành Criminal.
- Rời sớm hợp pháp có thể mất quyền lợi chưa kiếm được; completion dựa thời gian tối thiểu + service đủ chuẩn, không mốc 5–10 năm.
- Quyền hôn nhân, tài sản, tiền, nghỉ/liên lạc/điều trị/khiếu nại/riêng tư phù hợp assignment đã chốt; implementation và compatibility Undie còn mở.

---

##### Undie

- Hệ sinh thái nhiều nhánh nghề chồng lấn, không một job hoặc thang nghề chung.
- Citizen + người hành nghề Undie là tổ hợp đã chốt; gia nhập/rời nghề không đổi địa vị pháp lý.
- Môi trường hoạt động rộng và di động; sex work chỉ là một nhánh có thể có.
- Nghề, tính hợp pháp, dịch vụ, đồng thuận, hợp đồng và nơi làm việc là những biến riêng.
- Tương thích với nghĩa vụ Civil/Criminal hoặc điều kiện giấy phép cụ thể còn mở; `13` kiểm soát chi tiết.

---

##### Criminal

- Current confirmed regime: cực thấp/bẩn/nguy hiểm/không đáng dùng robot; ví dụ waste, hospital cleaning, sewer cleaning.
- `UNKNOWN / NEEDS USER RESOLUTION:` metallurgy/construction/factory list trong merged source có còn current hay không.

#### 3A. CIVIL AUDIT MATRIX — baseline 2026-10-05

| Trục | Chốt hiện hành | Còn mở |
| --- | --- | --- |
| Ontology | Service, không Slave/punishment/caste; citizenship độc lập | Tên pháp lý cuối |
| Entry | Tự nguyện; poor/homeless/immigrant/Citizen có thể ứng tuyển; phải xét khả năng tiếp nhận | Eligibility, tiêu chuẩn và cơ quan |
| Allocation | Assignment phù hợp là nghĩa vụ; preference không veto | Matching, priority, profile verification |
| Appeal | Sai dữ kiện, thay đổi tình trạng, trái chuẩn/an toàn | Thủ tục đầy đủ |
| Pay / upkeep | Upkeep + tiền công tách; tài sản hợp pháp được giữ | Mức, housing, medical coverage |
| Personal life | Hôn nhân/tài sản/liên lạc/nghỉ/privacy phù hợp assignment | Gia đình/dependents và luật đầy đủ |
| Discipline | Tách không thể/thiện chí/từ chối/phạm tội; không hạ class tự động | Ladder, limits, appeal |
| Early exit | Có đường hợp pháp; mất benefits chưa kiếm, không upkeep debt | Notice, procedure, forced termination |
| Completion | Minimum time + đủ chuẩn; gói nền tự lập | Thời hạn/công thức/bonus |
| Immigration | Completion mở tuyến xét cư trú/nhập tịch mạnh, không trì hoãn vô hạn | Cư trú trước hay direct eligibility |
| Post-service | Gói có thể khác theo nhu cầu/đầu vào, không phân biệt pay cùng việc vì giàu nghèo | Mức cụ thể; tax support nếu có |
| Re-entry | Không chốt nút reset vô hạn | Điều kiện quay lại |

---

#### 4. CAREER RANK

**Definition:** trục tiến trình nghề nghiệp dùng để mở facility/shopping/necessities và điều chỉnh Credits; không phải class hoặc color.

**Known values:** `Entry`, `Intermediate`, `Support`, `Advanced`, `Ultimate`.

**Relation:** Career Rank ngoài Undie là trục riêng. Đồ thị màu Undie cũ đã nghỉ hưu; không dùng Career Rank để khôi phục nó hoặc áp một tiến trình phổ quát cho nghề Undie.

**UNKNOWN / NOT ESTABLISHED:** full Career Rank rules và promotion formula ngoài phần đã chốt; chưa chốt việc dùng Career Rank trong nhánh nghề Undie mới.

#### 5. ZONE

**Definition:** operational geography, không phải status/class/rank.

**Known values:** Industrial, Commercial, Auctions, Entertainment. Capital có nhiều vòng; class/color có thể liên quan vùng hoạt động.

**Relations:** Undie có thể rời red-light district và đi trong đô thị; restriction nhắm vào disruptive activity hoặc specialized restricted points, không phải blanket presence ban. Capital có full/near-full Undie infrastructure; satellite cities có partial system.

**Phạm vi đô thị còn hiệu lực:** khu ăn chơi bao gồm phố đèn đỏ; tại thủ đô, cư dân phải từ 21 tuổi, kiểm soát bằng khuôn mặt/ID/vân tay. Đây là luật vào khu theo phạm vi cư dân đã chốt, không phải tuổi tuyển chung cho mọi nhánh Undie. Nội dung/quảng cáo người lớn bị hạn chế ngoài khu ăn chơi; hoạt động nghề trong đô thị không đồng nghĩa nội dung người lớn được phép khắp nơi.

**UNKNOWN:** full zone map, full access matrix, exact barrier/collar permission rules; staff/emergency exceptions chưa chốt. Không giữ quyền theo màu Undie cũ.

#### 6. CREDITS

**Definition:** Credits là tiền điện tử được nhà nước bảo chứng; cash là tiền cơ bản. Nhận Credits sau công việc là một giao diện đã mô tả, không phải định nghĩa mọi cách tạo/nhận Credits.

**Properties:** money; không phải Credit Score, Contribution Points, Career Rank, status hay class.

**Known uses của normal Credits:** ordinary consumption trong phạm vi được phép.

Facility proposals/upgrades và một số room/customization eligibility dùng source wording `credits` hoặc `credits nội bộ`; exact relation của chúng với normal personal Credits chưa chốt.

**UNKNOWN:** quan hệ kế toán chính xác giữa personal Credits và “credits nội bộ” của facility ngoài kiến trúc Undie đã nghỉ hưu; full credit economy. Không phục hồi uniform unlock/Pink cost/bonus dựa trên web cũ.

#### 7. CONTRIBUTION POINTS

**Definition:** vốn trách nhiệm/độ tin cậy theo vị trí.

**Properties:** không phải tiền, Credit Score hay morality score. Có thể reset khi tiến/lùi/đổi nghề trong các trường hợp đã chốt.

**UNKNOWN:** formula, authority và exact reset matrix ngoài phạm vi Undie. Contribution Points không còn là trục bắt buộc của hệ kinh tế/tiến trình Undie; việc còn mô tả nó ở miền khác không phục hồi kiến trúc ấy.

#### 8. OTHER ECONOMIC VARIABLES

##### Credit Score / Credit Line trong Undie

Kiến trúc Credit Score, Contribution Points theo nghề Undie và Credit Line thế chấp địa vị đã nghỉ hưu. Không còn điều kiện mobility/reset/White, khoản vay thế chấp người hay default→điều phối lao động ở cơ sở tư nhân.

Nợ tài chính, nghĩa vụ hợp đồng, ân tình xã hội và ân tình chính trị phải tách riêng; ân tình không phải tiền tệ. Nợ không tạo sở hữu người hoặc tự động cung cấp dịch vụ tình dục. Các nghiệp vụ vay/ứng trước/tài trợ mới còn cần thiết kế trong `13`.

---

##### Citizen credit profile / bad credit

- Financial/eligibility profile của Citizen; bad debt có thể làm giảm cơ hội việc làm.
- Không đồng nhất với tiền Credits hoặc các biến Undie đã nghỉ hưu; không tự xóa hồ sơ tín dụng Citizen vì retcon giới hạn ở Undie.

##### Legacy black credit

- Design history; không phải current canon.

#### 9. ACCESS PROFILE

**Definition:** quyền truy cập/di chuyển/dịch vụ được xác nhận qua collar/backend và rules; không phải class hay Career Rank.

**Known relations:**

- Career Rank có thể mở facility/shopping/necessities.
- Nghề/hoạt động, giấy phép, địa điểm và access là biến riêng; chưa chốt ma trận mới của Undie.
- Collar là administrative terminal cho ID, access, movement, task và enforcement links.
- Tư cách nghề nghiệp Undie không cho phép công quyền tùy tiện chặn subject; không gọi nó là legal status.
- Chỉ đăng ký chưa được nhận không tự phát sinh quyền lợi Civil; không giữ cơ chế status-conversion cũ.

**UNKNOWN:** full access matrix; permission changes của Career Rank ngoài phần đã chốt; public-service matrix Civil và điều kiện nghề/địa điểm Undie mới.

#### 10. BACKGROUND / PROVENANCE

**Definition:** nguồn gốc/hồ sơ lịch sử; không phải current operational classification.

**Known rules:**

- Nguồn gốc/đầu vào Civil không tạo caste hay đối xử kém; assignment dùng hồ sơ phù hợp hiện tại. Nhu cầu/tình trạng đầu vào có thể ảnh hưởng gói hậu Civil, không phân biệt tiền công cùng công việc chỉ vì giàu/nghèo.
- Không tạo Refugee/Nomad/Unemployed/Deserter Civil caste chỉ từ provenance.
- Lịch sử nghề nghiệp không phải địa vị pháp lý. Quy trình ẩn/truy xuất hồ sơ gắn với White→Citizen cũ không còn là mốc hiện hành; luật hồ sơ nghề mới chưa chốt.
- Genealogy của Yellow từ fake-Undie/impersonation không biến genealogy thành current class ontology.

**UNKNOWN:** luật truy cập provenance/hồ sơ nghề và trường hợp đặc biệt chưa chốt. Civil có đầu vào tự nguyện; không dựng nhánh non-voluntary từ lịch sử.

---

## Part II — Civil cơ sở canon sau tái thiết kế 2026-10-05

Nguồn controlling: `AetherFire_Civil_Co_So_Canon_2026-10-05.md`, đọc đủ 24 mục. Đây là mốc mới được nhập theo yêu cầu tác giả, không luật Civil/nhập cư/hình sự đầy đủ. Nội dung dưới đây giữ nguyên câu chữ của nguồn trong đúng scope; §22 giữ đủ UNKNOWN.

### 1. Nguyên tắc trung tâm

Civil là một **chế độ phục vụ lao động tự nguyện ở đầu vào**, trong đó cá nhân chấp nhận giao cho hệ thống quyền phân công công việc và địa điểm trong phạm vi phù hợp với năng lực, thể lực và điều kiện đã được xác nhận.

Đổi lại, AetherFire bảo đảm nền tảng sinh hoạt cần thiết, trả công lao động, cung cấp bảo vệ lao động và mở một con đường hoàn thành nghĩa vụ để người tham gia rời Civil với vị thế ổn định hơn lúc vào.

```text
CIVIL
= tự nguyện tham gia ở đầu vào
+ xét tuyển
+ nhà nước bảo đảm sinh hoạt cơ bản
+ có tiền công
+ phân công bắt buộc phù hợp
+ có thể điều động địa lý
+ bảo vệ lao động
+ quyền khiếu nại tính phù hợp
+ đường rời sớm có giới hạn
+ hoàn thành nghĩa vụ
+ gói quyền lợi đã kiếm được
```

Civil không phải chế độ trợ cấp thụ động.

Civil cũng không phải cơ chế lao động để trả nợ.

Civil không tồn tại để hạ địa vị xã hội của người tham gia.

---

### 2. Loại bỏ hoàn toàn kiến trúc Slave cũ

Trong phạm vi Civil hiện hành:

```text
CIVIL != SLAVE
CIVIL != PUNISHMENT STATUS
CIVIL != UNDIE ROUTE
CIVIL != SOCIAL CASTE THẤP
```

Toàn bộ cách đọc Civil dựa trên `Slave`, `Civil Slave`, tầng nô lệ, hạ cấp địa vị, dấu nhận dạng của Slave hoặc quan hệ cũ với Undie đều bị loại khỏi baseline.

Không được dùng lịch sử cũ để suy rằng:

- Civil là một loại Slave;
- vào Civil là “tụt xuống” một tầng người;
- Civil phải bị đánh dấu để công chúng nhận ra;
- Civil phải chịu nhục mạ hoặc kỳ thị do nhà nước tạo;
- Civil là bước trung gian tới Undie;
- thất bại trong Civil tự động dẫn tới một tầng người thấp hơn;
- Civil phải mang cơ chế sở hữu người, thế chấp người hoặc nợ giữ người.

Lịch sử cũ chỉ còn giá trị truy nguyên thiết kế nếu cần đối chiếu, không phải nền hiện hành.

---

### 3. Chức năng kép của Civil

Civil đồng thời giải quyết hai vấn đề tương thích.

#### 3.1. Đối với cá nhân

Civil hấp thụ những người không đủ khả năng tự duy trì ổn định chi phí sống hằng ngày hoặc muốn chủ động đổi một phần quyền tự chọn nghề và địa điểm lấy một giai đoạn phục vụ có bảo đảm.

Mục tiêu là:

```text
không tự duy trì được ổn định
hoặc
tự nguyện muốn bước vào chế độ phục vụ
→ có nền tảng sống
→ có việc
→ có tiền công
→ có đào tạo và kinh nghiệm
→ hoàn thành nghĩa vụ
→ rời hệ với khả năng tự lập tốt hơn
```

#### 3.2. Đối với AetherFire

Civil tạo một nguồn nhân lực có thể dự báo và điều động để bù biến động của thị trường lao động tự do, đặc biệt tại các ngành, địa điểm hoặc mắt xích khó tuyển.

```text
thị trường lao động tự do
→ biến động nhân lực

Civil
→ nguồn nhân lực ổn định hơn
→ điều phối theo nhu cầu thực
→ giảm nguy cơ thiếu người tại mắt xích thiết yếu
```

Civil không được giữ người chỉ để làm phình bộ máy hoặc tạo nguồn lao động vô hạn.

---

### 4. Đối tượng có thể tham gia

Các nhóm có thể đi vào Civil bao gồm:

- người nghèo;
- người vô gia cư;
- người nhập cư không có tài sản hoặc nền tảng sinh hoạt ổn định;
- người không đủ khả năng tự chi trả ăn, ở và chi phí duy trì cuộc sống hằng ngày;
- Citizen tự nguyện muốn thử thách bản thân trong một chế độ phục vụ có phân công;
- các trường hợp khác sau này nếu được canon hóa riêng.

Những nhóm trên không tạo các loại Civil khác nhau về nhân phẩm hay cách đối xử.

Nguồn gốc trước khi vào Civil là dữ kiện đầu vào và có thể ảnh hưởng quyền lợi sau hoàn thành, nhưng không tạo caste nội bộ.

---

### 5. Đầu vào là tự nguyện, nhưng admission không tự động

Quyền đăng ký không đồng nghĩa quyền được nhận.

```text
ĐĂNG KÝ
!=
ĐƯỢC NHẬN
```

Ứng viên phải qua vòng xét loại.

Tối thiểu, Civil phải đánh giá các yếu tố liên quan trực tiếp tới khả năng phục vụ như:

- sức khỏe;
- thể lực;
- năng lực;
- kỹ năng;
- khả năng thích nghi;
- điều kiện an ninh khi thật sự cần cho assignment;
- các giới hạn có thể ảnh hưởng tới việc phân công.

Exact procedure, tiêu chuẩn và cơ quan xét tuyển chưa được chốt.

Civil không được nhận người nếu hệ thống không có khả năng thực tế để bảo đảm sinh hoạt, phân công và triển khai họ.

```text
KHÔNG CÓ KHẢ NĂNG TIẾP NHẬN HỢP LỆ
→ KHÔNG NHẬN THÊM CIVIL
```

---

### 6. Phân công lao động

Sau khi đã qua xét tuyển và được nhận, Civil không có quyền chọn công việc theo sở thích như trên thị trường lao động tự do.

Assignment dựa trên:

```text
nhu cầu nhân lực
+
năng lực
+
thể lực
+
điều kiện đã được xác nhận
+
khả năng triển khai
```

Civil có thể khai nguyện vọng hoặc mức sẵn sàng, nhưng đó là dữ liệu hỗ trợ phân công, không phải quyền veto.

```text
PREFERENCE
!=
QUYỀN ĐÒI ASSIGNMENT
```

Một người có thể chủ động nói rằng họ sẵn sàng đi nơi xa, nhận việc khó hoặc nhận vị trí thiếu người. Hệ thống có thể dùng thông tin đó trong matching.

---

### 7. Nghĩa vụ sau khi đã được phân công

Khi assignment đã được xác nhận là phù hợp với hồ sơ năng lực, thể lực và điều kiện hợp lệ:

```text
ASSIGNMENT HỢP LỆ
→ PHẢI LÀM CÔNG VIỆC ĐÃ PHÂN
→ PHẢI ĐẾN ĐỊA ĐIỂM ĐÃ PHÂN
```

Không thích công việc, không thích địa điểm, thấy việc thấp kém, muốn chờ việc tốt hơn hoặc đơn giản không muốn đi không tạo quyền từ chối tự động.

Civil trao một phần quyền tự chọn nghề và địa điểm để đổi lấy bảo đảm của chế độ.

---

### 8. Khiếu nại assignment

Quyền khiếu nại tập trung vào **tính phù hợp và tính hợp lệ**, không phải sở thích.

Ba nhóm căn cứ chính:

#### 8.1. Sai dữ kiện hoặc sai đánh giá

Ví dụ:

- hồ sơ năng lực sai;
- đánh giá thể lực sai;
- assignment đòi kỹ năng không có;
- assignment vượt điều kiện đã được xác nhận.

#### 8.2. Tình trạng thay đổi

Ví dụ:

- chấn thương;
- bệnh;
- thai kỳ;
- khuyết tật mới phát sinh;
- tình trạng gia đình khẩn cấp được công nhận;
- thay đổi khác làm profile cũ không còn đúng.

#### 8.3. Assignment trái chuẩn hoặc không an toàn

Assignment có thể bị phản đối nếu:

- vượt thẩm quyền;
- vi phạm luật hoặc chuẩn Civil;
- có điều kiện an toàn không đạt;
- khác bản chất nghĩa vụ mà hệ thống có quyền giao.

```text
KHIẾU NẠI ASSIGNMENT
= kiểm tra tính phù hợp / tính hợp lệ

không phải

KHIẾU NẠI ASSIGNMENT
= quyền chọn việc theo sở thích
```

---

### 9. Phân biệt các dạng thất bại

Civil không được gom mọi vấn đề thành “chống lệnh”.

```text
KHÔNG THỂ LÀM
!=
LÀM KÉM NHƯNG THIỆN CHÍ
!=
KHÔNG MUỐN LÀM
!=
CỐ TÌNH TỪ CHỐI
!=
PHẠM TỘI
```

Cách xử lý nền:

```text
assignment sai profile / không thể làm
→ đánh giá lại / phân công lại

khả năng chưa đủ nhưng có thiện chí
→ đào tạo lại / assignment phù hợp hơn

tình trạng sức khỏe thay đổi
→ tuyến y tế / tạm chuyển nhiệm vụ / đánh giá lại

cố tình từ chối assignment hợp lệ
→ kỷ luật Civil

gian lận / bạo lực / phá hoại / hành vi phạm pháp nghiêm trọng
→ luật thông thường có thẩm quyền
```

```text
THẤT BẠI TRONG CIVIL
!=
TỰ ĐỘNG TRỞ THÀNH TỘI PHẠM
```

---

### 10. Kỷ luật Civil

Kỷ luật nằm trong chế độ phục vụ, không tạo class thấp hơn.

Các công cụ có thể gồm:

- cảnh cáo chính thức;
- mất một số quyền lợi tùy nghi;
- kéo dài nghĩa vụ trong giới hạn hợp pháp;
- phân công lại;
- mất một phần quyền lợi hoàn thành chưa kiếm được;
- chấm dứt Civil vì lỗi;
- chuyển sang luật thông thường nếu hành vi độc lập cấu thành vi phạm pháp luật.

Exact ladder, giới hạn và thủ tục kháng nghị còn `UNKNOWN`.

Không được tạo:

```text
không tuân thủ
→ hạ thành tầng người thấp hơn
```

---

### 11. Bảo đảm sinh hoạt và tiền công là hai thứ khác nhau

```text
BẢO ĐẢM SINH HOẠT
!=
TIỀN CÔNG
```

AetherFire phải bảo đảm phần cần thiết để Civil có thể sống và thực hiện assignment, có thể gồm:

- ăn;
- ở;
- chăm sóc y tế cơ bản;
- vận chuyển cần thiết cho assignment;
- trang bị cần thiết cho công việc;
- các nhu cầu thiết yếu khác được xác định theo assignment.

Ngoài ra Civil vẫn được trả công lao động.

Civil không làm việc chỉ để đổi lấy đồ ăn và chỗ ở.

Tiền công có thể phản ánh việc một phần chi phí sống đã được hệ thống bảo đảm, nhưng không được bằng không chỉ vì Civil được nuôi ở.

Civil có quyền tích lũy tài sản và tiền cá nhân hợp pháp.

---

### 12. Nhà ở Civil

Nhà ở phục vụ nhu cầu triển khai, không phải mặc định giam giữ tập thể.

Các hình thức có thể gồm:

- ký túc hoặc nhà ở tập thể;
- căn hộ được hỗ trợ;
- nhà ở tại điểm triển khai;
- nhà ở chuyển tiếp;
- đơn vị phù hợp cho gia đình khi sau này được thiết kế.

```text
NHÀ Ở CIVIL
→ theo nhu cầu assignment và điều kiện cá nhân hợp lệ

không phải

MỌI CIVIL
→ barracks bắt buộc
```

Exact family housing, dependent support, trường học cho con, việc làm của bạn đời và quyền đi cùng người thân chưa được chốt.

---

### 13. Đời sống cá nhân

Civil không mặc định giao toàn bộ đời sống cá nhân cho nhà nước.

Civil vẫn có:

- tài sản cá nhân;
- tiền cá nhân;
- quan hệ tình cảm;
- hôn nhân;
- thời gian nghỉ;
- quyền liên lạc;
- quyền được điều trị;
- quyền khiếu nại;
- quyền riêng tư ở mức phù hợp với assignment;
- khả năng tích lũy và chuyển tiền hợp pháp.

Nhà nước kiểm soát trong phạm vi Civil chủ yếu:

```text
nghĩa vụ công việc
+
địa điểm phục vụ
+
lịch nghĩa vụ cần thiết
+
các điều kiện trực tiếp để assignment vận hành
```

Không tự mở rộng thành quyền kiểm soát toàn bộ cơ thể, gia đình, tài sản hoặc đời tư.

---

### 14. Rời Civil sớm

Civil có đường rời sớm hợp pháp.

```text
RỜI SỚM
→ có thể
→ mất quyền lợi hoàn thành chưa kiếm được
→ mất con đường hậu Civil nếu con đường đó phụ thuộc hoàn thành
```

Civil không bị giữ lại bằng cách biến chi phí ăn, ở và upkeep cơ bản đã sử dụng thành khoản nợ khổng lồ.

```text
UPKEEP ĐÃ ĐƯỢC BẢO ĐẢM
!=
KHOẢN NỢ GIỮ NGƯỜI
```

Nếu có ứng trước hoặc khoản riêng ngoài upkeep cơ bản, nghĩa vụ hoàn trả chỉ tồn tại khi được thiết lập độc lập và hợp pháp.

Đối với người nhập cư, rời sớm có thể làm mất con đường cư trú hoặc nhập tịch dựa trên Civil.

Đối với Citizen, rời sớm có thể làm mất gói hoàn thành và đưa họ trở lại việc tự chịu rủi ro thị trường và chi phí sống.

Exact notice period, thủ tục rời sớm và trường hợp chấm dứt bắt buộc còn `UNKNOWN`.

---

### 15. Hoàn thành Civil

Không giữ cấu trúc mặc định cũ `5 năm review / 10 năm tự động trở lại Citizen`.

Civil hiện dùng primitive:

```text
THỜI GIAN TỐI THIỂU
+
NGHĨA VỤ PHỤC VỤ ĐỦ CHUẨN
→ đủ điều kiện hoàn thành
```

Exact thời gian và công thức chưa được chốt.

Civil có thể ghi nhận mức khó của assignment để tạo động lực phục vụ tại nơi khó tuyển.

Ba nhóm khung hiện hành:

```text
THÔNG THƯỜNG
KHÓ TUYỂN
CỰC KHÓ / CHIẾN LƯỢC
```

Assignment khó hơn có thể:

- giúp hoàn thành nghĩa vụ nhanh hơn;
- hoặc tạo quyền lợi hoàn thành tốt hơn;
- hoặc cả hai nếu sau này được quy định.

Không có con số canon hiện tại.

Không biến cơ chế này thành hệ điểm số trò chơi quá chi li nếu không cần.

---

### 16. Gói hoàn thành chung

Người hoàn thành Civil bình thường được nhận một gói giúp họ có khả năng sống độc lập sau khi rời hệ.

Gói chung có thể bao gồm:

- khoản tích lũy hoặc trợ lực chuyển tiếp;
- nhà ở chuyển tiếp;
- hồ sơ chứng nhận hoàn thành Civil;
- chứng nhận kỹ năng và đào tạo đã tích lũy;
- hỗ trợ chuyển sang thị trường lao động dân sự;
- quyền giữ toàn bộ tài sản và tiền hợp pháp đã tích lũy;
- chăm sóc hậu nhiệm vụ đối với thương tật phát sinh từ service.

Primitive:

```text
GÓI HOÀN THÀNH
→ ĐỦ NỀN ĐỂ TỰ LẬP

không phải

GÓI HOÀN THÀNH
→ BẢO ĐẢM GIÀU CÓ / THOẢI MÁI VĨNH VIỄN
```

Exact số tiền, thời lượng nhà ở chuyển tiếp, phạm vi y tế và hình thức hỗ trợ việc làm còn `UNKNOWN`.

---

### 17. Quyền lợi sau hoàn thành phụ thuộc trạng thái đầu vào

Mọi Civil chịu cùng chế độ phục vụ nền, nhưng quyền lợi dựa trên nhu cầu hoặc tình trạng pháp lý ban đầu không bắt buộc giống nhau.

```text
CÙNG CHẾ ĐỘ PHỤC VỤ
+
TRẠNG THÁI ĐẦU VÀO KHÁC
→ GÓI HẬU CIVIL CÓ THỂ KHÁC
```

Điều này không cho phép trả lương khác nhau cho cùng công việc chỉ vì người này giàu hay nghèo hơn.

```text
TIỀN CÔNG LAO ĐỘNG
!=
HỖ TRỢ DỰA TRÊN NHU CẦU
```

#### 17.1. Người nhập cư

Hoàn thành Civil có thể tạo con đường mạnh tới:

- cư trú dài hạn;
- đủ điều kiện nhập tịch;
- hoặc một tuyến tăng tốc tương đương.

Baseline hiện tại:

```text
HOÀN THÀNH CIVIL
→ quyền được xét theo tuyến cư trú / nhập tịch mạnh
```

Không dùng review cuối để trì hoãn vô hạn một người đã đáp ứng điều kiện.

Exact việc là cư trú trước rồi nhập tịch, hay có trường hợp đi thẳng tới eligibility nhập tịch, còn `UNKNOWN`.

#### 17.2. Citizen nghèo hoặc homeless

Gói hậu Civil thiên về:

- nhà ở chuyển tiếp;
- tiền tích lũy;
- đào tạo;
- chứng nhận;
- hỗ trợ việc làm;
- tái lập khả năng sống độc lập.

Không giữ tax privilege vĩnh viễn như hệ cũ.

Nếu sau này có ưu đãi thuế, nó phải được thiết kế như hỗ trợ tái hòa nhập có phạm vi và thời hạn rõ.

#### 17.3. Citizen tự nguyện muốn thử thách bản thân

Họ vẫn được:

- upkeep trong thời gian service;
- tiền công;
- đào tạo;
- chứng nhận;
- thành quả phục vụ;
- completion bonus phù hợp.

Nhưng hỗ trợ dựa trên nhu cầu sau Civil có thể thấp hơn người thật sự không có nền tảng sinh hoạt.

---

### 18. Công quyền trung lập tuyệt đối

Cơ quan công quyền phải trung lập tuyệt đối trong đối xử với class, nghề, tình trạng kinh tế hoặc nguồn gốc xã hội.

```text
CLASS / STATUS / NGHỀ / NGHÈO GIÀU
!=
LÝ DO ĐỂ NHẬN THỦ TỤC KÉM HƠN
!=
LÝ DO ĐỂ ĐƯỢC BẢO VỆ KÉM HƠN
!=
LÝ DO ĐỂ CƠ QUAN CÔNG QUYỀN HẠ THẤP CÁ NHÂN
```

Civil được công quyền đối xử như Citizen trong:

- thủ tục;
- bảo vệ pháp luật;
- xử lý hành chính;
- tiếp cận các dịch vụ công áp dụng;
- chuẩn tôn trọng nhân phẩm;
- chuẩn công bằng thủ tục.

```text
CIVIL
→ CÔNG QUYỀN ĐỐI XỬ NHƯ CITIZEN
```

Điều này không tự xác lập rằng Civil và Citizen có mọi quyền chính trị, nhập cư hoặc nghĩa vụ giống hệt nhau.

Khác biệt hợp lệ của Civil phải xuất phát từ chế độ phục vụ mà họ đã tham gia, không phải từ quan niệm rằng Civil là người thấp hơn.

Cơ quan công quyền không được tạo stigma, humiliation hoặc caste distinction cho Civil.

---

### 19. Civil không bảo đảm thành công đời đời

Hoàn thành Civil cho một nền tảng để tự đứng, không phải bảo hiểm chống mọi thất bại tương lai.

Former Civil vẫn có thể:

- thất nghiệp;
- phá sản;
- tiêu hết tiền;
- mất nhà;
- gặp biến cố;
- thất bại trên thị trường lao động.

Việc một người có được quay lại Civil lần nữa hay không vẫn `UNKNOWN`.

Không mặc định Civil là nút reset vô hạn.

---

### 20. Quan hệ với Undie

Civil và Undie là hai miền độc lập.

```text
CIVIL
= chế độ phục vụ lao động và bảo đảm sinh hoạt

UNDIE
= hệ sinh thái nghề nghiệp
```

Không còn:

- Civil → Undie như chuyển địa vị;
- ưu đãi phí Undie mặc định cho Civil;
- framing Civil và Undie như hai tầng fallback tương đương;
- dùng Undie để giải thích stigma, quyền hoặc exit của Civil.

Nếu một Civil đồng thời tham gia một nhánh nghề Undie, điều đó phải được xét như một quan hệ nghề độc lập và không làm mất nghĩa vụ Civil.

Exact compatibility còn `UNKNOWN`.

---

### 21. Những phần Civil cũ bị supersede

Không dùng làm baseline hiện hành:

- `Civil Slave`;
- Civil thuộc `Slave` umbrella;
- Civil là tầng thấp hơn Citizen;
- Brown như dấu status bắt buộc của Civil;
- vào Civil là “xuống” một tầng xã hội;
- stigma nhà nước đối với Civil;
- luật bảo vệ danh dự đặc biệt để bù cho stigma do hệ thống tạo;
- `Citizen → Civil → Citizen` như ontology duy nhất;
- Citizen là nguồn vào duy nhất;
- billet phải được subject chọn và chấp nhận theo sở thích trước admission;
- quyền từ chối assignment chỉ vì không thích;
- `5 năm review / 10 năm tự động Citizen` như universal lifecycle;
- ưu đãi phí Undie;
- former-Civil tax privilege vĩnh viễn;
- Civil và Undie như hai fallback cùng ontology;
- homelessness → Civil như một hình phạt hoặc hạ status;
- kỷ luật Civil bằng hạ class;
- upkeep biến thành nợ giữ người;
- failure trong Civil tự động dẫn tới Criminal;
- mọi cơ chế khác chỉ có lý do tồn tại vì kiến trúc Slave–Undie cũ.

---

### 22. Những điểm còn UNKNOWN

Chưa tự điền các mục sau:

- tên pháp lý/chính thức cuối cùng của Civil nếu sau này cần đổi;
- cơ quan xét tuyển;
- exact eligibility;
- tiêu chuẩn sức khỏe/thể lực/kỹ năng;
- mức screening an ninh;
- matching algorithm;
- quy tắc ưu tiên khi nhiều assignment cùng phù hợp;
- exact manpower envelope;
- exact thời hạn tối thiểu;
- cách tính tiến độ hoàn thành;
- trọng số giữa assignment thông thường / khó tuyển / cực khó hoặc chiến lược;
- lương cụ thể;
- mức upkeep;
- chuẩn nhà ở;
- full labor code;
- ngày nghỉ và thời giờ làm;
- exact medical coverage;
- full appeal procedure;
- full discipline ladder;
- giới hạn kéo dài service;
- early-exit notice;
- family accompaniment;
- dependent support;
- school cho con;
- spouse employment;
- exact immigration / residency / citizenship pathway;
- exact completion bonus;
- exact reintegration package;
- former-Civil tax support nếu có;
- Civil re-entry;
- compatibility với Undie profession;
- các trường hợp đặc biệt khác chưa được tác giả chốt.

`UNKNOWN` không cho phép phục hồi hệ Civil cũ.

---

### 23. Hạt nhân chống drift

```text
CIVIL KHÔNG PHẢI SLAVE.

CIVIL KHÔNG PHẢI HÌNH PHẠT.

CIVIL KHÔNG PHẢI MỘT TẦNG NGƯỜI THẤP HƠN.

CIVIL LÀ CHẾ ĐỘ PHỤC VỤ LAO ĐỘNG TỰ NGUYỆN Ở ĐẦU VÀO.

QUYỀN ĐĂNG KÝ != QUYỀN ĐƯỢC NHẬN.

SAU KHI ĐƯỢC NHẬN, ASSIGNMENT HỢP LỆ LÀ NGHĨA VỤ.

PHÂN CÔNG DỰA TRÊN NHU CẦU + NĂNG LỰC + THỂ LỰC + ĐIỀU KIỆN HỢP LỆ.

PREFERENCE != QUYỀN VETO.

KHÔNG THỂ LÀM != KHÔNG MUỐN LÀM != PHẠM TỘI.

BẢO ĐẢM SINH HOẠT != TIỀN CÔNG.

UPKEEP != NỢ GIỮ NGƯỜI.

THẤT BẠI TRONG CIVIL != TỰ ĐỘNG TRỞ THÀNH CRIMINAL.

RỜI SỚM CÓ THỂ HỢP PHÁP, NHƯNG MẤT QUYỀN LỢI CHƯA KIẾM ĐƯỢC.

HOÀN THÀNH CIVIL → NỀN TẢNG TỰ LẬP, KHÔNG PHẢI GIÀU CÓ BẢO ĐẢM.

CÙNG NGHĨA VỤ PHỤC VỤ != MỌI GÓI HỖ TRỢ HẬU CIVIL PHẢI GIỐNG NHAU.

TIỀN CÔNG LAO ĐỘNG != HỖ TRỢ DỰA TRÊN NHU CẦU.

CƠ QUAN CÔNG QUYỀN PHẢI TRUNG LẬP.

CIVIL ĐƯỢC CÔNG QUYỀN ĐỐI XỬ NHƯ CITIZEN.

CIVIL != UNDIE.

THIẾU CHI TIẾT MỚI != QUYỀN PHỤC HỒI HỆ CŨ.
```

---

### 24. Trạng thái thiết kế sau baseline này

Baseline hiện đã đủ để tiếp tục thiết kế mà không cần dựa vào ontology Slave–Undie cũ.

Các trục nên được xử lý tiếp từ baseline này, không từ lịch sử cũ:

1. vòng xét tuyển và điều kiện đủ;
2. cơ quan Civil và ranh giới thẩm quyền;
3. phân công và matching;
4. lương, upkeep và nhà ở;
5. thời hạn phục vụ và completion;
6. kỷ luật, appeal và early exit;
7. gói hậu Civil;
8. immigration / residency / citizenship;
9. family/dependent rules;
10. re-entry và chống lợi dụng hệ thống.

Không trục nào ở trên được tự điền bằng cơ chế Civil cũ nếu chưa có quyết định canon mới.

---

## Part III — Current cross-status and labor canon

> Imported once from the revamp anchor; Undie-specialized sections are located in the sibling Undie file.

### 0. Nguyên tắc đọc

Các distinction bắt buộc:

```text
SOCIAL HIERARCHY
≠ LEGAL STATUS
≠ CLASS
≠ OCCUPATION
≠ CAREER RANK
≠ AUTHORITY
≠ ASSET VALUE
```

Một actor có thể ở địa vị xã hội thấp nhưng có asset value rất cao, hoặc có backend quản trị như Slave nhưng frontend xã hội rất cao.

---

---

### 1. Thứ bậc xã hội chính thức

Thứ bậc ngoài phạm vi Civil giữ ở Part I §1A. Civil không Slave/caste/tầng người thấp; công quyền đối xử như Citizen trong thủ tục/pháp luật/dịch vụ áp dụng, không tự đồng nhất citizenship hoặc mọi quyền chính trị. Undie không là caste.

---

### 2. Civil và hoạt động nghề Undie

Civil→Undie như chuyển địa vị một chiều đã nghỉ hưu. Gia nhập nghề không tự đổi citizenship hoặc chấm dứt Civil service/assignment; điều kiện làm nghề bên cạnh nghĩa vụ Civil còn mở.

---

### 5. Yellow

Citizen vi phạm lần đầu→Yellow một tuần→Citizen là chế tài tạm thời đã chốt. Yellow→Red/Undie, quota nghề ×2 và Undi làm dấu trừng phạt không còn là mốc mặc định. Trang phục Yellow và chế tài tái phạm cần quyết định riêng; không suy Yellow đã bị xóa.

---

### 6. POW

**CANON**

POW có hai lớp:

```text
FRONTEND / SOCIAL:
POW = Sĩ quan quân đội

BACKEND / ADMIN:
POW = Slave category
```

POW:

- làm việc theo điều phối;
- quản lý bằng collar như Slave thường;
- nhưng frontend ngang sĩ quan quân đội.

```text
backend Slave
≠ social inferiority
```

---

---

### 7. Civil, quyền cá nhân và hoàn thành

Part II §§6–18 kiểm soát assignment/nghĩa vụ, labor protection, tài sản/tiền/hôn nhân/nghỉ/liên lạc và public neutrality. Không giữ phạt nhục mạ Civil ×2 như luật đặc biệt bù stigma; cơ chế chế tài độc lập chưa được chốt lại.

Mốc 5y review/10y tự động Citizen và tax privilege vĩnh viễn nghỉ hưu. Civil service không tự biến mọi Citizen thành non-Citizen rồi đổi lại. Người nhập cư hoàn thành có tuyến được xét mạnh, exact pathway UNKNOWN.

---

### 14. Người hành nghề Undie vi phạm pháp luật

Undie không phải class hoặc địa vị pháp lý. Không tự duy trì hệ tư pháp/kỷ luật riêng thay luật thường chỉ vì nghề. Hành vi, địa vị thực, luật nghề/hợp đồng và cơ quan có thẩm quyền phải được xác định trong đúng phạm vi; ma trận chế tài còn mở.

---

### 15. Criminal

**CANON**

Criminal là Slave class.

Nguồn vào:

```text
đối diện án tử
→ thỏa thuận nhận tội
→ tránh tử hình
→ Criminal Slave
```

Criminal làm các việc cực thấp mà robot còn “chê”, ví dụ:

- rác thải sinh hoạt;
- vệ sinh bệnh viện;
- vệ sinh cống rãnh;
- các việc tương tự bẩn/nguy hiểm/không đáng dùng robot.

Criminal vẫn có quyền cơ bản. So sánh điều kiện sống với một lớp Undie thấp hơn Civil đã bị supersede; không tự tạo chuẩn sống mới cho người hành nghề.

Không tha bổng.

Không tự suy `không tha bổng = không kháng cáo / không tái thẩm`.

---

---

### 28. Bailout — correction

**CANON / SUPERSEDE**

Ngoại lệ loại trừ Undie theo class cũ đã bị supersede. Quy tắc Citizen bên dưới giữ nguyên; không tự chốt ma trận áp dụng mới theo nghề hoặc mọi nhánh dịch vụ.

**Giao diện chưa đối chiếu xong:** chuẩn công quyền trung lập theo Part II §18 không tự giải quyết quan hệ tiền/financial liability với phân loại dân sự/Criminal ở đoạn dưới. AF-CR-OPEN-006 trong `92` giữ câu hỏi; không dùng đó để chứng minh poor people được inferior protection hợp lệ hoặc tự xóa bailout law.

Nó áp dụng cho **Citizen từ Thượng lưu trở xuống**.

```text
Citizen từ Thượng lưu trở xuống
→ bailout rất nặng
→ tối đa 2 lần
→ sau đó phải ra tòa
```

Tại tòa:

```text
có tiền
→ xử như dân sự

không có tiền
→ nguy cơ xuống Criminal rất cao
```

Core design:

```text
cho phép hành vi rủi ro
→ Citizen tự chịu trách nhiệm
→ vi phạm tạo legal trigger
→ fine / bailout / civil liability
→ extraction
```

Không dùng tư cách nghề Undie để thay quy tắc theo địa vị pháp lý; xem mục 14 về phần triển khai chưa chốt.

---

---

### 29. Bia rượu

**CANON**

Không giới hạn độ tuổi uống bia rượu.

Triết lý:

```text
Citizen
→ tự ý thức
→ tự chịu trách nhiệm hành vi
```

AetherFire cố ý không chặn quá nhiều ở đầu vào, nhưng phạt nặng ở downstream behavior.

Ví dụ:

- sàm sỡ cư dân Hoa Nguyệt;
- vận động tay chân/bạo lực với Undie.

---

---

### 32. Citizen career system

**CANON**

Citizen có:

- nghề riêng;
- promotion riêng;
- career progression riêng.

Citizen có thể đồng thời là người hành nghề Undie. White→Citizen đã nghỉ hưu; không có career class mới được tạo từ việc rời nghề.

---

---

### 33. Quyền lợi hậu Civil

Completion tạo gói giúp tự lập, có thể khác theo nhu cầu/đầu vào. Không giữ tax exemption/reduction vĩnh viễn và tax-arbitrage Citizen→Civil→Citizen. Ưu đãi thuế tương lai nếu có phải có scope/thời hạn và được chốt riêng.

---

### 35. Citizen và Undie

Citizen có thể gia nhập nghề Undie mà không mất citizenship/legal status. Quyền rời nghề và hậu quả hợp đồng/tài chính truy nguyên được do `13` kiểm soát; không còn one-way status entry hoặc White exit.

---

### 36. Citizen có thể thất bại kinh tế

**CANON**

Citizen status không bảo đảm:

- có việc;
- không nợ;
- không bị xiết nợ;
- không bị nợ gia đình;
- không có bad credit;
- không bị giảm khả năng tìm việc do credit status/vay xấu.

Có thể hình thành vòng:

```text
thất nghiệp / nợ
→ credit profile xấu
→ cơ hội việc làm giảm
→ thu nhập giảm
→ credit profile tiếp tục xấu
```

---

---

### 37. Civil và thị trường lao động

Civil vừa phục vụ nhu cầu ổn định cá nhân vừa giảm biến động nhân lực AF. Không phải welfare thụ động, cheap labor định nghĩa sẵn hoặc cơ chế giảm prestige. Undie là nghề độc lập; không là fallback chuyển địa vị tương đương Civil.

### 41. Dịch vụ Undie

Civil có thể sử dụng dịch vụ nhưng **không còn preferential fee mặc định** theo Civil status. Compatibility làm nghề Undie vẫn UNKNOWN; không mất nghĩa vụ service chỉ vì quan hệ nghề.

### 42. Vô gia cư và đầu vào Civil

Người vô gia cư có thể tự nguyện ứng tuyển Civil, không tự được nhận và không bị phạt bằng admission/hạ status. Không giữ binary homeless→Civil Slave hoặc trục xuất như hai route duy nhất. Quy tắc xử lý khi từ chối/không đủ điều kiện/capacity, trợ giúp ngoài Civil và pháp luật trục xuất độc lập còn UNKNOWN; không khẳng định mọi người vô gia cư đều được Civil hấp thụ.

Chính sách/khẩu hiệu không có homeless population ổn định trong hồ sơ cũ không chứng minh hệ mới đã đạt zero homelessness. Không viết thêm route trợ cấp, nhập cư hoặc hình phạt để lấp gap.

---

### 42A. Disability và debt

**CANON**

Disability làm mất khả năng hoạt động được xử lý bằng magic + technology hybrid.

```text
disability
→ hybrid treatment
→ phục hồi khả năng hoạt động
→ phát sinh debt
```

Do đó:

```text
social problem visibility ↓
individual economic obligation ↑
```

AetherFire có thể tuyên truyền rằng:

- không có người vô gia cư;
- không ai bị bỏ mặc vì khuyết tật;

trong khi cost được chuyển thành debt/status/economic obligation.

---

---

### 43. Core exploitation design — phạm vi còn hiệu lực

AetherFire có thể giữ tự do/lựa chọn rủi ro→trách nhiệm cá nhân→legal/economic trigger→fine/bailout/debt trong các miền còn hiệu lực, ví dụ tuổi uống rượu/bailout. Civil không phải punishment/status extraction hoặc lao động trả nợ; upkeep bảo đảm không thành khoản giữ người.

Không dùng Undi để tạo nhầm lẫn/hạ nhục rồi phạt như mục đích mặc định, hoặc dùng nghề Undie làm một engine kiểm soát Slave. Nợ, thị trường, patronage và lạm dụng có thể tạo hậu quả khi có cơ chế riêng; retcon không khẳng định mọi bóc lột đã biến mất.

---

### 44. Địa vị và nghề là hai quan hệ khác nhau

```text
eligible applicant → voluntary application + admission screening/capacity → Civil service
Civil → lawful early exit hoặc minimum time + qualified service → exit
citizenship / residency / completion benefits → theo đầu vào và luật áp dụng, không automatic conversion
Citizen → first offense → Yellow một tuần → Citizen
death-sentence exposure → plea → Criminal
```

Citizen từ Thượng lưu trở xuống vẫn có bailout tối đa hai lần→tòa→nguy cơ Criminal khi không có tiền, trong phạm vi đã chốt.

```text
Citizen + nghề Undie
gia nhập/rời nghề Undie ≠ legal-status transition
```

Chế tài tái phạm Yellow và điều kiện nghề cho Civil/Criminal còn mở; không nối lại đồ thị cũ.

---

### 46. UNKNOWN bắt buộc giữ

- Full hierarchy/progression của nghề Citizen; promotion formula.
- Thời hạn/công thức completion Civil, authority/eligibility/assignment/exit/family/residency; support thuế tương lai nếu có. Không giữ year-5 review hoặc vĩnh viễn tax privilege.
- Criminal rights/labor matrix, bailout amount và court procedure.
- Yellow repeat timing, chế tài mới và trang phục.
- Nghề/giấy phép/hợp đồng/access Undie mới, tương thích nghĩa vụ Civil và eligibility Criminal.
- Luật hồ sơ, kế vị/tước vị riêng không suy từ nghề.
- Medical debt terms ngoài upkeep Civil; disability không chữa được bằng hybrid treatment. Điều kiện pháp lý trục xuất, xử lý vô gia cư không được nhận Civil và hỗ trợ độc lập chưa chốt; không dùng binary cũ.
- Public-content moderation, staff/emergency exceptions của khu ăn chơi và các triển khai dịch vụ ngoài phần đã chốt.
- Các nhóm unknown Undie mới nằm ở `13` §17 và `92`; không giữ threshold/rank/status collateral cũ như kiến trúc hiện hành.

---

### 47. Tóm tắt ranh giới hiện hành

Civil là service tự nguyện ở đầu vào, không Slave/caste/punishment. Được nhận rồi có assignment phù hợp bắt buộc, upkeep + pay, appeal/early exit/completion, public neutrality và quyền cá nhân; exact thời hạn/benefits/immigration còn mở. Citizenship không tự đổi. POW frontend ngang sĩ quan/backend Slave security; Criminal giữ pipeline/quyền độc lập.

Undie = nghề/hệ sinh thái, không phải Slave/caste/punishment. Citizen + Undie có thể đồng thời; entry/exit không đổi địa vị. Không còn đồ thị màu, White→Citizen, Yellow→Red/Undie, triệt sản bắt buộc hoặc web tín dụng thế chấp người.

Cash + Credits được nhà nước bảo chứng; nợ ≠ sở hữu người ≠ tự động dịch vụ tình dục. Hồ sơ tín dụng Citizen ngoài phạm vi không bị xóa; cơ chế Civil nay theo Part II, không dùng nợ để giữ người hoặc trả upkeep.

Undi là họ đồng phục nghề theo ngữ cảnh; Hoa Nguyệt appropriation có ý định thật nhưng không được người ngoài chứng minh chắc chắn. Tử vong, nghề, an ninh và MC2 theo mốc `13` mới; chưa tự viết các triển khai còn mở.

Ưu đãi phí Civil đã nghỉ hưu. Luật tuổi uống rượu và hybrid disability treatment/debt độc lập giữ trong scope cũ, không áp debt vào basic upkeep Civil. Không dùng homelessness để phục hồi coercive intake hoặc caste.

---

## Part IV — Giao diện phân công còn hiệu lực và ranh giới nguồn

Các cơ chế vận hành tiền nhiệm **không phụ thuộc Civil Slave hoặc mốc 5–10 năm** được giữ trong phạm vi tương thích, không dựng lại admission gate cũ:

- Nguồn việc/phân công là pool toàn AetherFire, gồm thủ đô, đô thị vệ tinh, thuộc địa và điểm triển khai khác; không suy chỉ local market.
- Phân công cụ thể có công việc, địa điểm, đơn vị tiếp nhận, thời điểm bắt đầu và điều kiện triển khai cần thiết. Không dùng danh mục này để buộc applicant phải chọn/chấp nhận một billet theo sở thích trước admission; exact admission/matching còn mở.
- Demand từ cơ quan sử dụng lao động và allocation của hệ Civil là thẩm quyền khác nhau; Civil authority không tự tạo nhu cầu để phình hệ. Cơ quan/tổ chức và quyền hạn cụ thể chưa chốt.
- Placement kết thúc không mặc định biến Civil thành unemployed welfare recipient; có reserve/transitional duty và reassignment phù hợp. Đây là trạng thái vận hành, không status/class Slave. Catalogue, duration, giới hạn điều động và thủ tục còn UNKNOWN.
- Relocation cần cho assignment hợp lệ thuộc trách nhiệm bảo đảm triển khai của Civil; exact reimbursement/housing/family chưa chốt.
- Có thể vận hành giới hạn nhân lực được phê chuẩn; exact manpower envelope, công thức, thẩm quyền và chu kỳ đều UNKNOWN. Không suy vô hạn capacity hoặc mặc định mọi applicant được nhận.

Ranh giới mới ở Part II kiểm soát quyền khiếu nại, rời sớm, pay/upkeep và hậu service. Những assertion cũ billet phải do applicant chọn/chấp nhận trước admission, Slave conversion, hết service tự Citizen, guaranteed tax/fee ưu đãi và humiliation identification không còn hiệu lực.

Nguồn cũ và các nhãn CURRENT ở hồ sơ lịch sử chỉ mang giá trị thời điểm. `91` ghi AF-CR-001–012, `92` giữ AF-CR-OPEN-001–007 và các mục được cụ thể hóa một phần. Không đọc Source_Archive để tái dựng baseline.
