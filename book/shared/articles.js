/* de of het? — a typing drill for the articles. Screen only, never the PDF.
 *
 * The nouns come from the chapter's Woordenlijst (shared/lib/articles.py). Each
 * card shows the bare noun; you type it whole, "de koffie", so the article is
 * learned together with the word. The article is judged the moment it is typed:
 * when the space after it goes in, it turns green or red. Enter checks the whole
 * word. A miss comes back a few cards later until every word has been typed right.
 *
 * Built at runtime inside #nl-articles, like the practice deck, and styled with
 * the deck's classes so the two panels read as one study area.
 */
(function () {
  "use strict";

  var mount = document.getElementById("nl-articles");
  var data  = document.getElementById("nl-articles-data");
  if (!mount || !data) return;
  var WORDS = JSON.parse(data.textContent);
  if (!WORDS.length) return;

  function esc(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
  function norm(s) { return s.trim().toLowerCase().replace(/\s+/g, " "); }
  function bare(s) { return norm(s).normalize("NFD").replace(/[̀-ͯ]/g, ""); }
  function shuffle(a) {
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  mount.className = "deck";
  mount.innerHTML =
    '<div class="deck-head">' +
      '<h2 class="sec deck-title">de of het?</h2>' +
      '<p class="deck-sub">Type each word with its article, e.g. <i>de koffie</i>. ' +
      WORDS.length + ' words from this chapter.</p>' +
    '</div>' +
    '<div class="deck-meter"><i></i></div>' +
    '<div class="deck-card">' +
      '<div class="deck-kicker"></div>' +
      '<div class="deck-front deck-nl"></div>' +
      '<div class="deck-context deck-en"></div>' +
      '<div class="art-field">' +
        '<div class="art-mirror" aria-hidden="true"></div>' +
        '<input class="deck-input art-input" autocomplete="off" autocapitalize="off" ' +
          'autocorrect="off" spellcheck="false" lang="nl" aria-label="the word with its article">' +
      '</div>' +
      '<div class="deck-back"></div>' +
      '<div class="deck-actions"></div>' +
    '</div>' +
    '<div class="deck-hint">Enter checks the word · Enter again for the next one</div>';

  var el = {
    meter:  mount.querySelector(".deck-meter i"),
    card:   mount.querySelector(".deck-card"),
    kicker: mount.querySelector(".deck-kicker"),
    front:  mount.querySelector(".deck-front"),
    en:     mount.querySelector(".deck-context"),
    mirror: mount.querySelector(".art-mirror"),
    input:  mount.querySelector(".art-input"),
    back:   mount.querySelector(".deck-back"),
    actions:mount.querySelector(".deck-actions"),
    hint:   mount.querySelector(".deck-hint")
  };

  var queue, word, done, firstTry, missed, judged, checked;

  function start() {
    queue = shuffle(WORDS.slice());
    done = 0; firstTry = 0; missed = [];
    el.input.hidden = false; el.mirror.hidden = false; el.hint.hidden = false;
    el.en.hidden = false;
    next(false);
  }

  function next(focus) {
    word = queue.shift();
    if (!word) return finish();
    judged = null; checked = false;
    el.card.className = "deck-card";
    el.kicker.textContent = (done + 1) + " / " + WORDS.length;
    el.front.textContent = word.noun;
    el.en.textContent = word.en;
    el.back.innerHTML = ""; el.actions.innerHTML = "";
    el.input.value = ""; el.input.disabled = false;
    paint();
    el.meter.style.width = (100 * done / WORDS.length) + "%";
    if (focus !== false) el.input.focus({ preventScroll: true });
  }

  // The input's own text is transparent; this mirror draws the same characters
  // underneath, so the typed article can be coloured in place.
  function paint() {
    var v = el.input.value, m = v.match(/^(\s*)(\S+)(\s)([\s\S]*)$/);
    if (!m) { el.mirror.innerHTML = esc(v); return; }
    var ok = m[2].toLowerCase() === word.article;
    if (judged === null) {
      judged = ok;
      if (!ok && missed.indexOf(word) < 0) missed.push(word);
    }
    el.mirror.innerHTML = esc(m[1]) + '<span class="' + (ok ? "art-ok" : "art-bad") + '">' +
      esc(m[2]) + "</span>" + esc(m[3] + m[4]);
  }

  function check() {
    var want = word.article + " " + word.noun, got = el.input.value;
    if (!norm(got)) return;
    checked = true;
    el.input.disabled = true;
    var right = norm(got) === norm(want), almost = !right && bare(got) === bare(want);
    var answer = '<span class="art-ok">' + word.article + "</span> " + esc(word.noun);
    if (right || almost) {
      el.card.classList.add(almost ? "is-close" : "is-right");
      if (missed.indexOf(word) < 0) firstTry++;     // a red article already put it there
      done++;
      el.back.innerHTML = answer + (almost ? '<span class="deck-en">mind the accent</span>' : "");
      if (!almost && judged !== false) { setTimeout(function () { if (checked) next(); }, 650); return; }
    } else {
      el.card.classList.add("is-wrong");
      if (missed.indexOf(word) < 0) missed.push(word);
      // back again a few cards later, so it is answered from memory, not echo
      queue.splice(Math.min(3, queue.length), 0, word);
      el.back.innerHTML = answer;
    }
    var b = document.createElement("button");
    b.className = "deck-btn deck-btn--go"; b.type = "button";
    b.innerHTML = 'Next <span class="deck-key">Enter</span>';
    b.addEventListener("click", function () { next(); });
    el.actions.appendChild(b);
    b.focus({ preventScroll: true });
  }

  function finish() {
    el.meter.style.width = "100%";
    el.card.className = "deck-card";
    el.kicker.textContent = "";
    el.front.className = "deck-front deck-done";
    el.front.textContent = firstTry + " of " + WORDS.length + " right the first time";
    el.en.hidden = true;
    el.input.hidden = true; el.mirror.hidden = true; el.hint.hidden = true;
    el.back.innerHTML = missed.length
      ? '<span class="deck-en">Practise these again: ' + missed.map(function (w) {
          return w.article + " " + esc(w.noun); }).join(", ") + "</span>"
      : "";
    el.actions.innerHTML = "";
    var b = document.createElement("button");
    b.className = "deck-btn deck-btn--go"; b.type = "button"; b.textContent = "Again";
    b.addEventListener("click", function () {
      el.front.className = "deck-front deck-nl"; start(); el.input.focus({ preventScroll: true });
    });
    el.actions.appendChild(b);
  }

  el.input.addEventListener("input", paint);
  el.input.addEventListener("keydown", function (e) {
    if (e.key === "Enter") { e.preventDefault(); check(); }
  });
  // after a check the input is disabled; Enter anywhere in the panel moves on
  document.addEventListener("keydown", function (e) {
    // e.target === input is the Enter that just checked: show the result first
    if (e.key !== "Enter" || e.target === el.input || !checked || !word ||
        !mount.contains(document.activeElement)) return;
    e.preventDefault(); next();
  });

  start();
})();
