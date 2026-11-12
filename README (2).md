# 🚑 Emergency Ambulance Route Optimizer

A desktop simulation that finds the shortest emergency route for an ambulance using **Dijkstra's algorithm**. The ambulance travels from its starting point to an accident location, and then on to a hospital. You can close roads to simulate blockages and watch the route recalculate around them.

Built with Python and Tkinter, with no external dependencies.

---

## Features

- **Two-leg routing:** calculates Ambulance → Accident and Accident → Hospital separately, then combines them into one mission summary.
- **Interactive city map:** an 11-location road network drawn on a canvas, with distances (in km) labelled on every road.
- **Road closures:** close or restore any road and re-run the route to see how traffic blockages change the result.
- **Step-by-step algorithm view:** a log window shows every node Dijkstra selects, every edge it checks, and every distance it updates.
- **Click to set the accident:** click any location on the map to make it the accident site.
- **Route-unavailable handling:** if closed roads cut off a journey, the app tells you instead of crashing.
- **Mission summary:** shows both paths, distances, total distance, estimated travel time and the number of nodes explored.

## Requirements

- Python 3.6 or newer
- Tkinter (included with most Python installations)

No `pip install` is needed, because the app only uses the standard library (`tkinter`, `heapq`).

> **Linux users:** if Tkinter is missing, install it with `sudo apt install python3-tk`.

## How to Run

```bash
python main.py
```

The application window opens at 1150 × 850.

## How to Use

1. **Choose locations** in the *Route Configuration* panel:
   - **Ambulance Start:** where the ambulance begins
   - **Accident Location:** the incident site (you can also click it on the map)
   - **Destination Hospital:** Medical Center, North Hospital or South Hospital
2. Click **FIND OPTIMAL ROUTE**. The ambulance-to-accident leg is drawn in **blue** and the accident-to-hospital leg in **green**.
3. Click **SHOW DIJKSTRA STEPS** to see how the algorithm reached its answer.
4. To test a blockage, pick a road under *Road Management* and click **CLOSE / RESTORE ROAD**. Closed roads appear as red dashed lines. Then click **FIND OPTIMAL ROUTE** again.
5. Click **RESET ALL ROADS** to reopen every road and clear the current route.

### Map Legend

| Marker | Meaning |
|--------|---------|
| 🔵 **A** | Ambulance start |
| 🔴 **!** | Accident location |
| 🟢 **H** | Destination hospital |
| Red dashed line | Closed road |
| Blue / green thick line | Calculated route (leg 1 / leg 2) |

## How It Works

The road network is modelled as a weighted, undirected graph:

- **Nodes** are the locations (junctions, hospitals, the airport and so on), each with `(x, y)` canvas coordinates.
- **Edges** are roads, weighted by distance in kilometres.

`dijkstra(start, destination)` rebuilds the graph each time (skipping any closed roads), then uses a priority queue (`heapq`) to repeatedly expand the nearest unvisited node until the destination is reached. It returns the path, total distance, visited nodes and a log of every step.

**Estimated time** assumes an average ambulance speed of **30 km/h**:

```
time (min) = total distance (km) / 30 × 60
```

This is a simplified simulation. It does not use real traffic, road types or live map data.

## Customising the Map

All map data is at the top of `main.py`, so you can change the city without touching the algorithm:

```python
NODES = { "Location Name": (x, y), ... }          # locations and canvas positions
ROADS = [ ("Location A", "Location B", km), ... ]  # roads and their distances
HOSPITALS = [ "Medical Center", ... ]              # nodes offered as destinations
```

The colour theme is controlled by the constants `BG`, `PANEL`, `TEXT`, `BLUE`, `GREEN`, `RED` and `ROAD`.

## Project Structure

```
.
├── main.py      # entire application (graph data, Dijkstra, GUI)
└── README.md
```

## Known Limitations

- The fonts (Segoe UI, Consolas) are Windows defaults. On macOS or Linux, Tkinter will substitute a fallback font, so the look may vary slightly.
- Mouse-wheel scrolling in the sidebar is tuned for Windows. On macOS, scrolling speed may feel different.
- Estimated time uses one fixed speed and does not consider traffic or road conditions.

## Possible Improvements

- Add a speed or traffic weight per road, so the route minimises time instead of distance
- Animate the ambulance moving along the route
- Load the map from a JSON file
- Compare Dijkstra with A* in the step viewer

## Concepts Demonstrated

Graph representation (adjacency list), Dijkstra's shortest-path algorithm, priority queues / min-heaps, and event-driven GUI programming with Tkinter.

---

## Author

*Your name, course and college here*
