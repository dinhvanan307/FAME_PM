# Phân tích FAME từ quyết định tài trợ đến khai thác sau dự án

*Federated decentralized trusted dAta Marketplace for Embedded finance* (FAME) là dự án châu Âu xây dựng một thị trường dữ liệu cho tài chính nhúng. Các tổ chức có thể công bố, tìm, trao đổi và sử dụng dữ liệu, mô hình AI hoặc dịch vụ phân tích qua một đầu mối chung. Trong thí điểm số 5, hai công ty quản lý tài sản dùng dữ liệu thị trường và dữ liệu môi trường, xã hội, quản trị (ESG) để xếp hạng tài sản và tối ưu danh mục. Đó là tình huống có thể theo dõi từ nhu cầu kinh doanh đến kết quả sử dụng. [Hồ sơ FAME của Ủy ban châu Âu][fact] · [Hồ sơ Pilot 5][p5]

**Đánh giá của người viết.** Có bằng chứng FAME đã bàn giao nền tảng và rút ngắn thời gian tạo báo cáo trong Pilot 5. Việc người dùng có tiếp tục sử dụng, tín hiệu AI có hỗ trợ quyết định đầu tư, và nền tảng có tự trang trải được chi phí sau tài trợ là ba câu hỏi riêng. Chúng cần ba loại dữ liệu khác nhau. [Kết quả Pilot 5, Bảng 5][eval48] · [Công bố chuyển sang khai thác][live]

## 1. Năm 2022 — Vì sao dự án được tài trợ?

Một tổ chức có thể sở hữu lịch sử giá, tổ chức khác có bảng điểm ESG và tổ chức thứ ba có mô hình tối ưu danh mục. Để kết hợp các tài sản này, bên sử dụng phải tìm được nguồn phù hợp, hiểu ý nghĩa dữ liệu, xác định quyền sử dụng và có cách tiếp nhận kết quả. FAME chủ trương xây dựng hạ tầng chung để các bên giải quyết những việc đó. Dự án kế thừa hạ tầng i3-Market, bổ sung cơ chế trao đổi giữa nhiều nhà cung cấp, định giá và giao dịch tài sản dữ liệu, cùng các công cụ phân tích đáng tin cậy. [Mục tiêu dự án trên CORDIS][fact]

Ủy ban châu Âu ký thỏa thuận tài trợ số **101092639 ngày 16/11/2022**. GFT Italia là bên điều phối. Thời gian dự án được ghi nhận từ **01/01/2023 đến 31/12/2025**. Nguồn lực phải tạo ra cả hạ tầng dùng chung lẫn các thí điểm để kiểm tra hạ tầng có hỗ trợ công việc thực tế hay không. [Hồ sơ và thời hạn dự án][fact] · [Mô tả dự án của Ủy ban châu Âu][ec]

**Phân tích của người viết.** Dự án có hai nhóm người dùng với động cơ khác nhau. Nhà cung cấp cần kiểm soát điều kiện sử dụng tài sản. Chuyên viên phân tích cần tìm được dữ liệu đủ rõ để đưa vào công việc. Nếu chỉ đo số tài sản được đăng lên, ban điều phối có thể biết phía cung đã tham gia, nhưng còn thiếu bằng chứng về giá trị ở phía sử dụng.

## 2. Năm 2023 — Biến mục tiêu thành phạm vi và trách nhiệm

Nhóm dự án thu yêu cầu chung từ tài liệu và tổ chức workshop riêng cho từng thí điểm. Tại các workshop, đối tác nghiệp vụ diễn đạt nhu cầu dưới dạng câu chuyện người dùng, rồi cùng đội kỹ thuật chuyển thành yêu cầu chức năng. Bản D2.1 bàn giao ngày **31/07/2023** ghi **38 yêu cầu chung** và **116 yêu cầu nghiệp vụ riêng của các pilot**. Đây là số liệu của phiên bản này. Trong D6.4, khi việc chuẩn bị các pilot hoàn tất, nhóm báo cáo **121 yêu cầu nghiệp vụ, 23 thành phần hoặc tập dữ liệu và 65 KPI**. Hai số đếm yêu cầu thuộc hai tài liệu ở hai thời điểm. Muốn xác định yêu cầu cụ thể nào được thêm, đổi hoặc gộp, cần đối chiếu từng mã. [D2.1, tóm tắt và phương pháp lấy yêu cầu][req] · [D6.4, kết luận, tr. 84][spec84]

Một ví dụ là yêu cầu **P5_BR1** của Pilot 5. JRC và KM Cube cần xếp hạng tài sản theo ESG và công bố kết quả qua thị trường dữ liệu. Theo phân tích của người viết, để kiểm thử yêu cầu này cần chuẩn hóa mã tài sản và nguồn điểm, xác định trọng số, tạo bảng xếp hạng, mô tả cách tính và cho phép người dùng truy cập. Yêu cầu **P5_BR10** đi thêm một bước, tối ưu danh mục theo sở thích ESG của khách hàng. Hai đầu ra có quan hệ với nhau nhưng cần phép kiểm tra riêng. [D6.4, mục 3.5][spec55] · [D6.4, Phụ lục A5][spec90]

Song song với thiết kế tính năng, kế hoạch quản lý dữ liệu D1.2 quy định trách nhiệm bảo vệ dữ liệu tại từng đối tác và vai trò phụ trách an ninh của GFT. Tài liệu ghi các biện pháp như kiểm soát truy cập, kiểm tra tính toàn vẹn, sao lưu và phối hợp xử lý khi có sự cố. [D1.2, tr. 36–37][dmp36]

**Phân tích của người viết.** Với P5_BR1, PM cần biết ai chịu trách nhiệm về dữ liệu đầu vào, ai xác nhận cách tính và ai kiểm tra sản phẩm công bố. Với P5_BR10, PM còn phải thống nhất tiêu chí chất lượng của danh mục. Một bảng xếp hạng hiển thị đúng chỉ xác nhận một phần của chuỗi công việc.

## 3. Năm 2024 — Xây nền tảng rồi tích hợp các nhóm

Công việc kỹ thuật trải qua các gói kiến trúc nền tảng, quản lý dữ liệu liên kết, định giá và giao dịch, phân tích AI, rồi tích hợp vào các pilot. Tại kỳ họp ở Amsterdam ngày **26–27/03/2024**, các đối tác rà soát tiến độ kỹ thuật và thảo luận cách quản trị một hạ tầng liên kết. Bản D4.2 bàn giao ngày **23/05/2024** mô tả phiên bản đầu của ba nhóm chức năng gồm giao dịch và thương mại hóa, hỗ trợ định giá và tìm kiếm theo ngữ nghĩa. Nhóm mô tả đây là phiên bản khả dụng ở mức cơ bản. [Biên bản tường thuật kỳ họp Amsterdam][amsterdam] · [D4.2, trang bìa và kết luận][trade]

**Cách hệ thống tạo giá trị trong một lần sử dụng.** Nhà cung cấp đăng mô tả của một tài sản dữ liệu và điều kiện tiếp cận. Bên có nhu cầu tìm tài sản trong danh mục, kiểm tra mức phù hợp và quyền sử dụng. Công cụ phân tích nhận dữ liệu được phép dùng để tạo xếp hạng hoặc danh mục. Một số đầu ra lại có thể được công bố như tài sản cho người dùng khác. Đây là diễn giải của người viết từ chức năng nền tảng và hồ sơ Pilot 5. [Mô tả nền tảng][ec] · [Sản phẩm và người dùng của Pilot 5][p5]

Trong kỳ báo cáo cuối, FAME mô tả cơ chế điều phối qua các cuộc họp trưởng gói công việc, họp toàn thể và báo cáo kỹ thuật, hành chính sáu tháng một lần từ từng đối tác. Cơ chế này cho phép nhìn vào phụ thuộc giữa các nhóm, ví dụ công cụ phân tích đã chạy nhưng dữ liệu đầu vào hoặc quyền truy cập của đối tác sử dụng vẫn còn thiếu. Tình huống cuối là ví dụ quản lý của người viết. [Báo cáo kỳ hai, phần điều phối][rp]

## 4. Cuối 2024 đến đầu 2025 — Ngày giao trễ nói lên điều gì?

Bảng dưới so sánh trường ngày đến hạn và ngày bàn giao trên bìa cùng một tài liệu. **Chênh lệch do người viết tính theo ngày lịch.** Đây là các mốc có thể kiểm tra, không phải toàn bộ lịch dự án.

| Sản phẩm | Đến hạn | Bàn giao | Chênh lệch |
|---|---|---|---|
| D1.2 — Kế hoạch quản lý dữ liệu | 30/06/2023 | 29/06/2023 | Sớm 1 ngày. [Nguồn][dmp] |
| D4.2 — Phiên bản đầu công cụ giao dịch và định giá | 31/03/2024 | 23/05/2024 | Muộn 53 ngày. [Nguồn][trade] |
| D6.4 — Bản đặc tả thí điểm lần II | 30/09/2024 | 20/02/2025 | Muộn 143 ngày. [Nguồn][spec] |
| D6.3 — Báo cáo đánh giá các thí điểm | 31/12/2025 | 23/12/2025 | Sớm 8 ngày. [Nguồn][eval] |

D6.4 cho biết nhóm tiếp tục cập nhật tài sản dữ liệu ngày **21/11/2024**, cập nhật KPI và việc tham gia của các bên ngày **17/01/2025**, chuyển sang phản biện nội bộ ngày **03/02/2025**, ghi nhận ý kiến phản biện ngày **12/02/2025** và hoàn thiện bản cuối ngày **20/02/2025**. UNP chủ trì, ATOS và JRC phản biện, UPRC phụ trách bảo đảm chất lượng và điều phối viên chấp thuận. [D6.4, bìa và lịch sử phiên bản][hist]

**Phép tính và diễn giải của người viết.** Từ hạn giao đến khi có bản sẵn sàng phản biện là **126 ngày**. Từ mốc này đến khi bàn giao là **17 ngày**. Điểm đáng điều tra nằm ở quá trình chuẩn bị đầu vào trước phản biện. Hồ sơ không cho biết một nhóm cụ thể đã gây chậm, chi phí làm lại là bao nhiêu hoặc lịch kết thúc dự án sẽ thay đổi thế nào nếu D6.4 giao đúng hạn. Muốn trả lời, cần nhật ký vấn đề, chi phí và lịch cơ sở có quan hệ phụ thuộc. [D6.4, lịch sử phiên bản][hist]

## 5. Năm 2025 — Theo dấu Pilot 5 từ đầu vào đến người sử dụng

| Bước | FAME thực hiện | Câu hỏi quản lý của người viết |
|---|---|---|
| Chuẩn bị dữ liệu | Tập hợp mã chứng khoán, giá và chuỗi thời gian, điểm ESG, thông tin mô tả. [Đặc tả pilot][spec55] | Đội dự án có xác định cùng mã, cùng kỳ dữ liệu và cùng phương pháp chấm điểm không? |
| Phân tích | Kết hợp điểm ESG và dữ liệu tài chính, áp dụng trọng số theo hồ sơ, tạo xếp hạng và phương án phân bổ. [Hai tình huống sử dụng][spec55] | Khi người dùng thay đổi trọng số, chuyên viên có giải thích được vì sao kết quả thay đổi không? |
| Bàn giao | Cung cấp bảng xếp hạng, khuyến nghị theo tháng, dữ liệu danh mục tối ưu và công cụ hỗ trợ so sánh. [Hồ sơ đầu ra][p5] | Loại sản phẩm, chu kỳ cập nhật và đối tượng dùng có phù hợp với yêu cầu đã ghi không? |
| Kiểm chứng | Kiểm tra nội bộ tháng **01/2025**, tổ chức buổi chung Đức – Hy Lạp tháng **06/2025** và trình diễn ngày **13/11/2025**. [D6.3, tr. 50–51][eval50] | Kết quả nào chỉ được trình diễn? Kết quả nào có phép đo và đủ dữ liệu để đối chiếu với mục tiêu? |

**Ví dụ minh họa của người viết.** Giữ nguyên danh sách tài sản và ngày dữ liệu, tăng mức ưu tiên yếu tố môi trường trong một hồ sơ đầu tư. Người thử xem thứ hạng và tỷ trọng danh mục thay đổi ra sao, rồi kiểm tra xem hệ thống có giải thích được sự thay đổi qua các thành phần điểm không. Ví dụ này minh họa cách kiểm thử một yêu cầu tài chính có AI. Bằng chứng đo mà FAME công bố được trình bày dưới đây. [Đặc tả Pilot 5][spec55] · [Bài học nhóm pilot ghi nhận][less]

## 6. Nghiệm thu — Đã chứng minh được những kết quả nào?

Mục tiêu có trong Bảng 43 của D6.4. Kết quả dưới đây do nhóm FAME báo cáo ở Bảng 5 của D6.3. Cột cuối là đánh giá của người viết. [Bảng mục tiêu][targets] · [Bảng kết quả, tr. 48–50][eval48]

| Chỉ tiêu | Mục tiêu | Kết quả báo cáo | Đánh giá |
|---|---:|---|---|
| Thời gian trung bình từ nhập dữ liệu đến tạo báo cáo | ≤ 1 giờ | Trước > 2 giờ, sau < 45 phút. [Tr. 50][eval50] | Đạt trong quy trình thí điểm. |
| Điểm hài lòng về công cụ | ≥ 4,0/5 | 4,2/5. [Tr. 49][eval49] | Đạt theo điểm khảo sát đã công bố. |
| Số bên liên quan tích cực sử dụng công cụ | ≥ 30 | 35. [Tr. 48][eval48] | Đạt chỉ tiêu đếm. |
| Tỷ lệ người dùng mục tiêu sử dụng công cụ | ≥ 70% | Phản hồi tích cực về định tính. [Tr. 48][eval48] | Thiếu mẫu số và tỷ lệ quan sát để xác nhận. |
| Tương quan tín hiệu tin tức với hiệu suất | ≥ 50% | Tín hiệu bước đầu tích cực. [Tr. 50][eval50] | Chưa có hệ số tương quan đo được. |
| Mức cải thiện hiệu quả danh mục | ≥ 3% mỗi năm | Đã trình diễn trong môi trường thử. [Tr. 49][eval49] | Chưa có số liệu lợi suất đối chiếu ở cùng mức rủi ro. |

**Phép tính của người viết.** Từ hơn 120 phút xuống dưới 45 phút có nghĩa là tiết kiệm **hơn 75 phút** cho quy trình được so sánh. Đây là kết luận thực tế nhất đối với chuyên viên làm báo cáo. Để kết luận công cụ giúp đầu tư hiệu quả hơn, còn cần chuỗi hiệu suất, danh mục tham chiếu và điều kiện so sánh. [D6.3, Bảng 5][eval50]

## 7. Chi phí, rủi ro và những quyết định phải theo dõi suốt dự án

CORDIS ghi **tổng chi phí 16.621.394,20 EUR** và **đóng góp của EU 12.889.656,25 EUR**. Người viết tính tỷ lệ tài trợ là **77,55%**, phần còn lại là **3.731.737,95 EUR**. Riêng JRC có tổng chi phí tham gia **826.250 EUR** và phần EU đóng góp ròng **578.375 EUR**. Các giá trị của JRC bao quát hoạt động của tổ chức trong FAME. Hồ sơ này chưa tách phần chi riêng của Pilot 5 hoặc đối chiếu ngân sách cơ sở với thực chi theo kỳ. Vì vậy, chưa đủ căn cứ kết luận vượt ngân sách hay tính lợi tức đầu tư của pilot. [Hồ sơ chi phí toàn dự án và từng đối tác][fact]

| Rủi ro | Bằng chứng trong dự án | Quyết định của PM theo phân tích của người viết |
|---|---|---|
| Quyền sử dụng dữ liệu có thể chặn thử nghiệm | Ở Pilot 6, một bên liên quan lo ngại việc pháp chế và tuân thủ có cho phép dùng nền tảng. Đây là lo ngại được ghi nhận tại thời điểm đó. [D6.4, tr. 73][risk6] | Xác nhận quyền và phạm vi dữ liệu trước khi chốt lịch thử với bên đó. |
| Người dùng khó tin cách xếp hạng | Pilot 5 ghi nhận nhu cầu làm rõ nguồn, trọng số và cách hình thành điểm. [D6.3, bài học Pilot 5][less] | Bàn giao phiên bản nguồn dữ liệu và cách tính cùng bảng xếp hạng. |
| Quyết định nhân rộng vượt quá bằng chứng | Công cụ có người tham gia, nhưng KPI tỷ lệ sử dụng chưa có số đo. [D6.3, tr. 48][eval48] | Xác định nhóm đủ điều kiện, kỳ quan sát và hành vi được tính là sử dụng trước khi mở rộng. |

## 8. Khép lại năm 2025 và khai thác từ năm 2026

Báo cáo kỳ cuối ghi nhận **7 thí điểm đã triển khai**, **21 mô hình AI/ML đã huấn luyện và công bố**, cùng **660+ tài sản được lập chỉ mục**. Mục tiêu ban đầu là danh mục có 1.000+ tài sản. Theo đánh giá của người viết, con số 660+ được lập chỉ mục chỉ cho biết giới hạn dưới và chưa đủ để xác định tỷ lệ hoàn thành mục tiêu. [Mục tiêu trong hồ sơ tài trợ][fact] · [Số liệu kỳ cuối][rp] FAME kết thúc theo hồ sơ tài trợ ngày **31/12/2025**. Ngày **13/04/2026**, liên danh thông báo hệ sinh thái đã hoạt động trong môi trường production, gồm marketplace và hạ tầng để tổ chức gia nhập liên kết. Thông báo xác nhận một bước chuyển sang khai thác. Hồ sơ đã đối chiếu chưa có doanh thu hoặc tỷ lệ duy trì khách hàng để đánh giá khả năng tự trang trải. [CORDIS, kết quả kỳ cuối][rp] · [Thông báo vận hành của liên danh][live]

**Kết luận của người viết.** Nếu phải ra quyết định tại thời điểm kết thúc FAME, tôi sẽ ghi nhận ba việc khác nhau. Một, có bằng chứng bàn giao nền tảng và triển khai các pilot. Hai, Pilot 5 chứng minh được cải thiện thời gian làm báo cáo trong điều kiện thử nghiệm. Ba, quyết định đầu tư nhân rộng cần thêm số người dùng quay lại, hiệu quả phân tích tài chính trên dữ liệu đối chiếu và chi phí vận hành riêng. Chính khoảng cách giữa ba quyết định này khiến FAME trở thành một tình huống quản lý dự án đáng nghiên cứu.

[fact]: https://cordis.europa.eu/project/id/101092639
[rp]: https://cordis.europa.eu/project/id/101092639/reporting
[ec]: https://digital-strategy.ec.europa.eu/en/news/fame-project-federated-decentralised-trusted-data-marketplace-embedded-finance
[amsterdam]: https://www.fame-horizon.eu/fame-takes-stock-of-the-latest-progress-made-in-the-project-at-its-3rd-general-assembly/
[live]: https://www.fame-horizon.eu/news/
[p5]: https://www.fame-horizon.eu/wp-content/uploads/2025/12/Pilot-5_ok.pdf
[req]: https://www.fame-horizon.eu/wp-content/uploads/2023/05/FAME-D2.1-_-Requirements-Analysis-Specifications-and-Co_Creation.pdf
[dmp]: https://www.fame-horizon.eu/wp-content/uploads/2023/05/FAME-D1.2-Data-Management-Plan-v3.0.pdf
[dmp36]: https://www.fame-horizon.eu/wp-content/uploads/2023/05/FAME-D1.2-Data-Management-Plan-v3.0.pdf#page=41
[trade]: https://www.fame-horizon.eu/wp-content/uploads/2025/05/FAME-D4.2-Pricing-Trading-and-Monetization-Techniques-I.pdf
[spec]: https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D6.4-Use-Cases-Specification-and-Pilot-Sites-Preparation.-II.pdf
[spec55]: https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D6.4-Use-Cases-Specification-and-Pilot-Sites-Preparation.-II.pdf#page=59
[spec90]: https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D6.4-Use-Cases-Specification-and-Pilot-Sites-Preparation.-II.pdf#page=94
[spec84]: https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D6.4-Use-Cases-Specification-and-Pilot-Sites-Preparation.-II.pdf#page=88
[hist]: https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D6.4-Use-Cases-Specification-and-Pilot-Sites-Preparation.-II.pdf#page=2
[risk6]: https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D6.4-Use-Cases-Specification-and-Pilot-Sites-Preparation.-II.pdf#page=77
[targets]: https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D6.4-Use-Cases-Specification-and-Pilot-Sites-Preparation.-II.pdf#page=69
[eval]: https://www.fame-horizon.eu/wp-content/uploads/2025/05/FAME-D6.3-Techno-Economic-Evaluation-and-Stakeholders-Feedback.pdf
[eval48]: https://www.fame-horizon.eu/wp-content/uploads/2025/05/FAME-D6.3-Techno-Economic-Evaluation-and-Stakeholders-Feedback.pdf#page=52
[eval49]: https://www.fame-horizon.eu/wp-content/uploads/2025/05/FAME-D6.3-Techno-Economic-Evaluation-and-Stakeholders-Feedback.pdf#page=53
[eval50]: https://www.fame-horizon.eu/wp-content/uploads/2025/05/FAME-D6.3-Techno-Economic-Evaluation-and-Stakeholders-Feedback.pdf#page=54
[less]: https://www.fame-horizon.eu/wp-content/uploads/2025/05/FAME-D6.3-Techno-Economic-Evaluation-and-Stakeholders-Feedback.pdf#page=73
