# Phân tích quyết định quản lý dự án FAME

Khi nghiệm thu Pilot 5, trưởng dự án đứng trước ba câu hỏi. Tệp dữ liệu có cho đúng kết quả số học mà đối tác đã xuất? Công cụ có đáp ứng yêu cầu người dùng? Bằng chứng có đủ để mở rộng đầu tư? Ba câu hỏi này dẫn tới ba quyết định khác nhau. Lần đầu người viết tái tạo điểm E/S/G cho 91 mã. Lượt xác nhận trên cùng bản dữ liệu kiểm đủ 100 mã. Ba KPI nghiệp vụ có số đo được nghiệm thu riêng. Quyết định nhân rộng vẫn cần bằng chứng vận hành. Báo cáo kết quả kỳ cuối của FAME và bộ dữ liệu công bố cung cấp bằng chứng ở những cấp khác nhau. [Hồ sơ vòng đời](../FAME_Phan_tich_vong_doi_du_an.md) · [Kết quả do mã tính](../results/ket-qua.md)

## 1. Xác định đối tượng quản lý và đơn vị quan sát

FAME là dự án xây dựng thị trường dữ liệu cho tài chính nhúng. Phạm vi toàn dự án bao gồm nền tảng, các đối tác cung cấp tài sản dữ liệu, các dịch vụ và các thí điểm. Pilot 5 chỉ là một nhánh sử dụng nền tảng. Trong nhánh này, chuyên viên có thể đọc điểm ESG, điều chỉnh mức ưu tiên E/S/G và so sánh danh mục. Một chương trình tái tạo phép tính trên bản xuất công khai kiểm tra được một phần của chuỗi giá trị đó. Các hành vi như tiếp tục dùng sản phẩm sau thử nghiệm hay thay đổi quyết định đầu tư cần nguồn đo riêng. [Mô tả Pilot 5](https://www.fame-horizon.eu/wp-content/uploads/2025/12/Pilot-5_ok.pdf)

| Đơn vị quan sát | Câu hỏi | Mẫu và đối chứng | Kết luận có thể bảo vệ |
|---|---|---|---|
| Sản phẩm bàn giao | Sản phẩm giao sớm hay trễ? | 32 bìa có cùng hai trường ngày; đối chiếu với lịch tái dựng | Sai lệch ngày lịch của từng sản phẩm |
| Giá trị điểm E/S/G | Công thức có tái tạo được số đã xuất? | Dòng đầu hiệu chuẩn, 603 dòng giữ lại; đối chứng giữ nguyên điểm gốc | Độ nhất quán số học trên tập ghép được |
| Danh sách 5 mã dẫn đầu | Quyết định chọn tài sản có nhạy với trọng số? | Cùng một dòng, cùng 100 mã và quy tắc đồng điểm, thay duy nhất trọng số | Thay đổi thành phần hoặc thứ tự của danh sách |
| Hồ sơ nghiệm thu | Khi dùng checklist, hồ sơ còn thiếu có rõ đầu mối hơn? | Cùng 6 KPI, nhận xét lưu trước đó và hồ sơ sau rà soát | Mức đầy đủ của hồ sơ tại thời điểm ghi nhận |
| Quyết định của người chấm | Hiển thị gợi ý có thay đổi cách duyệt? | 2 người, 6 KPI, 12 lần bấm; mỗi KPI xuất hiện ở cả A và B | Mức khớp tham chiếu và thời gian thao tác trong buổi thử |

Cách chọn mẫu ảnh hưởng trực tiếp đến kết luận. Phần tiến độ bao phủ cả 32 báo cáo trong danh mục công khai đã rà. Mỗi quan sát là một sản phẩm có bìa, các công việc nội bộ cần nguồn lịch riêng. Sáu KPI được chọn vì liên quan đến người dùng và quy trình ESG. Có KPI có số đo, có KPI chỉ có bằng chứng định tính. Tỷ lệ khớp trong bài tập mô tả khả năng ra quyết định trên tập này. Không dùng nó làm tỷ lệ thành công của tất cả các thí điểm.

## 2. Tích hợp và phạm vi

### Tích hợp

Chuỗi bằng chứng đi từ đặc tả nghiệp vụ đến công cụ, bản xuất dữ liệu, phiên bản dùng để kiểm tra và quyết định nghiệm thu. Ở mỗi điểm chuyển giao, đầu ra trước đó trở thành điều kiện đầu vào cho nhóm tiếp theo. D6.4 ghi một phiên bản đặc tả chung cho nhiều pilot. D6.3 ghi nhận kết quả sử dụng. Một bảng dữ liệu tải từ Zenodo có phiên bản riêng. Khi review, PM cần ghi cả ba định danh để người sau biết mình đang xác nhận cái gì. Nếu thay bản đặc tả nhưng vẫn lấy ngưỡng từ workbook cũ, phép tính có thể đúng với một cam kết đã hết hiệu lực. [Sổ nguồn](../evidence/README.md)

**Quyết định đề xuất.** Tại buổi xác nhận đầu ra, đính phiên bản đặc tả, phạm vi pilot, kỳ đo, tham chiếu dữ liệu và kết luận của người duyệt vào cùng hồ sơ. Trong repo này, mã nối ngày bìa với UID của sản phẩm trong ProjectLibre, và nối mã KPI với hai trang nguồn. Một sai lệch giữa hai bản ghi được phát hiện ngay ở lần chạy kiểm tra. Với phụ thuộc tổ chức, PM vẫn cần chủ sở hữu xác nhận thay đổi bằng nhật ký quyết định.

### Phạm vi

P5_BR1 liên quan đến xếp hạng tài sản, còn P5_BR10 liên quan đến tối ưu danh mục theo sở thích ESG. Công sức để nghiệm thu hai yêu cầu khác nhau. Đối với xếp hạng, có thể cung cấp tập tài sản, bộ điểm đầu vào, trọng số, quy tắc xử lý đồng điểm và danh sách đầu ra để bên thứ hai chạy lại. Đối với tối ưu danh mục, còn cần vị thế, giá giao dịch, kỳ tái cân bằng, mô hình phí, danh mục chuẩn và ràng buộc rủi ro. Người duyệt phải có khả năng kiểm tra cả điều kiện “cùng mức rủi ro” trong đặc tả. [D6.4, phụ lục A5](https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D6.4-Use-Cases-Specification-and-Pilot-Sites-Preparation.-II.pdf#page=94)

**Ảnh hưởng đến phạm vi bàn giao.** Có thể đóng gói bài toán tái tính điểm độc lập với gói kiểm chứng hiệu quả đầu tư. Lượt đầu ghi chín ngoại lệ do chưa ghép được với một ngành duy nhất. Lượt sau đóng cả chín về tái tạo điểm theo từng dòng. Bảng phân ngành nội bộ vẫn cần chủ dữ liệu xác nhận. Nếu một hồ sơ ghi chung “ESG đã đạt”, người đọc khó xác định phần nào còn nằm ngoài kiểm thử. [Danh sách ngoại lệ ban đầu](../esg-data-audit/reproduction.json) · [Kết quả xử lý từng mã](../Pilot5_nghiem_thu/phep_do.json)

## 3. Tiến độ và chi phí

### Tiến độ

Đối chiếu 32 cặp ngày cho thấy 22 bản giao trễ, chín bản giao sớm và một bản giao đúng ngày. Trung vị có dấu là +22 ngày. Cả sáu bản ở WP3 và sáu bản ở WP4 đều có ngày giao sau hạn trên bìa. Đây là tín hiệu để PM kiểm tra lịch cơ sở theo gói công việc. D6.4 (+143 ngày) được chọn để phân tích tiếp vì có lịch sử phiên bản, phạm vi của nó gồm các thí điểm. [Ngày nguồn và phiên bản của từng sản phẩm](../evidence/deliverables.csv)

Khi quyết định có cần mở vấn đề tiến độ hay không, PM cần xác định đúng lần nộp và hạn được duyệt. D7.2 ghi +333 ngày cho bản nộp lại. D5.4 đổi từ trễ 182 ngày sang sớm một ngày nếu chọn cuối M33. D3.5 và D3.6 đều trễ theo cả hai cách đọc hạn (+122 hoặc +31). D6.1 có thông tin nộp ở M10 và nộp lại ở M20 trong D6.4. Nếu tạm tách cả năm hồ sơ cần làm rõ, 17/27 bản còn lại giao trễ và trung vị là +15 ngày. Phép kiểm tra độ nhạy này do người viết thực hiện. [D7.2, lịch sử phiên bản](https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D7.2-Dissemination-Communication-and-Standardization-Activities-I-v1.1.pdf.pdf#page=2) · [D6.4, tr. PDF 88](https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D6.4-Use-Cases-Specification-and-Pilot-Sites-Preparation.-II.pdf#page=88) · [Sổ hạn và ghi chú](../evidence/deliverables.csv)

Từ hạn 30/09/2024 tới bản sẵn sàng phản biện ngày 03/02/2025 là 126 ngày. Từ lúc đó tới ngày giao 20/02/2025 thêm 17 ngày. Các cập nhật về tài sản, KPI và tham gia của đối tác nằm trong khoảng đầu. Những mốc này hướng câu hỏi của PM về thời điểm đầu vào sẵn sàng. Chúng chưa đo số ngày một người làm việc, thời gian chờ bắt buộc hoặc nguyên nhân gốc. Muốn kết luận về nguyên nhân cần phiếu thay đổi, ngày yêu cầu bổ sung, ngày phản hồi và kết luận xử lý. Muốn kết luận về ngày kết thúc toàn dự án cần lịch phụ thuộc cơ sở và độ dự trữ. [Lịch sử phiên bản D6.4](https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D6.4-Use-Cases-Specification-and-Pilot-Sites-Preparation.-II.pdf#page=2)

**Quyết định đề xuất.** Lập mốc kiểm tra mức sẵn sàng của đầu vào trước khi chuyển phản biện. Ghi rõ phiên bản yêu cầu, dữ liệu đến từ đối tác nào và tiêu chí nào còn mở. Khi so với lịch, xem đồng thời hạn gốc và ngày giao thực tế, kể cả với sản phẩm đã hoàn thành. Một lần chuyển hạn có thể xóa dấu vết của sai lệch nếu chỉ giữ ngày mới. Kỳ RP2 trong lịch giúp đặt các lần giao vào đúng kỳ báo cáo. [Lịch ProjectLibre](../FAME_Lich_ProjectLibre.pod) · [Kỳ báo cáo CORDIS](https://cordis.europa.eu/project/id/101092639/reporting)

### Chi phí

Tổng chi phí và khoản EU tài trợ trả lời câu hỏi về cơ cấu vốn. Phần ngoài EU tính bằng phép trừ hai đại lượng cùng phạm vi. Số tổng dự án đã bao gồm các tổ chức tham gia. Vì vậy, không cộng bốn tổ chức minh họa vào tổng, và cũng không dùng chênh lệch tài trợ như số tiền vượt ngân sách. Ví dụ, số liệu JRC liên quan tới tổ chức trong FAME. Để phân bổ riêng cho Pilot 5 cần mã gói công việc, kỳ chi phí, giờ công, đơn giá và nguyên tắc phân bổ chi phí chung. [Dữ liệu tài trợ đã chép từ CORDIS](../evidence/cordis.json) · [Hồ sơ gốc](https://cordis.europa.eu/project/id/101092639)

**Quyết định đề xuất.** Trước khi tính CPI hay SPI theo phương pháp giá trị thu được, yêu cầu PV, EV và AC cùng ngày chốt và cùng phạm vi. PV là giá trị công việc theo kế hoạch; EV là giá trị ngân sách của phần thực sự hoàn thành; AC là chi phí thực tế. Ngày giao muộn không cho biết cả ba số này. PM có thể báo cáo ngay độ lệch ngày và cơ cấu tài trợ, đồng thời giữ câu hỏi vượt ngân sách và chi phí làm lại ở trạng thái chờ dữ liệu.

## 4. Chất lượng của dữ liệu và của quyết định nghiệm thu

### Kiểm tra đầu ra số học

Bước đầu so mã MD5 và kích thước tệp với metadata của bản Zenodo. Mã cổ phiếu là khóa ghép theo cột. Dòng đầu chỉ dùng để tìm chuỗi trung bình ngành khớp duy nhất với chênh giữa ESG tổng hợp và cột điều chỉnh. Sau khi chốt ánh xạ, mã tính lại điểm từng trụ cột trên các dòng 2–604 rồi so với giá trị phía phát hành. Đối chứng giữ nguyên điểm gốc trên cùng tập ô giúp kiểm tra xem việc khớp có đơn thuần do hai tệp giống nhau hay không. Lần đầu khớp 164.619 ô trên 91 mã và đối chứng khớp 0. Ngày 25/11/2026, áp dụng trung bình tám ngành theo từng dòng cho chín mã ngoại lệ giúp kiểm đủ 100 mã, với 180.900/180.900 ô E/S/G khớp trên cùng 603 dòng. Ánh xạ suy từ dữ liệu cần đối tác xác nhận nếu dùng làm phân ngành chính thức. [Mã thực nghiệm](../esg-data-audit/reproduce_pilot5.py) · [Nguồn Zenodo](https://zenodo.org/records/17175084)

### Khi thay trọng số, người dùng có nhìn thấy cùng danh sách?

Thử nghiệm bổ sung do người viết thiết kế đọc ba bảng điểm gốc của 100 mã. Với mỗi dòng, hồ sơ thứ nhất cho E/S/G trọng số bằng nhau và hồ sơ thứ hai dùng 60/20/20. Thứ tự tính từ điểm nguyên theo đơn vị một phần trăm điểm, không làm tròn điểm tổng trước khi xếp hạng. Nếu điểm tổng bằng nhau thì xếp mã theo thứ tự chữ cái. Mẫu số là 604 vị trí dòng. Các tệp không có cột ngày nên không thể gán một ngày giao dịch cho mỗi lần so sánh. [Mã tính toàn bộ các dòng](../fame_pm/sensitivity.py)

Ở **565/604** dòng, hai hồ sơ cho cùng năm mã nhưng thứ tự khác. Ở **39/604** dòng, chỉ ba trong năm mã giống nhau. Không có dòng nào giữ nguyên cả thứ tự. Không có đồng điểm tại ranh hạng năm và sáu trong hai cách tính trên bộ dữ liệu này. Đặc biệt, toàn bộ bản xuất chỉ tạo **ba cặp danh sách có thứ tự khác nhau**. Xem 604 dòng như 604 thị trường hoặc 604 phép thử độc lập sẽ đánh giá quá cao mức đa dạng của bằng chứng. [Phân bố giao nhau và quy tắc đồng điểm](../results/ranking_sensitivity.json)

**Ý nghĩa khi nghiệm thu P5_BR1.** Kiểm đếm “có đủ năm mã” sẽ bỏ qua sai thứ tự trên cùng tập mã và cả trường hợp thay đổi thành phần. Tiêu chí có thể thực hiện là chốt dữ liệu đầu vào, hồ sơ trọng số và quy tắc đồng điểm, rồi đối chiếu danh sách có thứ tự. Với 39 dòng thay thành phần, người đánh giá có thể kiểm tra cả mã đi vào và mã đi ra. Phép thử dùng điểm gốc để khảo sát độ nhạy. Muốn kết luận một danh mục sinh lời hơn, phải chạy một kiểm định hiệu quả theo thời gian với giá và giao dịch đối chiếu.

### Hai cách đánh giá checklist

Ở đối chiếu hồi cứu, trước và sau đều khớp tham chiếu 6/6. Mức cải thiện quan sát được là từ 0/3 lên 3/3 hồ sơ mở có đầu mối đề xuất. Đại lượng này đo tính đầy đủ của biên bản. Để đo lợi ích vận hành tiếp theo, cần xác nhận người nhận việc, thời điểm trả lời và số hồ sơ đóng với bằng chứng đạt yêu cầu. [Workbook hồi cứu](../FAME_Nghiem_thu_6_KPI.xlsx)

Trong buổi chấm độc lập, hai người chấm từng KPI một lần, với thứ tự thường/gợi ý đảo giữa hai phiếu. Mỗi điều kiện nhận đủ sáu KPI. Quyết định được quy về hai nút duyệt hoặc không duyệt. Cả hai điều kiện cho cùng 6/6 lượt duyệt, trong khi hồ sơ chỉ đủ cho ba KPI. Vì thế tỷ lệ đồng ý cao đi cùng tỷ lệ khớp tham chiếu 50%. Bộ đo ghi thời gian từ lúc hiển thị đến lúc bấm. Trung bình thấp hơn ở B nhưng trung vị lại cao hơn. Hai người và cùng một tập chỉ tiêu không đủ để quy toàn bộ chênh lệch cho gợi ý. [Bảng tổng hợp công khai](../Cham_doc_lap/Ket_qua/Tong_hop_A_B.xlsx)

**Quyết định đề xuất.** Với K04, yêu cầu tử số và mẫu số đủ điều kiện trong cùng kỳ. Với K05, yêu cầu tín hiệu có dấu thời gian, hiệu suất đối ứng, cửa sổ tính và hệ số. Với K06, yêu cầu lợi suất cùng kỳ với danh mục chuẩn, cách tính phí và mức rủi ro tương đương. Chỉ chuyển sang duyệt sau khi người xét có thể trỏ tới bản đo. Nếu thử cơ chế này, cần so trên hồ sơ mới hoặc phân bổ thứ tự để giảm hiệu ứng nhớ, đo riêng độ đúng và thời gian. Đây là thiết kế tiếp theo do người viết đề xuất. [Ba hồ sơ và bằng chứng cần bổ sung](../results/pm_results.json)

## 5. Nguồn lực, truyền thông và các bên liên quan

### Nguồn lực

Lịch sử D6.4 phân biệt bên chủ trì, các pilot đóng góp, bên phản biện và vai trò bảo đảm chất lượng. Phân công cho một tổ chức cung cấp bằng chứng về chức năng chịu trách nhiệm. Nó chưa đủ để tính tải người theo tuần hoặc chi phí theo giờ. Đặc biệt, 126 ngày trước phản biện bao gồm nhiều loại thời gian. Nhân con số đó với đơn giá của một người sẽ tạo một ước lượng thiếu căn cứ. Nếu PM cần điều phối quá tải, đầu vào cần bổ sung là kế hoạch năng lực, lịch công tác, effort thực tế và các khoảng chờ theo gói việc. [Trang bìa và lịch sử D6.4](https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D6.4-Use-Cases-Specification-and-Pilot-Sites-Preparation.-II.pdf#page=2)

### Truyền thông

Thông điệp “người dùng phản hồi tích cực” có giá trị mô tả, nhưng bộ phận vận hành cần một câu hỏi đủ cụ thể để trả lời trước khi nhân rộng. Ví dụ, với K04, cần nêu rõ kỳ quan sát, ai thuộc tập người dùng mục tiêu, hành vi nào tính là sử dụng và ai chịu trách nhiệm loại trùng. Người nhận có thể trả về một bảng tổng hợp thay vì thêm các nhận xét định tính. Bản ghi đề nghị cần mã KPI, tài liệu gốc, dữ liệu còn thiếu, người nhận, thời hạn và trạng thái. Trách nhiệm chỉ có hiệu lực vận hành sau khi bên nhận xác nhận. [Kết quả Pilot 5 trong D6.3](https://www.fame-horizon.eu/wp-content/uploads/2025/05/FAME-D6.3-Techno-Economic-Evaluation-and-Stakeholders-Feedback.pdf#page=52)

### Các bên liên quan

Nhà cung cấp dữ liệu, người vận hành pilot, chuyên viên tài chính và người phê duyệt có các quyết định khác nhau. Người vận hành xác nhận danh sách đủ điều kiện; chuyên viên mô hình giải thích tín hiệu; người quản lý danh mục chịu trách nhiệm về chuẩn so sánh. PM cần chọn đại diện có quyền xác nhận số đo. Trong hồ sơ FAME, 35 người sử dụng tích cực chứng minh một chỉ tiêu đếm; câu hỏi có đạt 70% nhóm mục tiêu vẫn mở vì mẫu số chưa xác định. Tại cuộc họp xét nhân rộng, nên trình hai dòng riêng cùng hai người có quyền xác nhận. [D6.4, ngưỡng sử dụng](https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D6.4-Use-Cases-Specification-and-Pilot-Sites-Preparation.-II.pdf#page=70)

## 6. Rủi ro và mua sắm

### Rủi ro

Điểm thiếu ở dữ liệu hiện tại là một vấn đề đã quan sát. Khả năng nó dẫn đến một quyết định đầu tư sai là rủi ro tương lai. Ví dụ, đã thấy hai tệp dữ liệu không có khóa ngày; ghép nhầm ngày sẽ làm sai đối chiếu tín hiệu với giá. Cách xử lý đề xuất là yêu cầu lịch giao dịch có phiên bản và có người nhận trách nhiệm xác nhận. Trước khi có lịch, vẫn có thể kiểm tra tính nhất quán số học theo vị trí trong cùng bản xuất. Khi tài liệu bổ sung đến, phải thử lại phép ghép và kiểm tra ngày khả dụng của tín hiệu để tránh dùng thông tin tương lai. [Kiểm tra cấu trúc dữ liệu](../evidence/esg_audit.json)

Tương tự, quyền truy cập hoặc giấy phép có thể trì hoãn thí điểm dù công cụ đã phát triển xong. D6.4 ghi nhận lo ngại tuân thủ ở Pilot 6. Bài sử dụng tình huống này để minh họa cách đặt điều kiện phê duyệt trước khi chuyển dữ liệu. Không có căn cứ để quy sự việc đó thành nguyên nhân khiến Pilot 5 hay D6.4 bị trễ. [D6.4, tình huống Pilot 6](https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D6.4-Use-Cases-Specification-and-Pilot-Sites-Preparation.-II.pdf#page=77)

#### RR-04. Duyệt KPI thiếu bằng chứng

Ở Bảng 5.1, RR-04 là nguy cơ người duyệt chấp nhận một KPI khi kết quả chỉ có mô tả định tính hoặc một bản demo. Bảng 5.2 ghi hai vấn đề cùng mã RR-04. **VD-04** là khoảng trống bằng chứng trong báo cáo Pilot 5 của FAME. **VD-05** là các quyết định nhầm trong buổi chấm của học phần. Bảng 5.3 xếp RR-04 ở ô P = 3, I = 3 vì tín hiệu lặp ở ba hồ sơ và có thể đảo kết luận nghiệm thu. Người viết gán mã và chấm mức ưu tiên. [Sổ rủi ro](../evidence/risk_register.csv) · [Nhật ký vấn đề](../evidence/risk_issues.csv)

| Câu hỏi quản lý | Bằng chứng và quyết định |
|---|---|
| Gợi ý trên phiếu có ngăn được duyệt nhầm? | A hiển thị ngưỡng và kết quả. B thêm bốn câu nhắc, vẫn cho phép bấm Duyệt ngay. Hai người chấm chéo cùng sáu KPI. A và B đều duyệt 3/3 hồ sơ thiếu căn cứ, mỗi cách khớp tham chiếu 3/6. Giữ RR-04 ở mức cao. [Phiếu đã dùng](../Cham_doc_lap/Duyet_nhanh_P1.html) · [Kết quả A/B](../Cham_doc_lap/Ket_qua/Tong_hop_A_B.xlsx) |
| Checklist giúp ở khâu nào? | Trong phép hồi cứu Excel riêng, số hồ sơ mở có đầu mối đề xuất tăng từ 0/3 lên 3/3. Quyết định khớp tham chiếu 6/6 ở cả hai cách. Các đầu mối còn chờ xác nhận nhận việc. [Workbook hồi cứu](../FAME_Nghiem_thu_6_KPI.xlsx) |
| PM làm gì với ba KPI? | Giữ mở K04 cho đến khi đầu mối vận hành cung cấp tử số, mẫu số đủ điều kiện và kỳ quan sát. K05 chờ đầu mối mô hình cung cấp chuỗi tín hiệu có ngày, hiệu suất đối ứng và hệ số tương quan. K06 chờ đầu mối danh mục cung cấp đối chứng, kết quả lợi suất ở cùng kỳ năm, chi phí và rủi ro. [Ngưỡng, kết quả và đề nghị cho từng KPI](../results/pm_results.json) |
| Khi nào xét lại mức rủi ro? | Người viết đề xuất bắt buộc nhập số đo hoặc cận, đơn vị, kỳ đo và nguồn. Hồ sơ thiếu chuyển sang “Chờ bằng chứng”. Đầu mối rà soát đối chiếu nội dung với nguồn trước khi ký. Thử phiếu mới và cách B trên cùng 12 hồ sơ mới có đáp án khóa trước, gồm 6 hồ sơ đủ bằng chứng đạt ngưỡng và 6 hồ sơ thiếu căn cứ. Mỗi hồ sơ có một quyết định ở mỗi điều kiện. Trưởng pilot chỉ xét hạ mức khi phiếu mới duyệt nhầm 0/6 hồ sơ thiếu, duyệt đúng 6/6 hồ sơ đủ và nguồn đã được đối chiếu. Đây là tiêu chí đề xuất, chưa có kết quả cho phiếu mới. |

Các lượt trên dùng mã K01–K06 ở Chương 6. Vòng kỹ thuật R1–R6 và phiếu tự kiểm ở Phụ lục K có sổ theo dõi riêng. [Trạng thái vòng kỹ thuật](../results/pilot5_review.json)

### Mua sắm

Hồ sơ tài trợ nêu đối tác và cơ cấu vốn; bản phát hành dữ liệu nêu điều kiện sử dụng. Để đánh giá một hợp đồng mua dịch vụ dữ liệu cần phạm vi cấp phép, đối tượng được phép dùng, chu kỳ cập nhật, chất lượng giao hàng, đơn giá và cách xử lý vi phạm. Với một dịch vụ điểm ESG, quyền đọc dữ liệu nội bộ và quyền công bố bảng xếp hạng dẫn xuất có thể khác nhau. Tình huống quản lý cần xem xét là một kết quả đã đúng về mặt số học nhưng chưa đủ quyền phân phối. PM phải yêu cầu bên phụ trách pháp lý hoặc hợp đồng xác nhận trước khi đưa đầu ra sang môi trường khai thác. Phần này là đề xuất điều kiện nghiệm thu mua sắm; hồ sơ đã xem chưa đủ để chấm hiệu quả nhà cung cấp. [Hồ sơ tài trợ](https://cordis.europa.eu/project/id/101092639) · [Bản phát hành dữ liệu kèm giấy phép](https://zenodo.org/records/17175084)

## 7. Quyết định cuối kỳ và điều kiện xem xét lại

| Hạng mục | Quyết định đề xuất của người viết | Điều kiện để thay đổi quyết định |
|---|---|---|
| 32 mốc giao | Ghi nhận chênh lệch theo từng bìa, ưu tiên điều tra phần trước phản biện của D6.4 | Lịch cơ sở có phụ thuộc và hồ sơ thay đổi giải thích tác động |
| Gói tính điểm | Chấp nhận bằng chứng số học trên v1 cho 100 mã sau hai lượt (91 mã ở lượt đầu) | Khi cần xác nhận phân ngành chính thức, bên dữ liệu cung cấp bảng ánh xạ có phiên bản |
| Danh sách xếp hạng | Đưa so sánh có thứ tự theo từng hồ sơ trọng số vào tiêu chí kiểm thử | Nghiệp vụ xác nhận công thức, quy tắc đồng điểm và mục đích sử dụng |
| Nghiệm thu sáu KPI | Công nhận ba chỉ tiêu có bằng chứng; yêu cầu bổ sung K04–K06 | Có đủ số đo, đơn vị, kỳ đo và nguồn để kiểm tra lại |
| Quyết định nhân rộng | Tách kết quả sử dụng, hiệu quả đầu tư và chi phí vận hành thành ba câu hỏi | Có số người dùng theo kỳ, danh mục đối chứng, dữ liệu giao dịch và chi phí riêng |

Một kết quả phép tính đúng không tự động đóng mọi hạng mục. Thành phẩm của phần thực hành là lịch có thể mở, hai phép so sánh có thể đọc lại, mã có thể chạy từ bản phát hành dữ liệu và một danh sách quyết định có điều kiện thay đổi. Đó là cơ sở để người khác phản biện từng kết luận mà không cần dùng báo cáo Word làm dữ liệu đầu vào.
