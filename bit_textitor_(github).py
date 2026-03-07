import tkinter as tk
from tkinter import ttk, font, filedialog, messagebox
from pathlib import Path
import importlib.util
import random
import math
import time

# import openai
try:
    from openai import OpenAI
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# ═══════════════════════════════════════════════════════════════════════════════
# BUILT-IN ANIMATIONS
# Format: {"interval_ms": int, "init_state": fn()->dict, "draw": fn(canvas,frame,w,h,state)}
# ═══════════════════════════════════════════════════════════════════════════════

def _sf_init():
    return {"stars": [[random.random(), random.random(),
                        random.uniform(0.3, 1.5), random.uniform(1.0, 2.5)]
                       for _ in range(150)]}

def _sf_draw(canvas, frame, w, h, state):
    canvas.configure(bg="#05060f")
    for s in state["stars"]:
        s[1] += s[2] / max(h, 1)
        if s[1] > 1.0:
            s[1] = 0.0
            s[0] = random.random()
        px, py = s[0] * w, s[1] * h
        bri = int(160 + 95 * math.sin(frame * 0.07 + s[0] * 20))
        c = f"#{bri:02x}{bri:02x}{min(bri + 20, 255):02x}"
        canvas.create_oval(px - s[3], py - s[3], px + s[3], py + s[3],
                           fill=c, outline="", tags="anim_layer")

MCHARS = "ｦｧｨｩｪｫｬｭｮｯｰｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def _mx_init():
    return {"cols": {}}

def _mx_draw(canvas, frame, w, h, state):
    canvas.configure(bg="#000000")
    cw = 14
    ncols = max(1, w // cw)
    cols = state["cols"]
    for c in range(ncols):
        if c not in cols:
            cols[c] = [random.randint(-h, 0), random.randint(6, 18), random.randint(6, 16)]
    for c in list(cols.keys()):
        if c >= ncols:
            del cols[c]
            continue
        y, spd, length = cols[c]
        x = c * cw + cw // 2
        for i in range(length):
            cy = y - i * cw
            if 0 <= cy <= h:
                g = int(200 * (1 - i / length))
                color = "#ccffcc" if i == 0 else f"#00{g:02x}00"
                canvas.create_text(x, cy, text=random.choice(MCHARS),
                                   fill=color, font=("Courier", 9, "bold"),
                                   tags="anim_layer")
        cols[c][0] += spd
        if y - length * cw > h:
            cols[c] = [random.randint(-30, 0), random.randint(6, 18), random.randint(6, 16)]

def _au_init():
    return {"t": 0.0}

def _au_draw(canvas, frame, w, h, state):
    canvas.configure(bg="#010108")
    t = state["t"]
    bands = [
        ((0, 180, 120), 0.30, 0.10),
        ((0,  80, 200), 0.42, 0.09),
        ((130, 0, 200), 0.25, 0.08),
        ((0, 200, 170), 0.36, 0.09),
    ]
    for (r, g, b), cy_frac, sigma_frac in bands:
        cy = h * cy_frac
        sigma = h * sigma_frac
        for row in range(0, h, 3):
            dist = abs(row - cy)
            intensity = math.exp(-dist ** 2 / (2 * sigma ** 2))
            wave = 0.6 + 0.4 * math.sin(row * 0.015 + t)
            v = int(intensity * wave * 220)
            if v < 4:
                continue
            col = f"#{min(r*v//220,255):02x}{min(g*v//220,255):02x}{min(b*v//220,255):02x}"
            canvas.create_line(0, row, w, row, fill=col, width=3, tags="anim_layer")
    state["t"] += 0.04

def _pt_init():
    cs = ["#4a90d9", "#e74c3c", "#2ecc71", "#9b59b6", "#f39c12", "#1abc9c"]
    return {"pts": [{"x": random.random(), "y": random.random(),
                     "vx": random.uniform(-0.0015, 0.0015),
                     "vy": random.uniform(-0.0015, 0.0015),
                     "r": random.uniform(2.5, 5.0),
                     "c": random.choice(cs),
                     "ph": random.uniform(0, 6.28)} for _ in range(50)]}

def _pt_draw(canvas, frame, w, h, state):
    canvas.configure(bg="#0a0a18")
    pts = state["pts"]
    for p in pts:
        p["x"] = (p["x"] + p["vx"]) % 1.0
        p["y"] = (p["y"] + p["vy"]) % 1.0
    for i, p in enumerate(pts):
        px, py = p["x"] * w, p["y"] * h
        for j in range(i + 1, len(pts)):
            q = pts[j]
            d = math.hypot(px - q["x"] * w, py - q["y"] * h)
            if d < 110:
                canvas.create_line(px, py, q["x"] * w, q["y"] * h,
                                   fill="#1a2a4a", width=1, tags="anim_layer")
    for p in pts:
        px, py = p["x"] * w, p["y"] * h
        r = p["r"] * (0.8 + 0.4 * math.sin(frame * 0.06 + p["ph"]))
        canvas.create_oval(px - r, py - r, px + r, py + r,
                           fill=p["c"], outline="", tags="anim_layer")

def _wv_init():
    return {"t": 0.0}

def _wv_draw(canvas, frame, w, h, state):
    canvas.configure(bg="#001f3f")
    t = state["t"]
    colors = ["#004080", "#0055aa", "#0074D9", "#7FDBFF"]
    for i, color in enumerate(colors):
        pts = [0, h]
        for x in range(0, w + 4, 4):
            y = (h * 0.45
                 + h * 0.15 * math.sin(x * 0.012 + t + i * 0.9)
                 + h * 0.08 * math.sin(x * 0.025 + t * 1.3 + i))
            pts += [x, y]
        pts += [w, h]
        canvas.create_polygon(pts, fill=color, outline="", tags="anim_layer")
    state["t"] += 0.025

ANIMATIONS: dict = {
    "None":        None,
    "Starfield":   {"interval_ms": 50, "init_state": _sf_init, "draw": _sf_draw},
    "Matrix Rain": {"interval_ms": 60, "init_state": _mx_init, "draw": _mx_draw},
    "Aurora":      {"interval_ms": 40, "init_state": _au_init, "draw": _au_draw},
    "Particles":   {"interval_ms": 45, "init_state": _pt_init, "draw": _pt_draw},
    "Waves":       {"interval_ms": 40, "init_state": _wv_init, "draw": _wv_draw},
}

ANIM_BORDER = 20  # px of animated canvas visible around the text widget

# ═══════════════════════════════════════════════════════════════════════════════
# THEMES
# ═══════════════════════════════════════════════════════════════════════════════
THEMES = {
    "light": {
        "bg":       "#ffffff", "fg":      "#1e1e1e",
        "sel_bg":   "#4a90d9", "sel_fg":  "#ffffff",
        "cursor":   "#1e1e1e",
        "toolbar":  "#ececec", "status":  "#d6d6d6",
        "ai_bg":    "#f5f5f5", "ai_fg":   "#333333",
        "pane":     "#bbbbbb", "root_bg": "#ececec",
        "btn_text": "Dark Mode",
    },
    "dark": {
        "bg":       "#1e1e2e", "fg":      "#cdd6f4",
        "sel_bg":   "#45475a", "sel_fg":  "#cdd6f4",
        "cursor":   "#f5c2e7",
        "toolbar":  "#181825", "status":  "#11111b",
        "ai_bg":    "#181825", "ai_fg":   "#a6adc8",
        "pane":     "#313244", "root_bg": "#11111b",
        "btn_text": "Light Mode",
    },
}

# ═══════════════════════════════════════════════════════════════════════════════
# STATE
# ═══════════════════════════════════════════════════════════════════════════════
ai_on_off        = False
saved            = False
file_name_asked  = False
file_path        = None
is_dirty         = False
current_anim     = None
current_interval = 200
anim_state       = {}
anim_frame_count = 0
_after_id        = None
current_theme    = "light"
_screensaver_on  = False
_ss_pre_anim     = "None"
_ss_cycle_idx    = 0
_ss_switch_id    = None
_last_activity   = 0.0   # set after root starts

# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def set_ai_output(msg):
    ai_output.configure(state=tk.NORMAL)
    ai_output.delete("1.0", tk.END)
    ai_output.insert(tk.END, msg)
    ai_output.configure(state=tk.DISABLED)

def mark_dirty(event=None):
    global is_dirty
    if not is_dirty:
        is_dirty = True
        t = root.title()
        if not t.startswith("* "):
            root.title("* " + t)
    update_status()

def mark_clean(path=None):
    global is_dirty, saved
    is_dirty = False
    saved = True
    root.title(f"Bit Textitor — {Path(path).name}" if path else "Bit Textitor — Untitled")

def update_status(event=None):
    content = text.get("1.0", "end-1c")
    words = len(content.split()) if content.strip() else 0
    chars = len(content)
    try:
        row, col = text.index(tk.INSERT).split(".")
        status_var.set(f"Ln {row}, Col {int(col)+1}   |   Words: {words}   |   Chars: {chars}")
    except Exception:
        status_var.set(f"Words: {words}   |   Chars: {chars}")

# ═══════════════════════════════════════════════════════════════════════════════
# THEME
# ═══════════════════════════════════════════════════════════════════════════════
def apply_theme(name):
    global current_theme
    current_theme = name
    t = THEMES[name]
    text.configure(bg=t["bg"], fg=t["fg"],
                   insertbackground=t["cursor"],
                   selectbackground=t["sel_bg"], selectforeground=t["sel_fg"])
    if current_anim is None:
        bg_canvas.configure(bg=t["bg"])
    ai_output.configure(state=tk.NORMAL, bg=t["ai_bg"], fg=t["ai_fg"])
    ai_output.configure(state=tk.DISABLED)
    style.configure("Toolbar.TFrame", background=t["toolbar"])
    style.configure("Status.TFrame",  background=t["status"])
    style.configure("Status.TLabel",  background=t["status"])
    pane.configure(background=t["pane"])
    root.configure(background=t["root_bg"])
    for lbl in _toolbar_labels:
        lbl.configure(background=t["toolbar"], foreground=t["fg"])
    theme_btn.configure(text=t["btn_text"])

def toggle_theme():
    apply_theme("dark" if current_theme == "light" else "light")

# ═══════════════════════════════════════════════════════════════════════════════
# FULLSCREEN
# ═══════════════════════════════════════════════════════════════════════════════
def toggle_fullscreen():
    state = root.attributes("-fullscreen")
    root.attributes("-fullscreen", not state)

# ═══════════════════════════════════════════════════════════════════════════════
# FILE OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════════
def new_file():
    global is_dirty, file_name_asked, file_path, saved
    if is_dirty:
        result = messagebox.askyesnocancel("New File", "Save current file first?", icon="warning")
        if result is True:
            update()
        elif result is None:
            return
    text.delete("1.0", tk.END)
    file_path = None
    file_name_asked = False
    saved = False
    is_dirty = False
    root.title("Bit Textitor — Untitled")
    update_status()

def open_file():
    global file_name_asked, file_path, saved, is_dirty
    fp = filedialog.askopenfilename(
        defaultextension=".txtr",
        filetypes=[("Textitor Files", "*.txtr"), ("Text Files", "*.txt"),
                   ("Log Files", "*.log"), ("All Files", "*.*")])
    if fp:
        with open(fp, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        text.delete("1.0", tk.END)
        text.insert(tk.END, content)
        file_path = fp
        file_name_asked = True
        mark_clean(fp)
        update_status()

def save_file():
    global file_name_asked, file_path
    fp = filedialog.asksaveasfilename(
        defaultextension=".txtr",
        filetypes=[("Textitor Files", "*.txtr"), ("Text Files", "*.txt"),
                   ("All Files", "*.*")])
    if fp:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(text.get("1.0", tk.END))
        file_path = fp
        file_name_asked = True
        mark_clean(fp)

def update():
    global file_name_asked, file_path
    if not file_name_asked or not file_path:
        save_file()
    elif file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text.get("1.0", tk.END))
        mark_clean(file_path)

def close():
    if is_dirty:
        r = messagebox.askyesnocancel("Unsaved Changes", "Save before closing?", icon="warning")
        if r is True:
            update()
            root.destroy()
        elif r is False:
            root.destroy()
    else:
        root.destroy()

# ═══════════════════════════════════════════════════════════════════════════════
# AI
# ═══════════════════════════════════════════════════════════════════════════════
def _call_ai(system_prompt):
    if not OPENAI_AVAILABLE:
        set_ai_output("OpenAI package not installed.\nRun: pip install openai")
        return
    content = text.get("1.0", "end-1c")
    if not content.strip():
        set_ai_output("Nothing to process — write some text first.")
        return
    set_ai_output("Working…")
    root.update()
    try:
        client = OpenAI(api_key="your-openai-api-key-here")
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": system_prompt + content}])
        set_ai_output(completion.choices[0].message.content)
    except openai.RateLimitError:
        set_ai_output("Rate limit reached. Please wait and try again.")
    except openai.AuthenticationError:
        set_ai_output("Invalid API key. Update api_key in the code.")
    except Exception as e:
        set_ai_output(f"Error: {e}")

def ai_on():
    global ai_on_off
    ai_on_off = True
    ai_toggle_btn.configure(text="AI: ON", foreground="green")
    set_ai_output("AI is ON. Select a function from the toolbar or AI menu.")

def ai_off():
    global ai_on_off
    ai_on_off = False
    ai_toggle_btn.configure(text="AI: OFF", foreground="red")
    set_ai_output("AI is OFF. Click 'AI: OFF' or use the AI menu to enable.")

def toggle_ai():
    ai_off() if ai_on_off else ai_on()

def ai_grammar():
    if not ai_on_off:
        set_ai_output("AI is OFF. Enable it first (F1).")
        return
    _call_ai("Review the following text for grammar, punctuation, and capitalization. "
             "Give specific numbered suggestions. If already correct, say so briefly.\n\n")

def ai_summarize():
    if not ai_on_off:
        set_ai_output("AI is OFF. Enable it first (F1).")
        return
    _call_ai("Summarize the following text in 3–5 bullet points:\n\n")

def ai_translate():
    if not ai_on_off:
        set_ai_output("AI is OFF. Enable it first (F1).")
        return
    _call_ai("Translate the following to English (or to Spanish if already English). "
             "Show the detected source language and the translation.\n\n")

# ═══════════════════════════════════════════════════════════════════════════════
# FORMATTING
# ═══════════════════════════════════════════════════════════════════════════════
def _toggle_format(tag, **font_kwargs):
    try:
        sel_start = text.index("sel.first")
        sel_end   = text.index("sel.last")
    except tk.TclError:
        return
    base = font.Font(font=text.cget("font"))
    base.configure(**font_kwargs)
    text.tag_configure(tag, font=base)
    if tag in text.tag_names(sel_start):
        text.tag_remove(tag, sel_start, sel_end)
    else:
        text.tag_add(tag, sel_start, sel_end)

def bolden_text():        _toggle_format("bold",          weight="bold")
def italicize_text():     _toggle_format("italic",        slant="italic")
def underline_text():     _toggle_format("underline",     underline=True)
def strikethrough_text(): _toggle_format("strikethrough", overstrike=True)

def apply_font(*_):
    try:
        text.configure(font=(font_family_var.get(), int(font_size_var.get())))
    except ValueError:
        pass

# ═══════════════════════════════════════════════════════════════════════════════
# ANIMATION SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════
def _resize_text_window():
    if _screensaver_on:
        bg_canvas.itemconfig(text_win, state="hidden")
        return
    w = bg_canvas.winfo_width()
    h = bg_canvas.winfo_height()
    border = ANIM_BORDER if current_anim is not None else 0
    bg_canvas.coords(text_win, border, border)
    bg_canvas.itemconfig(text_win, state="normal",
                         width=max(1, w - 2 * border),
                         height=max(1, h - 2 * border))

def _on_canvas_resize(event):
    if _screensaver_on:
        return
    border = ANIM_BORDER if current_anim is not None else 0
    bg_canvas.coords(text_win, border, border)
    bg_canvas.itemconfig(text_win, state="normal",
                         width=max(1, event.width - 2 * border),
                         height=max(1, event.height - 2 * border))

def _animation_loop():
    global anim_frame_count, _after_id
    if current_anim is not None:
        w = bg_canvas.winfo_width()
        h = bg_canvas.winfo_height()
        if w > 1 and h > 1:
            bg_canvas.delete("anim_layer")
            current_anim["draw"](bg_canvas, anim_frame_count, w, h, anim_state)
            anim_frame_count += 1
    _after_id = root.after(current_interval, _animation_loop)

def _apply_anim_raw(name):
    """Switch animation without touching anim_name_var (used by screensaver)."""
    global current_anim, current_interval, anim_state, anim_frame_count
    anim = ANIMATIONS.get(name)
    current_anim = anim
    bg_canvas.delete("anim_layer")
    if anim is None:
        current_interval = 200
        bg_canvas.configure(bg=THEMES[current_theme]["bg"])
    else:
        current_interval = anim.get("interval_ms", 50)
        anim_state = anim["init_state"]()
        anim_frame_count = 0

def set_animation(name):
    global current_anim, current_interval, anim_state, anim_frame_count
    anim_name_var.set(name)
    _apply_anim_raw(name)
    if current_anim is None:
        bg_canvas.configure(bg=THEMES[current_theme]["bg"])
    _resize_text_window()

def load_animation_from_file():
    global _anim_insert_idx
    fp = filedialog.askopenfilename(
        title="Load Animation from File",
        filetypes=[("Python files", "*.py"), ("All files", "*.*")])
    if not fp:
        return
    try:
        spec = importlib.util.spec_from_file_location("user_anim", fp)
        mod  = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        name = getattr(mod, "ANIMATION_NAME", Path(fp).stem)
        ANIMATIONS[name] = {
            "interval_ms": getattr(mod, "INTERVAL_MS", 50),
            "init_state":  mod.init_state,
            "draw":        mod.draw_frame,
        }
        anim_menu.insert_radiobutton(_anim_insert_idx, label=name,
                                     variable=anim_name_var, value=name,
                                     command=lambda n=name: set_animation(n))
        _anim_insert_idx += 1
        anim_cb["values"] = list(ANIMATIONS.keys())
        set_animation(name)
    except Exception as e:
        messagebox.showerror("Load Animation Error", f"Failed to load:\n{e}")

# ═══════════════════════════════════════════════════════════════════════════════
# SCREENSAVER
# ═══════════════════════════════════════════════════════════════════════════════
def _reset_activity(event=None):
    global _last_activity
    _last_activity = time.time()
    if _screensaver_on:
        _wake_screensaver()

def _wake_screensaver():
    global _screensaver_on
    _screensaver_on = False
    if _ss_switch_id is not None:
        root.after_cancel(_ss_switch_id)
    set_animation(_ss_pre_anim)  # restores UI selection + text widget

def _start_screensaver():
    global _screensaver_on, _ss_pre_anim, _ss_cycle_idx
    if _screensaver_on:
        return
    _screensaver_on = True
    _ss_pre_anim = anim_name_var.get()
    _ss_cycle_idx = 0
    _screensaver_step()

def _screensaver_step():
    global _ss_cycle_idx, _ss_switch_id
    if not _screensaver_on:
        return
    anim_names = [n for n in ANIMATIONS if n != "None"]
    if not anim_names:
        return
    name = anim_names[_ss_cycle_idx % len(anim_names)]
    _ss_cycle_idx += 1
    _apply_anim_raw(name)
    _resize_text_window()          # hides text widget during screensaver
    switch_ms = int(ss_switch_var.get() * 1000)
    _ss_switch_id = root.after(switch_ms, _screensaver_step)

def _check_screensaver():
    elapsed = time.time() - _last_activity
    timeout_sec = ss_timeout_var.get() * 60
    if not _screensaver_on and elapsed >= timeout_sec:
        _start_screensaver()
    root.after(10_000, _check_screensaver)   # re-check every 10 s

# ═══════════════════════════════════════════════════════════════════════════════
# BUILD GUI
# ═══════════════════════════════════════════════════════════════════════════════
root = tk.Tk()
root.title("Bit Textitor — Untitled")
root.state("zoomed")          # start maximised
root.minsize(800, 500)

style = ttk.Style()
style.theme_use("clam")
style.configure("Toolbar.TFrame", background="#ececec")
style.configure("Status.TFrame",  background="#d6d6d6")
style.configure("Status.TLabel",  background="#d6d6d6", font=("Segoe UI", 9))

# ── Menu bar ──────────────────────────────────────────────────────────────────
menu_bar  = tk.Menu(root)
root.config(menu=menu_bar)
file_menu = tk.Menu(menu_bar, tearoff=0)
ai_menu   = tk.Menu(menu_bar, tearoff=0)
fmt_menu  = tk.Menu(menu_bar, tearoff=0)
anim_menu = tk.Menu(menu_bar, tearoff=0)
view_menu = tk.Menu(menu_bar, tearoff=0)

menu_bar.add_cascade(label="File",       menu=file_menu)
menu_bar.add_cascade(label="View",       menu=view_menu)
menu_bar.add_cascade(label="AI",         menu=ai_menu)
menu_bar.add_cascade(label="Formatting", menu=fmt_menu)
menu_bar.add_cascade(label="Animations", menu=anim_menu)

file_menu.add_command(label="New",      command=new_file,  accelerator="Ctrl+N")
file_menu.add_command(label="Open…",    command=open_file, accelerator="Ctrl+O")
file_menu.add_command(label="Save",     command=update,    accelerator="Ctrl+S")
file_menu.add_command(label="Save As…", command=save_file, accelerator="Ctrl+Shift+S")
file_menu.add_separator()
file_menu.add_command(label="Quit",     command=close,     accelerator="Ctrl+Q")

view_menu.add_command(label="Toggle Dark Mode",  command=toggle_theme,      accelerator="F10")
view_menu.add_command(label="Toggle Fullscreen", command=toggle_fullscreen,  accelerator="F11")

ai_menu.add_command(label="Turn AI On",     command=ai_on,        accelerator="F1")
ai_menu.add_command(label="Turn AI Off",    command=ai_off,       accelerator="F2")
ai_menu.add_separator()
ai_menu.add_command(label="Check Grammar",  command=ai_grammar,   accelerator="F3")
ai_menu.add_command(label="Summarize Text", command=ai_summarize, accelerator="F4")
ai_menu.add_command(label="Translate Text", command=ai_translate, accelerator="F5")

fmt_menu.add_command(label="Bold",          command=bolden_text,        accelerator="Ctrl+B")
fmt_menu.add_command(label="Italic",        command=italicize_text,     accelerator="Ctrl+I")
fmt_menu.add_command(label="Underline",     command=underline_text,     accelerator="Ctrl+U")
fmt_menu.add_command(label="Strikethrough", command=strikethrough_text, accelerator="Ctrl+Shift+X")

anim_name_var = tk.StringVar(value="None")
for _aname in ANIMATIONS:
    anim_menu.add_radiobutton(label=_aname, variable=anim_name_var, value=_aname,
                              command=lambda n=_aname: set_animation(n))
_anim_insert_idx = anim_menu.index("end") + 1
anim_menu.add_separator()
anim_menu.add_command(label="Load from file…", command=load_animation_from_file)

# ── Keyboard shortcuts ────────────────────────────────────────────────────────
root.bind("<Control-n>",       lambda e: new_file())
root.bind("<Control-o>",       lambda e: open_file())
root.bind("<Control-s>",       lambda e: update())
root.bind("<Control-S>",       lambda e: save_file())
root.bind("<Control-q>",       lambda e: close())
root.bind("<Control-b>",       lambda e: bolden_text())
root.bind("<Control-i>",       lambda e: italicize_text())
root.bind("<Control-u>",       lambda e: underline_text())
root.bind("<Control-Shift-X>", lambda e: strikethrough_text())
root.bind("<F1>",  lambda e: ai_on())
root.bind("<F2>",  lambda e: ai_off())
root.bind("<F3>",  lambda e: ai_grammar())
root.bind("<F4>",  lambda e: ai_summarize())
root.bind("<F5>",  lambda e: ai_translate())
root.bind("<F10>", lambda e: toggle_theme())
root.bind("<F11>", lambda e: toggle_fullscreen())

# Activity tracking — any key, click, or mouse move resets screensaver timer
root.bind_all("<Key>",    _reset_activity)
root.bind_all("<Button>", _reset_activity)
root.bind_all("<Motion>", _reset_activity)

# ── Toolbar ───────────────────────────────────────────────────────────────────
toolbar = ttk.Frame(root, style="Toolbar.TFrame", padding=(4, 3))
toolbar.pack(side=tk.TOP, fill=tk.X)

# We keep a list of tk.Labels in the toolbar so apply_theme can update their bg
_toolbar_labels = []

ttk.Button(toolbar, text="New",     command=new_file,  width=5).pack(side=tk.LEFT, padx=2)
ttk.Button(toolbar, text="Open",    command=open_file, width=5).pack(side=tk.LEFT, padx=2)
ttk.Button(toolbar, text="Save",    command=update,    width=5).pack(side=tk.LEFT, padx=2)
ttk.Button(toolbar, text="Save As", command=save_file, width=8).pack(side=tk.LEFT, padx=2)

ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=6, pady=2)

ttk.Button(toolbar, text="B",  command=bolden_text,        width=3).pack(side=tk.LEFT, padx=1)
ttk.Button(toolbar, text="I",  command=italicize_text,     width=3).pack(side=tk.LEFT, padx=1)
ttk.Button(toolbar, text="U",  command=underline_text,     width=3).pack(side=tk.LEFT, padx=1)
ttk.Button(toolbar, text="S̶", command=strikethrough_text, width=3).pack(side=tk.LEFT, padx=1)

ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=6, pady=2)

font_family_var = tk.StringVar(value="Segoe UI")
font_family_cb = ttk.Combobox(toolbar, textvariable=font_family_var,
                               values=sorted(font.families()), width=20, state="readonly")
font_family_cb.pack(side=tk.LEFT, padx=2)
font_family_cb.bind("<<ComboboxSelected>>", apply_font)

font_size_var = tk.StringVar(value="14")
font_size_spin = ttk.Spinbox(toolbar, from_=6, to=96, textvariable=font_size_var,
                              width=4, command=apply_font)
font_size_spin.pack(side=tk.LEFT, padx=2)
font_size_spin.bind("<Return>", apply_font)

ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=6, pady=2)

_lbl = tk.Label(toolbar, text="Anim:", bg="#ececec", fg="#1e1e1e")
_lbl.pack(side=tk.LEFT, padx=(0, 2))
_toolbar_labels.append(_lbl)

anim_cb = ttk.Combobox(toolbar, textvariable=anim_name_var,
                        values=list(ANIMATIONS.keys()), width=12, state="readonly")
anim_cb.pack(side=tk.LEFT, padx=2)
anim_cb.bind("<<ComboboxSelected>>", lambda e: set_animation(anim_name_var.get()))

ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=6, pady=2)

# Screensaver controls
_lbl2 = tk.Label(toolbar, text="Screensaver:", bg="#ececec", fg="#1e1e1e")
_lbl2.pack(side=tk.LEFT, padx=(0, 2))
_toolbar_labels.append(_lbl2)

ss_timeout_var = tk.IntVar(value=2)
ttk.Spinbox(toolbar, from_=1, to=60, textvariable=ss_timeout_var,
            width=3).pack(side=tk.LEFT)

_lbl3 = tk.Label(toolbar, text="min  switch:", bg="#ececec", fg="#1e1e1e")
_lbl3.pack(side=tk.LEFT, padx=(2, 2))
_toolbar_labels.append(_lbl3)

ss_switch_var = tk.IntVar(value=30)
ttk.Spinbox(toolbar, from_=5, to=300, textvariable=ss_switch_var,
            width=3).pack(side=tk.LEFT)

_lbl4 = tk.Label(toolbar, text="s", bg="#ececec", fg="#1e1e1e")
_lbl4.pack(side=tk.LEFT, padx=(2, 4))
_toolbar_labels.append(_lbl4)

ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=6, pady=2)

# Theme toggle button (tk.Button so bg is easily controllable)
theme_btn = tk.Button(toolbar, text="Dark Mode", command=toggle_theme,
                       bg="#ececec", fg="#1e1e1e", relief=tk.FLAT,
                       activebackground="#d0d0d0", padx=6)
theme_btn.pack(side=tk.LEFT, padx=2)

ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=6, pady=2)

ai_toggle_btn = ttk.Label(toolbar, text="AI: OFF", foreground="red",
                           font=("Segoe UI", 10, "bold"), cursor="hand2", padding=(4, 0))
ai_toggle_btn.pack(side=tk.LEFT, padx=4)
ai_toggle_btn.bind("<Button-1>", lambda e: toggle_ai())

ttk.Button(toolbar, text="Grammar",   command=ai_grammar,   width=9).pack(side=tk.LEFT, padx=2)
ttk.Button(toolbar, text="Summarize", command=ai_summarize, width=9).pack(side=tk.LEFT, padx=2)
ttk.Button(toolbar, text="Translate", command=ai_translate, width=9).pack(side=tk.LEFT, padx=2)

# ── Status bar ────────────────────────────────────────────────────────────────
status_bar = ttk.Frame(root, style="Status.TFrame", relief=tk.SUNKEN)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)
status_var = tk.StringVar(value="Ln 1, Col 1   |   Words: 0   |   Chars: 0")
ttk.Label(status_bar, textvariable=status_var,
          style="Status.TLabel", anchor=tk.W).pack(side=tk.LEFT, padx=8, pady=2)

# ── Main split pane ───────────────────────────────────────────────────────────
pane = tk.PanedWindow(root, orient=tk.VERTICAL, sashrelief=tk.FLAT,
                       sashwidth=6, background="#bbbbbb")
pane.pack(expand=True, fill=tk.BOTH)

# ── Editor (canvas + embedded text widget) ────────────────────────────────────
editor_frame = ttk.Frame(pane)
pane.add(editor_frame, minsize=250)

text_scroll_y = ttk.Scrollbar(editor_frame, orient=tk.VERTICAL)
text_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

bg_canvas = tk.Canvas(editor_frame, bg="#ffffff", highlightthickness=0)
bg_canvas.pack(fill=tk.BOTH, expand=True)

text = tk.Text(
    bg_canvas, wrap="word", undo=True,
    bg="#ffffff", fg="#1e1e1e", insertbackground="#1e1e1e",
    selectbackground="#4a90d9", selectforeground="#ffffff",
    font=("Segoe UI", 14), relief=tk.FLAT,
    padx=16, pady=12, spacing1=2, spacing3=2,
    yscrollcommand=text_scroll_y.set,
)
text_win = bg_canvas.create_window(0, 0, anchor="nw", window=text)
text_scroll_y.config(command=text.yview)

bg_canvas.bind("<Configure>", _on_canvas_resize)
text.bind("<KeyRelease>",    mark_dirty)
text.bind("<ButtonRelease>", update_status)

# ── AI output panel ───────────────────────────────────────────────────────────
ai_frame = ttk.LabelFrame(pane, text=" AI Output ", padding=4)
pane.add(ai_frame, minsize=90)

ai_scroll = ttk.Scrollbar(ai_frame, orient=tk.VERTICAL)
ai_scroll.pack(side=tk.RIGHT, fill=tk.Y)

ai_output = tk.Text(ai_frame, wrap=tk.WORD, height=7, state=tk.DISABLED,
                     bg="#f5f5f5", fg="#333333", font=("Segoe UI", 10),
                     relief=tk.FLAT, padx=10, pady=6,
                     yscrollcommand=ai_scroll.set)
ai_output.pack(expand=True, fill=tk.BOTH)
ai_scroll.config(command=ai_output.yview)

set_ai_output("AI is OFF. Enable it from the toolbar or AI menu (F1).")

# ── Start ─────────────────────────────────────────────────────────────────────
root.protocol("WM_DELETE_WINDOW", close)
_last_activity = time.time()
_animation_loop()
root.after(10_000, _check_screensaver)
root.mainloop()
