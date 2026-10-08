/* Answer key — screen only, never the PDF.
 *
 * The answers come from the book's own Bijlage 8 ("Antwoorden bij de opdrachten")
 * and are built into the page at runtime, so print-to-pdf produces an unanswered
 * workbook. Printing a key into the PDF would spoil every exercise in it.
 *
 * Answers land ON the question wherever the exercise has somewhere to put them —
 * in the blank, on the chosen option, in front of the noun — because a list of
 * answers underneath makes you count items to find the one you want. The shapes:
 *
 *   blanks        ol.items > li with .blank      fill each blank in order
 *   a / b items   ol.choice-items                mark the correct .opt
 *   one choice    a grid of a/b/c rows           mark the right row
 *   article list  bare words in a grid           prefix each with de / het
 *   model answers "Mogelijke antwoorden: ..."    a block underneath, which is
 *                                                what those genuinely are
 *
 * Everything is revealed by one class on <html>, so the toggle is pure CSS and
 * nothing has to be re-rendered or undone.
 */
(function () {
  "use strict";

  var KEY = "nl-answers-on";

  var data = document.getElementById("nl-answers-data");
  if (!data) return;
  var ANSWERS;
  try { ANSWERS = JSON.parse(data.textContent); } catch (e) { return; }
  if (!ANSWERS || !Object.keys(ANSWERS).length) return;

  function stored() {
    try { return localStorage.getItem(KEY) === "1"; } catch (e) { return false; }
  }
  function remember(on) {
    try { localStorage.setItem(KEY, on ? "1" : "0"); } catch (e) { /* ignore */ }
  }

  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    return n;
  }
  function decoded(html) { return el("div", null, html); }
  function clean(s) { return String(s).replace(/\s+/g, " ").trim(); }

  /* ---------- "1 Hij – 2 jij / je – 3 Hij" -> ["Hij", "jij / je", "Hij"] ----------
   * Returns null unless the whole string is a clean 1..N run, which is what keeps
   * sentence answers and "Mogelijke antwoorden" out of the in-place path. */
  function numbered(raw) {
    var text = clean(decoded(raw).textContent);
    // "Mogelijke antwoorden:" marks a sample answer, not the only one. Keep the
    // caveat and parse the list behind it rather than giving up on placing it.
    var note = "";
    var m0 = /^(mogelijke\s+(?:antwoorden|vragen)\s*:)\s*([\s\S]+)$/i.exec(text);
    if (m0) { note = m0[1]; text = m0[2]; }
    var parts = text.split(/\s[\u2013\u2014-]\s/);
    var out = [];
    for (var i = 0; i < parts.length; i++) {
      var m = /^(\d+)\s+([\s\S]+)$/.exec(parts[i].trim());
      if (!m || parseInt(m[1], 10) !== i + 1) return null;
      out.push(m[2].trim());
    }
    if (out.length < 2) return null;
    out.note = note;
    return out;
  }

  function bare(v) { return v.replace(/\.$/, ""); }

  /* ---------- shape 1: fill the blanks ---------- */
  function fillBlanks(task, items) {
    var lis = task.querySelectorAll("ol.items > li");
    if (!lis.length || lis.length !== items.length) return false;
    var plan = [];
    for (var i = 0; i < lis.length; i++) {
      var blanks = lis[i].querySelectorAll(".blank");
      if (!blanks.length) return false;
      // a comma inside one item's answer means that item has several blanks
      // ("1 op, om"); a slash does not ("jij / je" is one answer).
      var vals = items[i].split(/,\s*/).map(bare);
      if (blanks.length !== vals.length) return false;
      plan.push([blanks, vals]);
    }
    plan.forEach(function (pair) {
      for (var j = 0; j < pair[0].length; j++)
        pair[0][j].appendChild(el("span", "answer-fill", pair[1][j]));
    });
    return true;
  }

  /* ---------- shape 2: pick one of two forms, marked at the choice ---------- */
  function markChoiceForms(task, items) {
    var lis = task.querySelectorAll("ol.items > li");
    if (!lis.length || lis.length !== items.length) return false;
    var picks = [];
    for (var i = 0; i < lis.length; i++) {
      var c = lis[i].querySelector(".choice");
      if (!c) return false;
      picks.push(c);
    }
    // The right form is written after the pair rather than highlighted inside it:
    // some choices contain a nested gloss, so splitting their markup in half is
    // not safe, and naming the answer is just as clear.
    for (var j = 0; j < picks.length; j++)
      picks[j].parentNode.insertBefore(
        el("span", "answer-fill", "\u2192 " + items[j]), picks[j].nextSibling);
    return true;
  }

  /* ---------- shape 3: one of a / b per item ---------- */
  function markChoices(task, items) {
    var lis = task.querySelectorAll("ol.choice-items > li");
    if (!lis.length || lis.length !== items.length) return false;
    items = items.map(bare);
    if (!items.every(function (v) { return /^[a-z]$/i.test(v); })) return false;
    var hits = 0;
    for (var i = 0; i < lis.length; i++) {
      var opts = lis[i].querySelectorAll(".opt");
      for (var j = 0; j < opts.length; j++) {
        var tag = opts[j].querySelector("span");
        if (tag && clean(tag.textContent).toLowerCase() === items[i].toLowerCase()) {
          opts[j].classList.add("is-answer");
          hits++;
        }
      }
    }
    return hits === lis.length;
  }

  /* ---------- shape: an answer under each numbered question ----------
   * "Answer the questions" has no blank to fill and no option to tick, but its
   * answers are numbered 1..N against N questions, so each one belongs under the
   * question it answers rather than in a list at the foot of the exercise. */
  function answerPerItem(task, items) {
    var lis = task.querySelectorAll("ol.items > li");
    if (!lis.length || lis.length !== items.length) return false;
    for (var i = 0; i < lis.length; i++)
      lis[i].appendChild(el("span", "answer-inline", items[i]));
    if (items.note) {
      var head = task.querySelector(".ins") || task.querySelector("ol.items");
      head.parentNode.insertBefore(el("div", "answer-note", items.note),
                                   task.querySelector("ol.items"));
    }
    return true;
  }

  /* ---------- shape 3: a single a / b / c, in a plain grid ---------- */
  // An exercise's illustration can sit after the .task div rather than inside it
  // (ch3's Opdracht 10 is a photograph with a/b/c labels over it), so the search
  // runs over the task plus everything up to the next exercise.
  function scopeOf(task) {
    var nodes = [task];
    for (var n = task.nextElementSibling; n; n = n.nextElementSibling) {
      if (n.classList && n.classList.contains("task")) break;
      nodes.push(n);
    }
    return nodes;
  }
  function findAll(task, sel) {
    var out = [];
    scopeOf(task).forEach(function (n) {
      if (n.matches && n.matches(sel)) out.push(n);
      out.push.apply(out, n.querySelectorAll(sel));
    });
    return out;
  }

  function markSingle(task, raw) {
    var letter = clean(decoded(raw).textContent).toLowerCase();
    if (!/^[a-z]$/.test(letter)) return false;
    // .dutch is the lettered column of a plain a/b/c grid; .photolabels span is
    // the same question asked over a photograph
    var tags = findAll(task, ".dutch, .photolabels span");
    for (var i = 0; i < tags.length; i++) {
      if (clean(tags[i].textContent).toLowerCase() !== letter) continue;
      tags[i].classList.add("is-answer");
      var next = tags[i].nextElementSibling;
      if (next) next.classList.add("is-answer");
      return true;
    }
    return false;
  }

  /* ---------- shape 4: put the article in front of each noun ---------- */
  function prefixArticles(task, raw) {
    var spans = decoded(raw).querySelectorAll(".answer-cols span");
    if (!spans.length) return false;
    var article = {};
    for (var i = 0; i < spans.length; i++) {
      var m = /^(de|het)\s+(.+)$/i.exec(clean(spans[i].textContent));
      if (m) article[m[2].toLowerCase()] = m[1];
    }
    if (!Object.keys(article).length) return false;

    // walked by hand rather than with a TreeWalker: one less global to depend on,
    // and it is the same traversal
    var targets = [];
    (function walk(n) {
      for (var c = n.firstChild; c; c = c.nextSibling) {
        if (c.nodeType === 3) {
          var word = clean(c.nodeValue).toLowerCase();
          if (word && article[word]) targets.push([c, article[word]]);
        } else if (c.nodeType === 1) walk(c);
      }
    })(task);
    if (!targets.length) return false;
    targets.forEach(function (t) {
      var span = el("span", "answer-article", t[1] + " ");
      t[0].parentNode.insertBefore(span, t[0]);
    });
    return true;
  }

  /* ---------- attach ---------- */
  var placed = 0, inline = 0;
  Object.keys(ANSWERS).forEach(function (num) {
    var task = document.querySelector('.task[data-opdracht="' + num + '"]');
    if (!task) return;
    var raw = ANSWERS[num];
    var items = numbered(raw);

    var done = (items && fillBlanks(task, items)) ||
               (items && markChoiceForms(task, items)) ||
               (items && markChoices(task, items)) ||
               (items && answerPerItem(task, items)) ||
               markSingle(task, raw) ||
               prefixArticles(task, raw);

    if (done) { inline++; }
    else {
      // model answers and rewritten sentences have nowhere to sit inside the
      // question, and a block is the honest shape for them
      task.appendChild(el("div", "answer",
        '<span class="answer-tag">Antwoord</span>' +
        '<div class="answer-body">' + raw + "</div>"));
    }
    placed++;
  });
  if (!placed) return;

  /* ---------- the toggle ---------- */
  var bar = el("button", "answers-toggle");
  bar.type = "button";
  document.body.appendChild(bar);

  function paint(on) {
    document.documentElement.classList.toggle("answers-on", on);
    bar.setAttribute("aria-pressed", on ? "true" : "false");
    bar.innerHTML = '<span class="answers-dot" aria-hidden="true"></span>' +
      (on ? "Answers shown" : "Show answers") +
      ' <span class="answers-count">' + placed + "</span>";
  }
  function set(on) { paint(on); remember(on); }

  bar.addEventListener("click", function () {
    set(!document.documentElement.classList.contains("answers-on"));
  });
  document.addEventListener("keydown", function (e) {
    if (e.key !== "a" && e.key !== "A") return;
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    var t = e.target;
    if (t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.isContentEditable)) return;
    set(!document.documentElement.classList.contains("answers-on"));
  });

  paint(stored());
})();
