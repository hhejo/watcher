import chokidar from "chokidar";

const WATCH_PATH = "./watched";

const watcher = chokidar.watch(WATCH_PATH, {
  persistent: true,
  ignoreInitial: false,
});

watcher
  .on("add", (path) => console.log("📄 새로 생성 →", path))
  .on("change", (path) => console.log("✏️  수정됨   →", path))
  .on("unlink", (path) => console.log("🗑️  삭제됨   →", path))
  .on("error", (err) => console.error("🚨 에러", err))
  .on("ready", () => console.log("🔍 준비 완료"));
