# FAME Project Management Case Study

Repo này là nơi thực hiện bài phân tích. Có thể lấy dữ liệu, chạy mã, kiểm tra toàn bộ phép tính quản lý và đối chiếu với ProjectLibre, Excel. Bản Word và PDF ở thư mục gốc dùng để đọc và nộp bài.

| Muốn làm gì? | Mở từ đây |
|---|---|
| Đối chiếu Innovation Pentagon và theo dõi phản hồi của Pilot 5 | [Bảng 35 điểm, nguồn từng hình và quyết định quản lý](docs/innovation-pentagon.md) · Trang **Innovation Pentagon** trong Excel · Mục 6.2, 7.1 và Phụ lục J trong báo cáo |
| Tra mục tiêu, kết quả, kỳ đo và quyết định cho đủ 65 KPI | [Excel có bộ lọc](FAME_Ma_tran_65_KPI.xlsx) · [Bảng dữ liệu và từng trang nguồn](evidence/kpi_matrix.csv) · [Quy tắc và lệnh kiểm tra](evidence/README.md#ma-trận-nghiệm-thu-65-kpi) · Phụ lục G trong PDF |
| Nghiệm thu riêng Pilot 5 và xử lý chín mã ngoại lệ | [Hồ sơ và lệnh chạy](Pilot5_nghiem_thu/) · [Lịch ProjectLibre](Pilot5_nghiem_thu/Lich_nghiem_thu.pod) · [Phiếu bấm P1](Pilot5_nghiem_thu/Duyet_P1.html) · [Phiếu bấm P2](Pilot5_nghiem_thu/Duyet_P2.html) · Phụ lục K |
| Kiểm bằng chứng năm mức trọng số ESG của Pilot 5 | [R4 và R6 · ảnh giao diện, đầu ra MS023, mã nguồn và quyết định nghiệm thu](Pilot5_nghiem_thu/ra_soat_R4_R6.md) · Phụ lục K |
| Phân tích tín hiệu MarketSenseAI và đối chiếu ESG theo mã, ngày | [CSV gốc, kết quả và cách chạy](esg-data-audit/marketsense-sp100/) · [Bảng đối chiếu từng tín hiệu](results/marketsense_sp100.csv) · Phụ lục K |
| Rà lại 25 hồ sơ còn mở ở phiên bản trước | Trang **Ra soat 25 KPI** trong Excel và Phụ lục H. [Quyết định từng KPI](evidence/kpi_review.csv) · [Trang nguồn và dấu SHA-256](evidence/kpi_review_sources.csv) |
| Chạy lại phần kiểm được của 23 KPI còn mở | Trang **Kiem thu 23 KPI** trong Excel và Phụ lục I. [Kết quả và lệnh chạy](docs/kiem-thu-23-kpi.md) · [Trường cần xin cho từng KPI](evidence/open23_requests.csv) |
| Rà từng yêu cầu của mẫu, đối chiếu cả bảy pilot và chạy mã gốc Pilot 7 | [Bản rà trước khi nộp và lệnh tái lập](docs/ra-soat-truoc-khi-nop.md) · [Kết quả theo pilot](evidence/pilot-outcomes.csv) |
| Hiểu dự án từ quyết định tài trợ tới lúc kết thúc | [Phân tích vòng đời](FAME_Phan_tich_vong_doi_du_an.md) |
| Xem quyết định của PM, phép thử, phản chứng và điều kiện nghiệm thu theo mười miền | [Phân tích quản lý chuyên sâu](docs/phan-tich-quan-ly.md) |
| Truy một con số về đúng tài liệu, trang và phạm vi | [Sổ nguồn](evidence/README.md) |
| Xem các số được chương trình tính lại | [Bảng kết quả](results/ket-qua.md) · [Dữ liệu JSON](results/pm_results.json) · [Thử trọng số trên 604 dòng](results/ranking_sensitivity.json) |
| Kiểm tra quy tắc và trường hợp biên | [Mã phân tích](fame_pm/) · [Bộ kiểm thử](tests/) |
| Chạy trực tiếp trên GitHub | [Verify FAME analysis](https://github.com/dinhvanan307/FAME_PM/actions/workflows/verify.yml). Trong Run workflow, chọn `original_data` để tải CSV Zenodo hoặc `pilot_sources` để kiểm hồ sơ 7 pilot, các nguồn bổ sung, bộ kiểm thử 23 KPI và thành phần gốc của Pilot 7. |
| Xuất lại tài liệu nộp | [Cách dựng Word và PDF](report/README.md) |

## Từ bản clone đến kết quả

Dùng Python 3.10 trở lên. Chạy các lệnh tại thư mục gốc của repo.

```bash
git clone https://github.com/dinhvanan307/FAME_PM.git
cd FAME_PM
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m fame_pm --check
```

Trên Windows PowerShell, kích hoạt môi trường bằng `.venv\Scripts\Activate.ps1`. Lần kiểm tra trên đọc XML, hai sổ Excel, dữ liệu bìa và tài trợ, cùng bản kết quả ESG đã lưu. Để tự tái lập từ bản phát hành Zenodo, chạy thêm các lệnh sau.

```bash
python -m fame_pm --check --download --data-dir du_lieu
python -m fame_pm --check --data-dir du_lieu
```

Lệnh đầu tải metadata và 12 CSV, kiểm tra MD5 rồi chạy lại cả kiểm tra cấu trúc, hiệu chỉnh ngành và hai hồ sơ trọng số. Lệnh sau làm lại từ bản tải trên máy. Nếu chủ động cập nhật đầu vào, dùng `python -m fame_pm --write --data-dir du_lieu`, xem thay đổi trong `results/` rồi chạy lại `--check`. Khi có hai CSV gốc do điều phối viên lưu, thêm `--reviews-dir /duong/dan/thu_muc_phieu` để tái tính thống kê nhóm và đối chiếu với Excel. Hai tệp chi tiết được đọc tại chỗ.

**Kết quả đáng xem.** D6.4 giao trễ 143 ngày lịch. Ba trong sáu KPI có đủ bằng chứng. Trong hồ sơ hồi cứu, số hồ sơ mở có đầu mối đề xuất tăng từ 0/3 lên 3/3. Trong buổi chấm độc lập, cả hai cách đều khớp tham chiếu 3/6. Khi thử hai hồ sơ trọng số ESG trên 604 dòng, có 39 dòng đổi thành phần top 5. Các kết quả này trả lời những câu hỏi khác nhau về tiến độ, chất lượng hồ sơ, quyết định của con người và hành vi công cụ. [Số liệu và nguồn theo từng phép tính](results/ket-qua.md)

## Bối cảnh

FAME (*Federated decentralized trusted dAta Marketplace for Embedded finance*) là dự án Horizon Europe do GFT Italia điều phối, triển khai từ năm 2023 đến 2025. Dự án xây dựng một thị trường dữ liệu để các tổ chức tìm, trao đổi và sử dụng dữ liệu, mô hình AI và dịch vụ phân tích tài chính. Kho này là một bài nghiên cứu tình huống độc lập về cách dự án được lập kế hoạch, thực hiện và đánh giá. [Hồ sơ dự án của Ủy ban châu Âu](https://cordis.europa.eu/project/id/101092639)

## Nội dung

- [Phân tích vòng đời dự án FAME](./FAME_Phan_tich_vong_doi_du_an.md) theo dõi quyết định tài trợ, cách thu thập yêu cầu, tiến độ bàn giao, chi phí, rủi ro và kết quả sau khi dự án kết thúc. Bài ghi nguồn cho số liệu và đánh dấu các phép tính, nhận định của người viết.
- [Kiểm tra dữ liệu ESG và tín hiệu AI](./esg-data-audit/README.md) đi sâu vào một câu hỏi liên quan đến Pilot 5 về xếp hạng ESG và tối ưu danh mục. Hai tệp công khai có đủ thông tin để ghép điểm ESG với tín hiệu MarketSenseAI theo đúng mã cổ phiếu và ngày giao dịch hay không?

## Báo cáo và tệp thực hành

- [Báo cáo cuối kỳ dạng PDF](./FAME_Bao_cao_cuoi_ky.pdf) và [bản Word](./FAME_Bao_cao_cuoi_ky.docx). Chương 3 trình bày D6.4 và kỳ RP2. Mục 6.5 ghi kết quả hồi cứu, mục 6.6 trình bày 12 quyết định từ hai người chấm độc lập.
- [Lịch ProjectLibre](./FAME_Lich_ProjectLibre.pod) và [bản Microsoft Project XML](./FAME_Lich_MS_Project.xml). Mở tệp .pod bằng ProjectLibre. Các dòng 24–26 hiển thị khoảng báo cáo RP2 và hai ngày ranh giới do CORDIS công bố.
- [Workbook nghiệm thu hồi cứu](./FAME_Nghiem_thu_6_KPI.xlsx) lưu quyết định ban đầu, phép kiểm tra và sổ đối chiếu ngày.

### Kết quả chấm nhanh sáu KPI

Ngày 23/11/2026, hai người chấm độc lập hoàn tất [phiếu P1](./Cham_doc_lap/Duyet_nhanh_P1.html) và [phiếu P2](./Cham_doc_lap/Duyet_nhanh_P2.html). Tải tệp HTML và mở bằng trình duyệt để dùng phiếu. Mỗi phiếu ghi sáu lần bấm, tự đo thời gian từng KPI và xuất CSV.

Cả hai cách đều duyệt 6/6 KPI và khớp tham chiếu của người viết ở 3/6 KPI. Ba KPI còn thiếu bằng chứng là tỷ lệ sử dụng, tương quan tín hiệu và mức cải thiện danh mục. Thời gian trung bình từ hiển thị đến bấm là 1,579 giây/KPI khi chấm thông thường và 1,192 khi có gợi ý checklist. Trung vị theo thứ tự là 0,757 và 1,301 giây. Buổi này chưa chứng minh gợi ý làm giảm thời gian thẩm định. [Bảng Excel tổng hợp hai điều kiện](./Cham_doc_lap/Ket_qua/Tong_hop_A_B.xlsx)

### Mẫu Excel ba lựa chọn cho buổi chấm chi tiết

1. Điều phối viên giao riêng [phiếu P1](./Cham_doc_lap/Phieu_P1.xlsx) và [phiếu P2](./Cham_doc_lap/Phieu_P2.xlsx). Mỗi bạn chỉ cần phiếu của mình và các nguồn FAME đã liên kết ở trang hướng dẫn. Giữ kín báo cáo, workbook hồi cứu và đáp án cho đến khi chốt cả hai phiếu.
2. Mỗi bạn làm Luot_1 rồi Luot_2, ba KPI mỗi lượt, ghi thời điểm bắt đầu và kết thúc cố định đến giây cho từng KPI. Ghi căn cứ cho quyết định. Ở lượt B, điền thêm bốn mục checklist. Lưu lại phiếu đã chấm.
3. Trong [sổ riêng của điều phối viên](./Cham_doc_lap/Tong_hop_dieu_phoi.xlsx), dùng **Paste Special → Values** cho A13:L15 ở mỗi lượt. Dán vào Nhap_phieu từ A6, A9, A12, A15 theo thứ tự P1–lượt 1, P1–lượt 2, P2–lượt 1, P2–lượt 2. Đối chiếu 12 dòng rồi đọc trang Ket_qua. Mẫu phát hành để trống quyết định và thời gian thực.

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
