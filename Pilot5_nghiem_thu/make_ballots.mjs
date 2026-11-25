import fs from "node:fs/promises";
import path from "node:path";
import { Workbook, SpreadsheetFile } from "@oai/artifact-tool";

const [root, dest, preview] = process.argv.slice(2);
if (!root || !dest) throw Error("Use: node make_ballots.mjs <round-directory> <output-directory> [preview-directory]");
const spec = JSON.parse(await fs.readFile(path.join(root, "ho_so.json")));
const run = JSON.parse(await fs.readFile(path.join(root, "phep_do.json")));
const pdf = "https://www.fame-horizon.eu/wp-content/uploads/";
const links = [
  ["S1 · Bản phát hành Zenodo v1", "https://zenodo.org/records/17175084"],
  ["S2 · Kết quả đo và bản kê 12 CSV", "https://github.com/dinhvanan307/FAME_PM/blob/main/Pilot5_nghiem_thu/phep_do.json"],
  ["S3 · Đặc tả D6.4, bảng 43, trang PDF 70", pdf+"2026/02/FAME-D6.4-Use-Cases-Specification-and-Pilot-Sites-Preparation.-II.pdf#page=70"],
  ["S4 · Kết quả D6.3, bảng 5, trang PDF 53", pdf+"2025/05/FAME-D6.3-Techno-Economic-Evaluation-and-Stakeholders-Feedback.pdf#page=53"]
];
const navy="#1D394C", teal="#176966", light="#EAF2F3", sand="#FFF1C8";
const put=(s,cell,value)=>{s.getRange(cell).values=[[value]];};
function block(s, address, value, height) {
  const r=s.getRange(address);r.merge();r.getCell(0,0).values=[[value]];
  r.format.wrapText=true;r.format.verticalAlignment="center";r.format.rowHeight=height;return r;
}
function header(range, color=teal){
  range.format.fill=color;range.format.font={name:"Calibri",color:"#FFFFFF",size:11,bold:true};
  range.format.wrapText=true;range.format.verticalAlignment="center";
}
function setup(s,widths){
  s.showGridLines=false;widths.forEach((w,i)=>{s.getCell(0,i).format.columnWidthPx=w;});
}
function row(s,n,values){s.getRangeByIndexes(n-1,0,1,values.length).values=[values];}
function list(s,range,values){s.getRange(range).dataValidation={rule:{type:"list",values}};}
for(const person of ["P1","P2"]){
  const w=Workbook.create(), help=w.worksheets.add("Huong dan");setup(help,[205,210,215,245]);
  header(block(help,"A1:D1","Pilot 5    |    Phiếu độc lập "+person,35),navy);
  [
    "Mở đúng phiếu "+person+". Hoàn tất Luot 1, lưu file rồi mới mở Luot 2. Làm riêng và trả bản đã chấm trực tiếp cho PM.",
    "Trước khi đọc từng hồ sơ, ghi một thời điểm cố định đến giây. Sau khi chọn quyết định và ghi căn cứ, điền thời điểm kết thúc. Dùng ngày và giờ của cùng thiết bị, ví dụ 26/11/2026 19:30:04.",
    "Chọn Duyệt khi đủ bằng chứng cho toàn bộ điều kiện. Chọn Không duyệt nếu vi phạm ngưỡng hoặc thiếu căn cứ. Trong ô lý do ghi rõ trường hợp nào, trang hoặc trường dữ liệu và số vừa đối chiếu.",
    "Lượt B yêu cầu trả lời thêm ba câu checklist. Có và Không đều là lựa chọn hợp lệ. Nếu gián đoạn, ghi trong lý do. Khi hoàn tất, cả sáu dòng cần hiện Đủ trường.",
    "Trang Bang chung cung cấp số đo gốc của đợt tái kiểm và liên kết S1–S4. Trong buổi chấm chỉ dùng phiếu và bốn nguồn này. Giữ kín quyết định cho đến khi PM nhận đủ hai phiếu."
  ].forEach((t,i)=>{block(help,`A${i+3}:D${i+3}`,t,48).format.fill=i%2?light:"#FFFFFF";});
  for(const [i,[mode,ids]] of spec[person].entries()){
    const s=w.worksheets.add("Luot "+(i+1));setup(s,[88,200,275,200,150,150,84,160,305,106,100,117,111]);
    header(block(s,"A1:I1",person+"    |    Lượt "+(i+1)+"    |    "+(mode==="A"?"Đánh giá thông thường":"Đánh giá có checklist"),36),navy);
    block(s,"A2:I2","Bấm giờ trước khi đọc từng dòng. Tra trang Bang chung và nguồn ghi ở cột D. Mỗi hồ sơ chỉ chấm một lần.",28);
    block(s,"A3:I3",mode==="B"?"Điền J–L trước khi chốt. Ghi trang, số liệu và lý do cho quyết định.":"Ghi trang hoặc trường dữ liệu, số liệu và lý do cho quyết định.",26);
    const heads=["Hồ sơ","Nội dung","Điều kiện để duyệt","Bằng chứng cần mở","Bắt đầu","Kết thúc","Giây","Quyết định","Căn cứ và vị trí nguồn"];
    if(mode==="B")heads.push("Đúng nguồn?","Đủ mẫu số?","Đúng phạm vi?");
    const state=mode==="B"?"M":"J";heads.push("Tình trạng phiếu");
    row(s,5,heads);header(s.getRange("A5:"+state+"5"));s.getRange("A5:"+state+"5").format.rowHeight=33;
    ids.forEach((key,k)=>{
      const n=k+6;row(s,n,[key,...spec.cases[key]]);
      s.getRange("A"+n+":"+state+n).format.rowHeight=72;
      s.getRange("A"+n+":"+state+n).format.wrapText=true;
      s.getRange("A"+n+":"+state+n).format.verticalAlignment="center";
      for(const a of ["E","F","H","I",...(mode==="B"?["J","K","L"]:[])])s.getRange(a+n).format.fill=sand;
      s.getRange("G"+n).formulas=[[`=IF(AND(ISNUMBER(E${n}),ISNUMBER(F${n}),E${n}>0,F${n}>E${n}),ROUND((F${n}-E${n})*86400,0),"")`]];
      const checklist=mode==="B"?`,COUNTIF(J${n}:L${n},"Có")+COUNTIF(J${n}:L${n},"Không")=3`:"";
      s.getRange(state+n).formulas=[[`=IF(COUNTA(E${n}:F${n},H${n}:I${n}${mode==="B"?",J"+n+":L"+n:""})=0,"Chưa chấm",IF(AND(ISNUMBER(G${n}),G${n}>0,OR(H${n}="Duyệt",H${n}="Không duyệt"),LEN(TRIM(I${n}))>0${checklist}),"Đủ trường","Kiểm tra"))`]];
    });
    s.getRange("E6:F8").setNumberFormat("dd/mm/yyyy hh:mm:ss");list(s,"H6:H8",["Duyệt","Không duyệt"]);if(mode==="B")list(s,"J6:L8",["Có","Không"]);
    s.freezePanes.freezeRows(5);
  }
  const e=w.worksheets.add("Bang chung");setup(e,[175,205,205,195,230]);
  header(block(e,"A1:E1","Bằng chứng cho sáu hồ sơ",35),navy);
  links.forEach(([label,url],k)=>{const n=3+k;const c=block(e,`A${n}:E${n}`,label,27);c.getCell(0,0).formulas=[[`=HYPERLINK("${url}","${label}")`]];c.format.font={color:"#155B88",underline:"single"};});
  block(e,"A8:E8","S2 · Dòng hiệu chuẩn 1. Dòng chấm 2–604. Điểm được so theo vị trí dòng. Số liệu dưới đây lấy từ tệp phép đo của đợt này.",35);
  row(e,9,["Số tệp CSV đối chiếu","Số mã","Ô E/S/G so sánh","Ô E/S/G khớp","Sai số lớn nhất (điểm)"]);header(e.getRange("A9:E9"));
  row(e,10,[run.files.length,run.tickers,run.denominator,run.matched,Number(run.max_abs_pillar_error)]);
  e.getRange("E10").setNumberFormat("0.00E+00");row(e,12,["Mã","Ô trụ khớp / 1.809","Điều chỉnh tổng khớp / 603","Ô khớp khi cố định / 1.809","Sai số trụ lớn nhất"]);header(e.getRange("A12:E12"));e.getRange("A12:E12").format.rowHeight=38;
  run.exceptions.forEach((r,i)=>row(e,13+i,[r.ticker,r.adjusted_pillars_matched,r.adjusted_total_matched,r.frozen_reference_matched,Number(r.max_abs_pillar_error)]));
  e.getRange("E13:E21").setNumberFormat("0.00E+00");
  block(e,"A23:E23","S3/S4 · D6.3 ghi chức năng hiển thị là “Available” và chức năng trọng số là “Available”. Kiểm tra đơn vị, số mức và công cụ được mô tả bằng cách đối chiếu hai dòng với D6.4.",40);
  w.recalculate();
  await (await SpreadsheetFile.exportXlsx(w)).save(path.join(dest,person+".xlsx"));
  if(preview) for(const [sheet,area] of [["Huong dan","A1:D7"],["Luot 1",spec[person][0][0]==="A"?"A1:J8":"A1:M8"],["Luot 2",spec[person][1][0]==="A"?"A1:J8":"A1:M8"],["Bang chung","A1:E23"]]){
    const b=await w.render({sheetName:sheet,range:area,scale:0.8,format:"png"});await fs.writeFile(path.join(preview,person+"-"+sheet+".png"),new Uint8Array(await b.arrayBuffer()));
  }
}
