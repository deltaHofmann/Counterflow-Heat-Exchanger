# ==================================================
# Geometry
# ==================================================

L = 2.0
H_FLUID = 0.002
H_WALL = 0.0001


# ==================================================
# Grid
# ==================================================

NX = 300
NY = 40


# ==================================================
# Hot fluid
# ==================================================

rho_hot = 1000.0   # kg/m³
cp_hot = 4180.0    # J/(kg K)
k_hot = 0.6        # W/(m K)
u_hot = 0.05       # m/s
T_hot_in = 100.0   # degree Celsius


# ==================================================
# Cold fluid
# ==================================================

rho_cold = 1000.0
cp_cold = 4180.0
k_cold = 0.6
u_cold = -0.05
T_cold_in = 10.0


# ==================================================
# Wall
# ==================================================

rho_wall = 8960.0
cp_wall = 385.0
k_wall = 400.0


# ==================================================
# Simulation
# ==================================================

dt = 0.001
N_STEPS = 100000
FRAME_EVERY = 100


# ==================================================
# Imports
# ==================================================

from simulation import run_simulation
from visualization import create_visualization


# ==================================================
# Main
# ==================================================

def main():

    frames, frame_times, hot_out_history, cold_out_history = run_simulation(
        L,
        H_FLUID,
        H_WALL,
        NX,
        NY,
        rho_hot,
        cp_hot,
        k_hot,
        u_hot,
        T_hot_in,
        rho_cold,
        cp_cold,
        k_cold,
        u_cold,
        T_cold_in,
        rho_wall,
        cp_wall,
        k_wall,
        dt,
        N_STEPS,
        FRAME_EVERY
    )

    create_visualization(
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
    )


if __name__ == "__main__":
    main()