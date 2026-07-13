import http from "node:http";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(process.argv[2]);
const port = Number(process.argv[3] || 8081);

const types = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
  ".svg": "image/svg+xml",
  ".woff2": "font/woff2",
  ".mp4": "video/mp4",
};

http
  .createServer((req, res) => {
    const url = decodeURIComponent((req.url || "/").split("?")[0]);
    let file = path.join(root, url === "/" ? "index.html" : url);
    if (!file.startsWith(root)) {
      res.writeHead(403).end();
      return;
    }
    if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, "index.html");
    if (!fs.existsSync(file)) {
      res.writeHead(404).end("not found");
      return;
    }
    res.writeHead(200, { "Content-Type": types[path.extname(file)] || "application/octet-stream" });
    fs.createReadStream(file).pipe(res);
  })
  .listen(port, () => console.log(`serving ${root} on ${port}`));
