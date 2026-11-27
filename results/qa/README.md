# Tải QA của ba hồ sơ bàn giao ngày 31/07/2025

**Câu hỏi của PM.** Nếu cả ba bản cùng đến đầu ngày và đều cần một ca QA, bố trí thêm một người đủ thẩm quyền thay đổi lượng việc vượt năng lực và ngày giao như thế nào?

**Căn cứ FAME.** D2.4 do GFT chủ trì, D3.5 do UNP chủ trì, D3.6 do NUIG chủ trì. Cả ba bìa ghi UPRC đảm bảo chất lượng và giao ngày 31/07/2025. Ngày đó được chọn làm mốc so trong mô phỏng. Hạn hợp đồng và các lần bàn giao của dự án được lưu riêng trong [sổ 32 báo cáo](../../evidence/deliverables.csv). [Bìa D2.4](https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D2.4-Integrated-FAME-Data-Marketplace-II.pdf#page=1) · [Bìa D3.5](https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D3.5-Federated-Data-Assets-Catalogue-II.pdf#page=1) · [Bìa D3.6](https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D3.6-Mechanisms-and-Tools-for-Regulatory-Compliance-II.pdf#page=1)

**Giả định của người viết.** Cả ba bản sẵn sàng lúc 08:00 ngày 31/07. Mỗi bản cần 8 giờ của một người, có thể giao ngay khi xong QA. Mỗi người có 8 giờ/ngày, thứ Hai đến thứ Sáu, làm 08:00–12:00 và 13:00–17:00. A có một người. B thêm một người hỗ trợ có cùng năng lực, quyền truy cập và thẩm quyền. Xếp D2.4, D3.5, D3.6 lần lượt cho người rảnh sớm nhất. Ưu tiên người chính khi hai người cùng rảnh. Hai phương án giữ nguyên 24 giờ công và cùng thứ tự ưu tiên. Số giờ thực của UPRC, thời điểm QA nhận bản, năng suất và chi phí huy động người chưa có trong các bìa.

## Mở trong ProjectLibre

1. Mở [nhu_cau.pod](nhu_cau.pod). Chọn **Resource Usage** và đặt thang thời gian theo ngày. Ngày 31/07, “A · QA chính” có 24 giờ. Ở B, “QA chính” có 16 giờ và “QA hỗ trợ” có 8 giờ. A và B là hai cách bố trí thay thế nhau. Chỉ cộng giờ trong cùng một phương án.
2. Mở [can_tai.pod](can_tai.pod). Ở **Gantt**, xem cột **Finish** của từng hồ sơ. Liên kết kết thúc–bắt đầu biểu diễn việc một người phải xong hồ sơ trước để nhận hồ sơ kế tiếp. Ở **Resource Usage**, mỗi người có tối đa 8 giờ mỗi ngày. Áp dụng lịch làm việc nêu trên, người viết xếp việc vào ca rảnh rồi kiểm lại ngày giao và tải theo ngày bằng ProjectLibre.
3. Đối chiếu [tải theo ngày](tai_theo_ngay.csv) và [ngày giao theo hồ sơ, kèm nguồn](lich_giao.csv). Hai tệp XML cùng tên cho phép nhập lại lịch vào ProjectLibre hoặc trao đổi qua định dạng Microsoft Project.

| Kết quả mô phỏng | A · Một người | B · Hai người |
|---|---:|---:|
| Phần vượt năng lực nếu giao hết ngày 31/07 | 16 giờ | 8 giờ |
| D2.4 sau khi cân tải | 31/07/2025 | 31/07/2025 |
| D3.5 sau khi cân tải | 01/08/2025 | 31/07/2025 |
| D3.6 sau khi cân tải | 04/08/2025 | 01/08/2025 |
| Số hồ sơ giao được trong ngày 31/07 | 1/3 | 2/3 |
| Tổng giờ vượt năng lực sau khi xếp vào ca rảnh | 0 | 0 |

**Diễn giải.** Với từng người và ngày, số giờ vượt năng lực bằng phần dương của giờ được giao trừ 8. Nếu phải giao cả ba trong ngày mục tiêu, B giảm 8 giờ việc vượt năng lực nhưng vẫn còn thiếu một ca. Khi cho phép dời việc, cả hai phương án đều khả thi, B hoàn tất sớm hơn A một ngày làm việc, tương ứng ba ngày lịch qua cuối tuần. Đây là kết quả mô phỏng. Ba bản của FAME thực tế cùng ghi ngày giao 31/07.

## Tái lập từ thư mục gốc

```bash
python -m fame_pm.qa_capacity --check
python -m fame_pm.qa_capacity --write
```

Lệnh đầu kiểm hai CSV và hai XML với các giả định và ngày nguồn. Lệnh sau tạo lại bốn tệp đó. Có thể kiểm riêng hai POD đã phát hành bằng Java 21 và JAR ProjectLibre 1.9.8 như sau. Đặt biến môi trường PROJECTLIBRE_JAR trỏ đến tệp JAR của bản cài. Đổi thao tác check thành write để tạo lại POD sau khi sửa đầu vào, rồi chạy check trong tiến trình mới.

```bash
for view in nhu_cau can_tai; do
  java -Djava.awt.headless=true -Duser.timezone=UTC -cp "$PROJECTLIBRE_JAR" \
    bsh.Interpreter fame_pm/projectlibre_qa.bsh check \
    "$PWD/results/qa/$view.xml" "$PWD/results/qa/$view.pod" \
    "$PWD/results/qa/tai_theo_ngay.csv"
done
```

Phép kiểm mở lại POD bằng ProjectLibre, kiểm tên, hạn mô phỏng, ngày bắt đầu và kết thúc, phân công, mức sẵn sàng 100%, các liên kết và số giờ mà ProjectLibre tính cho từng người trong từng ngày được ghi ở CSV.
