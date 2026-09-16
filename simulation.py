import numpy as np


def calculate_outlet_temperatures(
    T,
    hot_region,
    cold_region
):
    """
    Calculate the outlet temperatures of the hot and cold fluids.

    Parameters
    ----------
    T : np.ndarray
        Current temperature field.
    hot_region : np.ndarray
        Boolean mask for the hot fluid region.
    cold_region : np.ndarray
        Boolean mask for the cold fluid region.

    Returns
    -------
    T_hot_out : float
        Mean temperature at the hot-fluid outlet.
    T_cold_out : float
        Mean temperature at the cold-fluid outlet.
    """

    # --------------------------------------------------------
    # HEISSER AUSLASS
    #
    # rechts
    # --------------------------------------------------------

    hot_out_rows = np.where(
        hot_region[:, -1]
    )[0]

    T_hot_out = np.mean(
        T[
            hot_out_rows,
            -1
        ]
    )

    # --------------------------------------------------------
    # KALTER AUSLASS
    #
    # links
    # --------------------------------------------------------

    cold_out_rows = np.where(
        cold_region[:, 0]
    )[0]

    T_cold_out = np.mean(
        T[
            cold_out_rows,
            0
        ]
    )

    return (
        T_hot_out,
        T_cold_out
    )


def run_simulation(
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
):
    """
    Run the 2D counterflow heat exchanger simulation.

    The numerical calculation is based on the original
    vectorized NumPy implementation.

    Returns
    -------
    frames : list[np.ndarray]
        Stored temperature fields for visualization.
    frame_times : list[float]
        Simulation time corresponding to each stored frame.
    hot_out_history : list[float]
        Hot outlet temperature corresponding to each stored frame.
    cold_out_history : list[float]
        Cold outlet temperature corresponding to each stored frame.
    """

    # ========================================================
    # 1. GEOMETRIE
    # ========================================================

    H_TOTAL = (
        2 * H_FLUID
        + H_WALL
    )

    # ========================================================
    # 2. NUMERISCHES GITTER
    # ========================================================

    dx = L / NX
    dy = H_TOTAL / NY

    x = np.linspace(
        0,
        L,
        NX
    )

    y = np.linspace(
        0,
        H_TOTAL,
        NY
    )

    X, Y = np.meshgrid(
        x,
        y
    )

    # X wird aktuell für die Berechnung nicht benötigt.
    _ = X

    # ========================================================
    # 3. REGIONEN
    # ========================================================

    y_wall_min = H_FLUID

    y_wall_max = (
        H_FLUID
        + H_WALL
    )

    hot_region = (
        Y < y_wall_min
    )

    wall_region = (
        (Y >= y_wall_min)
        &
        (Y < y_wall_max)
    )

    cold_region = (
        Y >= y_wall_max
    )

    # ========================================================
    # 4. DIFFUSIVITÄTEN
    # ========================================================

    alpha_hot = (
        k_hot
        / (rho_hot * cp_hot)
    )

    alpha_cold = (
        k_cold
        / (rho_cold * cp_cold)
    )

    alpha_wall = (
        k_wall
        / (rho_wall * cp_wall)
    )

    alpha_max = max(
        alpha_hot,
        alpha_cold,
        alpha_wall
    )

    # ========================================================
    # 5. STABILITÄTSPRÜFUNG
    # ========================================================

    dt_diffusion = (
        0.25
        * min(dx, dy)**2
        / alpha_max
    )

    dt_advection = (
        dx
        / max(
            abs(u_hot),
            abs(u_cold)
        )
    )

    print()
    print("=" * 60)
    print("NUMERISCHE PARAMETER")
    print("=" * 60)

    print(
        f"dx = {dx:.6e} m"
    )

    print(
        f"dy = {dy:.6e} m"
    )

    print(
        f"dt = {dt:.6e} s"
    )

    print(
        f"max. dt Diffusion = "
        f"{dt_diffusion:.6e} s"
    )

    print(
        f"max. dt Advektion = "
        f"{dt_advection:.6e} s"
    )

    # --------------------------------------------------------
    # STABILITÄTSCHECK
    #
    # Wie im ursprünglichen Code auskommentiert.
    # --------------------------------------------------------

    # if dt > dt_diffusion:
    #
    #     raise ValueError(
    #         "\nDT IST ZU GROSS FÜR DIE DIFFUSION!\n"
    #         f"dt = {dt:.3e} s\n"
    #         f"maximal = {dt_diffusion:.3e} s"
    #     )
    #
    #
    # if dt > dt_advection:
    #
    #     raise ValueError(
    #         "\nDT IST ZU GROSS FÜR DIE STRÖMUNG!\n"
    #         f"dt = {dt:.3e} s\n"
    #         f"maximal = {dt_advection:.3e} s"
    #     )

    # ========================================================
    # 6. TEMPERATURFELD INITIALISIEREN
    # ========================================================

    T = np.zeros(
        (NY, NX)
    )

    # Heißer Kanal

    T[hot_region] = (
        T_hot_in
    )

    # Kalter Kanal

    T[cold_region] = (
        T_cold_in
    )

    # Wand

    T[wall_region] = (
        T_hot_in
        + T_cold_in
    ) / 2

    # ========================================================
    # 7. MATERIALFELDER
    # ========================================================

    rho = np.zeros_like(
        T
    )

    cp = np.zeros_like(
        T
    )

    k = np.zeros_like(
        T
    )

    # Heißes Fluid

    rho[hot_region] = (
        rho_hot
    )

    cp[hot_region] = (
        cp_hot
    )

    k[hot_region] = (
        k_hot
    )

    # Wand

    rho[wall_region] = (
        rho_wall
    )

    cp[wall_region] = (
        cp_wall
    )

    k[wall_region] = (
        k_wall
    )

    # Kaltes Fluid

    rho[cold_region] = (
        rho_cold
    )

    cp[cold_region] = (
        cp_cold
    )

    k[cold_region] = (
        k_cold
    )

    # ========================================================
    # 8. GESCHWINDIGKEITSFELD
    # ========================================================

    u = np.zeros_like(
        T
    )

    u[hot_region] = (
        u_hot
    )

    u[cold_region] = (
        u_cold
    )

    # Wand bleibt bei u = 0

    # ========================================================
    # 9. SPEICHER FÜR VIDEOFRAMES
    # ========================================================

    frames = []

    frame_times = []

    hot_out_history = []

    cold_out_history = []

    # ========================================================
    # 10. SIMULATION
    # ========================================================

    print()
    print("=" * 60)
    print("STARTE SIMULATION")
    print("=" * 60)

    for step in range(
        N_STEPS
    ):

        T_old = T.copy()

        # ====================================================
        # WÄRMELEITUNG
        # ====================================================

        laplacian = np.zeros_like(
            T
        )

        laplacian[
            1:-1,
            1:-1
        ] = (

            (
                T_old[
                    1:-1,
                    2:
                ]

                - 2
                * T_old[
                    1:-1,
                    1:-1
                ]

                + T_old[
                    1:-1,
                    :-2
                ]
            )
            / dx**2

            +

            (
                T_old[
                    2:,
                    1:-1
                ]

                - 2
                * T_old[
                    1:-1,
                    1:-1
                ]

                + T_old[
                    :-2,
                    1:-1
                ]
            )
            / dy**2
        )

        diffusion = (
            k
            / (rho * cp)
            * laplacian
        )

        # ====================================================
        # ADVEKTION
        # ====================================================

        advection = np.zeros_like(
            T
        )

        # ----------------------------------------------------
        # HEISSES FLUID
        #
        # Strömung:
        #
        #       -------->
        #
        # u > 0
        #
        # Upwind:
        #
        # dT/dx = (T_i - T_i-1) / dx
        # ----------------------------------------------------

        hot_gradient = np.zeros_like(
            T
        )

        hot_gradient[
            :,
            1:
        ] = (
            T_old[
                :,
                1:
            ]

            - T_old[
                :,
                :-1
            ]
        ) / dx

        advection[
            hot_region
        ] = (
            -u_hot
            * hot_gradient[
                hot_region
            ]
        )

        # ----------------------------------------------------
        # KALTES FLUID
        #
        # Strömung:
        #
        #       <--------
        #
        # u < 0
        # ----------------------------------------------------

        cold_gradient = np.zeros_like(
            T
        )

        cold_gradient[
            :,
            :-1
        ] = (
            T_old[
                :,
                1:
            ]

            - T_old[
                :,
                :-1
            ]
        ) / dx

        advection[
            cold_region
        ] = (
            -u_cold
            * cold_gradient[
                cold_region
            ]
        )

        # ====================================================
        # TEMPERATURÄNDERUNG
        # ====================================================

        T = (
            T_old
            + dt
            * (
                diffusion
                + advection
            )
        )

        # ====================================================
        # RAND BEDINGUNGEN
        # ====================================================

        # ----------------------------------------------------
        # HEISSER EINLASS
        #
        # links
        # ----------------------------------------------------

        hot_in_rows = np.where(
            hot_region[:, 0]
        )[0]

        T[
            hot_in_rows,
            0
        ] = T_hot_in

        # ----------------------------------------------------
        # KALTER EINLASS
        #
        # rechts
        # ----------------------------------------------------

        cold_in_rows = np.where(
            cold_region[:, -1]
        )[0]

        T[
            cold_in_rows,
            -1
        ] = T_cold_in

        # ----------------------------------------------------
        # ADIABATISCHE AUSSENWÄNDE
        # ----------------------------------------------------

        T[
            0,
            :
        ] = T[
            1,
            :
        ]

        T[
            -1,
            :
        ] = T[
            -2,
            :
        ]

        # ====================================================
        # ZEIT
        # ====================================================

        current_time = (
            step * dt
        )

        # ====================================================
        # AUSLASSTEMPERATUREN
        # ====================================================

        T_hot_out, T_cold_out = (
            calculate_outlet_temperatures(
                T,
                hot_region,
                cold_region
            )
        )

        # ====================================================
        # VIDEOFRAME
        #
        # Die Ausgangstemperaturen werden nur zusammen mit
        # dem jeweiligen gespeicherten Frame gespeichert.
        # Dadurch haben alle Listen denselben Index.
        # ====================================================

        if step % FRAME_EVERY == 0:

            frames.append(
                T.copy()
            )

            frame_times.append(
                current_time
            )

            hot_out_history.append(
                T_hot_out
            )

            cold_out_history.append(
                T_cold_out
            )

            # ------------------------------------------------
            # Fortschrittsausgabe
            # ------------------------------------------------

            if step % (
                FRAME_EVERY * 20
            ) == 0:

                print(
                    f"t = {current_time:7.3f} s | "
                    f"Hot out = {T_hot_out:6.2f} °C | "
                    f"Cold out = {T_cold_out:6.2f} °C"
                )

    # ========================================================
    # SIMULATION ENDE
    # ========================================================

    print()
    print("=" * 60)
    print("SIMULATION FERTIG")
    print("=" * 60)

    print(
        f"Simulationszeit: "
        f"{frame_times[-1]:.3f} s"
    )

    print(
        f"Heißer Auslass: "
        f"{hot_out_history[-1]:.2f} °C"
    )

    print(
        f"Kalter Auslass: "
        f"{cold_out_history[-1]:.2f} °C"
    )

    # ========================================================
    # RÜCKGABE
    # ========================================================

    return (
        frames,
        frame_times,
        hot_out_history,
        cold_out_history
    )