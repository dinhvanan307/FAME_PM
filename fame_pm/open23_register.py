"""Map the reproducible checks and outstanding evidence requests to individual KPIs."""

import json
from .portfolio import ROOT
from .kpi_review import OPEN, records

ZENODO = "https://zenodo.org/records/17175084"
SUMMARY_FILE = ROOT / "results/open23_runs.json"
BASELINE = "2ee504207ad4c5aae6f5b213d02503c11e0f0732"


def vi(value):
    return str(value).replace(".", ",")


def published():
    result = json.loads(SUMMARY_FILE.read_text(encoding="utf-8"))
    if result["baseline"] != BASELINE:
        raise ValueError("Wrong execution baseline")
    return result


def measured(result):
    third = result["pilot3"]
    fifth = result["pilot5"]
    s, j, m, grid = (fifth[k] for k in ("scores", "join", "ms023_one_year", "weights"))
    profiles = grid["profiles"]
    if [(p["pillar"], p["weight_percent"]) for p in profiles] != [
        (axis, w) for axis in "ESG" for w in (0, 25, 50, 75, 100)
    ]:
        raise ValueError("Incomplete weight trials")
    neutral = next(
        p for p in profiles if p["pillar"] == "E" and p["weight_percent"] == 50
    )
    blend, esg = m["Balanced blend"], m["ESG only"]
    imports = result["pilot4"]
    return {
        "use_cases": f"Trích được {len(third['use_cases'])} ca sử dụng từ D6.2 tr. 31. D6.2 tr. 32 mô tả một nguyên mẫu phục vụ cả hai ca.",
        "manifests": f"Đọc {len(third['manifests'])} cấu hình FDAC (Deployment, Ingress, Service) và {len(third['operations'])} thao tác OpenAPI của marketplace chung. Chưa định danh hai dịch vụ riêng của pilot.",
        "schemas": f"Swagger của FDAC khai báo {len(third['schema_names'])} kiểu yêu cầu/kết quả tìm kiếm. Không có ánh xạ các kiểu này sang mẫu nghiệp vụ hay số lượt trao đổi của Pilot 3.",
        "fdac": f"Hàm searchAssets gốc chuyển đúng nội dung của {len(third['replay']['examples'])}/{len(third['replay']['examples'])} ví dụ OpenAPI và trả đúng phản hồi thử. Tầng danh mục được mô phỏng tại máy. Số lượt gọi qua mạng là {third['replay']['network_requests']}.",
        "replicas": f"Gói triển khai FDAC chung khai báo {third['manifests']['Deployment']['replicas']} replica. D6.2 xác nhận Pilot 3 chạy AWS. Chưa có số đo tải của pilot.",
        "coverage": f"Đếm {s['nonempty_cells']:,} ô điểm có dữ liệu cho {s['tickers']} mã × {s['rows']} dòng. Chưa có lịch sử các mã được hiển thị cho người dùng.".replace(
            ",", "."
        ),
        "scores": f"Dòng cuối của bảng điểm tài sản có điểm thấp nhất {vi(s['last_row_min'])} và cao nhất {vi(s['last_row_max'])}. Hai giá trị nằm hai phía ngưỡng 70. Thiếu cơ cấu và tập danh mục thực tế để tính trung bình.",
        "ms023": f"Tính lại từ số liệu MS023 một năm. So với Sharpe optimizer, Balanced blend chênh {vi(blend['return_pct_delta_pp'])} điểm % lợi suất và {vi(blend['max_drawdown_pct_delta_pp'])} điểm % sụt giảm tối đa. ESG only chênh {vi(esg['return_pct_delta_pp'])} và {vi(esg['max_drawdown_pct_delta_pp'])} điểm %. Chưa có điểm ESG và phép đối sánh rủi ro theo KPI.",
        "vector": f"Tạo {len(profiles)} vector, thử 0/25/50/75/100% trên từng trụ, chia đều phần còn lại. Đã tính được điểm và thứ hạng cho {grid['tickers']} mã ở {grid['ordinal_rows']} dòng bằng mã của bài. Chưa quan sát giao diện FAME hiển thị các vector này.",
        "weights": f"Tính {len(profiles) * grid['ordinal_rows']:,} bảng xếp hạng. Với E/S/G = 50/25/25, {neutral['rows_changing_top5_members_vs_equal']}/{grid['ordinal_rows']} dòng thay thành phần top 5 so với trọng số bằng nhau. Chưa chạy bộ tối ưu KM Cube.".replace(
            ",", "."
        ),
        "dates": f"Tệp tín hiệu có {j['signal_rows']} dòng, tệp giá có {j['price_rows']} dòng, chung {j['common_tickers']} mã. Dữ liệu tín hiệu thiếu {j['missing_signal_cells']} ô. Cả hai thiếu khóa ngày tường minh. Hệ số tương quan để trống.",
        "imports": f"D6.3 tr. 44 ghi {imports['before']} và {imports['after']} bản ghi. Tái tính mức tăng {imports['delta_records']} bản ghi. Chưa có số bản ghi đầu vào cho từng nguồn.",
    }


METHOD = {
    "use_cases": "Tái tính từ báo cáo",
    "imports": "Tái tính từ báo cáo",
    "ms023": "Tái tính từ báo cáo",
    "schemas": "Kiểm cấu hình chung",
    "manifests": "Kiểm cấu hình chung",
    "replicas": "Kiểm cấu hình chung",
    "fdac": "Chạy mã FAME với phản hồi mô phỏng",
    "coverage": "Chạy trên dữ liệu gốc",
    "scores": "Chạy trên dữ liệu gốc",
    "vector": "Chạy trên dữ liệu gốc",
    "weights": "Chạy trên dữ liệu gốc",
    "dates": "Kiểm khóa ghép dữ liệu",
    "internal": "Cần hồ sơ nội bộ",
}


def attach_runs(rows):
    plans = records("open23_requests.csv")
    expected = {r["id"] for r in rows if r["review"] and r["review"]["after"] == OPEN}
    if len(plans) != 23 or {p["id"] for p in plans} != expected:
        raise ValueError(
            "Execution register must cover the 23 open dossiers at 2ee5042"
        )
    source = {r["ref"]: r["url"] for r in records("kpi_review_sources.csv")}
    links = {
        "coverage": ZENODO,
        "scores": ZENODO,
        "vector": ZENODO,
        "weights": ZENODO,
        "dates": ZENODO,
        "ms023": source["deck24"],
        "fdac": source["fdac"],
        "schemas": source["fdac"],
        "manifests": source["deploy"],
        "replicas": source["deploy"],
        "use_cases": source["D6.2p32"].split("#")[0] + "#page=31",
    }
    by_id = {r["id"]: r for r in rows}
    snapshot = published()
    observations = measured(snapshot)
    for order, plan in enumerate(plans):
        row = by_id[plan["id"]]
        probe = plan["probe"]
        row["execution"] = dict(
            plan,
            order=order,
            method=METHOD[probe],
            observation=observations[probe]
            if probe != "internal"
            else "Chưa có đầu vào công khai để tính KPI. " + row["actual"],
            url=links.get(probe, row["actual_url"]),
        )
    by_id["P5-13"]["execution"]["profiles"] = snapshot["pilot5"]["weights"]["profiles"]
    return rows
