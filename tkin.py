import tkinter as tk
from tkinter import ttk
import requests
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

API = "http://127.0.0.1:8000"
REFRESH_MS = 2000

# ---------------- COLORS ----------------
BG = "#0b1220"
PANEL = "#111b2e"
CARD = "#162235"
CARD_ALT = "#1b2940"
TEXT = "#e5eefc"
MUTED = "#9fb0cc"
ACCENT = "#7c3aed"
ACCENT_2 = "#06b6d4"
GOOD = "#22c55e"
WARN = "#f59e0b"
BAD = "#ef4444"
BORDER = "#24324d"

# ---------------- APP ----------------
root = tk.Tk()
root.title("Eco-Monitor Dashboard")
root.geometry("1600x950")
root.configure(bg=BG)
root.minsize(1300, 850)

# ---------------- FONTS ----------------
FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_SUBTITLE = ("Segoe UI", 11)
FONT_CARD_TITLE = ("Segoe UI", 12, "bold")
FONT_CARD_VALUE = ("Segoe UI", 26, "bold")
FONT_CARD_SMALL = ("Segoe UI", 11)
FONT_BUTTON = ("Segoe UI", 13, "bold")

# ---------------- STYLES ----------------
style = ttk.Style()
style.theme_use("clam")
style.configure("TSeparator", background=BORDER)
style.configure("TNotebook", background=BG, borderwidth=0)
style.configure("TNotebook.Tab", background=PANEL, foreground=TEXT, padding=(16, 10))
style.map("TNotebook.Tab", background=[("selected", CARD)], foreground=[("selected", TEXT)])

# ---------------- MAIN LAYOUT ----------------
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# ---------------- TOP BAR ----------------
topbar = tk.Frame(root, bg=BG, height=90)
topbar.grid(row=0, column=0, sticky="ew", padx=24, pady=(18, 8))
topbar.grid_columnconfigure(1, weight=1)

brand = tk.Frame(topbar, bg=BG)
brand.grid(row=0, column=0, sticky="w")

tk.Label(
    brand,
    text="Eco-Monitor Dashboard",
    font=("Segoe UI", 24, "bold"),
    fg=TEXT,
    bg=BG
).pack(anchor="w")

tk.Label(
    brand,
    text="Live energy, environment, relay, and carbon intelligence",
    font=FONT_SUBTITLE,
    fg=MUTED,
    bg=BG
).pack(anchor="w", pady=(4, 0))

status_wrap = tk.Frame(topbar, bg=BG)
status_wrap.grid(row=0, column=2, sticky="e")

system_status = tk.Label(
    status_wrap,
    text="● CONNECTING",
    font=("Segoe UI", 11, "bold"),
    fg=WARN,
    bg=BG,
    padx=12,
    pady=6
)
system_status.pack(anchor="e")

# ---------------- HERO + METRICS ----------------
hero = tk.Frame(root, bg=BG)
hero.grid(row=1, column=0, sticky="nsew", padx=24, pady=(0, 18))
hero.grid_columnconfigure(0, weight=1)
hero.grid_rowconfigure(1, weight=1)

# Header cards row
metrics_row = tk.Frame(hero, bg=BG)
metrics_row.grid(row=0, column=0, sticky="ew")
metrics_row.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

def card(parent, title, big=True, subtitle=None):
    outer = tk.Frame(parent, bg=BORDER, bd=0, highlightthickness=0)
    inner = tk.Frame(outer, bg=CARD, padx=18, pady=16)
    inner.pack(fill="both", expand=True, padx=1, pady=1)

    tk.Label(inner, text=title, font=FONT_CARD_TITLE, fg=MUTED, bg=CARD).pack(anchor="w")
    value = tk.Label(
        inner,
        text="--",
        font=FONT_CARD_VALUE if big else ("Segoe UI", 20, "bold"),
        fg=TEXT,
        bg=CARD
    )
    value.pack(anchor="w", pady=(6, 0))

    if subtitle:
        tk.Label(inner, text=subtitle, font=FONT_CARD_SMALL, fg=MUTED, bg=CARD).pack(anchor="w", pady=(4, 0))

    return outer, value

temp_card, temp_value = card(metrics_row, "Temperature (°C)")
hum_card, hum_value = card(metrics_row, "Humidity (%)")
light_card, light_value = card(metrics_row, "Light", subtitle="LDR digital state")
relay_card, relay_value = card(metrics_row, "Relay", subtitle="Manual control")
energy_card, energy_value = card(metrics_row, "Energy (kWh)")
cost_card, cost_value = card(metrics_row, "Cost (₹)")
carbon_card, carbon_value = card(metrics_row, "CO₂ (kg)")

temp_card.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")
hum_card.grid(row=0, column=1, padx=8, pady=8, sticky="nsew")
light_card.grid(row=0, column=2, padx=8, pady=8, sticky="nsew")
relay_card.grid(row=0, column=3, padx=8, pady=8, sticky="nsew")
energy_card.grid(row=0, column=4, padx=8, pady=8, sticky="nsew")
cost_card.grid(row=0, column=5, padx=8, pady=8, sticky="nsew")
carbon_card.grid(row=0, column=6, padx=8, pady=8, sticky="nsew")

# ---------------- CONTROL / CHART AREA ----------------
body = tk.Frame(hero, bg=BG)
body.grid(row=1, column=0, sticky="nsew", pady=(16, 0))
body.grid_columnconfigure(0, weight=3)
body.grid_columnconfigure(1, weight=1)
body.grid_rowconfigure(0, weight=1)

# Chart panel
chart_panel = tk.Frame(body, bg=BORDER)
chart_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
chart_inner = tk.Frame(chart_panel, bg=PANEL, padx=18, pady=18)
chart_inner.pack(fill="both", expand=True, padx=1, pady=1)
chart_inner.grid_rowconfigure(1, weight=1)
chart_inner.grid_columnconfigure(0, weight=1)

chart_header = tk.Frame(chart_inner, bg=PANEL)
chart_header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
tk.Label(chart_header, text="Power Usage", font=("Segoe UI", 18, "bold"), fg=TEXT, bg=PANEL).pack(anchor="w")
tk.Label(chart_header, text="Live relay-based power estimate over time", font=FONT_SUBTITLE, fg=MUTED, bg=PANEL).pack(anchor="w", pady=(2, 0))

fig = Figure(figsize=(10, 5), dpi=100, facecolor=PANEL)
ax = fig.add_subplot(111)
ax.set_facecolor(PANEL)

canvas = FigureCanvasTkAgg(fig, master=chart_inner)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=1, column=0, sticky="nsew")

# Right side panel
side_panel = tk.Frame(body, bg=BORDER)
side_panel.grid(row=0, column=1, sticky="nsew")
side_inner = tk.Frame(side_panel, bg=PANEL, padx=18, pady=18)
side_inner.pack(fill="both", expand=True, padx=1, pady=1)

tk.Label(side_inner, text="Controls", font=("Segoe UI", 18, "bold"), fg=TEXT, bg=PANEL).pack(anchor="w")
tk.Label(side_inner, text="Toggle relay manually from the dashboard.", font=FONT_SUBTITLE, fg=MUTED, bg=PANEL).pack(anchor="w", pady=(2, 18))

relay_state = tk.StringVar(value="OFF")

relay_status_chip = tk.Label(
    side_inner,
    text="RELAY: OFF",
    font=("Segoe UI", 12, "bold"),
    fg=TEXT,
    bg="#312e81",
    padx=12,
    pady=8
)
relay_status_chip.pack(anchor="w", fill="x", pady=(0, 18))

def set_chip_state(on: bool):
    if on:
        relay_status_chip.config(text="RELAY: ON", bg=GOOD)
        system_status.config(text="● LIVE", fg=GOOD)
    else:
        relay_status_chip.config(text="RELAY: OFF", bg="#312e81")
        system_status.config(text="● LIVE", fg=ACCENT_2)

def toggle_relay():
    try:
        current = relay_state.get()
        new_state = "off" if current == "ON" else "on"
        res = requests.post(f"{API}/relay", json={"state": new_state}, timeout=5)
        if res.status_code == 200:
            relay_state.set("ON" if new_state == "on" else "OFF")
            set_chip_state(new_state == "on")
        else:
            relay_state.set("ERROR")
            relay_status_chip.config(text="RELAY: ERROR", bg=BAD)
    except Exception:
        relay_state.set("ERROR")
        relay_status_chip.config(text="RELAY: ERROR", bg=BAD)

toggle_btn = tk.Button(
    side_inner,
    textvariable=relay_state,
    command=toggle_relay,
    font=FONT_BUTTON,
    bg=CARD_ALT,
    fg=TEXT,
    activebackground=ACCENT,
    activeforeground=TEXT,
    relief="flat",
    padx=22,
    pady=12,
    cursor="hand2"
)
toggle_btn.pack(anchor="w", fill="x", pady=(0, 18))

# KPI mini-panel
kpi_box = tk.Frame(side_inner, bg=CARD, padx=14, pady=14)
kpi_box.pack(fill="x", pady=(0, 12))

tk.Label(kpi_box, text="System Snapshot", font=FONT_CARD_TITLE, fg=MUTED, bg=CARD).pack(anchor="w")

snapshot_text = tk.StringVar(value="Waiting for live data...")
snapshot_label = tk.Label(
    kpi_box,
    textvariable=snapshot_text,
    font=("Segoe UI", 11),
    fg=TEXT,
    bg=CARD,
    justify="left",
    wraplength=280
)
snapshot_label.pack(anchor="w", pady=(10, 0))

# small footer note
tk.Label(
    side_inner,
    text="Power is estimated from relay state because ACS712 is not used.",
    font=("Segoe UI", 10),
    fg=MUTED,
    bg=PANEL,
    wraplength=280,
    justify="left"
).pack(anchor="w", pady=(16, 0))

# ---------------- DATA ----------------
def pretty_num(v, fmt="{:.1f}", fallback="--"):
    try:
        return fmt.format(float(v))
    except Exception:
        return fallback

def update_chart(times, powers):
    ax.clear()
    ax.set_facecolor(PANEL)

    if times and powers:
        ax.plot(times, powers, linewidth=2.8, marker="o", markersize=5, color="#60a5fa")
        ax.fill_between(range(len(powers)), powers, color="#60a5fa", alpha=0.08)

    ax.set_title("Power Usage", fontsize=16, fontweight="bold", color=TEXT, pad=12)
    ax.set_xlabel("Time", color=MUTED, fontsize=11)
    ax.set_ylabel("Power (W)", color=MUTED, fontsize=11)
    ax.tick_params(axis="x", labelrotation=30, labelsize=9, colors=MUTED)
    ax.tick_params(axis="y", labelsize=10, colors=MUTED)
    for spine in ax.spines.values():
        spine.set_color(BORDER)
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.35)
    fig.tight_layout()
    canvas.draw_idle()

def update():
    try:
        status = requests.get(f"{API}/status", timeout=5).json()
        summary = requests.get(f"{API}/summary", timeout=5).json()
        history = requests.get(f"{API}/history", timeout=5).json()

        # top cards
        temp_value.config(text=pretty_num(status.get("temperature"), "{:.1f}"))
        hum_value.config(text=pretty_num(status.get("humidity"), "{:.1f}"))
        light_value.config(text=str(status.get("light", "--")))

        relay_on = bool(status.get("relay"))
        relay_value.config(
            text="ON" if relay_on else "OFF",
            fg=(GOOD if relay_on else TEXT)
        )
        set_chip_state(relay_on)
        relay_state.set("ON" if relay_on else "OFF")

        # summary cards
        energy_value.config(text=pretty_num(summary.get("energy_kwh"), "{:.6f}"))
        cost_value.config(text=f"₹ {pretty_num(summary.get('cost'), '{:.4f}', '0.0000')}")
        carbon_value.config(text=pretty_num(summary.get("carbon"), "{:.6f}"))

        # snapshot
        snapshot_text.set(
            f"Temp: {pretty_num(status.get('temperature'), '{:.1f}')} °C\n"
            f"Humidity: {pretty_num(status.get('humidity'), '{:.1f}')} %\n"
            f"Light: {status.get('light', '--')}\n"
            f"Relay: {'ON' if relay_on else 'OFF'}\n"
            f"Power: {pretty_num(status.get('power'), '{:.2f}')} W"
        )

        # chart
        history = history[-20:]
        times = [h["time"] for h in history]
        powers = [h["power"] for h in history]
        update_chart(times, powers)

    except Exception as e:
        system_status.config(text="● DISCONNECTED", fg=BAD)
        snapshot_text.set(f"Waiting for backend...\n{e}")

    root.after(REFRESH_MS, update)

# initial state
set_chip_state(False)
update()
root.mainloop()