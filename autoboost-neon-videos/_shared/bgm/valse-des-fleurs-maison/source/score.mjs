// autoboost-62-valse-full — OUR OWN SEQUENCE of Tchaikovsky's "Valse des fleurs"
// (Casse-Noisette op. 71a n.6). Writes two Standard MIDI Files, rendered separately
// by FluidSynth (see render_music.sh).
//
// WHY WE SEQUENCE IT OURSELVES
//   The SCORE is public domain (Tchaikovsky d. 1893). A RECORDING is not, and neither is
//   somebody else's MIDI sequence: a sequencer's performance data (velocities, timing,
//   orchestration choices) is their work. No MIDI of this piece could be found under an
//   explicitly free licence — Mutopia has nine Tchaikovsky pieces and none from the
//   Nutcracker; midiworld's "nutcracker waltz" slot serves an unrelated file; flutetunes
//   publishes a melody-only .mid with no licence statement at all. So every note, duration,
//   velocity, harmonisation and instrument assignment below is written here, by us. The only
//   third-party asset in the chain is the FluidR3_GM sample bank (Frank Wen, MIT licence).
//
// PITCHES
//   The melodic line is the public-domain score: theme A is the horn theme of the Tempo di
//   valse (D major, 3/4) and theme B is the second theme (the descending long-short pattern).
//   Pitches were cross-checked note by note against a published rendering of the same public
//   -domain melody before being written out here. The harmonisation, the counterpoint, the
//   bass line, the accompaniment figures and the whole dynamic plan are ours.
//
// TEMPO
//   Bar = 1.000 s exactly (quarter = 180 bpm, dotted-half = 60). Measured, not assumed: an
//   onset-envelope autocorrelation of the reference recording peaks at 1000 ms (r=0.137) with
//   a secondary peak at 310-330 ms, i.e. three quarters to the bar at ~182-194 bpm. 1.000 s
//   per bar also makes every bar line land on a whole second of the edit, which is why the
//   musical events below sit exactly on the picture's beats.
//
// TWO ORCHESTRATIONS, ONE CONTINUOUS PERFORMANCE
//   tutti.mid   = the TOP half of the orchestra (flute, oboe, clarinet, violins, trumpet,
//                 timpani). It exists only over 0 -> 6.667 s.
//   hollow.mid  = the BOTTOM half (horn, cello, contrabass, viola, harp, pizzicati). It plays
//                 CONTINUOUSLY from 0.000 to 35.400 s — during the hook it is the lower half
//                 of the tutti, after the hook it is the whole orchestra.
//   So the A -> B transition is not a cut and not a crossfade: the top desks simply stop
//   playing at the end of the phrase while the bottom desks play straight through. There is
//   no seam to hide because there is no seam.
//
// THE HANDOVER (this is the delicate point of the brief)
//   The hook's phrase is the horn theme compressed to six bars: A-D-F# | G | F#—— | G F# E |
//   A—— D. The climax note A5 falls on bar 6 beat 1 (t=6.000) and the phrase RESOLVES onto the
//   tonic D on bar 6 beat 3 (t=6.667). The top half plays the climax A5 and releases on the
//   resolution; the D at 6.667 is taken by the cellos and the horn alone. A phrase handed from
//   the top desks to the bottom desks on its own tonic resolution is an ordinary orchestration
//   device, not an edit — and 6.667 s is 13 ms from the 6.68 switch point of the reference
//   variant, i.e. still under the peak of sfx-arrival-stop.
import fs from 'node:fs';

const DIV = 480;               // ticks per quarter
const BEAT = 1;                // 1 beat = 1 quarter
const BAR = 3;                 // 3/4
const bar = (n) => n * BAR;    // bar number -> absolute beat

// ---------------------------------------------------------------- MIDI writer
const vlq = (n) => {
  const out = [n & 0x7f];
  n >>= 7;
  while (n > 0) { out.unshift((n & 0x7f) | 0x80); n >>= 7; }
  return out;
};

class Track {
  constructor(name, ch, program) {
    this.name = name; this.ch = ch; this.program = program; this.ev = [];
  }
  // t and len in beats
  n(t, pitch, len, vel, { gate = 0.92 } = {}) {
    const on = Math.round(t * DIV), off = Math.round((t + len * gate) * DIV);
    this.ev.push({ tick: on, ord: 1, b: [0x90 | this.ch, pitch, vel] });
    this.ev.push({ tick: off, ord: 0, b: [0x80 | this.ch, pitch, 0] });
    return this;
  }
  chord(t, pitches, len, vel, o) { for (const p of pitches) this.n(t, p, len, vel, o); return this; }
  cc(t, num, val) {
    this.ev.push({ tick: Math.round(t * DIV), ord: 2, b: [0xb0 | this.ch, num, Math.max(0, Math.min(127, Math.round(val)))] });
    return this;
  }
  // linear controller ramp, one event every 1/8 beat
  ramp(t0, t1, num, v0, v1) {
    const steps = Math.max(1, Math.round((t1 - t0) * 8));
    for (let i = 0; i <= steps; i++) this.cc(t0 + (t1 - t0) * i / steps, num, v0 + (v1 - v0) * i / steps);
    return this;
  }
  bytes() {
    this.ev.sort((a, b) => a.tick - b.tick || a.ord - b.ord);
    const out = [];
    // track name
    const nm = [...Buffer.from(this.name, 'utf8')];
    out.push(0x00, 0xff, 0x03, ...vlq(nm.length), ...nm);
    out.push(0x00, 0xc0 | this.ch, this.program);
    let last = 0;
    for (const e of this.ev) { out.push(...vlq(e.tick - last), ...e.b); last = e.tick; }
    out.push(0x00, 0xff, 0x2f, 0x00);
    return Buffer.from(out);
  }
}

function writeMidi(file, tracks, usPerQuarter) {
  const head = Buffer.alloc(14);
  head.write('MThd', 0, 'ascii'); head.writeUInt32BE(6, 4);
  head.writeUInt16BE(1, 8); head.writeUInt16BE(tracks.length + 1, 10); head.writeUInt16BE(DIV, 12);
  const tempo = Buffer.from([0x00, 0xff, 0x51, 0x03,
    (usPerQuarter >> 16) & 0xff, (usPerQuarter >> 8) & 0xff, usPerQuarter & 0xff,
    0x00, 0xff, 0x58, 0x04, 3, 2, 24, 8,          // 3/4
    0x00, 0xff, 0x2f, 0x00]);
  const chunks = [head, mtrk(tempo), ...tracks.map(t => mtrk(t.bytes()))];
  fs.writeFileSync(file, Buffer.concat(chunks));
}
function mtrk(body) {
  const h = Buffer.alloc(8); h.write('MTrk', 0, 'ascii'); h.writeUInt32BE(body.length, 4);
  return Buffer.concat([h, body]);
}

// ---------------------------------------------------------------- pitches
const P = {}; // note name -> midi
['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'].forEach((n, i) => {
  for (let o = 0; o <= 8; o++) P[n + o] = (o + 1) * 12 + i;
});
const p = (s) => { if (P[s] === undefined) throw new Error('bad pitch ' + s); return P[s]; };
const ch_ = (...s) => s.map(p);

// harmony used by the accompaniment, per bar of the hollow part
// [bass beat-1 note, "pah" chord for beats 2 and 3]
const H = {
  D:      { bass: 'D2',  pah: ch_('D3', 'F#3', 'A3') },
  Dsus:   { bass: 'D2',  pah: ch_('D3', 'G3', 'A3') },
  A7:     { bass: 'A1',  pah: ch_('C#3', 'E3', 'G3') },
  A:      { bass: 'A1',  pah: ch_('C#3', 'E3', 'A3') },
  A7_Cs:  { bass: 'C#2', pah: ch_('E3', 'G3', 'A3') },
  G_B:    { bass: 'B1',  pah: ch_('D3', 'G3', 'B3') },
  G:      { bass: 'G1',  pah: ch_('D3', 'G3', 'B3') },
  D_Fs:   { bass: 'F#1', pah: ch_('D3', 'F#3', 'A3') },
  A7_E:   { bass: 'E1',  pah: ch_('C#3', 'E3', 'G3') },
};

// =================================================================== TUTTI
// Top desks only. Silent after beat 20 (t = 6.667 s).
function buildTutti() {
  const fl = new Track('Flute', 0, 73);
  const ob = new Track('Oboe', 1, 68);
  const cl = new Track('Clarinet', 2, 71);
  const v1 = new Track('Violins I', 3, 48);   // string ensemble = section, not solo
  const v2 = new Track('Violins II', 4, 48);
  const tp = new Track('Trumpet', 5, 56);
  const ti = new Track('Timpani', 6, 47);
  const all = [fl, ob, cl, v1, v2, tp, ti];
  for (const t of all) { t.cc(0, 7, 100); t.cc(0, 11, 127); t.cc(0, 91, 58); t.cc(0, 93, 0); }

  // --- bar 0 (0.000 -> 1.000): the swing. The top desks are ALMOST absent, per the
  // validated profile (-25..-34 dB RMS). Only a soft clarinet lead-in on the last two
  // eighths, which delivers the theme onto the downbeat of bar 1.
  cl.n(bar(0) + 2.0, p('D5'), 0.5, 48).n(bar(0) + 2.5, p('E5'), 0.5, 56);
  fl.n(bar(0) + 2.5, p('E6'), 0.5, 38);

  // --- bar 1 (1.000 -> 2.000): the tutti enters. Theme A b1: A4 D5 F#5.
  const b1 = [['A4', 3], ['D5', 4], ['F#5', 5]];
  for (const [nt, t] of b1) {
    ob.n(t, p(nt), 1, 74);
    cl.n(t, p(nt), 1, 70);
    v1.n(t, p(nt), 1, 78);
    fl.n(t, p(nt) + 12, 1, 54);
  }
  v2.chord(3, ch_('D4', 'F#4', 'A4'), 3, 60);

  // --- bar 2 (2.000 -> 3.000): G5, Dsus4. The accent the glass break at 2.15 lands on.
  ob.n(6, p('G5'), 3, 88); cl.n(6, p('G5'), 3, 82); v1.n(6, p('G5'), 3, 92);
  fl.n(6, p('G6'), 3, 62);
  v2.chord(6, ch_('D4', 'G4', 'A4'), 3, 72);
  ti.n(6, p('D2'), 0.5, 72);

  // --- bars 3-4 (3.000 -> 5.000): F#5 held, the orchestra thins out (-21..-25 dB zone),
  // then a crescendo through the second half of bar 4 into the cadence.
  ob.n(9, p('F#5'), 5.8, 76); v1.n(9, p('F#5'), 5.8, 78);
  v2.chord(9, ch_('D4', 'F#4', 'A4'), 5.8, 68);
  for (const t of [ob, v1, v2]) t.ramp(9, 13.5, 11, 106, 98).ramp(13.5, 15, 11, 98, 120);

  // --- bar 5 (5.000 -> 6.000): the cadence, crescendo. G5 | F#5 | E5 (pickup at 5.917).
  for (const t of [ob, cl, v1]) { t.n(15, p('G5'), 1, 100); t.n(16, p('F#5'), 1.75, 104); t.n(17.75, p('E5'), 0.25, 100); }
  fl.n(15, p('G6'), 1, 74); fl.n(16, p('F#6'), 1.75, 78); fl.n(17.75, p('E6'), 0.25, 74);
  v2.chord(15, ch_('D4', 'G4', 'A4'), 1, 88);
  v2.chord(16, ch_('D4', 'F#4', 'A4'), 1, 92);
  v2.chord(17, ch_('C#4', 'E4', 'G4'), 1, 96);
  for (const t of [ob, cl, v1, v2, fl]) t.ramp(15, 18, 11, 110, 127);

  // --- bar 6 (6.000 -> 6.667): THE SUMMIT. A5, ff, held under the dolly-in and released
  // on the resolution at 6.667. Nothing in the top desks sounds after that.
  const SUM = 2;                 // beats 18 -> 20 = 6.000 -> 6.667 s
  ob.n(18, p('A5'), SUM, 118, { gate: 1.0 });
  cl.n(18, p('F#5'), SUM, 108, { gate: 1.0 });
  v1.n(18, p('A5'), SUM, 122, { gate: 1.0 });
  v2.chord(18, ch_('D5', 'F#5', 'A4'), SUM, 104, { gate: 1.0 });
  fl.n(18, p('A6'), SUM, 96, { gate: 1.0 });
  tp.n(18, p('D5'), SUM, 92, { gate: 1.0 }); tp.n(18, p('A4'), SUM, 84, { gate: 1.0 });
  ti.n(18, p('D2'), 1.2, 104);
  return all;
}

// =================================================================== HOLLOW
// Bottom desks only, ONE continuous performance 0.000 -> 35.400 s.
// Everything here lives under ~700 Hz in fundamental; the brief's forbidden 1-3.5 kHz band
// is left to the top desks, which only exist during the hook.
function buildHollow() {
  const hn = new Track('French Horn', 0, 60);
  const vc = new Track('Cellos', 1, 42);
  const cb = new Track('Contrabass', 2, 43);
  const hp = new Track('Harp', 3, 46);
  const pz = new Track('Pizzicati', 4, 45);
  const va = new Track('Violas', 5, 41);
  const all = [hn, vc, cb, hp, pz, va];
  for (const t of all) { t.cc(0, 7, 100); t.cc(0, 11, 127); t.cc(0, 91, 46); t.cc(0, 93, 0); }

  // the waltz "oom-pah-pah": contrabass on 1, pizzicati on 2 and 3, both kept low.
  // OOM-pah-pah. The contrabass alone is arco and slow to speak, so the first beat also
  // gets a pizzicato an octave above it — cellos pizz on 1, violas pizz on 2 and 3, which is
  // how the accompaniment of a waltz is actually laid out. Without it the off-beats measured
  // 3.5 dB LOUDER than the downbeat and the bar lost its floor.
  const oompah = (b, h, { vel = 58, bassVel = 62 } = {}) => {
    cb.n(b, p(h.bass), 0.9, bassVel, { gate: 0.8 });
    pz.n(b, p(h.bass) + 12, 0.5, Math.min(127, bassVel + 6), { gate: 0.55 });
    pz.chord(b + 1, h.pah, 0.6, vel - 6, { gate: 0.6 });
    pz.chord(b + 2, h.pah, 0.6, vel - 10, { gate: 0.6 });
  };
  const harpArp = (b, notes, vel = 42) => notes.forEach((n, i) => hp.n(b + i * 0.5, p(n), 0.5, vel, { gate: 0.9 }));

  // ---------------- HOOK 0.000 -> 6.667 : the lower half of the tutti
  // bar 0: the swing. Harp alone plus a barely-there viola. This is the -25..-34 dB opening.
  harpArp(bar(0), ['D2', 'A2', 'D3', 'F#3', 'A3', 'D4'], 62);
  va.n(bar(0), p('A3'), 3, 46);
  cb.n(bar(0), p('D2'), 2.8, 54, { gate: 0.9 });

  // bar 1: the tutti enters — the horn doubles the theme an octave below the top desks.
  const theme_b1 = [['A3', 3], ['D4', 4], ['F#4', 5]];
  for (const [nt, t] of theme_b1) { hn.n(t, p(nt), 1, 92); vc.n(t, p(nt), 1, 80); }
  oompah(bar(1), H.D, { vel: 66, bassVel: 78 });
  harpArp(bar(1), ['D3', 'A3', 'D4', 'F#4', 'A4', 'D5'], 52);

  // bar 2: G, Dsus4, the accent under the glass break.
  hn.n(6, p('G4'), 3, 100); vc.n(6, p('G4'), 3, 88);
  oompah(bar(2), H.Dsus, { vel: 72, bassVel: 88 });
  harpArp(bar(2), ['D3', 'G3', 'D4', 'G4', 'A4', 'D5'], 56);

  // bars 3-4: F# held, thinning out, then the crescendo into the cadence.
  hn.n(9, p('F#4'), 5.8, 88); vc.n(9, p('F#4'), 5.8, 82);
  oompah(bar(3), H.D, { vel: 66, bassVel: 78 });
  oompah(bar(4), H.D, { vel: 70, bassVel: 82 });
  harpArp(bar(3), ['D3', 'F#3', 'A3', 'D4', 'F#4', 'A4'], 58);
  harpArp(bar(4), ['D3', 'F#3', 'A3', 'D4', 'F#4', 'A4'], 64);
  for (const t of [hn, vc]) t.ramp(9, 13.5, 11, 108, 100).ramp(13.5, 15, 11, 100, 122);

  // bar 5: the cadence, crescendo.
  for (const t of [hn, vc]) { t.n(15, p('G4'), 1, 104); t.n(16, p('F#4'), 1.75, 108); t.n(17.75, p('E4'), 0.25, 100); }
  cb.n(15, p('D2'), 1.8, 92, { gate: 0.9 }); pz.chord(16, ch_('D3', 'F#3', 'A3'), 0.6, 76, { gate: 0.6 });
  cb.n(17, p('A1'), 0.9, 96, { gate: 0.85 });
  harpArp(bar(5), ['D3', 'G3', 'A3', 'D4', 'F#4', 'A4'], 62);
  for (const t of [hn, vc, hp]) t.ramp(15, 18, 11, 112, 127);

  // bar 6, beats 1-2: THE SUMMIT, doubling the top desks an octave down.
  hn.n(18, p('A4'), 2, 118, { gate: 1.0 }); vc.n(18, p('A3'), 2, 112, { gate: 1.0 });
  cb.n(18, p('D2'), 1.9, 118, { gate: 0.95 });
  va.chord(18, ch_('D4', 'F#4'), 2, 96, { gate: 1.0 });
  harpArp(bar(6), ['D3', 'A3', 'D4', 'F#4'], 72);

  // ---------------- THE HANDOVER at beat 20 = 6.667 s
  // The top desks have just released on the climax. The tonic resolution is played by the
  // cellos and the horn alone, and the diminuendo that turns the tutti into a bed is written
  // into the performance (expression ramp + velocities), not applied afterwards as a fader move.
  hn.n(20, p('D4'), 1, 84); vc.n(20, p('D4'), 1, 80);
  cb.n(20, p('D2'), 0.9, 76, { gate: 0.85 });
  for (const t of all) t.ramp(19.5, 22.5, 11, 127, 104);

  // ---------------- BED 7.000 -> 35.400 : the hollowed orchestration under the voice
  // Theme A low (cellos), theme B low, theme A' with a harp descant, then the cadence.
  const BED = 76, BEDB = 72;

  // theme A, one octave below the hook statement, as a calm eight-bar period.
  const themeA = (b0, { vel = BED, descant = false, lead = vc } = {}) => {
    const seq = [
      [0, 'A3', 1], [1, 'D4', 1], [2, 'F#4', 1],           // bar 1
      [3, 'G4', 3],                                        // bar 2
      [6, 'F#4', 5.8],                                     // bars 3-4
      [12, 'A3', 1], [13, 'D4', 1], [14, 'F#4', 1],        // bar 5
      [15, 'G4', 1], [16, 'F#4', 1.75], [17.75, 'E4', 0.25],// bar 6
      [18, 'A4', 2], [20, 'D4', 1],                        // bar 7
      [21, 'D4', 2.6],                                     // bar 8
    ];
    for (const [t, nt, l] of seq) lead.n(b0 + t, p(nt), l, vel);
    const harms = [H.D, H.Dsus, H.D, H.D, H.D, H.A7, H.D, H.D];
    harms.forEach((h, i) => oompah(b0 + i * BAR, h, { vel: vel - 10, bassVel: vel + 16 }));
    // bar 6 is the only bar that changes chord inside the bar: Dsus -> D -> A7
    for (let i = 0; i < 8; i++) {
      const arp = harms[i] === H.Dsus ? ['D3', 'G3', 'D4', 'G4', 'A4', 'D5']
        : harms[i] === H.A7 ? ['A2', 'E3', 'G3', 'C#4', 'E4', 'G4']
          : ['D3', 'A3', 'D4', 'F#4', 'A4', 'D5'];
      harpArp(b0 + i * BAR, descant ? arp : arp.slice(0, 4), descant ? vel - 8 : vel - 20);
    }
  };

  themeA(bar(7), { vel: BED });                                  //  7.000 -> 15.000
  // theme B: the second theme, low, over a bass line that walks the octave down D-C#-B-A-G-F#-E-D.
  const themeB = [
    ['F#4', 2, 'C#4', 1, H.D], ['E4', 2, 'B3', 1, H.A7_Cs], ['D4', 2, 'G3', 1, H.G_B], ['C#4', 3, null, 0, H.A],
    ['G4', 2, 'D4', 1, H.G], ['F#4', 2, 'C#4', 1, H.D_Fs], ['E4', 2, 'A3', 1, H.A7_E], ['D4', 3, null, 0, H.D],
  ];
  themeB.forEach(([n1, l1, n2, l2, h], i) => {
    const b0 = bar(15) + i * BAR;
    vc.n(b0, p(n1), l1, BEDB);
    if (n2) vc.n(b0 + l1, p(n2), l2, BEDB - 4);
    oompah(b0, h, { vel: BEDB - 10, bassVel: BEDB + 16 });
    // the harp rests through theme B — the colour change is part of what keeps 35 s of waltz
    // from turning into wallpaper.
    va.chord(b0, h.pah.slice(0, 2).map(x => Math.max(p('C3'), x - 12)), 2.6, 34);
  });                                                            // 15.000 -> 23.000
  themeA(bar(23), { vel: BED + 4, descant: true, lead: hn });    // 23.000 -> 31.000 (recap, horn)
  // the horn recap gets the cellos underneath in octaves
  [[0, 'A2', 1], [1, 'D3', 1], [2, 'F#3', 1], [3, 'G3', 3], [6, 'F#3', 5.8],
  [12, 'A2', 1], [13, 'D3', 1], [14, 'F#3', 1], [15, 'G3', 1], [16, 'F#3', 1.75],
  [18, 'A3', 2], [20, 'D3', 1], [21, 'D3', 2.6]]
    .forEach(([t, nt, l]) => vc.n(bar(23) + t, p(nt), l, BED - 10));

  // ---------------- CODA 31.000 -> 35.400 : the cadence, then the chord the edit fades on.
  vc.n(bar(31), p('A3'), 1, BED).n(bar(31) + 1, p('D4'), 1, BED).n(bar(31) + 2, p('F#4'), 1, BED);
  hn.n(bar(31), p('A3'), 1, BED - 6).n(bar(31) + 1, p('D4'), 1, BED - 6).n(bar(31) + 2, p('F#4'), 1, BED - 6);
  oompah(bar(31), H.D, { vel: BED - 12, bassVel: BED + 14 });
  harpArp(bar(31), ['D3', 'A3', 'D4', 'F#4', 'A4', 'D5'], BED - 16);

  vc.n(bar(32), p('G4'), 3, BED - 2); hn.n(bar(32), p('G4'), 3, BED - 8);
  oompah(bar(32), H.Dsus, { vel: BED - 12, bassVel: BED + 12 });
  harpArp(bar(32), ['D3', 'G3', 'D4', 'G4', 'A4', 'D5'], BED - 16);

  vc.n(bar(33), p('E4'), 3, BED - 4); hn.n(bar(33), p('C#4'), 3, BED - 10);
  oompah(bar(33), H.A7, { vel: BED - 14, bassVel: BED + 8 });
  harpArp(bar(33), ['A2', 'E3', 'G3', 'C#4', 'E4', 'G4'], BED - 18);

  vc.n(bar(34), p('D4'), 3, BED - 6); hn.n(bar(34), p('A3'), 3, BED - 12);
  oompah(bar(34), H.D, { vel: BED - 16, bassVel: BED + 4 });
  harpArp(bar(34), ['D3', 'A3', 'D4', 'F#4', 'A4', 'D5'], BED - 20);

  // last bar: the tonic chord left ringing. The edit's own 1.4 s fade (34.0 -> 35.4) takes it out.
  vc.n(bar(35), p('D4'), 2.2, BED - 14, { gate: 1.0 });
  va.chord(bar(35), ch_('F#3', 'A3'), 2.2, 32, { gate: 1.0 });
  cb.n(bar(35), p('D2'), 2.2, BED - 12, { gate: 1.0 });
  harpArp(bar(35), ['D3', 'A3', 'D4', 'F#4'], BED - 24);
  return all;
}

const OUT = '/work/autoboost-neon-videos/autoboost-62-valse-full/work/midi';
fs.mkdirSync(OUT, { recursive: true });
const US = Math.round(60e6 / 180);        // quarter = 180 bpm -> bar = 1.000 s
writeMidi(`${OUT}/tutti.mid`, buildTutti(), US);
writeMidi(`${OUT}/hollow.mid`, buildHollow(), US);
for (const f of ['tutti.mid', 'hollow.mid']) {
  console.log(`${f.padEnd(12)} ${fs.statSync(`${OUT}/${f}`).size} bytes`);
}
