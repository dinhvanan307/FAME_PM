// Render the CSV exported by python -m fame_pm.kpi_matrix --json.
import { readFile, writeFile } from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const [source, output, preview] = process.argv.slice(2);
if (!source || !output) throw new Error("Usage: node kpi_workbook.mjs matrix.json output.xlsx [preview.png]");
const rows = JSON.parse(await readFile(source, "utf8"));
const book = Workbook.create();
const summary = book.worksheets.add("Tong hop");
const matrix = book.worksheets.add("Ma tran");
const states = ["Đạt", "Không đạt", "Thiếu bằng chứng", "Không áp dụng theo FAME"];
const ink = "#17344B", teal = "#14666B", pale = "#EDF5F4";
const keys = ["id", "pilot", "kpi", "target", "actual", "assessment", "rationale", "period",
              "target_pages", "actual_pages", "period_url", "supporting_url", "source_name", "legacy_id"];
const headers = ["Mã KPI", "Pilot", "Chỉ tiêu", "Mục tiêu D6.4", "Kết quả FAME (D6.3)", "Kết luận của người viết",
                 "Căn cứ / phần còn thiếu", "Kỳ đánh giá", "Trang D6.4", "Trang D6.3", "Nguồn kỳ đo", "Nguồn bổ sung",
                 "Tên trong đặc tả", "Mã 6 KPI"];
const end = rows.length + 1;
function widths(sheet, values) {
  values.forEach((px, i) => { sheet.getCell(0, i).format.columnWidthPx = px; });
}
function heading(range, fill=teal) {
  range.format.fill = fill;
  range.format.font = {name:"Calibri", bold:true, size:11, color:"#FFFFFF"};
  range.format.verticalAlignment = "center";
  range.format.wrapText = true;
}
function mergedText(sheet, address, text) {
  const range = sheet.getRange(address);
  range.merge();
  range.getCell(0, 0).values = [[text]];
  return range;
}
for (const sheet of [summary, matrix]) sheet.showGridLines = false;
summary.tabColor = ink;
matrix.tabColor = teal;
matrix.getRange("A1:N1").values = [headers];
const page = url => url.split("#page=")[1];
matrix.getRange(`A2:N${end}`).values = rows.map(row => keys.map(k => {
  if (k === "pilot") return Number(row[k]);
  if (k === "target_pages") return "D6.4 · " + row[k];
  if (k === "actual_pages") return "D6.3 · " + row[k];
  if (k === "period_url") return "D6.3 · " + page(row[k]);
  if (k === "supporting_url") return row[k] ? "D6.2 · " + page(row[k]) : "—";
  return row[k] || null;
}));
const table = matrix.tables.add(`A1:N${end}`, true, "MaTranKPI");
table.style = "TableStyleMedium2";
table.showFilterButton = true;
widths(matrix, [85,65,225,305,310,165,350,246,104,104,106,110,245,85]);
const body = matrix.getRange(`A2:N${end}`);
body.format.wrapText = true;
body.format.verticalAlignment = "center";
body.format.rowHeight = 76;
body.format.font = {name:"Calibri", size:11, color:ink};
heading(matrix.getRange("A1:N1"));
matrix.getRange("A1:N1").format.rowHeight = 30;
matrix.getRange(`I2:L${end}`).format.font = {name:"Calibri",size:11,color:"#155B88",underline:"single"};
rows.forEach((r,i) => {
  const cell = matrix.getCell(i + 1,5);
  cell.format.fill = ["#D9EFE4","#F8DFDC","#FFF0CB","#E5E9F2"][states.indexOf(r.assessment)];
  cell.format.font = {name:"Calibri",size:11,bold:true,color:ink};
});
matrix.freezePanes.freezeRows(1);
widths(summary, [86,112,110,130,160,200]);
const title = mergedText(summary,"A1:F1","Nghiệm thu 65 KPI của FAME");
heading(title, ink);
title.format.font = {name:"Calibri", size:18,bold:true,color:"#FFFFFF"};
title.format.rowHeight=38;
const intro=mergedText(summary,"A2:F2","Đặc tả D6.4 và kết quả giai đoạn 2 trong D6.3. Kết luận do người viết đánh giá theo mục tiêu gốc.");
intro.format.rowHeight=36; intro.format.wrapText=true;
summary.getRange("A5:F5").values = [["Pilot","Số KPI",...states]];
heading(summary.getRange("A5:F5")); summary.getRange("A5:F5").format.rowHeight=34;
for(let p=1;p<=7;p++){
  const r=p+5;
  summary.getCell(r-1,0).values=[[p]];
  summary.getCell(r-1,1).formulas=[[`=COUNTIF('Ma tran'!$B$2:$B$${end},A${r})`]];
  for(let j=2;j<=5;j++) {
    const letter = String.fromCharCode(65+j);
    summary.getCell(r-1,j).formulas=[[`=COUNTIFS('Ma tran'!$B$2:$B$${end},$A${r},'Ma tran'!$F$2:$F$${end},${letter}$5)`]];
  }
}
summary.getRange("A6:F12").format.rowHeight=25;
summary.getRange("A13").values=[["Tổng"]];
for(let j=1;j<=5;j++){
  const col=String.fromCharCode(65+j);summary.getCell(12,j).formulas=[[`=SUM(${col}6:${col}12)`]];
}
heading(summary.getRange("A13:F13"),ink);summary.getRange("A13:F13").format.rowHeight=29;
const notes=[
  "Cách đọc ma trận",
  "Trong trang Ma tran, lọc theo Pilot hoặc Kết luận của người viết. Bấm các ô nguồn để mở đúng trang PDF.",
  "Đạt và Không đạt dựa trên số đo hoặc kết luận dưới ngưỡng mà dự án công bố. Đọc cột căn cứ để biết phạm vi xác nhận.",
  "Thiếu bằng chứng giữ mở hồ sơ khi thiếu mẫu số, thiếu một vế của mục tiêu hoặc dùng thước đo khác. Số 0 là kết quả khi nguồn ghi rõ 0.",
  "Không áp dụng theo FAME dùng cho phép thử dữ liệu ngoài ở Pilot 1. Nguồn chưa ghi nhận quyết định miễn trừ.",
  "Kỳ đánh giá là khoảng dự án công bố. Khi thiếu ngày vận hành hoặc ngày lấy mẫu riêng, ma trận ghi rõ giới hạn đó.",
  "P1-01 đến P7-04 là mã của bài. Cột cuối nối sáu KPI Pilot 5 với workbook nghiệm thu trước đây."
];
notes.forEach((value,i)=>{
  const r=15+i;const line=mergedText(summary,`A${r}:F${r}`,value);
  line.format.wrapText=true;line.format.verticalAlignment="center";line.format.rowHeight=i===0?26:34;
  if(i===0)heading(line);else {line.format.font={name:"Calibri",size:11,color:ink};if(i%2)line.format.fill=pale;}
});
book.recalculate();
if(preview){
  const png = await book.render({sheetName:"Tong hop",range:"A1:F21",scale:1,format:"png"});
  await writeFile(preview,new Uint8Array(await png.arrayBuffer()));
}
await (await SpreadsheetFile.exportXlsx(book)).save(output);
