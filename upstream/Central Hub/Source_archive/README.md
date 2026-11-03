# Lưu nguồn lịch sử của migration

ARCHIVE != RUNTIME SOURCE

ARCHIVE != FALLBACK

ARCHIVE != LATEST VERSION

ARCHIVE PRESENCE != ACTIVATION

Chỉ dùng để xem lịch sử, đối chiếu, audit hoặc rollback có đích do người dùng chỉ định. Không router/control nào được tự đọc archive để bù nguồn thiếu, tự phục hồi hoặc chọn bản mới nhất. Chỉ đọc về governance; không sửa bytes đã lưu nếu chưa có chỉ dẫn rõ.

Migration giữ toàn bộ bytes của ba cây nguồn cũ. Các thư mục archive cũ được đặt tên `historical_sources` bên trong lịch sử để toàn Hub có một root Source_archive. Mapping đường dẫn cũ, đích và SHA-256 nằm trong `ARCHIVE_RECEIPT.json`; receipt là bằng chứng tệp, không phải registry hoặc authority runtime. Tài liệu cũ có thể chứa liên kết/metadata của kiến trúc đã nghỉ; không dùng chúng như chỉ dẫn hiện hành.

Nhóm `Central Hub legacy v1.0/` lưu CI/Router v1.0 và source TECHNICAL/CREATIVE/BRAINSTORM đã bị thay thế. Mapping/SHA-256 tại `HUB_LEGACY_ARCHIVE_RECEIPT_2026-10-19.json`; byte-exact, không còn là runtime source. Candidate snapshots và evidence records vẫn ở vị trí lịch sử riêng để kiểm thử/đối chiếu.
