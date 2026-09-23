/* Practice cards — screen only, never the PDF.
 *
 * Linked, not inlined, so editing this file changes every chapter at once with no
 * rebuild; only *new cards* need one. Everything is built at runtime inside the
 * mount point build.py places after the word list, so the print document never
 * contains a node of it and build.py's layout check (which measures inside .page)
 * cannot see it either.
 *
 * Every card is one entry of the chapter's Woordenlijst — nothing else in the
 * book becomes a card. Two stages per word, following the recall research:
 *
 *   A · recognition   de verjaardag + its sentence   -> FLIP -> birthday, self-grade
 *   B · production    "Gefeliciteerd met je ______." -> TYPE the Dutch   (box 3+)
 *
 * Recognition flips because that is what a flashcard is, and because recall
 * research asks you to *produce* the Dutch, not to spell English. Production
 * types, because that is the half where typing earns its keep: it is where the
 * de/het article and Dutch spelling actually get learned.
 */
(function () {
  "use strict";

  var DAYS     = { 1: 0, 2: 1, 3: 3, 4: 7, 5: 21 };  // box -> days before it returns
  var GRADUATE = 3;          // box at which a translate card unlocks production
  var KEY      = "nl-deck-v1";
  var DAY      = 86400000;

  var mount = document.getElementById("nl-deck");
  var data  = document.getElementById("nl-deck-data");
  if (!mount || !data) return;
  var DECK = JSON.parse(data.textContent);
  if (!DECK.length) return;

  /* ---------- storage: must survive being unavailable ----------
   * Chrome restricts localStorage on file:// origins, and private windows throw
   * on write. Fall back to memory for the session and say so, rather than break. */
  var store = (function () {
    var memory = {}, ok = true;
    try { localStorage.setItem("__probe", "1"); localStorage.removeItem("__probe"); }
    catch (e) { ok = false; }
    return {
      ok: ok,
      read: function () {
        if (!ok) return memory;
        try { return JSON.parse(localStorage.getItem(KEY) || "{}"); }
        catch (e) { return {}; }
      },
      write: function (s) {
        if (!ok) { memory = s; return; }
        try { localStorage.setItem(KEY, JSON.stringify(s)); }
        catch (e) { ok = false; memory = s; }
      }
    };
  })();

  var state = store.read();

  function slot(card, stage) { return card.id + "|" + stage; }
  function box(card, stage)  { var s = state[slot(card, stage)]; return s ? s.box : 0; }
  function due(card, stage, now) {
    var s = state[slot(card, stage)];
    return !s || now >= s.due;
  }
  function grade(card, stage, right) {
    var k = slot(card, stage), s = state[k] || { box: 1 };
    s.box = right ? Math.min(5, (s.box || 1) + 1) : 1;
    s.due = Date.now() + DAYS[s.box] * DAY;
    state[k] = s;
    store.write(state);
  }

  /* ---------- what to study ---------- */
  function queue() {
    var now = Date.now(), old = [], fresh = [];
    DECK.forEach(function (card) {
      if (due(card, "A", now)) (box(card, "A") ? old : fresh).push([card, "A"]);
      // production only once recognition is solid, and only with a sentence
      if (card.cloze && box(card, "A") >= GRADUATE && due(card, "B", now))
        (box(card, "B") ? old : fresh).push([card, "B"]);
    });
    shuffle(old); shuffle(fresh);
    return old.concat(fresh);            // no cap: the whole chapter is available
  }

  function shuffle(a) {
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t;
    }
  }

  function stats() {
    var now = Date.now(), n = { neu: 0, due: 0, rust: 0, klaar: 0 };
    DECK.forEach(function (c) {
      var b = box(c, "A");
      if (!b) n.neu++;
      else if (due(c, "A", now)) n.due++;
      else if (b >= 5) n.klaar++;
      else n.rust++;
    });
    return n;
  }

  /* ---------- answer checking (production only) ---------- */
  function norm(s) {
    return String(s).toLowerCase().normalize("NFC")
      .replace(/[.,!?;:"'’]/g, "").replace(/\s+/g, " ").trim();
  }
  function distance(a, b) {
    var prev = [], i, j;
    for (j = 0; j <= b.length; j++) prev[j] = j;
    for (i = 1; i <= a.length; i++) {
      var cur = [i];
      for (j = 1; j <= b.length; j++)
        cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1,
                          prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
      prev = cur;
    }
    return prev[b.length];
  }
  // "de man / de echtgenoot" accepts either side; the article is never optional.
  function answers(card) {
    return String(card.dutch).split(/\s*\/\s*|\s+·\s+/)
      .map(norm).filter(Boolean);
  }
  function check(typed, card) {
    var got = norm(typed);
    if (!got) return "empty";
    var want = answers(card);
    if (want.indexOf(got) >= 0) return "right";
    for (var i = 0; i < want.length; i++)
      if (distance(got, want[i]) === 1) return "close";
    return "wrong";
  }

  /* ---------- speech: the browser's own Dutch voice ----------
   * No audio files at all. Nothing to generate per chapter, nothing to ship, and
   * chapter 18 speaks the day it is written. Prefer a LOCAL nl-NL voice (macOS
   * ships Xander) over a network one: a study page that goes silent when you are
   * offline is worse than one that sounds a little flat. nl-BE is the last
   * resort — this book teaches Netherlands Dutch, not Flemish. */
  var voice = null, armed = false;

  function pickVoice() {
    var all = window.speechSynthesis ? speechSynthesis.getVoices() : [];
    var nl = all.filter(function (v) { return /^nl/i.test(v.lang); });
    return nl.filter(function (v) { return v.localService && /^nl-NL/i.test(v.lang); })[0]
        || nl.filter(function (v) { return /^nl-NL/i.test(v.lang); })[0]
        || nl[0] || null;
  }

  if (window.speechSynthesis) {
    voice = pickVoice();
    // the list is populated asynchronously, and is empty on the first call
    speechSynthesis.addEventListener("voiceschanged", function () {
      voice = pickVoice() || voice;
    });
  }

  var sayText = "";
  function say(text) {
    sayText = text || "";
    el.say.hidden = !sayText;
    if (armed) speak(sayText);           // never speak before the reader acts
  }

  function speak(text) {
    if (!window.speechSynthesis || !text) return;
    try {
      speechSynthesis.cancel();
      // "luister · heb · ben" reads better as a list than as one run-on word
      var u = new SpeechSynthesisUtterance(String(text).replace(/\s*·\s*/g, ", "));
      if (voice) u.voice = voice;
      u.lang = voice ? voice.lang : "nl-NL";
      u.rate = 0.9;                      // a shade under natural: this is a drill
      speechSynthesis.speak(u);
    } catch (e) { /* no speech available; the cards still work */ }
  }

  /* ---------- UI ---------- */
  var el = {}, round = [], at = 0, shown = false, tally = { right: 0, wrong: 0 };

  mount.className = "deck";
  mount.innerHTML =
    '<div class="deck-head">' +
      '<h2 class="sec deck-title">Practise the words</h2>' +
      '<p class="deck-sub">Every word from this chapter — ' + DECK.length + ' cards.</p>' +
    '</div>' +
    '<div class="deck-card">' +
      '<div class="deck-meter"><i></i></div>' +
      '<button type="button" class="deck-say" aria-label="Hear it" hidden>' +
        '<span aria-hidden="true">\u25b6</span> hear it</button>' +
      '<div class="deck-kicker"></div>' +
      '<div class="deck-front"></div>' +
      '<div class="deck-context"></div>' +
      '<input class="deck-input" autocomplete="off" autocapitalize="off" ' +
             'autocorrect="off" spellcheck="false">' +
      '<div class="deck-back"></div>' +
      '<div class="deck-actions"></div>' +
      '<div class="deck-hint"></div>' +
    '</div>';

  el.card    = mount.querySelector(".deck-card");
  el.say     = mount.querySelector(".deck-say");
  el.meter   = mount.querySelector(".deck-meter i");
  el.kicker  = mount.querySelector(".deck-kicker");
  el.front   = mount.querySelector(".deck-front");
  el.context = mount.querySelector(".deck-context");
  el.input   = mount.querySelector(".deck-input");
  el.back    = mount.querySelector(".deck-back");
  el.actions = mount.querySelector(".deck-actions");
  el.hint    = mount.querySelector(".deck-hint");
  el.sub     = mount.querySelector(".deck-sub");

  // key: an optional keycap chip, so the shortcut sits on the control itself
  // instead of being spelled out in a line of hint text underneath
  function button(label, kind, fn, key) {
    var b = document.createElement("button");
    b.type = "button";
    b.className = "deck-btn" + (kind ? " deck-btn--" + kind : "");
    b.innerHTML = esc(label) +
      (key ? ' <kbd class="deck-key">' + esc(key) + "</kbd>" : "");
    b.addEventListener("click", fn);
    el.actions.appendChild(b);
    return b;
  }

  // The sentence's English, written for the cards (see translations.py) rather
  // than taken from the book, which prints none. Shown whole, not word by word.
  function meaningHtml(card) {
    if (!card.meaning) return "";
    return '<div class="deck-meaning">' + esc(card.meaning) + "</div>";
  }

  function clear() {
    el.actions.innerHTML = "";
    el.back.innerHTML = "";
    el.card.classList.remove("is-right", "is-wrong", "is-close", "is-flipped");
    el.input.hidden = true;
    el.input.disabled = false;
    el.input.value = "";
  }

  function start() {
    state = store.read();      // two chapter tabs must not clobber each other
    round = queue(); at = 0; tally = { right: 0, wrong: 0 };
    if (!round.length) return summary("Nothing due — everything is learned for now.");
    show();
  }

  function summary(message) {
    clear();
    var n = stats();
    el.meter.style.width = "100%";
    el.kicker.textContent = "";
    el.front.innerHTML = '<span class="deck-done">' + esc(message) + "</span>";
    el.context.innerHTML =
      '<span class="deck-tally">' + n.neu + " new · " + n.due +
      " due · " + n.rust + " resting · " + n.klaar + " learned</span>";
    el.hint.textContent = store.ok ? "" :
      "⚠ deze browser bewaart je voortgang niet — serve the page over http";
    button("Go again", "go", start);
  }

  function current() { return round[at]; }

  function show() {
    clear();
    shown = false;
    var pair = current(), card = pair[0], stage = pair[1];

    el.meter.style.width = (at / round.length * 100) + "%";
    el.sub.textContent = "Card " + (at + 1) + " of " + round.length +
      " · " + tally.right + " right, " + tally.wrong + " not yet";

    if (stage === "B") {                       // production: type the Dutch
      el.kicker.textContent = "write it";
      el.front.innerHTML = '<span class="deck-cloze">' + esc(card.cloze) + "</span>";
      el.context.innerHTML = '<span class="deck-en">' + esc(card.back) + "</span>";
      el.input.hidden = false;
      el.input.placeholder = "in Dutch…";
      el.hint.textContent = "include the article · enter to check";
      button("Check", "go", judge);
      say("");        // the sentence contains the answer — silent until checked
      el.input.focus();
      return;
    }

    // recognition: the Dutch word, its sentence, and a flip
    el.kicker.textContent = "recognise";
    el.front.innerHTML = '<span class="deck-nl">' + esc(card.front) + "</span>";
    el.context.innerHTML = card.sentence
      ? '<span class="deck-sentence">' + esc(card.sentence) + "</span>" : "";
    el.hint.textContent = "recall it, then flip";
    button("Flip", "go", flip, "space");
    say(card.dutch);
  }

  function flip() {
    var card = current()[0];
    shown = true;
    el.card.classList.add("is-flipped");
    el.actions.innerHTML = "";
    el.back.innerHTML = '<span class="deck-answer">' + esc(card.back) + "</span>"
                      + meaningHtml(card);
    el.hint.textContent = "did you know it?";
    button("Not yet", "no", function () { score(false); }, "1");
    button("Got it", "yes", function () { score(true); }, "2");
    say(card.dutch);
  }

  function judge() {
    if (shown) return next();
    var pair = current(), card = pair[0];
    var verdict = check(el.input.value, card);
    if (verdict === "empty") { el.input.focus(); return; }

    shown = true;
    el.input.disabled = true;
    var right = verdict !== "wrong";
    el.card.classList.add(verdict === "close" ? "is-close"
                          : right ? "is-right" : "is-wrong");
    el.back.innerHTML = verdict === "right"
      ? '<span class="deck-answer">✓ ' + esc(card.dutch) + "</span>"
      : verdict === "close"
        ? '<span class="deck-answer">≈ ' + esc(card.dutch) +
          ' <span class="deck-en">bijna — telt mee</span></span>'
        : '<span class="deck-answer">✗ ' + esc(card.dutch) + "</span>";
    if (card.sentence)
      el.back.innerHTML += '<div class="deck-said">' + esc(card.sentence) + "</div>"
                         + meaningHtml(card);
    el.hint.textContent = "enter for the next one";
    el.actions.innerHTML = "";
    button("Next", "go", next);
    say(card.dutch);
    record(right);
  }

  function score(right) { record(right); next(); }

  function record(right) {
    var pair = current();
    tally[right ? "right" : "wrong"]++;
    grade(pair[0], pair[1], right);
  }

  function next() {
    at++;
    if (at >= round.length)
      return summary(tally.right + " goed · " + tally.wrong + " nog niet");
    show();
  }

  el.say.addEventListener("click", function () { armed = true; speak(sayText); });
  // the first click anywhere in the deck counts as consent to speak
  mount.addEventListener("click", function () { armed = true; });

  /* keyboard: space flips, 1/2 grade, enter checks and advances */
  mount.addEventListener("keydown", function (e) {
    var typing = !el.input.hidden && !el.input.disabled;
    if (e.key === "Enter") {
      e.preventDefault();
      var go = el.actions.querySelector(".deck-btn--go");
      if (go) go.click();
      return;
    }
    if (typing) return;
    if (e.key === " ") {
      e.preventDefault();
      var first = el.actions.querySelector(".deck-btn--go");
      if (first) first.click();
    }
    if (shown && (e.key === "1" || e.key === "2")) {
      var b = el.actions.querySelector(e.key === "1" ? ".deck-btn--no" : ".deck-btn--yes");
      if (b) b.click();
    }
  });

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  start();
})();
