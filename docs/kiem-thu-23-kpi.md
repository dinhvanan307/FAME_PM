# Kiểm thử 23 KPI còn mở của FAME

Mốc trước khi chạy là commit [2ee5042](https://github.com/dinhvanan307/FAME_PM/commit/2ee504207ad4c5aae6f5b213d02503c11e0f0732). Người viết chạy được phép thử kỹ thuật, kiểm tra điều kiện dữ liệu hoặc đối chiếu số liệu công bố cho 13 hồ sơ. 10 hồ sơ còn lại cần bản ghi lịch sử để bắt đầu đo đúng chỉ tiêu. Cả 23 cần thêm bằng chứng để đóng. Hai người chấm độc lập trong bài chỉ chấm mẫu sáu KPI ban đầu. [Excel, trang Kiem thu 23 KPI](../FAME_Ma_tran_65_KPI.xlsx) · [Bên giữ hồ sơ, trường cần xin và quy tắc xét đủ 23 dòng](../evidence/open23_requests.csv)

| Công việc đã thực hiện | KPI | Kết quả và phạm vi có thể kết luận |
|---|---|---|
| Chạy hàm máy khách FDAC gốc | P3-04, P3-08 | Ba ví dụ nguyên bản trong OpenAPI đi qua hàm TypeScript gốc, với phản hồi danh mục mô phỏng bằng bộ nhớ. Kiểm tra nội dung yêu cầu và phản hồi trên cả ba. Số truy vấn thực tế của Pilot 3 và tính đúng của tìm kiếm liên miền vẫn cần log hoặc biên bản kiểm thử của pilot. |
| Đọc cấu hình do FAME phát hành | P3-02, P3-03, P3-09 | FDAC công bố 7 thao tác OpenAPI, 5 kiểu dữ liệu tìm kiếm và 3 hiện vật Kubernetes gồm Deployment, Ingress, Service. Deployment khai báo 1 replica. Phạm vi là FDAC chung; cần danh mục thành phần và kết quả chạy tải của Pilot 3. |
| Kiểm trên dữ liệu ESG gốc | P5-03, P5-09 | Có 60.400 ô điểm cấp cổ phiếu. Điểm ở dòng cuối nằm trong khoảng 52,66–76,40. Số tài sản được người dùng xem cần log hiển thị. Điểm trung bình danh mục cần tập danh mục, tỷ trọng và kỳ định giá. |
| Thử năm mức cho từng trụ E/S/G | P5-12, P5-13 | 15 cấu hình × 604 dòng × 100 mã. Mã của bài tự tính điểm và thứ hạng trên ba CSV gốc. Thiếu bản chạy của giao diện và bộ tối ưu KM Cube hoặc biên bản kiểm thử bản phát hành. |
| Kiểm khóa ghép tín hiệu và giá | P5-23 | Có 96 mã chung, 604 dòng tín hiệu và 1.443 dòng giá. Hai tệp thiếu cột ngày, tệp tín hiệu có 706 ô trống. Còn thiếu định danh riêng của tín hiệu tin tức, độ trễ và cửa sổ tính lợi suất. Hệ số được lưu là `null`. |
| Tính hoặc trích lại từ PDF của dự án | P3-01, P5-10, P4-02 | Xác nhận tên hai ca sử dụng. Với MS023 một năm, danh mục phối hợp hơn danh mục tối ưu Sharpe 8,4 điểm % lợi suất và có mức sụt giảm tối đa thấp hơn 4,1 điểm %. Chưa có phép đối sánh rủi ro và điểm ESG đáp ứng KPI. Số bản ghi Pilot 4 tăng từ 15 lên 33, còn thiếu tổng bản ghi theo từng nguồn. |
| Cần bản ghi lịch sử để đo KPI | P3-05, P3-10, P5-06, P5-07, P5-08, P2-03, P2-05, P4-06, P4-07, P7-02 | Phiếu từng dòng ghi bên giữ hồ sơ dự kiến, trường cần bổ sung và phép tính. Chẳng hạn P7-02 cần mã tài sản đã giao dịch trong kỳ. Hàm kiểm tra cảm biến của đối tác chạy lại thành công 279 ca biên trên 79 mã, nhưng đầu ra của hàm chỉ là chất lượng dữ liệu. |

Nguồn phần mềm, đặc tả và dữ liệu được ghim bằng SHA-256 hoặc bản phát hành Zenodo v1. FAME xuất bản gói FDAC dùng chung. D6.4 bảng 29 ghi dữ liệu JSON/TXT minh họa cho Pilot 3 trên SharePoint. D1.4 bảng 36 mô tả dịch vụ tối ưu KM/JRC có kiểm soát truy cập. Trong danh mục 14 tệp của bản Zenodo v1 có 12 CSV và 2 PDF. Dùng chính các tệp tải được làm căn cứ về khả năng tái chạy. [D6.4, trang PDF 44](https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D6.4-Use-Cases-Specification-and-Pilot-Sites-Preparation.-II.pdf#page=44) · [D1.4, trang PDF 58](https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D1.4-Data-Management-Plan-II.pdf#page=58) · [Zenodo v1](https://zenodo.org/records/17175084) · [Gói FDAC gốc](https://www.fame-horizon.eu/wp-content/uploads/2026/02/FDAC-Open-API.zip)

## Cách chạy lại

Cần Python với thư viện trong repo và Node.js 24. Từ thư mục gốc chạy:

```bash
python -m pip install -r report/requirements.txt
python -m fame_pm.kpi_review --source-dir du_lieu/portfolio --download
python esg-data-audit/reproduce_pilot5.py --data-dir du_lieu/zenodo --download
python -m fame_pm.open_kpi_runs --source-dir du_lieu/portfolio --data-dir du_lieu/zenodo --check
python -m fame_pm.kpi_matrix
```

Sau khi đã có dữ liệu, hai lệnh cuối chạy ngoại tuyến. Bỏ `--check` ở lệnh chạy thử để in JSON chi tiết cho từng cấu hình. Mã lấy nguyên tệp TypeScript từ ZIP đã đối chiếu checksum. Bộ thử chỉ thay tầng truyền dữ liệu để kiểm cách máy khách chuyển tiếp ba ví dụ gốc. [Bộ chạy](../fame_pm/open_kpi_runs.py) · [Phép thử hàm gốc](../fame_pm/fdac_replay.mjs) · [Kết quả đã lưu, gồm đủ 15 cấu hình](../results/open23_runs.json)

### Đọc thí nghiệm trọng số

Mỗi lượt chọn E, S hoặc G làm trụ thay đổi, gán 0%, 25%, 50%, 75% hoặc 100% và chia đều phần còn lại cho hai trụ kia. Ràng buộc tổng 100% khiến hai trụ còn lại cũng đổi. Với mỗi dòng, người viết tính điểm có trọng số rồi so thành phần top 5 với cấu hình ba trụ bằng nhau. Đồng điểm được xếp theo mã tăng dần. Trong 604 dòng có 3 bộ điểm phân biệt trên toàn bộ 100 mã, nên số dòng thay đổi mô tả đúng bản xuất này. Bản xuất thiếu khóa ngày để diễn giải đây là số ngày giao dịch độc lập.

| Trọng số trụ được chọn | Đổi thành phần top 5 khi thay E | Khi thay S | Khi thay G |
|---:|---:|---:|---:|
| 0% | 604 | 353 | 39 |
| 25% | 604 | 39 | 39 |
| 50% | 39 | 604 | 604 |
| 75% | 353 | 604 | 604 |
| 100% | 353 | 604 | 604 |

Đơn vị mỗi ô là số dòng trong 604 dòng. Thí nghiệm đo độ nhạy của danh sách cổ phiếu theo công thức do người viết triển khai. Để chốt P5-12 và P5-13, cần chạy cùng các mức trên đúng bản công cụ FAME và lưu cấu hình được chấp nhận, vector hiển thị và khuyến nghị đầu ra.
