// Local verification server for Expo's exported site. No directory listings or traversal.
import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { extname, resolve, sep } from 'node:path';

const root = resolve('apps/client/dist');
const configuredPort = process.env.DOTICK_E2E_WEB_PORT ?? '8081';
const port = Number(configuredPort);
if (!Number.isInteger(port) || port < 1 || port > 65535) {
  throw new Error('DOTICK_E2E_WEB_PORT must be an integer between 1 and 65535.');
}
const types = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
};
createServer(async (request, response) => {
  try {
    const pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
    const path = resolve(root, `.${pathname === '/' ? '/index.html' : pathname}`);
    if (!path.startsWith(root + sep) || !(await stat(path)).isFile()) {
      response.writeHead(404).end();
      return;
    }
    const content = await readFile(path);
    response.writeHead(200, {
      'Content-Type': types[extname(path)] ?? 'application/octet-stream',
      'Cache-Control': 'no-store',
      'X-Content-Type-Options': 'nosniff',
    });
    response.end(content);
  } catch {
    response.writeHead(404).end();
  }
}).listen(port, '127.0.0.1', () => process.stdout.write(`Dotick web: http://127.0.0.1:${port}\n`));
