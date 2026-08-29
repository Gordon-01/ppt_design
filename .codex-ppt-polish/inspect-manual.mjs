import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, PresentationFile } from "@oai/artifact-tool";

const workspace = "D:/A_project/workspace-side/PPT/.codex-ppt-polish";
const source = path.join(workspace, "source.pptx");
const outDir = path.join(workspace, "template-inspect");

async function saveBlob(filePath, blob) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, Buffer.from(await blob.arrayBuffer()));
}

const presentation = await PresentationFile.importPptx(await FileBlob.load(source));
await fs.mkdir(path.join(outDir, "source-slides"), { recursive: true });
await fs.mkdir(path.join(outDir, "layouts"), { recursive: true });

for (const [index, slide] of presentation.slides.items.entries()) {
  const number = String(index + 1).padStart(2, "0");
  await saveBlob(
    path.join(outDir, "source-slides", `slide-${number}.png`),
    await presentation.export({ slide, format: "png", scale: 1 }),
  );
  const layout = await slide.export({ format: "layout" });
  await fs.writeFile(
    path.join(outDir, "layouts", `slide-${number}.layout.json`),
    await layout.text(),
  );
}

const snapshot = await presentation.inspect({
  kind: "deck,slide,textbox,shape,image,table,chart,notes,thread,layout",
  maxChars: 2000000,
});
await fs.writeFile(path.join(outDir, "template-inspect.ndjson"), snapshot.ndjson, "utf8");

const montage = await presentation.export({ format: "png", montage: true, scale: 1 });
await saveBlob(path.join(outDir, "contact-sheet.png"), montage);

await fs.writeFile(
  path.join(outDir, "template-manifest.json"),
  `${JSON.stringify({ source, slideCount: presentation.slides.items.length }, null, 2)}\n`,
  "utf8",
);

console.log(`Inspected ${presentation.slides.items.length} slides.`);
