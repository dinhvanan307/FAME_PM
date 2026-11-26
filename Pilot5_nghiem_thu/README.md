# Nghiệm thu điểm ESG của Pilot 5

**Biên bản P5-V1, 25/11/2026, giờ Việt Nam.** PM học phần ghi nhận đủ bằng chứng kỹ thuật để đóng chín ngoại lệ về tái tạo giá trị trên Zenodo v1. Chờ hai người chấm độc lập và quyết định cuối của PM. Đợt này dùng sáu hồ sơ R1–R6 của Pilot 5. Kết quả ở thư mục `Cham_doc_lap` thuộc đợt chấm khác.

## Phạm vi và quyết định thay đổi

| Câu hỏi của PM | Bằng chứng và cách xử lý |
|---|---|
| Nghiệm thu đầu ra nào? | Đối chiếu theo dòng và mã chứng khoán các điểm E, S, G điều chỉnh với bản xuất do nhóm tác giả công bố. Tệp thô, mô tả và MD5 có trong [Zenodo v1](https://zenodo.org/records/17175084). |
| Chốt tiêu chí lúc nào? | Lúc 22:09 ngày 25/11, [commit chốt tiêu chí](https://github.com/dinhvanan307/FAME_PM/commit/7ac10f303550188d5dce2a6bc5ca2a4f1a7b305c) lưu cả kết quả thăm dò đã biết. [Quy tắc chốt trước lượt xác nhận](tieu_chi.md) dùng lại bản dữ liệu đã khảo sát. |
| Thay đổi gì? | CR-01 giữ phép ghép duy nhất với một ngành cho 91 mã. Với từng mã còn lại, chỉ dùng trung bình tám ngành nếu phần chênh lệch ở dòng hiệu chuẩn khớp trung bình đó. Khóa cách chọn trước khi tính các dòng 2–604. Rủi ro gán nhầm ngành được xử lý bằng cách ghi rõ đây là quy tắc suy ra từ dữ liệu. |
| Điều kiện đóng? | Tất cả 180.900 ô trụ đạt sai số tuyệt đối ≤ 10⁻⁸ điểm. Mỗi mã ngoại lệ phải đồng thời khớp 1.809 ô trụ và 603 giá trị tổng điều chỉnh. Nếu kiểm lại sai một ô, mở lại CR-01, lưu mã, dòng, giá trị hai phía và checksum. |
| Nguồn lực và chi phí? | Hai vai trò kỹ thuật/PM chuẩn bị dữ liệu và phiếu. Hai người chấm độc lập. Lịch dành 30 phút cho mỗi người và 30 phút đối soát. Đây là thời lượng dự kiến. Chi phí tiền tệ và thời gian chấm thực tế chưa có số liệu. |

## Kết quả kỹ thuật của người viết

[Phép đo theo mã với bản kê 12 tệp](phep_do.json) do [chương trình kiểm lại](verify.py) sinh ra. Công thức dùng điểm trụ gốc cộng điểm ESG tổng hợp rồi trừ tham chiếu của cùng dòng. Điểm điều chỉnh công bố ở dòng 1 dùng để chọn cách ghép. Các điểm công bố của 603 dòng tiếp theo là đáp án so sánh. Sai số lớn nhất trên ba trụ của 100 mã là 2 × 10⁻¹⁴ điểm.

| Phép đối chiếu | Số khớp / mẫu số | Ý nghĩa quản lý |
|---|---:|---|
| Lần đầu, trên tập ghép được với một ngành | 164.619 / 164.619 | Đạt trên 91 mã. Tính trên toàn bộ 100 mã, độ bao phủ ban đầu là 164.619 / 180.900 = 91%. |
| Kiểm lại với tham chiếu theo từng dòng | 180.900 / 180.900 | Độ bao phủ lên 100%, tăng 9 điểm phần trăm. |
| Riêng chín mã, giữ cố định trung bình của dòng 1 | 1.026 / 16.281 | Đối chứng chỉ khớp 114 / 1.809 ô ở từng mã. |
| Riêng chín mã, cập nhật trung bình tám ngành theo dòng | 16.281 / 16.281 ô trụ và 5.427 / 5.427 giá trị tổng điều chỉnh | Đóng cả chín ngoại lệ số học cho phiên bản v1. |

Các mã đã xử lý là CHTR.US, CMCSA.US, DIS.US, GOOGL.US, META.US, NFLX.US, T.US, TMUS.US và VZ.US. Phụ lục K của [báo cáo](../FAME_Bao_cao_cuoi_ky.pdf#page=80) ghi kết quả riêng từng mã. Ánh xạ nội bộ vẫn cần tác giả xác nhận.

| Hồ sơ còn mở | Căn cứ hiện có | Bằng chứng cần chủ hệ thống bổ sung |
|---|---|---|
| P5-12, giao diện hiển thị vector E/S/G | Trang PDF 66 của D6.4 cho thấy E 55%, S 33%, G 12% trên cả thanh chỉnh lẫn biểu đồ. | Ảnh hoặc log giao diện thể hiện đủ ba tỷ lệ ở ít nhất năm cấu hình phân biệt. |
| P5-13, thay trọng số khi đưa khuyến nghị | Hình 43 và 44 của D6.2 cho thấy tùy chọn trọng số và một danh mục MS023 có phân bổ theo mã. | Cùng tập đầu vào và phiên bản bộ tối ưu, ít nhất năm cấu hình trọng số và đầu ra khuyến nghị thực tế gắn với từng cấu hình. |
| Lợi suất MS020 | Tác giả ghi kết quả trên Zenodo. Các bảng CSV dùng ở đây không đủ khóa ngày. | Dữ liệu có ngày, quy tắc và cấu hình chính xác, nhật ký lệnh/khớp, chi phí và chuỗi giá trị danh mục trên cùng kỳ. |

Đợt rà ngày 26/11/2026 giữ mở cả R4 và R6. Có thể kiểm lại từng quan sát từ [hồ sơ đối chiếu ảnh gốc, webinar và bốn gói mã của FAME](ra_soat_R4_R6.md). Nguồn chỉ tiêu và kết quả do dự án công bố nằm ở [D6.4, bảng 43, trang PDF 70](https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D6.4-Use-Cases-Specification-and-Pilot-Sites-Preparation.-II.pdf#page=70) và [D6.3, bảng 5, trang PDF 53](https://www.fame-horizon.eu/wp-content/uploads/2025/05/FAME-D6.3-Techno-Economic-Evaluation-and-Stakeholders-Feedback.pdf#page=53).

## Lượt tự chấm của Codex ngày 26/11/2026

Codex mở biểu mẫu theo trình tự dành cho P1 và chấm đủ sáu hồ sơ. R1, R3 và R5 đủ căn cứ để duyệt. R2 bị từ chối do đối chứng cố định chỉ khớp 1.026/16.281 ô. R4 và R6 còn thiếu bằng chứng giao diện và đầu ra bộ tối ưu ở ít nhất năm mức. [Phiếu tự chấm có thời gian và căn cứ từng hồ sơ](Tu_cham_Codex.xlsx)

Phụ lục K đọc trực tiếp sáu quyết định từ phiếu tự chấm. Đồng hồ đã tính cả thời gian đọc nguồn và chạy công cụ. Codex đã biết kết quả kỹ thuật của vòng trước. Hai phiếu độc lập của người chấm được tổng hợp riêng.

## Lịch thực hiện và bàn giao

Mở [lịch ProjectLibre](Lich_nghiem_thu.pod) bằng File → Open. [Bản XML tương thích MS Project](Lich_nghiem_thu.xml) chứa cùng mã việc, lịch cơ sở, hạn, người phụ trách và liên kết kết thúc–bắt đầu. Đã lưu rồi mở lại tệp POD bằng bộ đọc gốc ProjectLibre 1.9.8, kiểm đủ tám công việc, lịch cơ sở, người phụ trách và hai tiền nhiệm của việc 7.

| ID | Công việc | Người phụ trách | Mốc hoặc khung giờ ICT | Tiền nhiệm | Trạng thái |
|---|---|---|---|---|---|
| 1 | Khóa tiêu chí | PM | 25/11 22:09 | — | Hoàn thành |
| 2 | Đối chiếu 12 CSV và 100 mã | Phân tích dữ liệu | 25/11 22:10 | 1 | Hoàn thành |
| 3 | Kiểm chứng sổ chín ngoại lệ | Phân tích dữ liệu | 25/11 22:10 | 2 | Hoàn thành trong cùng lượt chạy |
| 4 | Tạo hai phiếu Excel | PM | 25/11 22:12 | 3 | Hoàn thành |
| 5 | Chấm P1 | P1 | 26/11 19:30–20:00 | 4 | Dự kiến |
| 6 | Chấm P2 | P2 | 26/11 19:30–20:00 | 4 | Dự kiến |
| 7 | Đối soát, xử lý bất đồng | PM | 27/11 19:30–20:00 | 5 và 6 | Chờ |
| 8 | Quyết định nghiệm thu | PM | 27/11 20:00 | 7 | Chờ ký |

Bốn mốc đầu được dựng lại từ thời điểm khóa tiêu chí, chạy kiểm chứng và sinh phiếu, làm tròn xuống phút. Bốn mốc sau là lịch đề xuất của người viết. Nếu một phiếu đến muộn, PM cập nhật lịch hiện hành, giữ ngày cơ sở và dời việc 7–8. Các mốc này thuộc bài thực hành tháng 11/2026.

## Giao phiếu và đối soát

**Phiếu bấm giờ tự động.** Gửi [Duyet_P1.html](Duyet_P1.html) cho P1 và [Duyet_P2.html](Duyet_P2.html) cho P2. Mỗi người tải tệp rồi mở bằng trình duyệt. Bấm **Mở hồ sơ** trước khi tra bằng chứng. Ghi căn cứ, trả lời ba câu nếu có checklist, rồi bấm **Duyệt** hoặc **Không duyệt** để chốt giờ kết thúc. Sau sáu hồ sơ, bấm **Tải kết quả Excel** và gửi riêng tệp cho PM. Có thể mở lại cùng tệp trong cùng trình duyệt để tiếp tục nếu trình duyệt cho lưu bản nháp. Khi quay lại hồ sơ đang mở, đồng hồ tính cả thời gian gián đoạn.

PM nhận `P1.xlsx` và `P2.xlsx` cùng định dạng với phiếu Excel bên dưới. Lưu vào `du_lieu/phieu_pilot5/` rồi chạy `python report/build_report.py --pdf`. Giờ trong Excel theo UTC+7. Trang kết quả chỉ hiện các quyết định của người đang chấm. Bốn liên kết nguồn mở bằng Internet, còn việc chấm và xuất tệp chạy ngay trong trình duyệt.

**Cách nhập trực tiếp bằng Excel**

1. Gửi riêng [P1.xlsx](P1.xlsx) cho người thứ nhất và [P2.xlsx](P2.xlsx) cho người thứ hai. Mỗi người chỉ cần phiếu của mình. Mở **Huong dan**, làm **Luot 1**, lưu, rồi làm **Luot 2**. Chỉ mở bốn nguồn S1–S4 ở trang **Bang chung** trong buổi chấm.
2. Trước khi đọc từng hồ sơ, ghi ngày giờ tĩnh đến giây ở E. Chọn **Duyệt** hoặc **Không duyệt** ở H. Ở I, ghi trang hoặc trường dữ liệu, số đối chiếu và lý do. Lượt có checklist cần trả lời thêm ba ô J–L. Ghi giờ kết thúc ở F, kiểm tra dòng hiện **Đủ trường**, lưu và gửi riêng file cho PM.
3. PM lưu nguyên bản trả riêng ở ngoài repo hoặc trong thư mục bỏ qua bởi Git. Chạy lệnh dưới đây. Chương trình kiểm danh tính, thứ tự hồ sơ, ngày giờ, quyết định, căn cứ và checklist. PM đọc lý do và xác nhận độ phù hợp của nguồn.
4. Khi đủ hai phiếu, đối chiếu ca quyết định đúng, duyệt nhầm, từ chối nhầm (ghi cả mẫu số), thời gian trung bình/trung vị cho A và B cùng số cặp đồng thuận trên sáu hồ sơ. Nếu bất đồng hoặc lý do sai nguồn, ghi mã hồ sơ, quyết định P1 và P2, nguồn/trang xử lý, lý do, quyết định cuối, người xác nhận và ngày ký. Giữ nguyên hai bản ban đầu.

Tại ngày lập biên bản kỹ thuật 25/11/2026, số phiếu hoàn tất là **0/2**, số quyết định hợp lệ là **0/12**. Chỉ số hiệu quả checklist và quyết định ký cuối đang chờ. Mỗi người chấm cùng sáu hồ sơ một lần và thứ tự A/B được đảo giữa hai người. Mỗi điều kiện có sáu quan sát khi hoàn tất. Quy mô hai người và khác biệt về người chấm, hồ sơ, thứ tự làm việc giới hạn kết luận ở mức mô tả.

## Lệnh chạy từ thư mục gốc FAME_PM

```bash
python -m pip install -r requirements.txt
python esg-data-audit/reproduce_pilot5.py --download --data-dir du_lieu/zenodo
python Pilot5_nghiem_thu/verify.py --data-dir du_lieu/zenodo --check
python Pilot5_nghiem_thu/tong_hop.py Pilot5_nghiem_thu/P1.xlsx Pilot5_nghiem_thu/P2.xlsx
```

Để cập nhật Phụ lục K, đặt bản trả tên `P1.xlsx` và `P2.xlsx` vào `du_lieu/phieu_pilot5/` (Git bỏ qua) rồi chạy `python report/build_report.py --pdf`. Có thể dựng lại khi mới nhận một phiếu. [Trạng thái công bố](../results/pilot5_review.json) đi kèm Word/PDF. [Hướng dẫn dùng thư mục khác và dựng lại trên GitHub](../report/README.md#cập-nhật-phụ-lục-k).

Để xem số tổng trước khi dựng, thay hai đối số cuối của lệnh tổng hợp bằng đường dẫn đến hai bản trả riêng. Thông tin tổng hợp in ra màn hình. PM chỉ công bố thống kê của đợt và quyết định đã xác nhận. [Mã tạo mẫu Excel](make_ballots.mjs) đọc [bố trí hồ sơ](ho_so.json) và tệp số đo, dùng Node với `@oai/artifact-tool`. Hai tệp đã dựng có thể mở trực tiếp trong Excel.

Hai tệp HTML được dựng từ đúng hai mẫu Excel, thứ tự hồ sơ trong `ho_so.json` và số đo trong `phep_do.json`. Để dựng lại bằng Node có `jszip@3.10.1` và phụ thuộc `pako`, chạy `node Pilot5_nghiem_thu/make_click_forms.cjs` từ gốc repo. Người chấm chỉ cần tệp HTML tương ứng.
