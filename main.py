import tkinter as tk
from tkinter import ttk, messagebox
import heapq

# ==========================================
# EMERGENCY AMBULANCE ROUTE OPTIMIZER
# ==========================================

BG = "#101827"
PANEL = "#182538"
TEXT = "#F1F5F9"
BLUE = "#38BDF8"
GREEN = "#34D399"
RED = "#FB7185"
ROAD = "#42516A"

# City locations: name -> (x, y) coordinates
NODES = {
    "Ambulance Base": (65, 230),
    "West Junction": (180, 120),
    "University": (180, 350),
    "Medical Center": (320, 70),
    "Central Junction": (330, 230),
    "City Market": (450, 120),
    "South Junction": (350, 380),
    "Accident Zone": (480, 260),
    "Airport Junction": (620, 140),
    "North Hospital": (640, 330),
    "South Hospital": (570, 420),
}

# Roads and their distances in kilometres
ROADS = [
    ("Ambulance Base", "West Junction", 4),
    ("Ambulance Base", "University", 5),
    ("West Junction", "Central Junction", 3),
    ("West Junction", "Medical Center", 3),
    ("West Junction", "City Market", 6),
    ("University", "Central Junction", 2),
    ("University", "South Junction", 5),
    ("Medical Center", "City Market", 3),
    ("Medical Center", "Central Junction", 4),
    ("Central Junction", "City Market", 4),
    ("Central Junction", "Accident Zone", 3),
    ("Central Junction", "South Junction", 6),
    ("City Market", "Airport Junction", 4),
    ("City Market", "Accident Zone", 5),
    ("Accident Zone", "Airport Junction", 3),
    ("Accident Zone", "North Hospital", 5),
    ("Airport Junction", "North Hospital", 4),
    ("South Junction", "South Hospital", 4),
    ("South Junction", "North Hospital", 7),
    ("North Hospital", "South Hospital", 6),
]

HOSPITALS = [
    "Medical Center",
    "North Hospital",
    "South Hospital"
]

closed_roads = set()
current_routes = []
algorithm_logs = []


def road_key(a, b):
    return tuple(sorted((a, b)))


def build_graph():
    graph = {node: [] for node in NODES}

    for a, b, distance in ROADS:
        if road_key(a, b) not in closed_roads:
            graph[a].append((b, distance))
            graph[b].append((a, distance))

    return graph


def dijkstra(start, destination):
    """Calculate the shortest path using Dijkstra's algorithm."""
    graph = build_graph()

    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}
    distances[start] = 0

    queue = [(0, start)]
    visited = []
    logs = []

    while queue:
        distance, current = heapq.heappop(queue)

        if distance != distances[current]:
            continue

        visited.append(current)
        logs.append(
            f"Selected {current}: {distance} km"
        )

        if current == destination:
            break

        for neighbor, weight in graph[current]:
            new_distance = distance + weight

            logs.append(
                f"Check {current} -> {neighbor}: "
                f"{distance} + {weight} = {new_distance} km"
            )

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current
                heapq.heappush(
                    queue, (new_distance, neighbor)
                )

                logs.append(
                    f"Updated distance to {neighbor}: "
                    f"{new_distance} km"
                )

    if distances[destination] == float("inf"):
        return None, None, visited, logs

    path = []
    current = destination

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()
    logs.append("Final path: " + " -> ".join(path))

    return path, distances[destination], visited, logs


# ==========================================
# APPLICATION WINDOW
# ==========================================

root = tk.Tk()
root.title("Emergency Ambulance Route Optimizer")
root.geometry("1150x850")
root.minsize(1000, 750)
root.configure(bg=BG)

style = ttk.Style()
style.theme_use("clam")
style.configure(
    "TCombobox",
    fieldbackground="#26364B",
    background="#26364B",
    foreground=TEXT
)

main = tk.Frame(root, bg=BG)
main.pack(fill="both", expand=True, padx=16, pady=14)

tk.Label(
    main,
    text="🚑 EMERGENCY RESPONSE",
    font=("Segoe UI", 22, "bold"),
    bg=BG, fg=TEXT
).pack(anchor="w")

tk.Label(
    main,
    text="AMBULANCE ROUTE OPTIMIZER  |  DIJKSTRA'S ALGORITHM",
    font=("Segoe UI", 10, "bold"),
    bg=BG, fg=BLUE
).pack(anchor="w", pady=(4, 14))

content = tk.Frame(main, bg=BG)
content.pack(fill="both", expand=True)

# Scrollable sidebar
sidebar_container = tk.Frame(content, bg=PANEL, width=310)
sidebar_container.pack(
    side="left",
    fill="y",
    padx=(0, 12)
)
sidebar_container.pack_propagate(False)

sidebar_canvas = tk.Canvas(
    sidebar_container,
    bg=PANEL,
    width=290,
    highlightthickness=0
)
sidebar_scrollbar = ttk.Scrollbar(
    sidebar_container,
    orient="vertical",
    command=sidebar_canvas.yview
)

sidebar = tk.Frame(sidebar_canvas, bg=PANEL, width=290)

sidebar_window = sidebar_canvas.create_window(
    (0, 0),
    window=sidebar,
    anchor="nw",
    width=290
)

sidebar_canvas.configure(
    yscrollcommand=sidebar_scrollbar.set
)

sidebar_canvas.pack(side="left", fill="both", expand=True)
sidebar_scrollbar.pack(side="right", fill="y")

def update_sidebar_scroll(event=None):
    sidebar_canvas.configure(
        scrollregion=sidebar_canvas.bbox("all")
    )

sidebar.bind("<Configure>", update_sidebar_scroll)
sidebar_canvas.bind("<Configure>", lambda event: sidebar_canvas.itemconfigure(
    sidebar_window, width=event.width
))

# Mouse-wheel scrolling
def scroll_sidebar(event):
    sidebar_canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )

sidebar_canvas.bind(
    "<Enter>",
    lambda event: sidebar_canvas.bind_all(
        "<MouseWheel>", scroll_sidebar
    )
)
sidebar_canvas.bind(
    "<Leave>",
    lambda event: sidebar_canvas.unbind_all("<MouseWheel>")
)

map_panel = tk.Frame(content, bg=PANEL)
map_panel.pack(side="left", fill="both", expand=True)


def add_label(parent, text, color=TEXT, size=10):
    tk.Label(
        parent, text=text,
        bg=PANEL, fg=color,
        font=("Segoe UI", size, "bold")
    ).pack(anchor="w", padx=14, pady=(12, 4))


def add_button(parent, text, command, color=BLUE):
    return tk.Button(
        parent, text=text, command=command,
        bg=color, fg="#101827",
        activebackground=TEXT,
        font=("Segoe UI", 10, "bold"),
        relief="flat", cursor="hand2",
        pady=8
    )


def add_selector(parent, label, variable, values):
    tk.Label(
        parent, text=label,
        bg=PANEL, fg="#9CAEC3",
        font=("Segoe UI", 9)
    ).pack(anchor="w", padx=14, pady=(8, 3))

    combo = ttk.Combobox(
        parent, textvariable=variable,
        values=values, state="readonly"
    )
    combo.pack(fill="x", padx=14, ipady=3)
    return combo


add_label(sidebar, "ROUTE CONFIGURATION")

ambulance_var = tk.StringVar(value="Ambulance Base")
incident_var = tk.StringVar(value="Accident Zone")
hospital_var = tk.StringVar(value="North Hospital")

add_selector(
    sidebar, "AMBULANCE START",
    ambulance_var, list(NODES)
)

add_selector(
    sidebar, "ACCIDENT LOCATION",
    incident_var, list(NODES)
)

add_selector(
    sidebar, "DESTINATION HOSPITAL",
    hospital_var, HOSPITALS
)

summary_var = tk.StringVar(
    value="Choose locations, then find the optimal route."
)

status_var = tk.StringVar(value="SYSTEM READY")


def draw_map():
    canvas.delete("all")

    # Background grid
    for x in range(0, 751, 40):
        canvas.create_line(
            x, 0, x, 481, fill="#1D2B3D"
        )

    for y in range(0, 481, 40):
        canvas.create_line(
            0, y, 751, y, fill="#1D2B3D"
        )

    # Draw roads
    for a, b, distance in ROADS:
        x1, y1 = NODES[a]
        x2, y2 = NODES[b]

        is_closed = road_key(a, b) in closed_roads
        color = RED if is_closed else ROAD

        canvas.create_line(
            x1, y1, x2, y2,
            fill=color, width=2,
            dash=(6, 4) if is_closed else None
        )

        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2

        canvas.create_text(
            mid_x, mid_y,
            text=str(distance),
            fill="#CBD5E1",
            font=("Segoe UI", 8)
        )

    # Highlight the calculated routes
    for index, path in enumerate(current_routes):
        color = BLUE if index == 0 else GREEN

        for a, b in zip(path, path[1:]):
            x1, y1 = NODES[a]
            x2, y2 = NODES[b]

            canvas.create_line(
                x1, y1, x2, y2,
                fill=color, width=5
            )

    # Draw clickable locations
    for name, (x, y) in NODES.items():
        if name == ambulance_var.get():
            color = BLUE
            marker = "A"
        elif name == incident_var.get():
            color = RED
            marker = "!"
        elif name == hospital_var.get():
            color = GREEN
            marker = "H"
        else:
            color = "#E2E8F0"
            marker = ""

        canvas.create_oval(
            x - 12, y - 12, x + 12, y + 12,
            fill=color, outline="white", width=1
        )

        if marker:
            canvas.create_text(
                x, y, text=marker,
                fill="#101827",
                font=("Segoe UI", 9, "bold")
            )

        canvas.create_text(
            x, y + 23, text=name,
            fill=TEXT,
            font=("Segoe UI", 8, "bold")
        )


def calculate_route():
    global algorithm_logs

    start = ambulance_var.get()
    incident = incident_var.get()
    hospital = hospital_var.get()

    if start == incident or incident == hospital:
        messagebox.showwarning(
            "Invalid Locations",
            "The ambulance, accident and hospital "
            "must be different locations."
        )
        return

    path1, distance1, visited1, logs1 = dijkstra(
        start, incident
    )

    path2, distance2, visited2, logs2 = dijkstra(
        incident, hospital
    )

    if path1 is None or path2 is None:
        current_routes.clear()
        draw_map()

        summary_var.set(
            "No complete route is available. "
            "Restore a road or choose other locations."
        )

        status_var.set("ROUTE UNAVAILABLE")

        messagebox.showwarning(
            "Route Unavailable",
            "An open route could not be found for "
            "one or both journey sections."
        )
        return

    current_routes.clear()
    current_routes.extend([path1, path2])

    algorithm_logs = (
        ["AMBULANCE TO INCIDENT"] + logs1
        + ["", "INCIDENT TO HOSPITAL"] + logs2
    )

    total_distance = distance1 + distance2
    travel_time = total_distance / 30 * 60

    summary_var.set(
        f"AMBULANCE -> INCIDENT\n"
        f"{' -> '.join(path1)}\n"
        f"Distance: {distance1} km\n\n"
        f"INCIDENT -> HOSPITAL\n"
        f"{' -> '.join(path2)}\n"
        f"Distance: {distance2} km\n\n"
        f"TOTAL DISTANCE: {total_distance} km\n"
        f"EST. TIME: {travel_time:.1f} min\n\n"
        f"Nodes explored: "
        f"{len(visited1) + len(visited2)}"
    )

    status_var.set("OPTIMAL ROUTE FOUND - SIMULATION")
    draw_map()


def toggle_road():
    selected = road_var.get()

    for a, b, distance in ROADS:
        label = f"{a} <-> {b} ({distance} km)"

        if selected == label:
            key = road_key(a, b)

            if key in closed_roads:
                closed_roads.remove(key)
                status_var.set("ROAD RESTORED")
            else:
                closed_roads.add(key)
                status_var.set("ROAD CLOSED")

            draw_map()
            return


def reset_roads():
    closed_roads.clear()
    current_routes.clear()

    summary_var.set("Choose locations, then find the optimal route.")
    status_var.set("ALL ROADS RESTORED")

    draw_map()


def show_steps():
    if not algorithm_logs:
        messagebox.showinfo(
            "Algorithm Steps",
            "Calculate a route first."
        )
        return

    window = tk.Toplevel(root)
    window.title("Dijkstra Algorithm Steps")
    window.geometry("650x500")
    window.configure(bg=BG)

    tk.Label(
        window, text="DIJKSTRA'S ALGORITHM",
        bg=BG, fg=BLUE,
        font=("Segoe UI", 16, "bold")
    ).pack(anchor="w", padx=12, pady=12)

    frame = tk.Frame(window)
    frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    scrollbar = ttk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    output = tk.Text(
        frame, wrap="word",
        bg="#0B1220", fg=TEXT,
        font=("Consolas", 10),
        yscrollcommand=scrollbar.set
    )
    output.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=output.yview)

    output.insert("1.0", "\n".join(algorithm_logs))
    output.config(state="disabled")


add_button(
    sidebar, "FIND OPTIMAL ROUTE",
    calculate_route, GREEN
).pack(fill="x", padx=14, pady=(15, 5))

add_button(
    sidebar, "SHOW DIJKSTRA STEPS",
    show_steps
).pack(fill="x", padx=14, pady=5)

add_label(sidebar, "ROAD MANAGEMENT")

road_labels = [
    f"{a} <-> {b} ({d} km)"
    for a, b, d in ROADS
]

road_var = tk.StringVar(value=road_labels[0])

add_selector(
    sidebar, "SELECT A ROAD",
    road_var, road_labels
)

add_button(
    sidebar, "CLOSE / RESTORE ROAD",
    toggle_road, "#FBBF24"
).pack(fill="x", padx=14, pady=(10, 5))

add_button(
    sidebar, "RESET ALL ROADS",
    reset_roads, "#CBD5E1"
).pack(fill="x", padx=14, pady=5)

add_label(sidebar, "MISSION SUMMARY")

summary_label = tk.Label(
    sidebar,
    textvariable=summary_var,
    bg=PANEL,
    fg=TEXT,
    justify="left",
    anchor="nw",
    wraplength=260,
    font=("Segoe UI", 8)
)
summary_label.pack(
    fill="x",
    padx=14,
    pady=5
)

tk.Label(
    sidebar, textvariable=status_var,
    bg=PANEL, fg=GREEN,
    wraplength=260,
    font=("Segoe UI", 9, "bold")
).pack(fill="x", padx=14, pady=10)

tk.Label(
    map_panel, text="CITY ROAD NETWORK",
    bg=PANEL, fg=TEXT,
    font=("Segoe UI", 12, "bold")
).pack(anchor="w", padx=12, pady=10)

canvas = tk.Canvas(
    map_panel, bg="#111D2D",
    width=750, height=480,
    highlightthickness=0
)
canvas.pack(fill="both", expand=True, padx=10, pady=(0, 10))


def on_map_click(event):
    nearest = min(
        NODES,
        key=lambda name: (
            (NODES[name][0] - event.x) ** 2
            + (NODES[name][1] - event.y) ** 2
        )
    )

    x, y = NODES[nearest]

    if (x - event.x) ** 2 + (y - event.y) ** 2 <= 30 ** 2:
        incident_var.set(nearest)
        current_routes.clear()

        summary_var.set(
            f"Incident location: {nearest}\n"
            "Click FIND OPTIMAL ROUTE."
        )

        draw_map()


canvas.bind("<Button-1>", on_map_click)

draw_map()
root.mainloop()
