import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, PresentationFile } from "@oai/artifact-tool";

const workspace = "D:/A_project/workspace-side/PPT/.codex-ppt-polish";
const starter = path.join(workspace, "template-starter.pptx");
const output = "D:/A_project/workspace-side/PPT/2026年市场大调研总结复盘会模板(2)-美化版.pptx";
const renderDir = path.join(workspace, "final-render");

async function saveBlob(filePath, blob) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, Buffer.from(await blob.arrayBuffer()));
}

function styleBand(shape, position, tone) {
  shape.position = position;
  shape.fill = tone === "issue" ? "#FFF5F5" : "#F7F7F7";
  shape.line = {
    style: "solid",
    fill: tone === "issue" ? "#F0B2B2" : "#DDDDDD",
    width: 1,
  };
  shape.borderRadius = 6;
  shape.shadow = "shadow-sm";
  shape.text.insets = { top: 14, right: 18, bottom: 14, left: 18 };
  shape.text.verticalAlignment = "middle";
  shape.text.wrap = "square";
  shape.text.autoFit = "none";
}

const presentation = await PresentationFile.importPptx(await FileBlob.load(starter));

styleBand(
  presentation.resolve("sh/sb2lcnmd"),
  { left: 43, top: 246, width: 1115, height: 96 },
  "issue",
);
styleBand(
  presentation.resolve("sh/a543mx4r"),
  { left: 43, top: 548, width: 1115, height: 126 },
  "recommendation",
);

const slide12Images = [
  ["im/ehcj2t0n", { left: 112, top: 358, width: 228, height: 171 }],
  ["im/wzql8rup", { left: 386, top: 358, width: 228, height: 171 }],
  ["im/o7e183ip", { left: 705, top: 346, width: 158, height: 198 }],
  ["im/p8n218za", { left: 965, top: 346, width: 158, height: 198 }],
];
for (const [id, frame] of slide12Images) {
  const image = presentation.resolve(id);
  image.frame = frame;
  image.borderRadius = 4;
  image.shadow = "shadow-sm";
}

styleBand(
  presentation.resolve("sh/32ponyts"),
  { left: 43, top: 246, width: 1115, height: 132 },
  "issue",
);
styleBand(
  presentation.resolve("sh/1076lobm"),
  { left: 43, top: 408, width: 1115, height: 204 },
  "recommendation",
);

styleBand(
  presentation.resolve("sh/kfidonqx"),
  { left: 43, top: 246, width: 1115, height: 138 },
  "issue",
);
styleBand(
  presentation.resolve("sh/ehwvat8n"),
  { left: 43, top: 414, width: 1115, height: 198 },
  "recommendation",
);

await fs.mkdir(renderDir, { recursive: true });
for (const [index, slide] of presentation.slides.items.entries()) {
  const number = String(index + 1).padStart(2, "0");
  await saveBlob(
    path.join(renderDir, `slide-${number}.png`),
    await presentation.export({ slide, format: "png", scale: 1 }),
  );
  const layout = await slide.export({ format: "layout" });
  await fs.writeFile(path.join(renderDir, `slide-${number}.layout.json`), await layout.text());
}

const pptx = await PresentationFile.exportPptx(presentation);
await pptx.save(output);
console.log(output);
