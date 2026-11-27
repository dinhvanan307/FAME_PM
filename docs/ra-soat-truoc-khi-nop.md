# Rà soát bài quản lý dự án FAME trước khi nộp

Phạm vi toàn dự án gồm **7 pilot và 14 ca sử dụng**. Bài đã đối chiếu cả bảy pilot qua ba lần bàn giao: D6.4 xác định phạm vi và chỉ tiêu, D6.2 mô tả tích hợp, D6.3 đánh giá kết quả. Phần thực hành có hai đối tượng riêng: dữ liệu ESG do nhóm tác giả phát hành ở Pilot 5 và mã kiểm tra chất lượng cảm biến của đối tác Pilot 7. Lịch ProjectLibre theo dõi đủ 32 báo cáo trong danh mục công khai. Buổi chấm độc lập đo sáu KPI được chọn của Pilot 5. Các mẫu số này phục vụ những quyết định khác nhau. [Tổng quan FAME](https://www.fame-horizon.eu/the-project/) · [Chỉ mục được sinh từ ba PDF](../results/pilot_portfolio.json)

## Ba bài tham khảo của học phần

Mẫu gần nhất về nội dung là *Phân tích dự án INTERLINK* của Vũ Phúc Anh, báo cáo cuối kỳ 37 trang. Phần 1 trình bày dự án và đầu ra. Phần 2 rà WBS, Gantt, nguồn lực, rủi ro, chi phí và tổng hợp kết quả (trang PDF 2–34). Trang 34 giới thiệu hướng mô phỏng phần tiếp theo. Bản được cung cấp kết thúc bằng thuật ngữ và tài liệu tham khảo. Báo cáo EVM của Phạm Quang Vinh, trang PDF 14 và 50–53, hướng dẫn cách đọc riêng số liệu tham khảo và kịch bản tự tính. Bài phân tích Luo et al. của Vũ Phúc Anh, trang PDF 33–41, minh họa cách giữ cùng đối tượng quan sát và so sánh hai phương án. Đây là ba tài liệu tham khảo về cách làm bài. Số liệu FAME có nguồn riêng cho từng nhận định.

| Nội dung tham khảo | Áp dụng trong báo cáo FAME | Kết quả và giới hạn |
|---|---|---|
| Bối cảnh, WBS, sản phẩm và bàn giao | Phần I và mục 2.1–2.4. Từ WP6 đến đặc tả D6.4, hệ thống tích hợp D6.2 và báo cáo đánh giá D6.3 | WBS do người viết tái dựng. Chủ trì, phản biện và QA có căn cứ trên bìa. |
| Tiến độ và điều phối nguồn lực | Mục 2.5 và 3.1–3.5. Ba bìa ghi cùng đầu mối QA và cùng ngày giao. D6.4 có ba mốc của bản 0.6, 0.7 và 1.0 | Trong [mô phỏng QA](../results/qa/) nhu cầu vượt năng lực giảm từ 16 còn 8 giờ ngày 31/07. Sau khi cân tải, lô ba hồ sơ hoàn tất sớm một ngày làm việc. Muốn xác định quá tải thực tế cần lịch phân công và giờ công của UPRC. |
| Rủi ro và ứng phó | Bảng 5.1–5.3 dùng chung mã RR để nối [sổ rủi ro](../evidence/risk_register.csv), [nhật ký vấn đề](../evidence/risk_issues.csv) và ma trận P × I. Mục 5.4 theo dõi RR-04 qua VD-04 và VD-05 | Hai cách chấm đều duyệt 3/3 KPI thiếu căn cứ. Mức cao 9/9 do người viết giữ lại. Phiếu bắt buộc nhập căn cứ còn chờ thử. |
| Chi phí và câu hỏi EVM | Mục 4.3 phân biệt cơ cấu tài trợ, số thực chi và giá trị công việc đã hoàn thành | Tính được phần ngoài tài trợ EU. Muốn tính CPI, EAC phải có dữ liệu phù hợp cùng phạm vi, kỳ và đường cơ sở. |
| Kịch bản và phép so sánh | Mục 3.4 xét ba kịch bản chờ phản biện. Mục 6.5–6.6 xét sáu KPI trên Excel với cùng ngưỡng và tham chiếu | Dự phòng thu hồi 5 ngày **trong mô phỏng S2 so với S1**. Hồi cứu có thêm 3/3 hồ sơ mở được đề xuất đầu mối. Hai cách chấm độc lập cùng khớp 3/6. |

**Chạy lại kịch bản D6.4** từ thư mục gốc. Lệnh đầu đối chiếu ngày từ lịch đã xác minh với tệp công bố. Lệnh sau dựng lại CSV và Microsoft Project XML từ lịch lịch sử nếu cần.

```bash
python -m fame_pm.review_scenario --check
python -m fame_pm.review_scenario --write
```

Mở [lịch kịch bản](../results/D6_4_kich_ban_ProjectLibre.xml) bằng ProjectLibre. S0 dùng ngày 03/02, 12/02 và 20/02/2025. S1 thêm bảy ngày chờ; S2 vẫn có gián đoạn đó nhưng giả định người thay thế đủ năng lực có thể nhận sau hai ngày. Hai khoảng gốc 9 và 8 ngày giữ nguyên. Mỗi nhóm có ba mốc và hai liên kết kết thúc–bắt đầu. Độ trễ trên liên kết dùng lịch bảy ngày của bài. Mốc 10 giờ là quy ước hiển thị; bìa FAME chỉ công bố ngày. Kết quả xem ở [sổ kịch bản](../results/d64_review_scenarios.csv). Lịch có 32 báo cáo lịch sử vẫn ở [tệp ProjectLibre gốc của bài](../FAME_Lich_ProjectLibre.pod).

## 1. Mẫu cũ yêu cầu thể hiện điều gì?

Tệp được lớp dẫn là một khóa luận về dự đoán khách hàng ngừng sử dụng dịch vụ. Phần có thể áp dụng trực tiếp là cách nối câu hỏi, công cụ, phương pháp đề xuất, dữ liệu, cách đánh giá, kịch bản thử và kết quả. Các mục 4.1–4.4 của mẫu tương ứng bốn câu hỏi: lấy gì về, đo bằng gì, so sánh trường hợp nào và thực tế thu được gì. Đề bài học phần yêu cầu áp dụng kiến thức và kỹ thuật quản lý cho một dự án hệ thống thông tin có thật. Bảng sau dùng hai căn cứ đó để rà bài. Giảng viên chưa cung cấp thang điểm trong tài liệu được dẫn. [Mẫu báo cáo của lớp](https://drive.google.com/file/d/1NUqA7wXU1grDJe4b3ya_6D0xHUZAbdyv/view)

**Cách trình bày trong bản nộp.** Phần chính nêu câu hỏi PM phải quyết định, đơn vị quan sát và kết quả có mẫu số. Với tiến độ, Bảng 3.1 tổng hợp 32 sản phẩm theo gói công việc, D6.4 giải thích diễn biến và Phụ lục L dẫn từng bìa. Với nghiệm thu, mục 6.5 và 6.6 trình bày riêng bằng chứng hồi cứu và kết quả hai người chấm. Kết luận nêu đầu mối, dữ liệu cần bổ sung và điều kiện xét lại. Trang mở đầu phụ lục có liên kết tới từng hồ sơ A–L. [Mẫu của lớp, mục 4.1–4.4](https://drive.google.com/file/d/1NUqA7wXU1grDJe4b3ya_6D0xHUZAbdyv/view) · [Biểu mẫu nghiệm thu và kết thúc dự án PM²](https://pm2.europa.eu/pm2-artefacts_en) · [GAO, thực hành 9–10 về lịch dự án](https://www.gao.gov/assets/gao-16-89g.pdf)

| Yêu cầu và vị trí trong bài | Dữ liệu để đối chiếu | Chạy mã hoặc mở tệp | Kỹ thuật quản lý áp dụng | Kết quả quan sát | Phần còn thiếu hoặc giới hạn |
|---|---|---|---|---|---|
| Mở đầu, mục tiêu 5W1H và phạm vi. Mở đầu, Ch. 1–2, Phụ lục F | CORDIS cấp dự án, D6.4 Bảng 1 và Phụ lục A | [Vòng đời](../FAME_Phan_tich_vong_doi_du_an.md), lệnh A bên dưới | Xác định đối tượng, WBS, truy vết yêu cầu theo pilot và ca sử dụng | Định vị được cả 7 pilot, 14 ca sử dụng và các bảng kết quả | Số yêu cầu khác nhau theo cách đếm. Cần bảng đối chiếu phiên bản nếu muốn tuyên bố đóng từng yêu cầu |
| Công cụ, kỹ thuật và cách tổ chức. Ch. 2–3 | Bìa D6.4, lịch sử phiên bản, các vai trò tham gia | [ProjectLibre](../FAME_Lich_ProjectLibre.pod), [XML](../FAME_Lich_MS_Project.xml), [hình Gantt](../FAME_Gantt_ProjectLibre_D6_4.png) | Phân rã công việc, ma trận trách nhiệm, giữ hạn gốc và ngày giao, đặt RP2 làm kỳ báo cáo | Có thể lần từ bìa đến mốc tương ứng trên Gantt | Chưa có giờ công và lịch phụ thuộc được duyệt đủ để kết luận về đường găng |
| Mẫu 4.1, thu thập và chuẩn bị dữ liệu. Ch. 6, Phụ lục D và F | Ba PDF, 12 CSV trên Zenodo, 2 PDF tham khảo, bảng ngưỡng từ GitHub của đối tác | Lệnh A, B, C. [Danh mục dữ liệu](../evidence/README.md) | Quản lý cấu hình, dấu kiểm toàn vẹn, sổ ngoại lệ | Hai bảng ESG/tín hiệu có 604 dòng, 96 mã chung và 706 ô tín hiệu trống. Bảng ngưỡng Pilot 7 có một trường số cần xác nhận | Hai bảng ESG/tín hiệu thiếu khóa ngày. Lượt đầu ghi chín ngoại lệ. Lượt sau tái tạo đủ giá trị của chín mã này. Bảng ánh xạ ngành chính thức vẫn chờ xác nhận |
| Mẫu 4.2, phương pháp đánh giá. Ch. 3–6 | Ngày trên bìa, ngưỡng D6.4 và kết quả D6.3, phiếu và mốc thời gian do điều phối lưu | Lệnh B và D. [Mã tính](../fame_pm/analysis.py), [phiếu tổng hợp](../Cham_doc_lap/Ket_qua/Tong_hop_A_B.xlsx) | So kế hoạch với thực tế, kiểm tra cùng đơn vị và kỳ đo, xác định mẫu số trước khi nghiệm thu | Có quy tắc để giữ mở ba KPI thiếu căn cứ, đo thời gian thao tác theo từng lượt | Tham chiếu sáu KPI do người viết lập. Chưa có quyết định trọng tài nghiệp vụ bên ngoài |
| Mẫu 4.3–4.4, kịch bản và kết quả thực nghiệm kỹ thuật. Ch. 6, Phụ lục D–F và K | ESG gốc và điều chỉnh theo ngành, ba bảng E/S/G gốc, mã và cấu hình Pilot 7 | Lệnh B và C. [Lượt đầu](../esg-data-audit/reproduction.json), [lượt xác nhận ESG](../Pilot5_nghiem_thu/phep_do.json), [độ nhạy](../results/ranking_sensitivity.json), [Pilot 7](../results/pilot7_boundaries.json) | Đối chứng trên cùng ô, tách hiệu chuẩn và kiểm tra, phân tích độ nhạy, kiểm thử giá trị biên | Dòng 1 hiệu chuẩn, dòng 2–604 kiểm tra: lượt đầu khớp 164.619/164.619 ô trên 91 mã, đối chứng giữ điểm gốc khớp 0. Lượt sau kiểm đủ 100 mã và khớp 180.900/180.900 ô. Đổi trọng số làm 39/604 dòng đổi thành phần top 5. Pilot 7 khớp 279/279 ca biên | Chưa tái lập lợi suất MS020 hoặc chuỗi cảm biến nhà máy. Thay đổi thứ hạng chưa đo lợi ích đầu tư |
| Mẫu 4.3–4.4, tác động của biện pháp quản lý. Ch. 6.5–6.6 | Sáu hồ sơ Excel và kết quả hai người chấm độc lập | [Workbook hồi cứu](../FAME_Nghiem_thu_6_KPI.xlsx), lệnh D | Hồi cứu cùng hồ sơ trước/sau checklist, so sánh hai điều kiện chấm | Hồi cứu đồng nhất tham chiếu 6/6 ở cả hai cách. Trong ba hồ sơ mở, số có đầu mối đề xuất tăng 0 lên 3. Chấm độc lập khớp 3/6 mỗi cách, cả hai duyệt cả ba KPI thiếu bằng chứng | Đầu mối còn chờ nhận việc. Phiếu HTML đo từ lúc hiển thị tới lúc bấm. Muốn chứng minh giảm thời gian thẩm định cần đo cả tra nguồn và lặp trên hồ sơ mới |
| Tiến độ và chi phí. Ch. 3–4 | [32 bìa sản phẩm](../evidence/deliverables.csv), [kỳ RP2 và cơ cấu vốn](../evidence/cordis.json) | Lệnh B, đối chiếu 32 mốc trong lịch .pod và Phụ lục L. Trang Lich_giao trong Excel minh họa 5 mốc ban đầu | Sai lệch ngày lịch, phân tích cơ cấu tài trợ theo cấp | Có 22 bản trễ, 9 bản sớm, một bản đúng ngày. Trung vị có dấu +22 ngày. EU tài trợ 77,55% tổng chi phí 16.621.394,20 EUR | Chưa có tác động tiến độ thực của việc dùng ProjectLibre. Chưa có chi phí thực tế theo công việc, PV/EV/AC cùng kỳ hoặc số tiền tiết kiệm |
| Rủi ro, bên liên quan và bài học. Ch. 5, Ch. 7, Bảng 7.2 | D6.4 về quyền truy cập và chuẩn bị, D6.3 về sử dụng, kết quả của B/C/D | [Phân tích theo 10 miền](phan-tich-quan-ly.md), [kết quả quản lý](../results/ket-qua.md) | Phân biệt sự cố đã xảy ra và rủi ro, đề xuất chủ xử lý, xác định bằng chứng để đóng | Có thể chỉ tên hồ sơ cần bổ sung và người có thẩm quyền xác nhận. Pilot 6 có tài sản bàn giao và ba nhóm lượt tải đều bằng 0 | Chưa có nhật ký xử lý và xác nhận phía đối tác để định lượng mức giảm rủi ro |
| Kết luận, nguồn, khả năng chạy lại | README, sổ nguồn, mã, kết quả và tài liệu nộp | Lệnh A–D và [lệnh dựng Word/PDF](../report/README.md) | Kiểm soát phiên bản và truy vết con số | Có thể đi từ một kết luận đến đúng trang nguồn và phép tính | GitHub công khai số tổng buổi chấm. CSV từng lượt chỉ điều phối viên đối chiếu được |

### Đọc đúng kết quả tiến độ và nghiệm thu

- **D6.4** có hạn 30/09/2024, bản sẵn sàng phản biện 03/02/2025, giao 20/02/2025. Phép trừ của bài cho 126 ngày trước phản biện và 17 ngày sau đó, tổng cộng 143 ngày lịch. Đây là một tài liệu đặc tả dùng chung. Để quy nguyên nhân cho một pilot cần biên bản thay đổi và lịch phụ thuộc. [Bìa, lịch sử phiên bản](https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D6.4-Use-Cases-Specification-and-Pilot-Sites-Preparation.-II.pdf#page=2)
- **Hai người chấm** đều duyệt sáu mục. Trong mỗi điều kiện A và B có sáu quyết định, ba quyết định khớp tham chiếu. Thời gian trung bình A/B là 1,579/1,192 giây, trung vị là 0,757/1,301 giây. Hai chỉ số đi ngược chiều và chỉ đo thao tác bấm. Vòng P5-V1 ở Phụ lục K có bộ phiếu riêng. Bản tự chấm được ghi riêng với kết quả hai phiếu độc lập, có thể kiểm trạng thái tiếp nhận ở [sổ tổng hợp](../results/pilot5_review.json). [Excel tổng hợp](../Cham_doc_lap/Ket_qua/Tong_hop_A_B.xlsx)
- **Ba KPI còn mở trong mẫu sáu KPI Pilot 5** cần ba bằng chứng khác nhau. K04 cần số người dùng đủ điều kiện làm mẫu số của ngưỡng 70%. K05 cần tín hiệu và kết quả đối chiếu có ngày để tính hệ số tương quan. K06 cần hai danh mục cùng kỳ, cùng mức rủi ro để kiểm tra phần tăng theo năm. Giá trị 61,1% là tổng lợi suất MS020 do tác giả bộ dữ liệu công bố. [Ngưỡng và nguồn từng KPI](../results/ket-qua.md) · [Hồ sơ MS020](https://zenodo.org/records/17175084)

### Mục tiêu 5W1H ở cấp dự án

| Câu hỏi | Câu trả lời dùng để ra quyết định |
|---|---|
| What · Xác nhận điều gì? | Mỗi pilot thực hiện ca sử dụng nào, đã bàn giao gì, KPI nào có số đo và căn cứ nào đủ để nghiệm thu hoặc giữ mở? |
| Why · Vì sao cần làm? | Một dịch vụ đã bàn giao vẫn có thể thiếu người dùng, doanh thu, chất lượng dữ liệu hoặc bằng chứng về hiệu quả mô hình. PM cần quyết định riêng cho từng cam kết. |
| Who · Ai chịu trách nhiệm? | Bảng 1 D6.4 chỉ đầu mối từng pilot. FAME báo cáo kết quả lịch sử. Người viết đối chiếu lại tài liệu và chạy kiểm tra. Hai người độc lập thực hiện buổi chấm sáu KPI Pilot 5. |
| Where · Lấy bằng chứng ở đâu? | CORDIS, ba tài liệu WP6, Zenodo và kho mã gốc Pilot 7. GitHub FAME_PM lưu mã của bài, cấu hình phép thử, kết quả và đường dẫn nguồn. |
| When · Dùng kỳ nào? | Xét vòng đời FAME 2023–2025, ghi riêng RP2 từ 01/07/2024 đến 31/12/2025. Buổi chấm tháng 11/2026 là thực nghiệm hồi cứu của học phần. |
| How · Đánh giá thế nào? | Đối chiếu đặc tả, vận hành, kết quả theo pilot. Kiểm ngày và KPI qua ProjectLibre/Excel, tái tính điểm ESG, gọi hàm gốc Pilot 7, đọc kết quả trước/sau theo đúng đối tượng được đo. |

### Mười miền tri thức và bằng chứng đi kèm

| Miền | Quyết định PM có thể giải thích | Vật chứng và điều còn mở |
|---|---|---|
| Tích hợp | Nối bản cam kết D6.4, bản vận hành D6.2 và bản đánh giá D6.3 để xét đóng pilot | A tìm đúng trang ở ba phiên bản. Chưa có chữ ký của từng bên cho mọi quyết định của bài |
| Phạm vi | Giữ 14 ca sử dụng trong phạm vi, xác định rõ phần kỹ thuật nào đã tái tạo | A có ID và trang, số ID đối chiếu chưa khớp tổng công bố. Cần biên bản thống nhất danh mục nếu dùng làm cơ sở hợp đồng |
| Tiến độ | Kiểm tra D6.4 trước khi chuyển phản biện và giữ cả hai mốc ngày trên Gantt | B cho 126 + 17 ngày. Cần lịch phụ thuộc để đánh giá tác động lên ngày hoàn tất toàn dự án |
| Chi phí | Phân biệt cơ cấu tài trợ với chi phí theo pilot trước khi quyết định mở rộng | B đối chiếu CORDIS. Cần sổ chi phí và kỳ hạch toán để tính chênh lệch thực hiện |
| Chất lượng | Kiểm ngưỡng, đơn vị, khóa ghép và trường hợp biên trước khi ký | B kiểm ESG, C phát hiện một cấu hình cần đối soát. Tác động trong nhà máy cần dữ liệu vận hành |
| Nguồn lực | Gắn đầu mối cho ngoại lệ và làm rõ ai có quyền chốt đơn vị cảm biến | Hồi cứu Excel chuyển 0/3 thành 3/3 đầu mối đề xuất. Cần xác nhận nhận việc cùng công suất thực tế |
| Truyền thông | Trả cho người duyệt mã KPI, nguồn, đơn vị và lý do còn mở | A/B/D tạo vết đối chiếu. Hai người vẫn duyệt ba KPI thiếu số đo, cần ghi căn cứ đã đọc nếu làm lại |
| Rủi ro | Phân biệt lỗi cấu hình đã quan sát, nguy cơ ghép sai ngày và rủi ro khách hàng ít sử dụng | P5 thiếu khóa ngày, P6 báo 0 lượt tải, P7 có một ngoại lệ định dạng. Chưa đo xác suất hoặc tiền thiệt hại |
| Mua sắm | Xác nhận giấy phép, điều kiện dùng dữ liệu và tiêu chí bàn giao trước khi mua | Danh mục phần mềm, D6.4 và Zenodo nêu quyền cho từng tài sản. Chưa có hợp đồng, SLA và giá thực trả |
| Các bên liên quan | Tách phản hồi, sử dụng, chấp thuận và giao dịch thương mại | P2 có khảo sát, P6 có hội thảo, P7 có điểm hài lòng và ô giao dịch NA. Cần xác nhận từ đúng nhóm có quyền phê duyệt |

## 2. Phạm vi, số liệu và quyết định theo cả bảy pilot

Số trang dưới đây là số trang **PDF**. Cột kết quả ghi số liệu hoặc mô tả của FAME. Cột cuối ghi diễn giải và điều kiện nghiệm thu do người viết đề xuất. Các mã đầu mối dùng đúng ký hiệu ở D6.4 Bảng 1. [Đặc tả và danh sách ca sử dụng](https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D6.4-Use-Cases-Specification-and-Pilot-Sites-Preparation.-II.pdf#page=12) · [Bản chép kết quả có thể đọc bằng mã](../evidence/pilot-outcomes.csv)

| Pilot, đầu mối, số ca sử dụng | Dữ liệu và sản phẩm thuộc phạm vi | Kết quả do FAME báo cáo | Mã có thể kiểm tra và quyết định của người viết |
|---|---|---|---|
| 1 · FaMLy · MC · 2 | Dữ liệu lịch sử tài chính của Universo, công cụ gợi ý và giao diện ưu đãi. D6.4 tr. 16–23, D6.2 tr. 16 | Hai giải pháp được tích hợp, mục tiêu >2. ROC-AUC dưới ngưỡng 80%, giá trị cụ thể chưa nêu. [D6.3 tr. 19](https://www.fame-horizon.eu/wp-content/uploads/2025/05/FAME-D6.3-Techno-Economic-Evaluation-and-Stakeholders-Feedback.pdf#page=19) | A đối chiếu hồ sơ. Chưa xác minh được bộ hoàn chỉnh gồm mô hình phát hành, nhãn và dự đoán. Tách quyết định bàn giao dịch vụ khỏi quyết định chấp nhận chất lượng mô hình |
| 2 · Ví công dân Athens · DAEM · 2 | Dữ liệu đỗ xe, thanh toán, ưu đãi và khảo sát. D6.4 tr. 24–39, D6.2 tr. 20 | Độ chính xác khoảng 55% lên 82%, hài lòng khoảng 3,7 lên 4,4/5. [D6.3 tr. 28](https://www.fame-horizon.eu/wp-content/uploads/2025/05/FAME-D6.3-Techno-Economic-Evaluation-and-Stakeholders-Feedback.pdf#page=28) | A định vị nguồn. Mức tăng độ chính xác xấp xỉ **27 điểm phần trăm** vì mức nền là ước tính. Cần log đối chiếu chỗ đỗ và cùng cách lấy mẫu để tính lại. D6.4 mô tả một số thành phần có giấy phép riêng |
| 3 · Thông tin thanh toán và AML · BPFI · 2 | Dịch vụ thông tin phục vụ thanh toán và phòng chống rửa tiền. D6.4 tr. 40–51, D6.2 tr. 31 | Từ quy trình thủ công sang ứng dụng tự động, hạ tầng được đưa vào sử dụng. [D6.3 tr. 34](https://www.fame-horizon.eu/wp-content/uploads/2025/05/FAME-D6.3-Techno-Economic-Evaluation-and-Stakeholders-Feedback.pdf#page=34) | A đối chiếu hồ sơ. Đặc tả nói tài liệu thành phần sẽ được đưa lên GitLab, chưa xác nhận bản công khai đủ để chạy cả hai dịch vụ. Cần ca so sánh cùng đầu vào và mốc thời gian để lượng hóa năng suất. [D6.4 tr. 42](https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D6.4-Use-Cases-Specification-and-Pilot-Sites-Preparation.-II.pdf#page=42) |
| 4 · Hồ sơ xin tài trợ EU · INNEUROPE · 1 | Các đợt gọi, dữ liệu người thụ hưởng, khuyến nghị cho ngân hàng. D6.4 tr. 52–58, D6.2 tr. 38 | 15 lên 33 bản ghi. Ba đợt gọi mỗi lần so với mục tiêu ≥4. Thời gian cả hai lần đều <24 giờ. [D6.3 tr. 44](https://www.fame-horizon.eu/wp-content/uploads/2025/05/FAME-D6.3-Techno-Economic-Evaluation-and-Stakeholders-Feedback.pdf#page=44) | A đối chiếu hồ sơ. Thêm 18 bản ghi, nhưng mục tiêu gốc P4-02 là 100% mỗi bộ dữ liệu. Số tổng 33 chưa đủ để xác nhận độ đầy đủ. Muốn kết luận hệ thống nhanh hơn cần dấu thời gian và mẫu so sánh. Mô hình trả theo đầu mối khách hàng còn cần số doanh thu thực thu |
| 5 · ESG và danh mục · KM · 2 | Xếp hạng ESG và tối ưu danh mục, bản xuất ESG/MarketSenseAI. D6.4 tr. 59–71, D6.2 tr. 42 | Lập báo cáo từ >120 xuống <45 phút, 35 người dùng tích cực, hài lòng 4,2/5. [D6.3 Bảng 5](https://www.fame-horizon.eu/wp-content/uploads/2025/05/FAME-D6.3-Techno-Economic-Evaluation-and-Stakeholders-Feedback.pdf#page=52) | B chạy trên CSV tác giả. Công nhận phép tái tính phần điểm đã ghép được. Tỷ lệ sử dụng, tương quan tín hiệu và lợi ích tối ưu danh mục cần hồ sơ riêng. D kiểm tra phép thử checklist của bài |
| 6 · Bảo hiểm khí hậu · NRS · 3 | Định giá bất động sản, rủi ro danh mục bảo hiểm và so sánh phương án danh mục. CMIP, ERA5 là nguồn khí hậu đầu vào. D6.4 tr. 72–76, D6.2 tr. 50 | Đã tải lên dự báo cho 20 thành phố, 1 bộ toàn cầu, 2/5 chỉ số. Số lượt tải ghi nhận cho thành phố, toàn cầu và chỉ số lần lượt là 0, 0, 0. [D6.3 tr. 60](https://www.fame-horizon.eu/wp-content/uploads/2025/05/FAME-D6.3-Techno-Economic-Evaluation-and-Stakeholders-Feedback.pdf#page=60) | A đối chiếu hồ sơ. Đã có đầu ra. Muốn đánh giá độ đúng của định phí cần cấu hình xử lý, vị trí hợp đồng, phơi nhiễm và tổn thất quan sát. [Kế hoạch dữ liệu FAME](https://www.fame-horizon.eu/wp-content/uploads/2023/05/FAME-D1.2-Data-Management-Plan-v3.0.pdf) |
| 7 · Chất lượng và định giá dữ liệu công nghiệp · MOH · 2 | Đánh giá chất lượng, định giá và tạo tài sản dẫn xuất. D6.4 tr. 77–87, D6.2 tr. 54 | 4 tài sản dẫn xuất (đích ≥2), 4,25/5 hài lòng, 3 tài liệu đào tạo. Số tài sản giao dịch là NA. [D6.3 tr. 67](https://www.fame-horizon.eu/wp-content/uploads/2025/05/FAME-D6.3-Techno-Economic-Evaluation-and-Stakeholders-Feedback.pdf#page=67) | C chạy trực tiếp hàm tác giả với cấu hình công khai. Cần nhật ký bán hàng để đánh giá thương mại và chuỗi cảm biến gốc để đánh giá vận hành nhà máy |

**Sai khác cần giữ khi bảo vệ phạm vi.** FAME ghi 121 yêu cầu nghiệp vụ, 23 thành phần/bộ dữ liệu và 65 KPI tại kết luận D6.4. Mã A đếm các ID phân biệt đúng mẫu `P<n>_BR<m>` trong Phụ lục A và được **128**, từ Pilot 1 đến 7 là **33, 15, 0, 7, 21, 35, 17**. Riêng Pilot 3 có yêu cầu được viết bằng mô tả nhưng không có ID khớp mẫu đó trong phụ lục. Hai cách đếm chưa được tác giả đối chiếu. Không nên lấy hiệu hai số làm số yêu cầu phát sinh. Phụ lục G và [ma trận 65 KPI](../FAME_Ma_tran_65_KPI.xlsx) đối chiếu từng dòng đặc tả với hồ sơ kết quả. Sáu KPI dùng để thử checklist ở Pilot 5 có mã liên kết riêng trong ma trận. [Số FAME công bố](https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D6.4-Use-Cases-Specification-and-Pilot-Sites-Preparation.-II.pdf#page=88) · [ID và trang tìm thấy](../results/pilot_portfolio.json)

## 3. Mã nào là của FAME và có thể tái lập tới đâu?

- **Nền tảng chung.** Trang phần mềm do FAME công bố liệt kê 14 mô-đun với chủ sở hữu và tệp ZIP. Ví dụ, GFT và các đối tác cung cấp mã tích hợp, UPRC cung cấp dashboard, UNP cung cấp FDAC Open API. Danh mục ghi Apache 2.0 cho 13 mục và by-nc-nd/4.0 cho mô-đun Trading & Monetization. Đã kiểm tra trực tiếp ZIP tích hợp có các cấu hình triển khai AAI, APM và dashboard. D3.4 còn nêu GitLab của dự án. Bài rà soát chưa triển khai toàn bộ marketplace. [Danh mục chính thức](https://www.fame-horizon.eu/index.html%40p%3D3257.html) · [ZIP tích hợp](https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-integration.zip) · [D3.4 và địa chỉ GitLab](https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D3.4-Secure-Federated-Data-Management-II-1.pdf)
- **Pilot 5.** Có dữ liệu tác giả và kết quả công bố, gồm 12 CSV và 2 PDF trên Zenodo. Danh mục tệp của phiên bản này chưa có chương trình chạy lại chiến lược MS020. D6.4 mô tả nhiều nguồn và điều kiện sử dụng khác nhau cho ESG và công cụ tối ưu. Chưa xác minh được một bản phát hành công khai của tác giả chứa đồng thời mã chiến lược, chuỗi dữ liệu có ngày và cấu hình giao dịch đủ tái lập lợi suất 61,1%. Mã trong `esg-data-audit/` là phần thực nghiệm của người viết. [Zenodo](https://zenodo.org/records/17175084) · [D6.4, thành phần Pilot 5](https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D6.4-Use-Cases-Specification-and-Pilot-Sites-Preparation.-II.pdf#page=62)
- **Pilot 7.** D6.4 nêu đích danh kho IIoT của Innov-Acts, thư viện SAX4BPM của IBM và phần mềm StreamStory của JSI. Bài đã chạy hàm `QualityAssessmentEngine.validate_value` từ commit `d5eb4c69` của kho IIoT. Trong 82 cảm biến cấu hình, 79 có ngưỡng dùng được cho phép thử, 2 không khai báo loại ngưỡng và 1 có giá trị chữ số dùng dấu phẩy khác với SQL khởi tạo. Trên 93 ngưỡng hợp lệ, cả 279 phép thử ngay dưới, đúng bằng và ngay trên ngưỡng trả về kết quả dự kiến. Giá trị thử do bài tạo. Điểm hài lòng 4,25/5 ở trên đến từ khảo sát FAME. [Phần mềm được FAME dẫn](https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D6.4-Use-Cases-Specification-and-Pilot-Sites-Preparation.-II.pdf#page=80) · [Mã gốc đã chạy](https://github.com/giorgosfatouros/IIoT-Data-Quality-Assessment/tree/d5eb4c69addf9078c5d80042ea2229f50a43ed41) · [SAX4BPM](https://github.com/IBM/sax4bpm) · [StreamStory](https://github.com/E3-JSI/StreamStory2)

**Quyết định nghiệm thu Pilot 7 của người viết.** Ở mã cảm biến `75PI823`, CSV ghi `1,799,999,952,316,280` còn SQL ghi `1.799999952316280`. Hai biểu diễn dẫn đến cách nạp số khác nhau. Phép thử loại riêng dòng này và lưu nguyên giá trị. Trước khi dùng để duyệt dữ liệu, bên vận hành cần xác nhận đơn vị, nguồn cấu hình được duyệt và cùng một phép chuyển kiểu cho cả hai đường nạp. Chưa xác định lỗi này từng ảnh hưởng dữ liệu vận hành thực tế. [Dòng CSV](https://github.com/giorgosfatouros/IIoT-Data-Quality-Assessment/blob/d5eb4c69addf9078c5d80042ea2229f50a43ed41/backend/config/tags.csv#L61) · [Dòng SQL](https://github.com/giorgosfatouros/IIoT-Data-Quality-Assessment/blob/d5eb4c69addf9078c5d80042ea2229f50a43ed41/database/init/03_populate_sensor_thresholds.sql#L73)

## 4. Chạy lại từ thư mục gốc

Chuẩn bị môi trường Python chính theo [README](../README.md). Mỗi lệnh kiểm tra dưới đây so kết quả tính lại với kết quả lưu trong Git. Có thể xem cấu trúc kết quả bằng cách bỏ `--check` ở lệnh A hoặc C.

**A. Đối chiếu cả bảy pilot từ tài liệu tác giả.** Lệnh tải ba bản PDF công khai, khớp SHA-256, đọc trực tiếp Bảng 1 và Phụ lục A trong D6.4, tìm trang về vận hành trong D6.2 và trang kết thúc bảng kết quả tương ứng trong D6.3. Số đo đánh giá ở bảng trên do người viết chép từ trang đã dẫn. Lệnh này kiểm chỉ mục và số lượng, còn giá trị KPI cần đối chiếu bằng mắt trên PDF.

```bash
python -m pip install -r report/requirements.txt
python -m fame_pm.portfolio --data-dir du_lieu/portfolio --download --check
```

**B. Kiểm lịch, Excel, tài trợ và tái lập ESG.** Đồng thời đối chiếu 12 CSV gốc với bản phát hành đã chọn. Bỏ `--download` để chạy ngoại tuyến sau lần tải.

```bash
python -m unittest discover -s tests -v
python -m fame_pm --check --download --data-dir du_lieu
python Pilot5_nghiem_thu/verify.py --data-dir du_lieu --check
```

**C. Chạy thành phần Pilot 7 từ mã của đối tác.** Ví dụ dưới đây dùng Python 3.12 và shell macOS/Linux, từ thư mục gốc FAME_PM. Giữ môi trường của worker tách khỏi môi trường soạn báo cáo. Phép thử nạp bảng cấu hình vào bộ nhớ và gọi hàm gốc. Không cần máy chủ cơ sở dữ liệu cho kịch bản này.

```bash
git clone https://github.com/giorgosfatouros/IIoT-Data-Quality-Assessment.git du_lieu/pilot7-upstream
git -C du_lieu/pilot7-upstream checkout --detach d5eb4c69addf9078c5d80042ea2229f50a43ed41
python3.12 -m venv du_lieu/pilot7-env
du_lieu/pilot7-env/bin/python -m pip install -r du_lieu/pilot7-upstream/worker/requirements.txt
du_lieu/pilot7-env/bin/python -m fame_pm.pilot7 --checkout du_lieu/pilot7-upstream --check
```

**D. Tính lại buổi chấm độc lập.** Bản công khai kiểm tra được bảng tổng hợp. Điều phối viên có hai CSV gốc chạy thêm lệnh thứ hai với thư mục chứa phiếu đã hoàn tất.

```bash
python -m fame_pm --check
python -m fame_pm --check --reviews-dir "/duong/dan/thu_muc_phieu"
```

## 5. Trước khi nộp

| Việc cần kết luận | Tình trạng | Bằng chứng cần thêm nếu muốn mở rộng kết luận |
|---|---|---|
| Bài có dữ liệu thật, có công cụ quản lý và có thử nghiệm so sánh? | Có. Có cả phép tính kiểm độc lập với số tác giả và kết quả âm của buổi chấm. [Kết quả](../results/ket-qua.md) | Nếu giảng viên yêu cầu đúng định dạng .mpp, xác nhận điều kiện nộp. Hiện có .pod, XML và ảnh Gantt |
| Phạm vi có bao quát toàn FAME? | Phần hồ sơ đối chiếu 65/65 KPI trên 7 pilot. Đã chạy hai phép thực nghiệm kỹ thuật riêng ở P5 và P7. [Ma trận nguồn](../evidence/kpi_matrix.csv) | Đã rà đủ 25 dòng từng mở, chốt 2 và còn 23. Đợt kiểm thử tiếp theo đã phân loại cả 23 hồ sơ, chạy phần kiểm được và xác định trường dữ liệu cần xin. [Kết quả chạy lại](kiem-thu-23-kpi.md). [Bằng chứng và điều kiện đóng từng dòng](../evidence/kpi_review.csv). P1-02 được FAME ghi không áp dụng. Chín dòng có bằng chứng dưới ngưỡng |
| Checklist có hiệu quả gì? | Có cải thiện khả năng theo dõi ba hồ sơ thiếu bằng chứng trong hồi cứu. Hai người chấm chưa cho thấy độ chính xác tăng | Muốn chứng minh hiệu quả với người dùng thực cần thêm hồ sơ, người chấm, căn cứ họ đã xem, thời gian đọc đến lúc quyết định và cơ chế xử lý bất đồng |
| Dự án có tiết kiệm chi phí hoặc tạo doanh thu? | Có cơ cấu tài trợ và có mô tả mô hình kinh doanh. Chưa có số tiền tiết kiệm hay doanh thu thực hiện cho từng pilot | Cần sổ chi phí hoặc giao dịch theo phạm vi, thời kỳ và phương án so sánh |
| Nếu chỉ được nộp một PDF? | Phụ lục F tóm lược đủ bảy pilot, Phụ lục D–E ghi phép kiểm ESG ban đầu. Phụ lục K ghi lượt xác nhận đủ 100 mã và tình trạng phiếu P5-V1. Kho GitHub là nguồn thực hành chính | Đối chiếu yêu cầu hành chính của lớp về định dạng, thông tin bìa và chữ ký trước khi gửi. Lưu mã commit nộp bài để người chấm mở đúng phiên bản |
