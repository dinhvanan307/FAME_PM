# Dựng lại báo cáo cuối kỳ

Chạy từ thư mục gốc của repo sau khi đã dựng môi trường Python như hướng dẫn ở README.

```bash
python -m pip install -r report/requirements.txt
python -m fame_pm --check
python report/build_report.py --out build
python report/build_report.py --pdf --out build
```

Lệnh thứ ba tạo Word. Lệnh thứ tư tạo cả Word và PDF bằng LibreOffice (cần có `soffice` trong PATH hoặc biến môi trường `SOFFICE` chỉ đúng tệp thực thi). Nên cài bộ phông chữ có trong mẫu để tái hiện đúng bố cục. Số trang có thể đổi theo nền tảng và phông chữ. Khi xuất PDF, chương trình đối chiếu trang đích của các liên kết mục lục, cập nhật số trang lưu trong Word nếu cần và xuất lại. Để cập nhật hai tài liệu phát hành ở gốc repo, bỏ `--out build`.

**Nguồn biên tập.** `mau_bien_tap.docx` giữ bố cục UET, phần thuyết minh, hình Gantt và liên kết nguồn của báo cáo. Các dấu `[[...]]` đánh dấu trường số liệu chương trình điền từ `results/pm_results.json`. Các bảng lịch, tài trợ, hồi cứu, buổi chấm độc lập và phần phân tích trọng số được điền theo cơ chế này. Để sửa diễn giải học thuật, chỉnh văn bản nguồn trong mẫu hoặc phần phân tích trên GitHub rồi rà tính thống nhất; chỉnh trực tiếp tệp Word phát hành sẽ bị ghi đè ở lần dựng sau.

**Đối chiếu sau khi biên tập.** Chương 3 phải dùng ngày lịch trên bìa. Chương 4 ghi đúng phạm vi tài chính. Mục 6.5 và 6.6 có mẫu số và mục đích khác nhau. Phụ lục E đo độ nhạy thứ hạng trên bản xuất có vị trí dòng. Cần đọc kết quả này cùng giới hạn về khóa ngày và lợi suất. [Nguồn các phép tính](../results/ket-qua.md) · [Phân tích đầy đủ theo miền](../docs/phan-tich-quan-ly.md)

Phụ lục F dùng chỉ mục của ba PDF trong [pilot_portfolio.json](../results/pilot_portfolio.json), [bản chép kết quả và diễn giải theo pilot](../evidence/pilot-outcomes.csv) và [kết quả chạy mã gốc Pilot 7](../results/pilot7_boundaries.json). Xem [bản rà theo mẫu và hướng dẫn tái lập](../docs/ra-soat-truoc-khi-nop.md) để tính lại hai tệp JSON.

Phụ lục G dựng toàn bộ 65 dòng từ [CSV nghiệm thu](../evidence/kpi_matrix.csv). Lệnh `python -m fame_pm.kpi_matrix` kiểm tra bản Excel phát hành. Có thể dựng lại Word/PDF bằng Python từ CSV theo các lệnh đầu trang. Phụ lục H và trang thứ ba của Excel dùng [25 hồ sơ trước rà](../evidence/kpi_review.csv) và [danh mục nguồn](../evidence/kpi_review_sources.csv). Phụ lục I và trang thứ tư của Excel dùng chung [kết quả chạy](../results/open23_runs.json) và [yêu cầu dữ liệu cho từng KPI](../evidence/open23_requests.csv). Bộ dựng Excel dùng Node có `@oai/artifact-tool` (môi trường tạo tệp), rồi gắn liên kết PDF vào từng ô nguồn. Từ thư mục gốc, khi đã có thư mục `build`:

```bash
python -m fame_pm.kpi_matrix --json > build/kpi.json
node report/kpi_workbook.mjs build/kpi.json build/kpi-layout.xlsx
python report/attach_kpi_links.py build/kpi.json build/kpi-layout.xlsx FAME_Ma_tran_65_KPI.xlsx
python -m fame_pm.kpi_matrix
```

Phần 6.2 lấy chuỗi quyết định của Pilot 5 từ [sổ phản hồi](../evidence/pilot5_feedback.json) và kết quả chạy trọng số. Mục 7.1 và Phụ lục J liên hệ quyết định nghiệm thu với [35 điểm Pentagon](../evidence/innovation_pentagon.json). Trang **Innovation Pentagon** của Excel lấy cùng bộ điểm và dùng công thức tính lại Hình 16. [Phương pháp và lệnh đối chiếu](../docs/innovation-pentagon.md)

## Cập nhật Phụ lục K

Đặt phiếu trả của vòng P5-V1 vào `du_lieu/phieu_pilot5/P1.xlsx` và `du_lieu/phieu_pilot5/P2.xlsx`. Có thể đặt từng phiếu khi nhận được. Chạy từ thư mục gốc:

```bash
python report/build_report.py --pdf
```

Mỗi lần dựng, chương trình kiểm tra phiếu, đếm số phiếu hoàn tất và quyết định hợp lệ. Khi đủ 12 quyết định, Phụ lục K thêm bảng A/B về duyệt nhầm, từ chối nhầm, thời gian và mức đồng thuận. PM ghi nhận quyết định ký sau khi đối soát căn cứ. Các phiếu điền sai trường hoặc sai danh tính cần được sửa trước khi xuất báo cáo.

Nếu lưu phiếu ở thư mục riêng khác, dùng `--pilot5-ballots "/đường/dẫn/tới/thư mục"`. Dùng `--out build` để xuất thử. Bộ dựng đặt [bản tổng hợp ẩn danh](../results/pilot5_review.json) dưới `results/` trong thư mục đầu ra. Khi phát hành, đưa bản tổng hợp lên GitHub cùng Word/PDF. Một bản clone sạch sẽ dựng lại Phụ lục K từ số liệu đã công bố. Hai tệp Excel có lý do và giờ chấm chi tiết được giữ ở thư mục riêng.

Bảng 3.1 tổng hợp cả bảy gói công việc. Trang mở đầu phụ lục liên kết A–L tới đúng tiêu đề trong Word và PDF. Kết luận lấy các số đếm của vòng xác nhận từ [phép đo 100 mã](../Pilot5_nghiem_thu/phep_do.json), cùng nguồn với Phụ lục K. Chương 3 và Phụ lục L lấy số liệu từ [32 cặp ngày đã đối chiếu](../evidence/deliverables.csv). [Cách kiểm lại bìa PDF, lịch XML và bản ProjectLibre](../evidence/README.md#đối-chiếu-32-bìa-báo-cáo).

Bản nộp tổ chức bảy chương thành bốn phần. Mục 2.5, 3.4 và 5.3 lần lượt phân tích nguồn lực, kịch bản tiến độ và ưu tiên rủi ro theo mẫu INTERLINK. Mục 6.6 hiển thị chênh lệch B trừ A. Quá trình dựng đối chiếu [CSV và lịch kịch bản](../results/d64_review_scenarios.csv) bằng `python -m fame_pm.review_scenario --check`.
