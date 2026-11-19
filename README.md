# FAME Project Management Case Study

FAME (*Federated decentralized trusted dAta Marketplace for Embedded finance*) là dự án Horizon Europe do GFT Italia điều phối, triển khai từ năm 2023 đến 2025. Dự án xây dựng một thị trường dữ liệu để các tổ chức tìm, trao đổi và sử dụng dữ liệu, mô hình AI và dịch vụ phân tích tài chính. Kho này là một bài nghiên cứu tình huống độc lập về cách dự án được lập kế hoạch, thực hiện và đánh giá. [Hồ sơ dự án của Ủy ban châu Âu](https://cordis.europa.eu/project/id/101092639)

## Nội dung

- [Phân tích vòng đời dự án FAME](./FAME_Phan_tich_vong_doi_du_an.md) theo dõi quyết định tài trợ, cách thu thập yêu cầu, tiến độ bàn giao, chi phí, rủi ro và kết quả sau khi dự án kết thúc. Bài ghi nguồn cho số liệu và đánh dấu các phép tính, nhận định của người viết.
- [Kiểm tra dữ liệu ESG và tín hiệu AI](./esg-data-audit/README.md) đi sâu vào một câu hỏi liên quan đến Pilot 5 về xếp hạng ESG và tối ưu danh mục. Hai tệp công khai có đủ thông tin để ghép điểm ESG với tín hiệu MarketSenseAI theo đúng mã cổ phiếu và ngày giao dịch hay không?

## Chạy kiểm tra dữ liệu

Cần Git để tải repo, Python 3 và kết nối Internet để đọc hai tệp CSV từ Zenodo. Mã kiểm tra chỉ dùng thư viện chuẩn của Python.

```bash
git clone https://github.com/dinhvanan307/FAME_PM.git
cd FAME_PM
python3 esg-data-audit/audit.py
```

Chương trình đối chiếu mã MD5 của từng tệp với bản đã phát hành rồi in kết quả dạng JSON. Hai tệp có **96 mã cổ phiếu chung**, cùng **604 dòng dữ liệu** và đều thiếu cột ngày. Tệp tín hiệu có **706 ô trống**. Để ghép các dòng theo ngày, người phân tích cần xác nhận lịch giao dịch tương ứng. [Bộ dữ liệu và mã kiểm tra của Zenodo](https://zenodo.org/records/17175084)

Để chạy ngoại tuyến, tải hai CSV có tên kết thúc bằng `_esg.csv` và `_ms_daily.csv` từ bản Zenodo trên, giữ nguyên tên tệp trong cùng một thư mục, rồi truyền đường dẫn thư mục cho chương trình.

```bash
python3 esg-data-audit/audit.py --data-dir "/duong/dan/den/thu_muc_csv"
```

## Nguồn dữ liệu

Konstantinos Metaxas và Georgios Fatouros công bố bộ dữ liệu *ESG-Integrated Quantitative Trading Strategy Backtesting Data: MarketSenseAI Framework with FAME Project Integration* theo giấy phép CC BY 4.0. [Bản phát hành trên Zenodo](https://doi.org/10.5281/zenodo.17175084) · [Thông tin giấy phép tại DataCite](https://api.datacite.org/dois/10.5281/zenodo.17175084)
