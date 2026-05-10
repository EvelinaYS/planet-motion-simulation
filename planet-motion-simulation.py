import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

G = 6.67430e-11
M_SUN = 1.989e30
AU = 149.6e9

dt = 24 * 60 * 60
steps = 687

planets = {
    "Меркурий": (57.9e9, 47.4e3, "gray", 40),
    "Венера":   (108.2e9, 35.0e3, "gold", 70),
    "Земля":    (149.6e9, 29.8e3, "dodgerblue", 80),
    "Марс":     (227.9e9, 24.1e3, "red", 60)
}

trajectories = {}

for name, (r0, v0, color, size) in planets.items():
    x, y = r0, 0
    vx, vy = 0, v0

    xs, ys = [], []

    for _ in range(steps):
        r = np.sqrt(x**2 + y**2)

        ax = -G * M_SUN * x / r**3
        ay = -G * M_SUN * y / r**3

        vx += ax * dt
        vy += ay * dt

        x += vx * dt
        y += vy * dt

        xs.append(x / AU)
        ys.append(y / AU)

    trajectories[name] = np.array(xs), np.array(ys), color, size


fig, ax = plt.subplots(figsize=(9, 9))
fig.patch.set_facecolor("black")
ax.set_facecolor("black")

ax.set_xlim(-1.8, 1.8)
ax.set_ylim(-1.8, 1.8)
ax.set_aspect("equal")

ax.set_title("Моделирование движения планет вокруг Солнца", color="white")
ax.set_xlabel("x, а.е.", color="white")
ax.set_ylabel("y, а.е.", color="white")
ax.tick_params(colors="white")

for spine in ax.spines.values():
    spine.set_color("white")

np.random.seed(1)
ax.scatter(
    np.random.uniform(-1.8, 1.8, 140),
    np.random.uniform(-1.8, 1.8, 140),
    s=np.random.uniform(0.5, 2.2, 140),
    color="white",
    alpha=0.6
)

ax.scatter(0, 0, s=420, color="yellow", label="Солнце")

animated_objects = []

for name, (xs, ys, color, size) in trajectories.items():
    ax.plot(xs, ys, "--", color=color, linewidth=0.8, alpha=0.35)

    trail, = ax.plot([], [], "-", color=color, linewidth=1.5, alpha=0.95)
    planet = ax.scatter([], [], s=size, color=color, label=name)

    animated_objects.append((xs, ys, trail, planet))

day_text = ax.text(
    0.02, 0.95,
    "",
    transform=ax.transAxes,
    color="white",
    fontsize=12
)

ax.legend(facecolor="black", edgecolor="white", labelcolor="white")


def update(frame):
    artists = []

    for xs, ys, trail, planet in animated_objects:
        trail.set_data(xs[:frame + 1], ys[:frame + 1])
        planet.set_offsets([[xs[frame], ys[frame]]])

        artists.extend([trail, planet])

    day_text.set_text(f"День: {frame}")
    artists.append(day_text)

    return artists


animation = FuncAnimation(
    fig,
    update,
    frames=steps,
    interval=20,
    blit=True
)

plt.show()