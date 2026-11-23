# Hồ sơ nguồn và đường đi của từng số liệu

Các ngày và ngưỡng trong hồ sơ dự án dùng làm đầu vào. Số ngày lệch, tỷ lệ tài trợ, trạng thái nghiệm thu và độ nhạy thứ hạng là phép tính của người viết. Phiếu ngày 23/11/2026 đo một bài tập quản lý của hai người. Số tiền, ngày bàn giao và KPI lịch sử của FAME thuộc phạm vi khác.

| Câu hỏi | Bản ghi dùng để chạy | Cách quay lại nguồn độc lập |
|---|---|---|
| Giao đúng hạn? | [Năm cặp ngày](deliverables.csv), đối chiếu hai trường Baseline Finish và Actual Finish trong [MS Project XML](../FAME_Lich_MS_Project.xml) | Cột URL dẫn tới bìa đúng sản phẩm. D6.4 có thêm ngày sang phản biện tại [lịch sử v0.6](https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D6.4-Use-Cases-Specification-and-Pilot-Sites-Preparation.-II.pdf#page=2). Mã UID dùng để định vị, tên sản phẩm được kiểm tra riêng. |
| Mốc thuộc kỳ nào? | Hai ngày RP2 trong [hồ sơ CORDIS](cordis.json) và dòng 24–26 của XML | Kỳ 2 trong [báo cáo định kỳ](https://cordis.europa.eu/project/id/101092639/reporting). RP2 là khoảng báo cáo. |
| Ai tài trợ? | Mỗi hàng tài chính trong JSON lần lượt ghi tên, tổng chi phí và đóng góp EU bằng EUR. Dòng đầu là toàn dự án, bốn dòng tiếp theo là bốn tổ chức được chọn | Tra trường Total cost và EU contribution ở đầu [hồ sơ CORDIS](https://cordis.europa.eu/project/id/101092639), trường Net EU contribution ở từng tổ chức. Các tổ chức được chọn đã nằm trong tổng dự án. |
| Mục tiêu và kết quả Pilot 5? | Các dòng 5–10, trang Nguon_KPI của [sổ nghiệm thu](../FAME_Nghiem_thu_6_KPI.xlsx). Số phần trăm lưu dưới dạng tỷ lệ 0–1. Cột M là đánh giá tính so sánh của người viết | [D6.4 Bảng 43](https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D6.4-Use-Cases-Specification-and-Pilot-Sites-Preparation.-II.pdf#page=69) công bố mục tiêu. [D6.3 Bảng 5](https://www.fame-horizon.eu/wp-content/uploads/2025/05/FAME-D6.3-Techno-Economic-Evaluation-and-Stakeholders-Feedback.pdf#page=52) ghi kết quả. Liên kết đến trang PDF đúng cho từng KPI nằm trong [bảng kết quả](../results/ket-qua.md). |
| Checklist thay đổi hồ sơ thế nào? | Ho_so_A ghi nhận xét trước can thiệp và quyết định được mã hóa. Checklist_B lưu đầu mối đề xuất và gói bằng chứng. Python tự tính quyết định B, đối chiếu ô kết quả Excel | Cùng sáu hồ sơ và tham chiếu tài liệu ở hai lượt. Tham chiếu do người viết xây dựng. Vai trò đề xuất chưa chứng minh có người nhận việc. |
| Người chấm thực sự chọn gì? | [Bảng tổng hợp công khai](../Cham_doc_lap/Ket_qua/Tong_hop_A_B.xlsx) giữ hai nhóm A và B, mỗi nhóm sáu lượt. Mã tính lại trung bình và tỷ lệ khớp từ tổng | Hai phiếu HTML gốc ghi nhật ký cục bộ. Điều phối viên có thể chạy lại đối chiếu bằng `--reviews-dir`. Trung vị là thống kê đầu vào khi chỉ có bản tổng hợp; khi có CSV, mã tính lại trung vị từ từng lượt. |
| Điểm ESG có tái tạo được? | Bản [Zenodo v1](https://zenodo.org/records/17175084), metadata và 12 CSV. Đường dẫn tải nằm trong mã. [Kiểm tra cấu trúc](esg_audit.json) và [kiểm tra từng trụ cột](../esg-data-audit/reproduction.json) là bản kết quả đã lưu | Lệnh tải kiểm tra DOI, tên tệp, kích thước, MD5 của các CSV. Lệnh chạy phân tích mới đọc E/S/G gốc sau bước xác minh. Hai báo cáo PDF của bản Zenodo là tài liệu tham khảo. |

### Cách xác minh một nhận định

Với “D6.4 trễ 143 ngày”, mở bìa từ CSV, đối chiếu 30/09/2024 và 20/02/2025, tìm UID 17 trong XML, rồi đọc trường `variance_days` ở kết quả. Cả phép trừ và việc chọn đúng sản phẩm đều được kiểm tra. Với “hài lòng đạt mục tiêu”, tra ngưỡng ở trang PDF 70 của D6.4, đọc số đo ở trang PDF 53 của D6.3 và kiểm tra đơn vị điểm/5 ở hàng K02.

Với “hai người chấm đều duyệt”, bằng chứng công khai ở mức nhóm. Sổ chi tiết có hai mốc UTC cho mỗi thao tác và được giữ tại nơi điều phối. Cách phân phối phiếu chứng minh điều kiện A/B đã được thiết kế. Việc người tham gia thực sự đọc từng nguồn hoặc sử dụng từng câu gợi ý vẫn chưa được đo.

### Khi bằng chứng thay đổi

Một phiên bản đặc tả mới có thể thay mục tiêu nhưng vẫn giữ tên KPI cũ. Khi đó cần lấy cả kết quả của đúng kỳ, ghi lại phiên bản nguồn rồi chạy kiểm tra. Nếu ngưỡng thay đổi sau buổi chấm, giữ lại tham chiếu của buổi cũ để giải thích quyết định tại thời điểm đó. Bất đồng giữa lịch và bìa, checksum sai hoặc thay đổi nhãn trong sổ tổng hợp đều khiến lệnh kiểm tra dừng trước khi công bố kết quả mới.

## Ma trận nghiệm thu 65 KPI

[Ma trận Excel](../FAME_Ma_tran_65_KPI.xlsx) có hai trang tính. **Tong hop** đếm kết luận theo pilot bằng công thức, **Ma tran** cho lọc theo pilot và trạng thái. Bấm các ô nguồn để mở trang PDF, tính từ bìa. Khoảng trang được ghi khi dòng tiếp tục sang trang kế tiếp. [CSV nguồn](kpi_matrix.csv) là dữ liệu biên tập dùng để dựng cả Excel và Phụ lục G.

Mục tiêu lấy từ D6.4 bản 1.0, bảng 11, 25, 31, 35, 43, 49 và 56. Kết quả lấy từ D6.3 bản 3.0, bảng 1–7. Cột kỳ đo ghi giai đoạn đánh giá được nêu trong hồ sơ. P2 có kỳ 6–12/2025, P4 có kỳ 7–11/2025 và P5 có kỳ 4–12/2025. Bốn pilot còn lại chỉ gắn với pha 2 khi trang phương pháp không nêu khoảng ngày riêng cho KPI. Các số đếm có đơn vị thời gian như phiên/tuần hay lợi ích/năm giữ đơn vị đó ở cột mục tiêu.

Người viết gán bốn kết luận theo bằng chứng công bố. **Đạt** khi số đo hoặc sản phẩm được xác định đủ để đáp ứng tiêu chí. **Không đạt** khi số đo hụt đích hoặc dự án xác nhận dưới ngưỡng. **Thiếu bằng chứng** khi thiếu một vế của yêu cầu, thiếu mẫu số, hoặc đầu ra được đo bằng chỉ báo khác. **Không áp dụng theo FAME** chỉ xuất hiện khi phép thử chưa diễn ra vì điều kiện đầu vào vắng mặt và FAME ghi N/A. Giá trị NA ở kết quả giao dịch của Pilot 7 được giữ thiếu bằng chứng. Các kết luận là của người viết, phục vụ đánh giá hồ sơ công khai.

Mã `P5-01` đến `P5-23` cho phép tìm một dòng trong toàn danh mục Pilot 5. Sáu dòng có thêm `legacy_id` nối đúng phiếu cũ. Ví dụ, P5-21 là K01 (thời gian lập báo cáo). Buổi hai người chấm chỉ bao phủ sáu KPI đó.

```bash
python -m pip install -r report/requirements.txt
python -m fame_pm.kpi_matrix
python -m fame_pm.portfolio --data-dir du_lieu/portfolio --download --check
python -m fame_pm.kpi_matrix --source-dir du_lieu/portfolio
```

Lệnh đầu sau khi cài thư viện kiểm tra số dòng, sáu mã đối chiếu, giá trị giữa CSV và Excel, liên kết và tổng theo pilot. Chế độ có PDF xác thực dấu SHA-256 của ba tài liệu, định vị tên từng KPI trên trang bắt đầu và kiểm tra ngữ cảnh nguồn kỳ đo. Việc đọc, chuyển ngữ và đánh giá nội dung của từng dòng do người viết thực hiện.
