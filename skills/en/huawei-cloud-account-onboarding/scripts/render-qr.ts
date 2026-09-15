#!/usr/bin/env -S npx tsx
/**
 * Render a face-verification QR URL as a terminal-scannable image.
 *
 * Usage: npx tsx render-qr.ts <qr_code_url>
 * Exit: 0 rendered; 2 invalid argument
 *
 * Pure rendering with no side effects: no environment reads, hcloud calls,
 * file writes, or network requests. The URL is a one-time credential and is
 * printed only to stdout for the current user.
 */
import QRCode from "qrcode";

const CYAN = "\x1b[36m";
const BOLD = "\x1b[1m";
const DIM = "\x1b[2m";
const RESET = "\x1b[0m";

/**
 * Half-block rendering: each character covers two QR rows. Foreground is the
 * upper row and background the lower row, keeping the image nearly square in
 * common terminals. QR modules remain black and white; only framing is colored.
 */
function render(text: string): string[] {
  const qr = QRCode.create(text, { errorCorrectionLevel: "M" });
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

  const FG_BLACK = "\x1b[30m";
  const FG_WHITE = "\x1b[97m";
  const BG_BLACK = "\x1b[40m";
  const BG_WHITE = "\x1b[107m";

  const lines: string[] = [];
  for (let row = 0; row < total; row += 2) {
    let line = "";
    for (let col = 0; col < total; col += 1) {
      const top = dark(row, col);
      const bottom = row + 1 < total ? dark(row + 1, col) : false;
      line += (top ? FG_BLACK : FG_WHITE) + (bottom ? BG_BLACK : BG_WHITE) + "\u2580";
    }
    lines.push(line + RESET);
  }

  const bar = "\u2500".repeat(total + 2);
  return [
    `${CYAN}\u250c${bar}\u2510${RESET}`,
    ...lines.map((l) => `${CYAN}\u2502${RESET} ${l} ${CYAN}\u2502${RESET}`),
    `${CYAN}\u2514${bar}\u2518${RESET}`,
  ];
}

function main(): void {
  const url = process.argv[2];

  if (!url) {
    console.error("Usage: npx tsx render-qr.ts <qr_code_url>");
    process.exit(2);
  }

  let parsed: URL;
  try {
    parsed = new URL(url);
  } catch {
    console.error(`Invalid URL: ${url.slice(0, 40)}…`);
    process.exit(2);
  }
  if (parsed.protocol !== "https:") {
    console.error(`The QR URL must use https; received ${parsed.protocol}`);
    process.exit(2);
  }

  for (const line of render(url)) console.log(line);
  console.log();
  console.log(
    `${BOLD}Scan the QR code above with your phone${RESET} and follow the page to complete the liveness check.`,
  );
  console.log(
    `${DIM}Single use only: it expires after scanning or after 10 unscanned minutes.${RESET}`,
  );
  console.log(`${DIM}If scanning fails, open this URL manually: ${RESET}${url}`);
}

main();
