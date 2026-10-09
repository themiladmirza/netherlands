/* Chapter 3 only — practise the Rangtelwoorden (3.8). Screen only.
 *
 * The card shows "2e"; you type "tweede"; Enter checks it and the word is read
 * aloud (audio/rang-2e.mp3, recorded per audio_script.py). Wrong answers come
 * back three cards later, and the round ends with a first-try score.
 *
 * The pairs are read from the printed Rangtelwoorden card on the page, so the
 * book's list in content.py stays the only copy. The panel goes straight after
 * that page and uses the practice deck's classes.
 */
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    var keep = document.querySelector('[data-keep="rangtelwoorden-3.8"]');
    if (!keep) return;
    var PAIRS = [].map.call(keep.querySelectorAll(".numcols .n"), function (n) {
      return { num: n.querySelector("b").textContent.trim(),
               word: n.querySelector("span").textContent.trim() };
    });
    if (!PAIRS.length) return;

    var mount = document.createElement("div");
    mount.id = "nl-rang";
    keep.closest(".page").insertAdjacentElement("afterend", mount);
    build(mount, PAIRS);
  });

  function shuffle(a) {
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }
  function norm(s) { return s.trim().toLowerCase().replace(/\s+/g, " "); }

  function build(mount, PAIRS) {
    mount.className = "deck";
    mount.innerHTML =
      '<div class="deck-head">' +
        '<h2 class="sec deck-title">Rangtelwoorden</h2>' +
        '<p class="deck-sub">Type the word for each number. You hear it after Enter. ' +
        PAIRS.length + ' numbers.</p>' +
      '</div>' +
      '<div class="deck-meter"><i></i></div>' +
      '<div class="deck-card" tabindex="-1">' +
        '<div class="deck-kicker"></div>' +
        '<div class="deck-front deck-nl"></div>' +
        '<input class="deck-input" autocomplete="off" autocapitalize="off" ' +
          'autocorrect="off" spellcheck="false" lang="nl" aria-label="the number as a word">' +
        '<div class="deck-back"></div>' +
        '<div class="deck-actions"></div>' +
      '</div>' +
      '<div class="deck-hint">Enter checks the word · Enter again for the next one</div>';

    var el = {
      meter:   mount.querySelector(".deck-meter i"),
      card:    mount.querySelector(".deck-card"),
      kicker:  mount.querySelector(".deck-kicker"),
      front:   mount.querySelector(".deck-front"),
      input:   mount.querySelector(".deck-input"),
      back:    mount.querySelector(".deck-back"),
      actions: mount.querySelector(".deck-actions"),
      hint:    mount.querySelector(".deck-hint")
    };
    var audio = new Audio();
    var queue, item, done, firstTry, missed, checked, timer;

    function say(p) {
      audio.pause();
      audio.src = "audio/rang-" + p.num + ".mp3";
      audio.currentTime = 0;
      return audio.play().catch(function () {});
    }

    function start() {
      queue = shuffle(PAIRS.slice());
      done = 0; firstTry = 0; missed = [];
      el.input.hidden = false; el.hint.hidden = false;
      el.front.className = "deck-front deck-nl";
      next(false);
    }

    function next(focus) {
      clearTimeout(timer);
      item = queue.shift();
      if (!item) return finish();
      checked = false;
      el.card.className = "deck-card";
      el.kicker.textContent = (done + 1) + " / " + PAIRS.length;
      el.front.textContent = item.num;
      el.back.innerHTML = ""; el.actions.innerHTML = "";
      el.input.value = ""; el.input.disabled = false;
      el.meter.style.width = (100 * done / PAIRS.length) + "%";
      if (focus !== false) el.input.focus({ preventScroll: true });
    }

    function check() {
      if (checked || !norm(el.input.value)) return;
      checked = true;
      el.input.disabled = true;
      el.card.focus({ preventScroll: true });   // a disabled input drops focus; keep Enter here
      var right = norm(el.input.value) === item.word;
      el.back.innerHTML = '<button type="button" class="rang-say" title="Hear it again">' +
        item.word + "</button>";
      el.back.firstChild.addEventListener("click", function () { say(item); });
      say(item);
      if (right) {
        el.card.classList.add("is-right");
        if (missed.indexOf(item) < 0) firstTry++;
        done++;
        // move on once the word has been heard; the timer covers audio that
        // never plays (blocked, or the file missing)
        var p = item, go = function () {
          audio.onended = null; clearTimeout(timer);
          if (checked && item === p) timer = setTimeout(next, 350);
        };
        audio.onended = go;
        timer = setTimeout(go, 2500);
        return;
      }
      el.card.classList.add("is-wrong");
      if (missed.indexOf(item) < 0) missed.push(item);
      queue.splice(Math.min(3, queue.length), 0, item);
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
      el.front.textContent = firstTry + " of " + PAIRS.length + " right the first time";
      el.input.hidden = true; el.hint.hidden = true;
      el.back.innerHTML = missed.length
        ? '<span class="deck-en">Practise these again: ' + missed.map(function (p) {
            return p.num + " " + p.word; }).join(", ") + "</span>"
        : "";
      el.actions.innerHTML = "";
      var b = document.createElement("button");
      b.className = "deck-btn deck-btn--go"; b.type = "button"; b.textContent = "Again";
      b.addEventListener("click", function () { start(); el.input.focus({ preventScroll: true }); });
      el.actions.appendChild(b);
    }

    el.input.addEventListener("keydown", function (e) {
      if (e.key === "Enter") { e.preventDefault(); check(); }
    });
    // after a check the input is disabled; Enter anywhere in the panel moves on
    // (but not the Enter that did the checking — the result is shown first)
    document.addEventListener("keydown", function (e) {
      if (e.key !== "Enter" || e.target === el.input || !checked || !item ||
          !mount.contains(document.activeElement) ||
          (document.activeElement && document.activeElement.classList.contains("rang-say"))) return;
      e.preventDefault(); next();
    });

    start();
  }
})();
