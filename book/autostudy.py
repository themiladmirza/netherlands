#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Surface a Dutch practice pane while Claude Code is busy; hide it when it isn't.

Wired into Claude Code hooks (see `install` below):

    start   UserPromptSubmit / PreToolUse   -> mark busy, make sure a watcher runs
    stop    Stop / Notification / PermissionRequest / SessionEnd -> unmark, close pane

A detached watcher polls the marker. Only once Claude has been busy for
AUTOSTUDY_DELAY seconds (default 25) does it split the current iTerm2 pane and
start practice.py there, focused. The moment Claude finishes — or needs you —
the pane closes and focus snaps back.

Why a delay and not a prediction: nothing tells us in advance that a tool call
will be slow, so short calls simply never reach the threshold.

    python3 book/autostudy.py status     # what it thinks is going on
    python3 book/autostudy.py disable    # kill switch (survives restarts)
    python3 book/autostudy.py enable
    python3 book/autostudy.py install    # print the hook JSON to merge

Only acts inside iTerm2. Anywhere else (plain Terminal, ssh, CI) it is a no-op.
"""
import json, os, subprocess, sys, time

ROOT     = os.path.dirname(os.path.abspath(__file__))
STATE    = os.path.expanduser("~/.claude/autostudy")
OFF_FLAG = os.path.join(STATE, "disabled")
DELAY    = float(os.environ.get("AUTOSTUDY_DELAY", "25"))
IDLE_EXIT = 900            # watcher gives up after 15 min of quiet

def iterm_session():
    """The iTerm2 session id of the pane Claude is running in, or None."""
    sid = os.environ.get("ITERM_SESSION_ID", "")
    if os.environ.get("TERM_PROGRAM") != "iTerm.app" or ":" not in sid:
        return None
    return sid.split(":", 1)[1].strip()

def path_for(sid):
    os.makedirs(STATE, exist_ok=True)
    return os.path.join(STATE, f"{sid}.json")

def read(sid):
    try:    return json.load(open(path_for(sid), encoding="utf-8"))
    except Exception: return {"busy_since": None, "pane_id": None, "watcher_pid": None}

def write(sid, st):
    tmp = path_for(sid) + ".tmp"
    json.dump(st, open(tmp, "w", encoding="utf-8"))
    os.replace(tmp, path_for(sid))

def alive(pid):
    if not pid: return False
    try: os.kill(int(pid), 0); return True
    except Exception: return False

def osa(script):
    r = subprocess.run(["osascript", "-e", script],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20)
    return r.stdout.decode("utf-8", "replace").strip()

FIND = '''
  set target to missing value
  repeat with w in windows
    repeat with t in tabs of w
      repeat with s in sessions of t
        if (id of s) is "%s" then set target to s
      end repeat
    end repeat
  end repeat
'''

def open_pane(origin):
    cmd = f"python3 {ROOT}/autostudy.py run"
    script = f'''
tell application "iTerm2"
{FIND % origin}
  if target is missing value then return ""
  tell target
    set newSession to (split vertically with same profile)
  end tell
  tell newSession
    write text "clear; {cmd}"
    select
  end tell
  return id of newSession
end tell'''
    return osa(script) or None

def close_pane(pane_id, origin):
    script = f'''
tell application "iTerm2"
  repeat with w in windows
    repeat with t in tabs of w
      repeat with s in sessions of t
        if (id of s) is "{pane_id}" then
          try
            tell s to close
          end try
        end if
      end repeat
    end repeat
  end repeat
{FIND % origin}
  if target is not missing value then tell target to select
end tell'''
    osa(script)

# ---------------------------------------------------------------- hook entry points
def cmd_start():
    sid = iterm_session()
    if not sid or os.path.exists(OFF_FLAG): return
    st = read(sid)
    if st.get("busy_since") is None:
        st["busy_since"] = time.time()
    if not alive(st.get("watcher_pid")):
        p = subprocess.Popen([sys.executable, os.path.abspath(__file__), "watch", sid],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                             stdin=subprocess.DEVNULL, start_new_session=True)
        st["watcher_pid"] = p.pid
    write(sid, st)

def cmd_stop():
    sid = iterm_session()
    if not sid: return
    st = read(sid)
    st["busy_since"] = None
    pane = st.get("pane_id")
    if pane:
        close_pane(pane, sid)            # close immediately, don't wait on the watcher
        st["pane_id"] = None
    write(sid, st)

def cmd_watch(sid):
    last_active = time.time()
    while True:
        time.sleep(1)
        st = read(sid)
        busy, pane = st.get("busy_since"), st.get("pane_id")
        if os.path.exists(OFF_FLAG):
            busy = None
        if busy:
            last_active = time.time()
            if not pane and (time.time() - busy) >= DELAY:
                new = open_pane(sid)
                if new:
                    st["pane_id"] = new; write(sid, st)
        elif pane:
            close_pane(pane, sid)
            st["pane_id"] = None; write(sid, st)
        if not busy and (time.time() - last_active) > IDLE_EXIT:
            st["watcher_pid"] = None; write(sid, st); return

def cmd_run():
    """Runs inside the pane. Keeps offering rounds until the pane is closed."""
    practice = os.path.join(ROOT, "practice.py")
    while True:
        r = subprocess.run([sys.executable, practice, "--count", "30"])
        if r.returncode != 0:
            time.sleep(30)
        print("\n\033[2m— waiting for Claude · next round shortly —\033[0m")
        time.sleep(4)

def cmd_status():
    sid = iterm_session()
    print("iTerm2 session :", sid or "not in iTerm2 (autostudy is a no-op here)")
    print("enabled        :", not os.path.exists(OFF_FLAG))
    print("delay          :", DELAY, "s")
    if sid:
        st = read(sid)
        busy = st.get("busy_since")
        print("busy since     :", f"{time.time()-busy:.0f}s ago" if busy else "not busy")
        print("pane open      :", st.get("pane_id") or "no")
        print("watcher        :", "running" if alive(st.get("watcher_pid")) else "not running")

HOOKS = {
  "start": ["UserPromptSubmit", "PreToolUse"],
  "stop":  ["Stop", "StopFailure", "Notification", "PermissionRequest", "SessionEnd"],
}

def cmd_install():
    me = os.path.abspath(__file__)
    out = {}
    for action, events in HOOKS.items():
        for ev in events:
            out.setdefault(ev, []).append({"hooks": [{
                "type": "command", "command": f"python3 {me} {action}", "async": True}]})
    print(json.dumps({"hooks": out}, indent=2))

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    # Deliberately never read stdin. Claude Code sends the hook payload there,
    # but we don't need it, and reading blocks whenever the writer keeps the pipe
    # open (the case in several harnesses). Leave it untouched.
    try:
        if   cmd == "start":   cmd_start()
        elif cmd == "stop":    cmd_stop()
        elif cmd == "watch":   cmd_watch(sys.argv[2])
        elif cmd == "run":     cmd_run()
        elif cmd == "install": cmd_install()
        elif cmd == "disable":
            os.makedirs(STATE, exist_ok=True); open(OFF_FLAG, "w").close()
            cmd_stop(); print("autostudy disabled")
        elif cmd == "enable":
            os.path.exists(OFF_FLAG) and os.remove(OFF_FLAG); print("autostudy enabled")
        else: cmd_status()
    except Exception:
        pass                            # a hook must never break the session

if __name__ == "__main__":
    main()
