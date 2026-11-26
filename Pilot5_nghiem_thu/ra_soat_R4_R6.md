# Pilot 5 · Đối chiếu giao diện và khuyến nghị ở năm mức E/S/G

**Quyết định của PM học phần ngày 26/11/2026.** Giữ mở R4 (P5-12) và R6 (P5-13). Đã xác nhận giao diện của FAME hiển thị một bộ tỷ lệ cụ thể và bộ tối ưu có trả phân bổ theo mã. Hồ sơ công khai đã kiểm chưa đủ để duyệt yêu cầu năm mức cho hồ sơ nào. Các số trang dưới đây đếm từ trang đầu của tệp PDF. [Tiêu chí khóa trước lượt nghiệm thu](tieu_chi.md) · [D6.4, bảng 43, tr. 70][spec]

| Hồ sơ | Quan sát trực tiếp từ FAME | Kết luận nghiệm thu của người viết |
|---|---|---|
| R4 · Hiển thị trọng số | Ảnh của FAME hiển thị E 55%, S 33%, G 12%. Biểu đồ tròn trong cùng hình ghi lại cả ba giá trị. [D6.4, tr. 66][ui] | Chốt việc giao diện thể hiện được một vector tùy chỉnh. Còn thiếu một bộ bằng chứng đọc được đủ ba tỷ lệ cho ít nhất năm cấu hình phân biệt. |
| R6 · Khuyến nghị theo trọng số | Màn hình tham số có tùy chọn trọng số tùy chỉnh. Màn hình kết quả MS023 ngày 18/09/2025 có danh mục, gồm ABBV.US 15,54% và CVS.US 14,90%. [D6.2, hình 43][input] · [Hình 44][output] | Chốt việc hệ thống có đầu ra phân bổ. Hai tỷ lệ là trọng số của hai cổ phiếu trong một danh mục. Cần ghép từng bộ E/S/G với khuyến nghị mà bộ tối ưu trả về ở ít nhất năm cấu hình trên cùng điều kiện đầu vào. |

## Đọc đúng hai dòng KPI

D6.4 yêu cầu ít nhất năm mức phần trăm cho mỗi chỉ tiêu và đề nghị thu thập các bộ trọng số E/S/G. D6.3 ghi giao diện hiển thị được vector và cho phép điều chỉnh trọng số khi tạo khuyến nghị. Trong cùng bảng, kết quả **năm mức** thuộc dòng ngay phía trên, đo độ nhạy ESG so với lợi nhuận tài chính. Các con số **chín** ở những dòng sau là số phương án danh mục hoặc bảng được so sánh. Chuyển một trong các con số đó sang P5-12 hoặc P5-13 sẽ làm sai đối tượng đo. [D6.4, bảng 43][spec] · [D6.3, bảng 5][evaluation]

## Truy từ giao diện đến đầu ra

| Vị trí để kiểm lại | Những gì đọc được | Giá trị cho quyết định PM |
|---|---|---|
| [D6.4, tr. 64][scores] và [tr. 66][ui] | Trang 64 có bảng điểm Env/Soc/Gov theo cổ phiếu. Trang 66 có ba thanh trọng số trên thang 0–100 và biểu đồ 55/33/12. Thanh thứ tư trong hình, ở trên cùng, đặt tỷ trọng ESG so với tài chính ở 70. | Điểm của từng cổ phiếu, tỷ trọng ESG so với tài chính và ba trọng số E/S/G là ba đại lượng riêng. Hai đầu thang và biểu đồ lặp lại cùng cấu hình chỉ là một lần quan sát vector 55/33/12. |
| [D6.2, hình 40, tr. 45][profile] và [hình 41, tr. 46][rank] | Bảng hỏi cho chọn năm mức quan trọng bằng lời cho từng trụ. Hình 41 cho thấy bảng xếp hạng và một thanh điều chỉnh mức ưu tiên ESG tổng thể. | Cả hai minh họa cách cá nhân hóa. Riêng năm nhãn trong bảng hỏi chưa cho biết hệ thống hiển thị năm bộ tỷ lệ phần trăm nào sau khi chọn. |
| [D6.2, hình 43, tr. 48][input] và [hình 44, tr. 49][output] | Ở hình 43, ô dùng trọng số ESG tùy chỉnh đang để trống. Giao diện ghi sẽ dùng trọng số bằng nhau theo mặc định. Hình 44 hiện tên chiến lược, ngày tính, biểu đồ và bảng phân bổ theo mã. | Có căn cứ về khả năng cấu hình và một đầu ra cụ thể. Ảnh kết quả không ghi lại vector E/S/G đầu vào. Tài liệu không gắn bộ 55/33/12 ở D6.4 với danh mục này. |
| [Webinar do FAME công bố, từ 31:10][video] và [đoạn hiện danh mục, từ 31:50][videoout] | Khi đối chiếu các khung xem trước cách nhau 10 giây, có thể nhận ra màn hình tham số rồi hai biểu đồ danh mục. | Đoạn demo bổ sung dấu vết về trình tự thao tác. Độ phân giải và khoảng lấy mẫu chưa cho phép đọc, ghép và đếm năm bộ trọng số. |
| [Slide của KM Cube, tr. 27–28][slides] | Bảng chín hồ sơ thay đổi giới hạn biến động và hệ số ESG tổng thể. Slide 28 dẫn sang phần demo. | Bảng không liệt kê ba trọng số thành phần và danh mục tương ứng ở năm mức. |

## Kho phần mềm và bộ dữ liệu của tác giả

Danh mục FAME Open Sources liệt kê 14 mô-đun. Người viết đã mở bốn gói gần nhất với đường đi từ giao diện đến dịch vụ, xem cấu trúc thư mục và tìm tên pilot, MarketSense, ESG và bộ tối ưu trong mã, cấu hình và tài liệu. Không tìm thấy bộ kiểm thử năm mức hoặc bản ghi yêu cầu và phản hồi của bộ tối ưu Pilot 5 trong bốn bản phát hành này. [Danh mục gốc của FAME][catalog]

| Bản phát hành được kiểm | Tệp hoặc dấu vết có thể tra lại |
|---|---|
| [FAME-dashboard][dashboard] | Trong `src/app/pages/about-us/about-us-page.component.html`, Pilot 5 xuất hiện ở phần giới thiệu ca sử dụng. `src/app/app-routing.module.ts` định tuyến giao diện marketplace. |
| [FAME-integration][integration] | Các manifest triển khai dịch vụ của marketplace, trong đó có FDAC. |
| [FDAC Open-API][fdac] | `swagger.json` mô tả API danh mục tài sản. Ví dụ tìm kiếm trong danh mục trả thông tin tài sản. |
| [FAME-framework-search][search] | `src/services/ApiService.js` thuộc mô-đun tìm kiếm. README trỏ tới [repo GitLab gốc][gitlab]. Khi truy cập công khai ngày 26/11/2026, GitLab chuyển tới trang đăng nhập. |

D1.4 xác định KM và JRC phát triển dịch vụ ESG Ranking & Portfolio. Dịch vụ trả JSON và được phân phối qua marketplace bằng token và thuê bao. Bộ dữ liệu Zenodo cho phép kiểm lại điểm ESG. Trên chính dữ liệu đó, mã của bài đã thử 15 cấu hình × 604 dòng × 100 mã để đo thay đổi thứ hạng. Phép tính này độc lập với giao diện và dịch vụ của KM/JRC. [D1.4, bảng 36, tr. 58][service] · [Zenodo v1][dataset] · [Mã và kết quả từng cấu hình](../docs/kiem-thu-23-kpi.md)

## Bằng chứng đủ để PM xét lại

Một bộ hiện vật có thể giải quyết cả hai hồ sơ. Trên cùng phiên bản pilot, giữ cố định ngày dữ liệu, tập mã và các tham số tài chính. Cho mỗi lần chạy, lưu ba tỷ lệ E/S/G đã chọn, ảnh giao diện sau khi áp dụng và danh mục phản hồi có mã cổ phiếu cùng trọng số. Ghép ảnh và phản hồi bằng số lượt, dấu thời gian hoặc mã yêu cầu. Có thể dùng biên bản QA của KM/JRC có các trường tương đương. [Tiêu chí nghiệm thu](tieu_chi.md) · [Chủ dịch vụ và cơ chế truy cập][service]

PM có thể đóng R4 khi đối chiếu được ít nhất năm vector hiển thị phân biệt. Đóng R6 khi có khuyến nghị đối chiếu được với từng vector trong ít nhất năm cấu hình. Hai cấu hình có thể dẫn đến cùng một danh mục. Điều cần kiểm là bộ tối ưu đã nhận từng cấu hình và trả kết quả. Hai quyết định này là nhận định của người viết trong đợt rà nguồn, được lưu riêng với [phiếu tự chấm](Tu_cham_Codex.xlsx) và [hai phiếu độc lập](README.md).

[spec]: https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D6.4-Use-Cases-Specification-and-Pilot-Sites-Preparation.-II.pdf#page=70
[ui]: https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D6.4-Use-Cases-Specification-and-Pilot-Sites-Preparation.-II.pdf#page=66
[scores]: https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D6.4-Use-Cases-Specification-and-Pilot-Sites-Preparation.-II.pdf#page=64
[evaluation]: https://www.fame-horizon.eu/wp-content/uploads/2025/05/FAME-D6.3-Techno-Economic-Evaluation-and-Stakeholders-Feedback.pdf#page=53
[profile]: https://www.fame-horizon.eu/wp-content/uploads/2025/05/FAME-D6.2-_-Integrated-Pilot-Systems-and-Pilot-Operations.pdf#page=45
[rank]: https://www.fame-horizon.eu/wp-content/uploads/2025/05/FAME-D6.2-_-Integrated-Pilot-Systems-and-Pilot-Operations.pdf#page=46
[input]: https://www.fame-horizon.eu/wp-content/uploads/2025/05/FAME-D6.2-_-Integrated-Pilot-Systems-and-Pilot-Operations.pdf#page=48
[output]: https://www.fame-horizon.eu/wp-content/uploads/2025/05/FAME-D6.2-_-Integrated-Pilot-Systems-and-Pilot-Operations.pdf#page=49
[video]: https://www.youtube.com/watch?v=cmfj7OEz2Ow&t=1870s
[videoout]: https://www.youtube.com/watch?v=cmfj7OEz2Ow&t=1910s
[slides]: https://zenodo.org/records/17937391/files/fame_presentation%20(2).pdf#page=27
[catalog]: https://www.fame-horizon.eu/index.html@p=3257.html
[dashboard]: https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-dashboard.zip
[integration]: https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-integration.zip
[fdac]: https://www.fame-horizon.eu/wp-content/uploads/2026/02/FDAC-Open-API.zip
[search]: https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-framework-search.zip
[gitlab]: https://gitlab.gftinnovation.eu/fame/framework/search
[service]: https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D1.4-Data-Management-Plan-II.pdf#page=58
[dataset]: https://zenodo.org/records/17175084
