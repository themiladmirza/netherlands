/* Chapter 4 only — speak the dialogue (proof of concept). Screen only.
 *
 * You pick a role. The other speaker's turns play from audio/dialoog.mp3, cut
 * with the same sentence timings the click-to-replay uses (data-t). Your turns
 * are spoken one sentence at a time and checked by the browser's speech
 * recognition (nl-NL): words light up as they are recognised, and a sentence
 * passes at 80% of its words. Recognition is unreliable on a learner's accent,
 * so "Accept" always lets a sentence through.
 *
 * Hints fade over three rounds (retrieval first, then diminishing cues):
 *   round 1  the sentence appears faded after 3 s
 *   round 2  first letters only
 *   round 3  nothing
 * A miss, "Hint" or "Hear it" drops that sentence back one step.
 *
 * Everything is read from the printed dialogue, so content.py stays the only
 * copy. The panel goes straight after the dialogue page.
 */
(function () {
  "use strict";

  var PASS = 0.8, DELAY = 3000;
  var LEVELS = ["full", "letters", "none"];
  var ROUND_NAMES = ["the sentence, faded", "first letters", "no hints"];
  // what the recogniser may write for a word on the page: numbers as words,
  // and "wauw", which it spells the English way
  var SAME = { negenentwintigste: "29", dertig: "30", zestien: "16", wow: "wauw" };

  document.addEventListener("DOMContentLoaded", function () {
    var dl = document.querySelector("dl.dialogue[data-audio]");
    if (!dl) return;
    var turns = [], who = null;
    [].forEach.call(dl.children, function (n) {
      if (n.tagName === "DT") who = n.textContent.replace(/:\s*$/, "").trim();
      else if (n.tagName === "DD" && who) {
        var says = [].map.call(n.querySelectorAll(".say[data-t]"), function (s) {
          var t = s.dataset.t.split(",").map(Number);
          return { text: s.textContent.replace(/\s+/g, " ").trim(), a: t[0], b: t[1] };
        });
        if (says.length) turns.push({ who: who, says: says });
      }
    });
    if (!turns.length) return;
    var mount = document.createElement("div");
    mount.id = "nl-talk";
    dl.closest(".page").insertAdjacentElement("afterend", mount);
    build(mount, turns, dl.dataset.audio);
  });

  // ---- matching ------------------------------------------------------------
  function canon(w) {
    w = w.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "")
         .replace(/[’'`]/g, "").replace(/[^a-z0-9]/g, "");
    if (SAME[w]) w = SAME[w];
    if (/\d/.test(w)) w = w.replace(/\D/g, "").replace(/^(\d{1,2})00$/, "$1");
    return w;
  }
  function lev(a, b) {
    var d = [], i, j;
    for (i = 0; i <= a.length; i++) d[i] = [i];
    for (j = 1; j <= b.length; j++) d[0][j] = j;
    for (i = 1; i <= a.length; i++)
      for (j = 1; j <= b.length; j++)
        d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1,
                           d[i - 1][j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
    return d[a.length][b.length];
  }
  function near(a, b) {
    if (a === b) return true;
    var n = Math.max(a.length, b.length);
    return n >= 4 && lev(a, b) <= (n >= 7 ? 2 : 1);
  }
  // which of the sentence's words were heard, in any order
  function heard(words, transcript) {
    var got = transcript.split(/\s+/).map(canon).filter(Boolean);
    return words.map(function (w) {
      var c = canon(w);
      if (!c) return true;                         // a lone dash or the like
      for (var i = 0; i < got.length; i++)
        if (near(c, got[i])) { got.splice(i, 1); return true; }
      return false;
    });
  }

  // ---- the panel -------------------------------------------------------------
  function build(mount, turns, src) {
    var Rec = window.SpeechRecognition || window.webkitSpeechRecognition;
    var people = turns.reduce(function (a, t) {
      if (a.indexOf(t.who) < 0) a.push(t.who); return a; }, []);

    mount.className = "deck";
    mount.innerHTML =
      '<div class="deck-head">' +
        '<h2 class="sec deck-title">Speak the dialogue</h2>' +
        '<p class="deck-sub">Take one part. The other speaker talks; you answer out loud. ' +
        'Hints fade over three rounds, then swap parts.' +
        (Rec ? '' : ' <b>This browser has no speech recognition (use Chrome): ' +
                    'say each line, then press Accept.</b>') + '</p>' +
      '</div>' +
      '<div class="deck-meter"><i></i></div>' +
      '<div class="talk-log"></div>' +
      '<div class="deck-card talk-card">' +
        '<div class="deck-kicker"></div>' +
        '<div class="talk-line"></div>' +
        '<div class="talk-heard"></div>' +
        '<div class="deck-actions"></div>' +
      '</div>';

    var el = {
      meter:   mount.querySelector(".deck-meter i"),
      log:     mount.querySelector(".talk-log"),
      card:    mount.querySelector(".talk-card"),
      kicker:  mount.querySelector(".deck-kicker"),
      line:    mount.querySelector(".talk-line"),
      heard:   mount.querySelector(".talk-heard"),
      actions: mount.querySelector(".deck-actions")
    };
    var audio = new Audio(src), rec = null, watchId = 0;
    // state of one run through the dialogue
    var me, round, steps, pos, level, words, got, timer, listening, clean, total, token = 0;

    function button(label, cls, fn) {
      var b = document.createElement("button");
      b.type = "button"; b.className = "deck-btn" + (cls ? " " + cls : "");
      b.innerHTML = label; b.addEventListener("click", fn);
      el.actions.appendChild(b);
      return b;
    }

    // ---- audio: play a stretch of the recording ----
    function play(a, b, then) {
      stopAudio();
      var id = ++watchId;
      audio.currentTime = a;
      var done = function () { if (id === watchId) { watchId++; audio.pause(); if (then) then(); } };
      (function watch() {
        if (id !== watchId) return;
        if (audio.currentTime >= b || audio.ended) return done();
        requestAnimationFrame(watch);
      })();
      audio.play().catch(function () { setTimeout(done, (b - a) * 1000); });
    }
    function stopAudio() { watchId++; audio.pause(); }

    // ---- recognition ----
    function listen() {
      if (!Rec || listening) return;
      var my = token;
      rec = new Rec();
      rec.lang = "nl-NL"; rec.interimResults = true; rec.continuous = true;
      rec.maxAlternatives = 3;
      listening = true;
      el.card.classList.add("is-listening");
      var finals = "";
      rec.onresult = function (e) {
        if (my !== token) return;
        var interim = "", alts = [];
        for (var i = e.resultIndex; i < e.results.length; i++) {
          var r = e.results[i];
          if (r.isFinal) {
            finals += " " + r[0].transcript;
            for (var k = 1; k < r.length; k++) alts.push(r[k].transcript);
          } else interim += " " + r[0].transcript;
        }
        var text = (finals + interim).trim();
        el.heard.textContent = text ? "Heard: " + text : "";
        var h = heard(words, text + " " + alts.join(" "));
        h.forEach(function (ok, i) { if (ok) got[i] = true; });
        render();
        if (score() >= PASS) pass();
      };
      rec.onerror = function (e) {
        if (e.error === "not-allowed" || e.error === "service-not-allowed") {
          el.heard.textContent = "Microphone blocked — allow it for this page, or use Accept.";
          Rec = null;
        }
      };
      rec.onend = function () {
        listening = false;
        el.card.classList.remove("is-listening");
        // Chrome stops after a silence; keep listening while it is still my turn
        if (my === token && Rec && finals.trim() && score() < PASS) miss();
        if (my === token && Rec) setTimeout(function () { if (my === token) listen(); }, 250);
      };
      try { rec.start(); } catch (e) { listening = false; }
    }
    function deafen() {
      token++;
      clearTimeout(timer);
      if (rec) { try { rec.abort(); } catch (e) {} rec = null; }
      listening = false;
      el.card.classList.remove("is-listening");
    }

    // ---- one run --------------------------------------------------------------
    function start(role, r) {
      deafen(); stopAudio();
      me = role; round = r; pos = 0; clean = 0; total = 0;
      steps = [];
      turns.forEach(function (t, ti) {
        if (t.who === me) t.says.forEach(function (s, si) {
          steps.push({ mine: true, s: s, first: si === 0, ti: ti }); total++; });
        else steps.push({ mine: false, t: t, ti: ti });
      });
      el.log.innerHTML = "";
      step();
    }

    function step() {
      deafen();
      el.meter.style.width = (100 * pos / steps.length) + "%";
      el.actions.innerHTML = ""; el.heard.textContent = "";
      el.card.className = "deck-card talk-card";
      var st = steps[pos];
      if (!st) return finish();
      if (!st.mine) {
        el.kicker.textContent = st.t.who;
        el.line.className = "talk-line is-other";
        el.line.textContent = st.t.says.map(function (s) { return s.text; }).join(" ");
        button("Skip", "", function () { stopAudio(); logTurn(st); pos++; step(); });
        var my = token;
        play(st.t.says[0].a, st.t.says[st.t.says.length - 1].b, function () {
          if (my !== token) return;
          logTurn(st); pos++; setTimeout(step, 300);
        });
        return;
      }
      el.kicker.textContent = me + " — your turn · round " + (round + 1) + ": " + ROUND_NAMES[round];
      words = st.s.text.split(" ");
      got = words.map(function () { return false; });
      level = round;
      st.helped = false;
      el.line.className = "talk-line is-mine";
      // round 1: try first, the faded sentence comes after a few seconds
      if (round === 0) {
        level = 2;
        var my = token;
        timer = setTimeout(function () { if (my === token) { level = 0; render(); } }, DELAY);
      }
      render();
      button('Hint', "", function () { help(); });
      // stop listening while it plays, or the speakers answer for you
      button('Hear it', "", function () {
        help();
        deafen();
        play(st.s.a, st.s.b, listen);
      });
      button('Accept <span class="deck-key">Enter</span>', "deck-btn--go", function () { pass(true); });
      listen();
    }

    function score() {
      var n = 0; got.forEach(function (g) { if (g) n++; });
      return n / got.length;
    }
    function render() {
      el.line.innerHTML = words.map(function (w, i) {
        if (got[i]) return '<span class="w is-got">' + w + "</span>";
        if (level === 0) return '<span class="w is-faded">' + w + "</span>";
        if (level === 1) return '<span class="w is-faded">' + w.replace(
          /^([^A-Za-zÀ-ÿ0-9]*[A-Za-zÀ-ÿ0-9])(.*)$/, function (m, a, b) {
            return a + b.replace(/[A-Za-zÀ-ÿ0-9]/g, "_"); }) + "</span>";
        return '<span class="w is-hidden">' + w + "</span>";
      }).join(" ");
    }
    // one step more help for this sentence
    function help() {
      steps[pos].helped = true;
      clearTimeout(timer);
      if (level > 0) level--;
      render();
    }
    function miss() {
      el.card.classList.add("is-wrong");
      help();
      setTimeout(function () { el.card.classList.remove("is-wrong"); }, 600);
    }
    function pass(accepted) {
      var st = steps[pos];
      if (!st || !st.mine) return;
      deafen();
      got = words.map(function () { return true; });
      render();
      el.card.classList.add("is-right");
      if (!st.helped && !accepted) clean++;
      st.accepted = !!accepted;
      logTurn(st);
      pos++;
      setTimeout(step, 600);
    }

    // the conversation so far, above the card
    function logTurn(st) {
      var last = el.log.lastElementChild;
      var text = st.mine ? st.s.text : st.t.says.map(function (s) { return s.text; }).join(" ");
      var row;
      if (st.mine && !st.first && last && last.dataset.ti == st.ti) row = last;
      else {
        row = document.createElement("div");
        row.className = "talk-row" + (st.mine ? " is-mine" : "");
        row.dataset.ti = st.ti;
        row.innerHTML = "<b>" + (st.mine ? me : st.t.who) + ":</b> ";
        el.log.appendChild(row);
      }
      var span = document.createElement("span");
      span.textContent = text + " ";
      if (st.mine && (st.helped || st.accepted)) span.className = "is-helped";
      row.appendChild(span);
      el.log.scrollTop = el.log.scrollHeight;
    }

    function finish() {
      deafen();
      el.meter.style.width = "100%";
      el.kicker.textContent = "Round " + (round + 1) + " done";
      el.line.className = "talk-line deck-done";
      el.line.textContent = clean + " of " + total + " sentences with no help";
      el.heard.textContent = "";
      el.actions.innerHTML = "";
      if (round < 2)
        button("Round " + (round + 2) + ": " + ROUND_NAMES[round + 1], "deck-btn--go",
               function () { start(me, round + 1); });
      var other = people.filter(function (p) { return p !== me; })[0];
      if (other) button("Swap: be " + other, round === 2 ? "deck-btn--go" : "",
                        function () { start(other, 0); });
      button("Again", "", function () { start(me, round); });
    }

    function choose() {
      deafen(); stopAudio();
      el.log.innerHTML = "";
      el.meter.style.width = "0";
      el.kicker.textContent = "Choose your part";
      el.line.className = "talk-line"; el.line.textContent = "";
      el.heard.textContent = Rec ? "Chrome will ask for the microphone the first time." : "";
      el.actions.innerHTML = "";
      people.forEach(function (p, i) {
        button("Be " + p, i ? "" : "deck-btn--go", function () { start(p, 0); });
      });
    }

    // Enter accepts the current sentence, but only while the panel has focus
    document.addEventListener("keydown", function (e) {
      if (e.key !== "Enter" || !mount.contains(document.activeElement)) return;
      var st = steps && steps[pos];
      if (st && st.mine && document.activeElement.tagName !== "BUTTON") {
        e.preventDefault(); pass(true);
      }
    });
    mount.tabIndex = -1;

    choose();
  }
})();
