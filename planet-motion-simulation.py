# Импорт библиотек
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ---------------- ФИЗИЧЕСКИЕ КОНСТАНТЫ ----------------

# Гравитационная постоянная
G = 6.67430e-11

# Масса Солнца
M_SUN = 1.989e30

# Астрономическая единица (расстояние от Земли до Солнца)
AU = 149.6e9

# Шаг времени = 1 день
dt = 24 * 60 * 60

# Количество шагов анимации
steps = 687

# ---------------- ДАННЫЕ ПЛАНЕТ ----------------
# Формат:
# название : (расстояние до Солнца, скорость, цвет, размер)

planets = {
    "Меркурий": (57.9e9, 47.4e3, "gray", 40),
    "Венера":   (108.2e9, 35.0e3, "gold", 70),
    "Земля":    (149.6e9, 29.8e3, "dodgerblue", 80),
    "Марс":     (227.9e9, 24.1e3, "red", 60)
}

# Словарь для хранения траекторий
trajectories = {}

# ---------------- РАСЧЁТ ДВИЖЕНИЯ ПЛАНЕТ ----------------

for name, (r0, v0, color, size) in planets.items():

    # Начальные координаты планеты
    x, y = r0, 0

    # Начальная скорость
    vx, vy = 0, v0

    # Списки координат
    xs, ys = [], []

    # Цикл моделирования движения
    for _ in range(steps):

        # Расстояние до Солнца
        r = np.sqrt(x**2 + y**2)

        # Ускорение от силы гравитации
        ax = -G * M_SUN * x / r**3
        ay = -G * M_SUN * y / r**3

        # Изменение скорости
        vx += ax * dt
        vy += ay * dt

        # Изменение координат
        x += vx * dt
        y += vy * dt

        # Сохраняем координаты
        xs.append(x / AU)
        ys.append(y / AU)

    # Сохраняем траекторию планеты
    trajectories[name] = np.array(xs), np.array(ys), color, size

# ---------------- СОЗДАНИЕ ОКНА ----------------

fig, ax = plt.subplots(figsize=(9, 9))

# Цвет фона
fig.patch.set_facecolor("black")
ax.set_facecolor("black")

# Границы координат
ax.set_xlim(-1.8, 1.8)
ax.set_ylim(-1.8, 1.8)

# Одинаковый масштаб по осям
ax.set_aspect("equal")

# ---------------- ОФОРМЛЕНИЕ ГРАФИКА ----------------

ax.set_title(
    "Моделирование движения планет вокруг Солнца",
    color="white"
)

ax.set_xlabel("x, а.е.", color="white")
ax.set_ylabel("y, а.е.", color="white")

# Цвет делений осей
ax.tick_params(colors="white")

# Цвет рамок графика
for spine in ax.spines.values():
    spine.set_color("white")

# ---------------- СОЗДАНИЕ ЗВЁЗД ----------------

np.random.seed(1)

ax.scatter(
    np.random.uniform(-1.8, 1.8, 140),
    np.random.uniform(-1.8, 1.8, 140),
    s=np.random.uniform(0.5, 2.2, 140),
    color="white",
    alpha=0.6
)

# ---------------- СВЕЧЕНИЕ СОЛНЦА ----------------

# Несколько полупрозрачных кругов
for size, alpha in zip(
    [3500, 2200, 1200],
    [0.05, 0.08, 0.12]
):

    ax.scatter(
        0,
        0,
        s=size,
        color="yellow",
        alpha=alpha,
        zorder=1
    )

# ---------------- СОЛНЦЕ ----------------

ax.scatter(
    0,
    0,
    s=420,
    color="yellow",
    edgecolors="white",
    linewidths=1.5,
    label="Солнце",
    zorder=5
)

# ---------------- СОЗДАНИЕ ПЛАНЕТ ----------------

animated_objects = []

for name, (xs, ys, color, size) in trajectories.items():

    # Орбита планеты
    ax.plot(
        xs,
        ys,
        "--",
        color=color,
        linewidth=0.8,
        alpha=0.35
    )

    # Линия движения планеты
    trail, = ax.plot(
        [],
        [],
        "-",
        color=color,
        linewidth=1.5,
        alpha=0.95
    )

    # Планета
    planet = ax.scatter(
        [],
        [],
        s=size,
        color=color,
        label=name
    )

    animated_objects.append(
        (xs, ys, trail, planet)
    )

# ---------------- ТЕКСТ С ВРЕМЕНЕМ ----------------

day_text = ax.text(
    0.02,
    0.95,
    "",
    transform=ax.transAxes,
    color="white",
    fontsize=12
)

# ---------------- ЛЕГЕНДА ----------------

ax.legend(
    facecolor="black",
    edgecolor="white",
    labelcolor="white"
)

# ---------------- ФУНКЦИЯ АНИМАЦИИ ----------------

def update(frame):

    artists = []

    # Обновление каждой планеты
    for xs, ys, trail, planet in animated_objects:

        # Обновление траектории
        trail.set_data(
            xs[:frame + 1],
            ys[:frame + 1]
        )

        # Новое положение планеты
        planet.set_offsets([
            [xs[frame], ys[frame]]
        ])

        artists.extend([trail, planet])

    # Обновление текста времени
    day_text.set_text(f"День: {frame}")

    artists.append(day_text)

    return artists

# ---------------- ЗАПУСК АНИМАЦИИ ----------------

animation = FuncAnimation(
    fig,
    update,
    frames=steps,
    interval=20,
    blit=True
)

# ---------------- ОТОБРАЖЕНИЕ ----------------

plt.show()