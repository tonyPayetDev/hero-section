// Known script -> transcribed words: keep Whisper's timings, take the words from the script.
// Used when the text is known in advance (cloned voice, avatar take, teleprompter): no more « Comment trop beau »
// for « Commente ROBOT ». Alignment = LCS on normalised tokens; unmatched runs share their time span evenly.

const norm = (w) => w.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9]/g, "");

/** words: [{w,s,e}] from Whisper; script: plain text. Returns [{w,s,e}] with the script's words. */
export function alignScript(words, script) {
  const ref = String(script || "").replace(/\s+/g, " ").trim().split(" ").filter(Boolean);
  if (!ref.length || !words.length) return words;
  const A = words.map((w) => norm(w.w)), B = ref.map(norm);
  const n = A.length, m = B.length;
  const L = Array.from({ length: n + 1 }, () => new Int32Array(m + 1));
  for (let i = n - 1; i >= 0; i--) for (let j = m - 1; j >= 0; j--)
    L[i][j] = A[i] && A[i] === B[j] ? L[i + 1][j + 1] + 1 : Math.max(L[i + 1][j], L[i][j + 1]);
  const pairs = [];                    // matched (i, j)
  for (let i = 0, j = 0; i < n && j < m;) {
    if (A[i] && A[i] === B[j]) { pairs.push([i, j]); i++; j++; } else if (L[i + 1][j] >= L[i][j + 1]) i++; else j++;
  }
  const out = [];
  let pi = 0, pj = 0;
  const fill = (i0, i1, j0, j1) => {   // words i0..i1-1 (Whisper) carry script words j0..j1-1
    if (j1 <= j0) return;
    const s = i1 > i0 ? words[i0].s : (i0 > 0 ? words[i0 - 1].e : words[0].s);
    const e = i1 > i0 ? words[i1 - 1].e : (i0 < n ? words[i0].s : words[n - 1].e);
    const step = Math.max(0.05, (e - s) / (j1 - j0));
    for (let j = j0; j < j1; j++) out.push({ w: ref[j], s: +(s + (j - j0) * step).toFixed(3), e: +(s + (j - j0 + 1) * step).toFixed(3) });
  };
  for (const [i, j] of [...pairs, [n, m]]) {
    fill(pi, i, pj, j);
    if (i < n) out.push({ w: ref[j], s: words[i].s, e: words[i].e });
    pi = i + 1; pj = j + 1;
  }
  return out;
}
