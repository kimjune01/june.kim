import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const contentDir = path.join(root, "src/content/folklore");
const files = fs.readdirSync(contentDir).filter((file) => file.endsWith(".json"));
const records = files.map((file) => ({
  file,
  record: JSON.parse(fs.readFileSync(path.join(contentDir, file), "utf8")),
}));
const errors = [];
const ids = new Map();
const orders = new Map();

for (const { file, record } of records) {
  const label = `${file} (${record.id ?? "missing id"})`;

  for (const field of ["id", "title", "originalTitle", "sourceTitle", "sourceUrl", "image"]) {
    if (!record[field]) errors.push(`${label}: missing ${field}`);
  }
  if (!Number.isInteger(record.order)) errors.push(`${label}: order must be an integer`);
  if (!Array.isArray(record.scenes) || record.scenes.length === 0) errors.push(`${label}: scenes must not be empty`);
  if (!Array.isArray(record.pageArt) || record.pageArt.length !== 2) errors.push(`${label}: expected two interior pageArt entries`);

  if (ids.has(record.id)) errors.push(`${label}: duplicate id also used by ${ids.get(record.id)}`);
  else ids.set(record.id, file);
  if (orders.has(record.order)) errors.push(`${label}: duplicate order also used by ${orders.get(record.order)}`);
  else orders.set(record.order, file);

  const artPages = new Set();
  for (const art of record.pageArt ?? []) {
    if (!Number.isInteger(art.page) || art.page < 0 || art.page >= (record.scenes?.length ?? 0)) {
      errors.push(`${label}: pageArt page ${art.page} is outside the scene range`);
    }
    if (artPages.has(art.page)) errors.push(`${label}: duplicate pageArt page ${art.page}`);
    artPages.add(art.page);
    if (!art.image || !art.alt) errors.push(`${label}: pageArt entries require image and alt`);
  }

  if (record.published !== false) {
    const images = [record.image, ...(record.pageArt ?? []).map((art) => art.image)];
    for (const image of images) {
      if (!image || !fs.existsSync(path.join(root, "public", image.replace(/^\//, "")))) {
        errors.push(`${label}: published story is missing ${image ?? "an image path"}`);
      }
    }
  }
}

if (errors.length) {
  console.error(errors.join("\n"));
  process.exit(1);
}

const published = records.filter(({ record }) => record.published !== false).length;
console.log(`Folklore audit passed: ${records.length} records, ${published} published, ${records.length - published} withheld.`);
