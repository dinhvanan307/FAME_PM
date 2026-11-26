/* Build two standalone forms from their own released workbooks. Requires JSZip 3.10.1. */
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const here = __dirname;
const read = name => fs.readFileSync(path.join(here, name), "utf8");
const spec = JSON.parse(read("ho_so.json"));
const run = JSON.parse(read("phep_do.json"));
const sources = JSON.parse(read("../results/pilot_portfolio.json")).sources;
const template = read("phieu_bam.html.in");
const engine = fs.readFileSync(require.resolve("jszip/dist/jszip.min.js"), "utf8");
const license = fs.readFileSync(require.resolve("jszip/LICENSE.markdown"), "utf8");
const mit = license.split("\nGPL version 3\n")[0];
const pakoLicense = fs.readFileSync(require.resolve("pako/LICENSE"), "utf8");
const urls = [
  "https://zenodo.org/records/17175084",
  "https://github.com/dinhvanan307/FAME_PM/blob/e988ef7c9251e608904824907d084e1e9bc5640f/Pilot5_nghiem_thu/phep_do.json",
  sources.d64.url + "#page=70",
  sources.d63.url + "#page=53"
];
for (const person of ["P1", "P2"]) {
  const workbook = fs.readFileSync(path.join(here, person + ".xlsx"));
  const items = spec[person].flatMap(([mode, ids], i) => ids.map((id, j) => ({
    id, mode, pass: i, row: j, title: spec.cases[id][0],
    criterion: spec.cases[id][1], where: spec.cases[id][2]
  })));
  const payload = {
    person, items, urls, files: run.files, exceptions: run.exceptions,
    matched: run.matched, total: run.denominator, error: run.max_abs_pillar_error,
    version: crypto.createHash("sha256").update(workbook).update(JSON.stringify(items)).update(read("phep_do.json")).digest("hex").slice(0, 16),
    workbook: workbook.toString("base64")
  };
  const html = template.replaceAll("{{PERSON}}", person)
    .replace("{{DATA}}", () => JSON.stringify(payload).replaceAll("<", "\\u003c"))
    .replace("{{ZIP}}", () => engine)
    .replace("{{LICENSE}}", () => (mit + "\n" + pakoLicense).replaceAll("<", "&lt;"));
  fs.writeFileSync(path.join(here, "Duyet_" + person + ".html"), html);
}
