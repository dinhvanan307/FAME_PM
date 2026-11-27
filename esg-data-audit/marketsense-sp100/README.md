# MarketSenseAI S&P 100 và đối chiếu với ESG của Pilot 5

**Kết quả kiểm chứng ngày 27/11/2026.** Bản phát hành MarketSenseAI có 1.500 quyết định với lời giải thích, mỗi quyết định có một khóa mã chứng khoán và ngày. Đối chiếu được 22 khóa với bảng có ngày của Pilot 5 trong D6.4. Chưa gắn được ngày cho từng dòng trong các CSV điểm ESG của Pilot 5. [Bảng kết quả từng tín hiệu](../../results/marketsense_sp100.csv) · [Số liệu tổng hợp và kết quả đủ 15 kỳ](../../results/marketsense_sp100.json)

## Dữ liệu gốc và cách đọc

| Đầu vào | Đơn vị quan sát và nguồn |
|---|---|
| [MarketSenseAI_data_SP100.csv](MarketSenseAI_data_SP100.csv) | Bản gốc do Georgios Fatouros và Kostas Metaxas công bố ngày 15/07/2024, v1, theo [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Tệp được phân phối nguyên bản. Cột đầu không có tên là ID của tác giả. Các cột tiếp theo là `ticker`, `date`, `decision`, `why`. Một lý do có thể trải qua nhiều dòng văn bản. Dùng trình đọc CSV. MD5 của 3.040.603 byte là `f0bec18331b82b25282cc4a572a71d47`. [Zenodo và checksum](https://zenodo.org/records/12744005) · [Nghiên cứu gốc](https://doi.org/10.1007/s00521-024-10613-4) |
| Bộ ESG v1 của Pilot 5 | Từng trụ E, S, G có 100 cột mã và 604 dòng. Chương trình dùng bộ đọc sẵn có của repo, kiểm 12 CSV với metadata và bản kê MD5 đã công bố trong repo. [Bản xuất ESG](https://zenodo.org/records/17175084) · [Bản kê](../reproduction.json) |
| [Bản chép bảng xếp hạng có ngày](../../evidence/pilot5_d64_p64.csv) | Người viết chép thủ công đủ 22 dòng nhìn thấy ở trang PDF 64, trang in 60, mục Media Gallery ngay trước bảng 41. Giữ nguyên mã, ID hiển thị, nhãn và điểm ba trụ. Bảng ghi kỳ danh mục tháng 3/2024 và ngày dự báo 29/02/2024. Dùng ngày dự báo làm khóa. Ngày thu thập từng điểm thành phần không xuất hiện trong hình. [FAME, D6.4, trang 64](https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D6.4-Use-Cases-Specification-and-Pilot-Sites-Preparation.-II.pdf#page=64) |

## Tín hiệu mua, giữ và bán

Người viết đếm 100 mã ở mỗi một trong 15 ngày cuối tháng, không có khóa mã–ngày trùng. Tệp bao gồm **31/12/2022** và kết thúc ngày **29/02/2024**. Phần mô tả trên Zenodo ghi từ 01/01/2023. Kết quả dưới đây tính cả 100 dòng ngày 31/12/2022. Tổng số ở ba nhóm khớp số công bố trong bài báo. [CSV gốc](MarketSenseAI_data_SP100.csv) · [Bài báo, mục 4](https://doi.org/10.1007/s00521-024-10613-4)

| Quyết định | Số dòng | Tỷ lệ | Trung vị số từ mỗi giải thích |
|---|---:|---:|---:|
| Mua | 338 | 22,53% | 275 |
| Giữ | 1.150 | 76,67% | 297 |
| Bán | 12 | 0,80% | 297 |

Giữ chiếm đa số trên toàn tệp. Tháng 01/2024 có 50 mua, 48 giữ và 2 bán. Đến tháng 02/2024, phân bố là 43 mua, 56 giữ và 1 bán. Nhóm bán chỉ có 12 quan sát trong toàn kỳ, nên số lượt bán theo từng tháng rất nhạy với một quyết định đơn lẻ. Đây là phân bố đầu ra mô hình. Tệp không cung cấp nhãn đúng/sai cho quyết định. [Đủ số đếm từng tháng](../../results/marketsense_sp100.json)

## Lý do nào xuất hiện trong trường why

Toàn bộ 1.500 quyết định có văn bản, vẫn còn 1.500 nội dung phân biệt sau khi chuẩn hóa chữ hoa/thường và khoảng trắng. Người viết đếm từ tiếng Anh theo chuỗi chữ cái, cho phép dấu nháy trong từ. Mỗi quy tắc từ khóa dưới đây tính tối đa một lần cho mỗi lời giải thích. Một lời giải thích có thể khớp nhiều chủ đề. Các biểu thức chính xác được công bố cùng kết quả. [Mã phân tích](../marketsense_sp100.py) · [Quy tắc và tổng theo nhóm](../../results/marketsense_sp100.json)

| Có từ hoặc cụm từ về | Mua / 338 | Giữ / 1.150 | Bán / 12 |
|---|---:|---:|---:|
| Tin tức, tiêu đề | 280 | 841 | 11 |
| Giá, biến động, động lượng hoặc rủi ro giá | 331 | 1.108 | 11 |
| Kinh tế vĩ mô, lạm phát, lãi suất hoặc Fed | 280 | 1.029 | 11 |
| Nền tảng doanh nghiệp, dòng tiền, kết quả kinh doanh | 338 | 1.144 | 12 |
| Ghi đích danh ESG hoặc cụm đầy đủ tiếng Anh | 8 | 26 | 0 |

**Diễn giải của người viết khi đọc ba ví dụ.** Với Apple, giải thích ngày 31/08/2023 cân nhắc tăng trưởng dịch vụ và lượng tiền mặt với sức ép từ doanh thu và khả năng sinh lời, rồi chọn giữ (ID 1). Ngày 31/12/2023, phần giải thích nhấn mạnh vị thế thị trường, lợi nhuận và dòng tiền, rồi chọn mua (ID 0). Với Boeing ngày 31/01/2024, phần giải thích liên hệ sự cố vận hành 737 MAX 9, biến động giá và dòng tiền suy yếu với quyết định bán (ID 191). Đây là cách mô hình lập luận trong tệp. Đợt kiểm này chưa kiểm tra từng phát biểu với tin tức hoặc báo cáo tài chính tại ngày đó. 34 dòng nhắc đích danh ESG chỉ đo sự xuất hiện của thuật ngữ. [Dữ liệu tác giả theo ID](MarketSenseAI_data_SP100.csv)

## Ghép theo mã và thời gian

1. **Thử trên CSV ESG.** So sánh nguyên mã, kể cả hậu tố `.US` và dấu gạch trong `BRK-B.US`. Hai tập khớp 100/100 mã, bao phủ 1.500/1.500 dòng tín hiệu. Cột của ba bảng ESG đều là mã cổ phiếu, còn ngày bắt đầu và kết thúc nằm trong tên tệp. Thiếu khóa ngày cho 604 dòng, nên số cặp mã–ngày xác minh được từ các CSV này là **0**. Chương trình không suy lịch giao dịch từ số thứ tự dòng. [Bản ESG v1](https://zenodo.org/records/17175084)
2. **Thử trên ảnh báo cáo.** Ghép chính xác `(ticker, date)` ở MarketSenseAI với `(ticker, predicted_at)` của bảng chép. Có **22/22 dòng ảnh** khớp trên **một ngày**, tương đương **22/100 mã của kỳ đó** và **22/1.500 quan sát của toàn tệp**. Ví dụ, JPM.US có nhãn mua ở cả hai nguồn và ba điểm hiển thị E 7,1500, S 5,2900, G 7,5500. Cả 22 dòng ảnh đều mang nhãn mua và đều khớp nhãn CSV. Mẫu ảnh chỉ bao phủ 22 trong 43 tín hiệu mua của kỳ. Không thể suy tỷ lệ đồng thuận cho nhóm giữ, bán hoặc cho cả lịch sử. [Ảnh gốc, trang PDF 64](https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D6.4-Use-Cases-Specification-and-Pilot-Sites-Preparation.-II.pdf#page=64)
3. **Quyết định quản lý.** Chấp nhận khả năng truy vết 22 dòng tại ngày dự báo của bảng minh họa. Giữ trống các trường điểm ở 1.478 quan sát còn lại. Không suy đổi thang điểm giữa hai bản phát hành. Muốn mở rộng phải có ngày định giá cho từng dòng ESG hoặc các bản xếp hạng có ngày khác của tác giả. R4 và R6 tiếp tục cần bằng chứng riêng về năm cấu hình trọng số và khuyến nghị. [Hồ sơ R4/R6](../../Pilot5_nghiem_thu/ra_soat_R4_R6.md)

Trong [bảng 1.500 dòng](../../results/marketsense_sp100.csv), `source_id` nối về cột đầu CSV gốc để đọc nguyên lời giải thích. Lọc `d64_key_matched = 1` để xem 22 dòng có bằng chứng. `d64_env`, `d64_soc`, `d64_gov` giữ nguyên độ chính xác trên ảnh. Ô trống có nghĩa là thiếu quan sát ghép được. Các cột từ khóa có giá trị 0 hoặc 1.

## Chạy lại

Từ thư mục gốc FAME_PM, nếu máy chưa có bản ESG, chạy lệnh đầu để tải nguồn. CSV MarketSenseAI đã có sẵn trong repo. Lệnh thứ hai kiểm lại từng byte của hai đầu ra so với kết quả đã công bố. Bỏ `--check` để dựng lại CSV và JSON.

```bash
python esg-data-audit/reproduce_pilot5.py --data-dir du_lieu/zenodo --download
python esg-data-audit/marketsense_sp100.py --check
```
