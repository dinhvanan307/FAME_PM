# Tiêu chí khóa trước lượt nghiệm thu P5-V1

Ngày 25/11/2026, giờ Việt Nam. Đây là đợt tái kiểm của học phần do sinh viên giữ vai trò PM. Giả thuyết về chín mã và kết quả thăm dò đã được biết trước. Commit chứa văn bản này chốt quy tắc trước lượt chạy xác nhận. Lần kiểm sử dụng bản xuất v1 đã khảo sát.

## Đầu ra và quy tắc quyết định

* Bản nguồn có DOI 10.5281/zenodo.17175084. Đối chiếu tên, kích thước và MD5 của đủ 12 CSV với metadata Zenodo và bản kê đã lưu. Sai nguồn hoặc thiếu tệp thì dừng.
* Dòng 1 dùng để hiệu chuẩn. Chấm trên các dòng có vị trí 2–604, 100 mã và ba trụ E/S/G, tổng 180.900 ô. Ngưỡng cho mỗi ô là sai số tuyệt đối ≤ 10⁻⁸ điểm trước khi làm tròn. Thiếu một ô, ghép mơ hồ hoặc vượt ngưỡng thì giữ mở bàn giao kỹ thuật.
* Với từng mã, lấy điểm tổng hợp trừ giá trị điều chỉnh công bố ở dòng 1. Giữ cách ghép cũ nếu khớp duy nhất một trong tám ngành. Chỉ thử trung bình cộng tám ngành khi không khớp ngành nào và khớp duy nhất giá trị trung bình. Cố định cách chọn tham chiếu cho cả 603 dòng sau. Ở mỗi dòng sau, dự báo điểm trụ bằng điểm trụ gốc cộng điểm tổng hợp rồi trừ tham chiếu cùng dòng.
* Với mỗi mã ngoại lệ, yêu cầu đủ 1.809 ô E/S/G và 603 giá trị điều chỉnh tổng hợp khớp. Ghi riêng đối chứng giữ cố định tham chiếu ở dòng 1. Chỉ đóng ngoại lệ về tái tạo giá trị của v1. Việc xác nhận cách phân ngành hoặc thuật toán nội bộ thuộc tác giả.
* Ranh giới bàn giao gồm điểm E/S/G trên v1. P5-12 và P5-13 là hai yêu cầu riêng về giao diện và bộ tối ưu của FAME. Cả hai cần bằng chứng của bản chạy chính thức ở ít nhất năm mức. Lợi suất MS020 và hiệu quả làm việc của con người cần được kiểm chứng riêng.

## Sáu hồ sơ giao hai người chấm

| Mã | Câu hỏi cần quyết định |
|---|---|
| R1 | Có đủ 12 CSV đúng bản v1, khớp dung lượng và MD5? |
| R2 | Giữ tham chiếu cố định ở dòng 1 có đạt yêu cầu khớp toàn bộ ô E/S/G của chín mã? |
| R3 | Phương án dùng tham chiếu theo từng dòng có đáp ứng ngưỡng cho toàn bộ 180.900 ô? |
| R4 | Đã đủ bằng chứng giao diện chính thức hiển thị vector E/S/G ở ít nhất năm mức theo P5-12? |
| R5 | Từng mã trong chín ngoại lệ có đủ cả 1.809 ô trụ và 603 giá trị điều chỉnh tổng hợp đạt dung sai? |
| R6 | Đã đủ bằng chứng từ bộ tối ưu chính thức về khuyến nghị ở ít nhất năm mức theo P5-13? |

Mỗi người chấm cả sáu hồ sơ một lần, giữ kín phiếu đến khi trả cho PM. P1 làm A (R1, R2, R4) rồi B (R5, R6, R3). P2 làm B (R4, R1, R2) rồi A (R3, R5, R6). A dùng nguồn và tiêu chí. B bổ sung checklist về đúng nguồn, mẫu số và phạm vi của phép đo. Người chấm chọn Duyệt hoặc Không duyệt, ghi căn cứ, trang hoặc trường dữ liệu và hai thời điểm tĩnh đến giây cho từng hồ sơ. Khi không duyệt, nêu rõ số đo vi phạm hay bằng chứng còn thiếu.

PM chỉ tổng hợp khi nhận hai phiếu độc lập đủ 12 quyết định hợp lệ. Theo từng điều kiện A/B, đếm duyệt nhầm và từ chối nhầm với mẫu số tương ứng, so thời gian đọc đến chốt, đối chiếu sáu cặp quyết định. Hai người trong cùng điều kiện dữ liệu nhỏ chỉ cho kết quả mô tả. Nếu bất đồng, lưu nguyên hai phiếu, ghi căn cứ xử lý từng hồ sơ và quyết định riêng của PM. Khi chưa nhận phiếu, để trống thời gian, tỷ lệ và chữ ký.
