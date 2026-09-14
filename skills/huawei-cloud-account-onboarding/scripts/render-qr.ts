#!/usr/bin/env -S npx tsx
/**
 * 把人脸实名认证二维码地址渲染成终端可扫图形。
 *
 * 用法: npx tsx render-qr.ts <qr_code_url>
 * 退出: 0 已渲染 · 2 参数不合法
 *
 * 纯渲染，无副作用：不读环境变量、不调用 hcloud、不写文件、不发网络请求。
 * 地址是一次性凭据，只输出到 stdout 供用户当次扫描。
 */
import QRCode from 'qrcode';

const CYAN = '\x1b[36m';
const BOLD = '\x1b[1m';
const DIM = '\x1b[2m';
const RESET = '\x1b[0m';

/**
 * 半块字符渲染：每个字符覆盖两行模块（前景=上行，背景=下行），
 * 使二维码在常见终端行高下接近正方形。模块保持纯黑白以确保可扫，
 * 只有外框和说明文字着色。
 */
function render(text: string): string[] {
  const qr = QRCode.create(text, { errorCorrectionLevel: 'M' });
  const size = qr.modules.size;
  const data = qr.modules.data;
  const QUIET = 2;
  const total = size + QUIET * 2;

  const dark = (row: number, col: number): boolean => {
    const r = row - QUIET;
    const c = col - QUIET;
    if (r < 0 || c < 0 || r >= size || c >= size) return false;
    return data[r * size + c] === 1;
  };

  const FG_BLACK = '\x1b[30m';
  const FG_WHITE = '\x1b[97m';
  const BG_BLACK = '\x1b[40m';
  const BG_WHITE = '\x1b[107m';

  const lines: string[] = [];
  for (let row = 0; row < total; row += 2) {
    let line = '';
    for (let col = 0; col < total; col += 1) {
      const top = dark(row, col);
      const bottom = row + 1 < total ? dark(row + 1, col) : false;
      line += (top ? FG_BLACK : FG_WHITE) + (bottom ? BG_BLACK : BG_WHITE) + '\u2580';
    }
    lines.push(line + RESET);
  }

  const bar = '\u2500'.repeat(total + 2);
  return [
    `${CYAN}\u250c${bar}\u2510${RESET}`,
    ...lines.map((l) => `${CYAN}\u2502${RESET} ${l} ${CYAN}\u2502${RESET}`),
    `${CYAN}\u2514${bar}\u2518${RESET}`,
  ];
}

function main(): void {
  const url = process.argv[2];

  if (!url) {
    console.error('用法: npx tsx render-qr.ts <qr_code_url>');
    process.exit(2);
  }

  let parsed: URL;
  try {
    parsed = new URL(url);
  } catch {
    console.error(`不是合法的 URL: ${url.slice(0, 40)}…`);
    process.exit(2);
  }
  if (parsed.protocol !== 'https:') {
    console.error(`二维码地址必须是 https，实际为 ${parsed.protocol}`);
    process.exit(2);
  }

  for (const line of render(url)) console.log(line);
  console.log();
  console.log(`${BOLD}请用手机扫描上方二维码${RESET}，按页面提示完成人脸活体核身。`);
  console.log(`${DIM}二维码仅限单次使用，扫描后即失效；10 分钟内未扫描自动作废。${RESET}`);
  console.log(`${DIM}无法扫描时可手动打开：${RESET}${url}`);
}

main();
