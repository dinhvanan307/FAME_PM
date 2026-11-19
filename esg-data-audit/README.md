# FAME ESG Data Quality Audit

Kiểm tra liệu hai tệp điểm ESG và tín hiệu MarketSenseAI do dự án FAME công bố có đủ khóa để ghép theo **mã cổ phiếu và ngày giao dịch**. Đây là phân tích độc lập phục vụ bài học quản lý dự án. Mã kiểm tra và phép đếm do người viết thực hiện.

## Kết quả chạy trên bản dữ liệu đã phát hành

| Nội dung kiểm tra | Điểm ESG tổng hợp | Tín hiệu AI hằng ngày |
|---|---:|---:|
| Số dòng dữ liệu, đã loại hàng tiêu đề | 604 | 604 |
| Số mã cổ phiếu khác nhau trong tiêu đề | 100 | 96 |
| Số cột ngoài các mã cổ phiếu | 0 | 0 |
| Số ô trống hoặc chỉ chứa khoảng trắng | 0 | 706 |

**96 mã cổ phiếu** xuất hiện trong cả hai tệp. Mỗi cột là một mã có hậu tố `.US`. Cả hai tệp đều có 604 dòng và đều thiếu cột ngày. Khoảng thời gian ghi trong tên tệp chưa cho biết ngày tương ứng của từng dòng. Số ô trống ở trên là phép đếm ký tự trong CSV. Giá trị số 0 là một tín hiệu hợp lệ và được giữ nguyên.

**Ý nghĩa với Pilot 5.** Trước khi dùng hai bảng để đối chiếu tín hiệu AI với giá hoặc để kiểm thử chiến lược ESG, người phụ trách dữ liệu cần xác nhận lịch giao dịch và ánh xạ ngày cho từng dòng. Chỉ ghép theo vị trí có thể dẫn tới việc so sánh dữ liệu của hai ngày khác nhau. Đây là rủi ro khi tái sử dụng hai tệp công khai. Kết quả kiểm tra chưa xác định cách nhóm dự án đã ghép dữ liệu nội bộ.

## Chạy lại

Từ thư mục chứa `audit.py`, dùng Python 3 và kết nối Internet.

```bash
python3 audit.py
```

Chương trình đọc trực tiếp hai CSV từ phiên bản Zenodo đã ghim, đối chiếu mã MD5 do Zenodo công bố rồi in JSON. Nếu đã tải nguyên hai tệp và giữ tên gốc, có thể chạy ngoại tuyến bằng `python3 audit.py --data-dir /duong/dan/toi/thu_muc_csv`.

## Nguồn và ghi công

Bộ dữ liệu *ESG-Integrated Quantitative Trading Strategy Backtesting Data: MarketSenseAI Framework with FAME Project Integration* của Konstantinos Metaxas và Georgios Fatouros, phát hành trên Zenodo ngày 22/09/2025, DOI `10.5281/zenodo.17175084`. Giấy phép của bộ dữ liệu là CC BY 4.0. Thư mục này chứa mã và kết quả tổng hợp. Các CSV gốc được truy cập tại Zenodo. [Dữ liệu gốc](https://zenodo.org/records/17175084) · [Metadata giấy phép](https://api.datacite.org/dois/10.5281/zenodo.17175084) · [Danh mục kết quả FAME tại CORDIS](https://cordis.europa.eu/project/id/101092639/results)

Thông tin về mục tiêu nghiệp vụ, phạm vi và người dùng được mô tả trong tài liệu Pilot 5. [ESG Scorecard Ranking & Sustainable Portfolio Optimisation](https://www.fame-horizon.eu/wp-content/uploads/2025/12/Pilot-5_ok.pdf)
