/* Answer key — screen only, never the PDF.
 *
 * The answers come from the book's own Bijlage 8 ("Antwoorden bij de opdrachten")
 * and are built into the page at runtime, so print-to-pdf produces an unanswered
 * workbook. Printing a key into the PDF would spoil every exercise in it.
 *
 * The toggle is fixed to the viewport so it is reachable from any page of the
 * chapter without scrolling back, and the choice is remembered between visits.
 *
 * Only some exercises have answers: the book answers 2 of chapter 1's 12
 * Opdrachten, 5 of chapter 2's 16, and 4 of chapter 3's 13. Exercises with no
 * answer are left completely untouched — no empty block, no "no answer" note,
 * because speaking and open writing tasks are not meant to have one.
 */
(function () {
  "use strict";

  var KEY = "nl-answers-on";

  var data = document.getElementById("nl-answers-data");
  if (!data) return;
  var ANSWERS;
  try { ANSWERS = JSON.parse(data.textContent); } catch (e) { return; }
  if (!ANSWERS || !Object.keys(ANSWERS).length) return;

  /* ---------- remember the setting, but never break without storage ---------- */
  function stored() {
    try { return localStorage.getItem(KEY) === "1"; } catch (e) { return false; }
  }
  function remember(on) {
    try { localStorage.setItem(KEY, on ? "1" : "0"); } catch (e) { /* ignore */ }
  }

  /* ---------- attach each answer to its exercise ---------- */
  var count = 0;
  Object.keys(ANSWERS).forEach(function (num) {
    var task = document.querySelector('.task[data-opdracht="' + num + '"]');
    if (!task) return;                     // exercise not on this page
    var box = document.createElement("div");
    box.className = "answer";
    box.innerHTML = '<span class="answer-tag">Antwoord</span>' +
                    '<div class="answer-body">' + ANSWERS[num] + "</div>";
    task.appendChild(box);
    count++;
  });
  if (!count) return;

  /* ---------- the toggle ---------- */
  var bar = document.createElement("button");
  bar.type = "button";
  bar.className = "answers-toggle";
  bar.setAttribute("aria-pressed", "false");
  document.body.appendChild(bar);

  function paint(on) {
    document.documentElement.classList.toggle("answers-on", on);
    bar.setAttribute("aria-pressed", on ? "true" : "false");
    bar.innerHTML = '<span class="answers-dot" aria-hidden="true"></span>' +
      (on ? "Answers shown" : "Show answers") +
      ' <span class="answers-count">' + count + "</span>";
  }

  function set(on) { paint(on); remember(on); }

  bar.addEventListener("click", function () {
    set(!document.documentElement.classList.contains("answers-on"));
  });

  // "a" toggles from anywhere, as long as you are not typing into the deck
  document.addEventListener("keydown", function (e) {
    if (e.key !== "a" && e.key !== "A") return;
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    var t = e.target;
    if (t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.isContentEditable)) return;
    set(!document.documentElement.classList.contains("answers-on"));
  });

  paint(stored());
})();
