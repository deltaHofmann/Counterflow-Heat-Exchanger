# visualization.py

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button

from playback import PlaybackController


def create_visualization(
    frames,
    frame_times,
    hot_out_history,
    cold_out_history,
    L,
    H_FLUID,
    H_WALL,
    T_hot_in,
    T_cold_in,
    u_hot,
    u_cold
):
    """
    Create and display the interactive visualization of the
    counterflow heat exchanger simulation.
    """

    # --------------------------------------------------
    # Geometry
    # --------------------------------------------------

    H_TOTAL = (
        2 * H_FLUID
        + H_WALL
    )

    y_wall_min = H_FLUID

    y_wall_max = (
        H_FLUID
        + H_WALL
    )

    # Center positions of the two fluid channels

    hot_y = (
        H_FLUID / 2
    )

    cold_y = (
        H_WALL
        + H_FLUID
        + H_FLUID / 2
    )

    # --------------------------------------------------
    # Figure
    # --------------------------------------------------

    fig = plt.figure(
        figsize=(16, 6.5)
    )

    ax = fig.add_axes(
        [0.06, 0.27, 0.78, 0.58]
    )

    # --------------------------------------------------
    # Heatmap
    # --------------------------------------------------

    cmap = plt.get_cmap(
        "RdYlBu_r"
    )

    im = ax.imshow(
        frames[0],
        extent=[
            0,
            L,
            0,
            H_TOTAL
        ],
        origin="lower",
        aspect="auto",
        cmap=cmap,
        vmin=T_cold_in,
        vmax=T_hot_in
    )

    # --------------------------------------------------
    # Colorbar
    # --------------------------------------------------

    cbar = fig.colorbar(
        im,
        ax=ax,
        pad=0.015,
        fraction=0.035
    )

    cbar.set_label(
        "Temperature [°C]",
        fontsize=11
    )

    # --------------------------------------------------
    # Wall
    # --------------------------------------------------

    ax.axhspan(
        y_wall_min,
        y_wall_max,
        facecolor="black",
        alpha=0.9,
        zorder=5
    )

    ax.axhline(
        y_wall_min,
        color="white",
        linewidth=1.5,
        zorder=6
    )

    ax.axhline(
        y_wall_max,
        color="white",
        linewidth=1.5,
        zorder=6
    )

    # WALL label at the edge of the heatmap

    ax.text(
        L,
        (
            y_wall_min
            + y_wall_max
        ) / 2,
        "  WALL",
        color="black",
        fontsize=9,
        fontweight="bold",
        ha="left",
        va="center",
        clip_on=False,
        zorder=10
    )

    # --------------------------------------------------
    # Inlet / outlet temperature labels
    # --------------------------------------------------

    hot_in_text = ax.text(
        0.015 * L,
        hot_y,
        "",
        ha="left",
        va="center",
        fontsize=10,
        fontweight="bold",
        color="black",
        zorder=10
    )

    hot_out_text = ax.text(
        0.985 * L,
        hot_y,
        "",
        ha="right",
        va="center",
        fontsize=10,
        fontweight="bold",
        color="black",
        zorder=10
    )

    cold_in_text = ax.text(
        0.985 * L,
        cold_y,
        "",
        ha="right",
        va="center",
        fontsize=10,
        fontweight="bold",
        color="black",
        zorder=10
    )

    cold_out_text = ax.text(
        0.015 * L,
        cold_y,
        "",
        ha="left",
        va="center",
        fontsize=10,
        fontweight="bold",
        color="black",
        zorder=10
    )

    # --------------------------------------------------
    # Flow arrows
    # --------------------------------------------------

    # Hot: left -> right

    hot_arrow = ax.annotate(
        "",
        xy=(
            0.72 * L,
            hot_y
        ),
        xytext=(
            0.28 * L,
            hot_y
        ),
        arrowprops=dict(
            arrowstyle="->",
            linewidth=1.2,
            color="black"
        ),
        zorder=8
    )

    hot_velocity_text = ax.text(
        0.50 * L,
        hot_y + 0.00012,
        f"→  {abs(u_hot):.2f} m/s",
        ha="center",
        va="bottom",
        fontsize=9,
        color="black",
        zorder=8
    )

    # Cold: right -> left

    cold_arrow = ax.annotate(
        "",
        xy=(
            0.28 * L,
            cold_y
        ),
        xytext=(
            0.72 * L,
            cold_y
        ),
        arrowprops=dict(
            arrowstyle="->",
            linewidth=1.2,
            color="black"
        ),
        zorder=8
    )

    cold_velocity_text = ax.text(
        0.50 * L,
        cold_y - 0.00012,
        f"←  {abs(u_cold):.2f} m/s",
        ha="center",
        va="top",
        fontsize=9,
        color="black",
        zorder=8
    )

    # --------------------------------------------------
    # Axis
    # --------------------------------------------------

    ax.set_xlabel(
        "Length [m]"
    )

    ax.set_ylabel(
        "Height [m]"
    )

    ax.set_xlim(
        0,
        L
    )

    ax.set_ylim(
        0,
        H_TOTAL
    )

    ax.set_title(
        "Counterflow Heat Exchanger",
        fontsize=15,
        fontweight="bold",
        pad=14
    )

    # --------------------------------------------------
    # Simulation time
    # --------------------------------------------------

    info_text = fig.text(
        0.385,
        0.085,
        "",
        ha="center",
        va="center",
        fontsize=11,
        fontweight="bold"
    )

    # --------------------------------------------------
    # Playback controller
    # --------------------------------------------------

    playback = PlaybackController()

    # --------------------------------------------------
    # Time slider
    # --------------------------------------------------

    slider_ax = fig.add_axes(
        [0.10, 0.14, 0.57, 0.035]
    )

    time_slider = Slider(
        slider_ax,
        "Time [s]",
        0,
        frame_times[-1],
        valinit=0,
        valstep=(
            frame_times[1]
            - frame_times[0]
        )
    )

    # --------------------------------------------------
    # Playback buttons
    # --------------------------------------------------

    slower_ax = fig.add_axes(
        [0.70, 0.115, 0.065, 0.055]
    )

    slower_button = Button(
        slower_ax,
        "◀ Slower"
    )

    play_ax = fig.add_axes(
        [0.77, 0.115, 0.065, 0.055]
    )

    play_button = Button(
        play_ax,
        "▶ Play"
    )

    pause_ax = fig.add_axes(
        [0.84, 0.115, 0.065, 0.055]
    )

    pause_button = Button(
        pause_ax,
        "⏸ Pause"
    )

    faster_ax = fig.add_axes(
        [0.91, 0.115, 0.065, 0.055]
    )

    faster_button = Button(
        faster_ax,
        "Faster ▶"
    )

    # --------------------------------------------------
    # Set frame
    # --------------------------------------------------

    def set_frame(frame_index):
        """
        Update the complete visualization to a given frame.
        """

        frame_index = int(
            max(
                0,
                min(
                    frame_index,
                    len(frames) - 1
                )
            )
        )

        # --------------------------------------------------
        # Update heatmap
        # --------------------------------------------------

        im.set_data(
            frames[frame_index]
        )

        # --------------------------------------------------
        # Current simulation time
        # --------------------------------------------------

        current_time = (
            frame_times[frame_index]
        )

        # --------------------------------------------------
        # Outlet temperatures
        #
        # IMPORTANT:
        # hot_out_history and cold_out_history now contain
        # only values for stored frames. Therefore their
        # indices correspond directly to frame_index.
        # --------------------------------------------------

        hot_out = (
            hot_out_history[frame_index]
        )

        cold_out = (
            cold_out_history[frame_index]
        )

        # --------------------------------------------------
        # Update temperature labels
        # --------------------------------------------------

        hot_in_text.set_text(
            f"Hot In\n"
            f"{T_hot_in:.1f} °C"
        )

        hot_out_text.set_text(
            f"Hot Out\n"
            f"{hot_out:.1f} °C"
        )

        cold_in_text.set_text(
            f"Cold In\n"
            f"{T_cold_in:.1f} °C"
        )

        cold_out_text.set_text(
            f"Cold Out\n"
            f"{cold_out:.1f} °C"
        )

        # --------------------------------------------------
        # Update simulation time
        # --------------------------------------------------

        info_text.set_text(
            f"Simulation time: "
            f"{current_time:.2f} s"
        )

        # --------------------------------------------------
        # Synchronize slider
        # --------------------------------------------------

        time_slider.eventson = False

        time_slider.set_val(
            current_time
        )

        time_slider.eventson = True

        # --------------------------------------------------
        # Store current frame
        # --------------------------------------------------

        playback.current_frame = (
            frame_index
        )

        fig.canvas.draw_idle()

    # --------------------------------------------------
    # Slider callback
    # --------------------------------------------------

    def slider_changed(val):

        frame_index = int(
            np.argmin(
                np.abs(
                    np.array(frame_times)
                    - val
                )
            )
        )

        set_frame(
            frame_index
        )

    time_slider.on_changed(
        slider_changed
    )

    # --------------------------------------------------
    # Button callbacks
    # --------------------------------------------------

    def play(event):
        playback.play()

    def pause(event):
        playback.pause()

    def slower(event):
        playback.slower()

    def faster(event):
        playback.faster()

    play_button.on_clicked(
        play
    )

    pause_button.on_clicked(
        pause
    )

    slower_button.on_clicked(
        slower
    )

    faster_button.on_clicked(
        faster
    )

    # --------------------------------------------------
    # Animation update
    # --------------------------------------------------

    def animation_update(frame):
        """
        Update the playback animation.
        """

        if not playback.playing:
            return []

        next_frame = playback.get_next_frame(
            len(frames)
        )

        set_frame(
            next_frame
        )

        return []

    # --------------------------------------------------
    # Animation
    # --------------------------------------------------

    animation = FuncAnimation(
        fig,
        animation_update,
        frames=len(frames),
        interval=50,
        blit=False,
        repeat=True
    )

    # Keep a reference to prevent garbage collection

    fig._animation = animation

    # --------------------------------------------------
    # Initial frame
    # --------------------------------------------------

    set_frame(0)

    # --------------------------------------------------
    # Show
    # --------------------------------------------------

    plt.show()