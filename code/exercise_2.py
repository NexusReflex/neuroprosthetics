import numpy as np
from .Neuroprosthetics.slope_fields import plotIsoc

# 1. Plot slope fields and isocline

# Differential equations - comment out all but one
# Define the DGL right hand side
dV_dt_1 = lambda V, t: 1 - V - t  # DGL nr.1
dV_dt_2 = lambda V, t: np.sin(t) - V / 1.50  # DGL nr.2

# Get slope fields
v = np.linspace(-5, 5, 30)  # voltage Interval
t = np.linspace(-5, 5, 30)  # time Interval
t_grid, v_grid = np.meshgrid(t, v)  # create a mesh

# Get slpoe field for first DGL
lng = np.sqrt(dV_dt_1(v_grid, t_grid) ** 2 + 1)  # Length of the vector
dt_1 = 1 / lng  # Get the horizontal component
dv_1 = dV_dt_1(v_grid, t_grid) / lng  # Get the vertical component
dv_iso_1 = dV_dt_1(v_grid, t_grid)

# Get slope field for second DGL
lng = np.sqrt(dV_dt_2(v_grid, t_grid) ** 2 + 1)  # Length of the vector
dt_2 = 1 / lng  # Get the horizontal component
dv_2 = dV_dt_2(v_grid, t_grid) / lng  # Get the vertical component
dv_iso_2 = dV_dt_2(v_grid, t_grid)

# Plot slope fields with isoclines
plotIsoc(t_grid, v_grid, dv_iso_1, dt_1, dv_1, 'isoclines_DGL_1.eps')
plotIsoc(t_grid, v_grid, dv_iso_2, dt_2, dv_2, 'isoclines_DGL_2.eps')

# 2. Plot Circuit slope field
R = 1.3
C = 0.8
dV_dt_3 = lambda V, t, I_max: (
            (I_max * np.sin(t) - V / R) / C)  # DGL for circuit
dV_dt_4 = lambda V, t, I_max: ((I_max * np.sin(
    t) - V / R) / C) + 2  # add D=2 as const.

for i_max in [0, 1]:
    lng = np.sqrt(
        dV_dt_3(v_grid, t_grid, i_max) ** 2 + 1)  # Length of the vector
    dt_circuit_1 = 1 / lng  # Get the horizontal component
    dv_circuit_1 = dV_dt_3(v_grid, t_grid,
                           i_max) / lng  # Get the vertical component
    dv_iso_3 = dV_dt_3(v_grid, t_grid, i_max)
    plotIsoc(t_grid, v_grid, dv_iso_3, dt_circuit_1, dv_circuit_1,
             'slopes_circuitDGL_' + str(i_max) + '.eps', plot_isoclines=False)

for i_max in [0, 1]:
    lng = np.sqrt(
        dV_dt_4(v_grid, t_grid, i_max) ** 2 + 1)  # Length of the vector
    dt_circuit_2 = 1 / lng  # Get the horizontal component
    dv_circuit_2 = dV_dt_4(v_grid, t_grid,
                           i_max) / lng  # Get the vertical component
    dv_iso_4 = dV_dt_4(v_grid, t_grid, i_max)
    plotIsoc(t_grid, v_grid, dv_iso_4, dt_circuit_2, dv_circuit_2,
             'slopes_circuitDGL_' + str(i_max) + 'withConst.eps',
             plot_isoclines=False)
