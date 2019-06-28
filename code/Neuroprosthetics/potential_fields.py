import numpy as np


def potential(r, rho, i):
    phi = (rho * i) / (4 * np.pi * r)
    return phi


def calculate_point_source_potential_field(center_point, slicesize, rho,
                                           i_point_source, distance, resolution=1e-6):
    x, y = int(slicesize[0] / resolution)+1, int(slicesize[1] / resolution)+1   # +1 for proper plot (50x50)

    potentialfield = np.zeros((x, y))

    def compute_potential(n, m):
        current_point = np.array([n, m])
        distance_from_center = np.sqrt((np.linalg.norm(current_point * resolution -
            center_point)) ** 2 + distance ** 2)
        return potential(distance_from_center, rho, i_point_source)

    for n in range(x):
        for m in range(y):
            potentialfield[n, m] = compute_potential(n, m)

    return potentialfield


def calculate_external_potential(rho, current, resolution, axon_length=50e-6, vertical_distance=10e-6, center_point=25e-6):
    '''Calculates external potential, e-field and action potential along a neuron.'''
    x_position = np.arange(0, axon_length, resolution)

    def compute_potential(x_position):
        distance_from_source = np.sqrt((x_position -
            center_point) ** 2 + vertical_distance ** 2)
        return potential(distance_from_source, rho, current), distance_from_source

    potential_array, distances_array= compute_potential(x_position)
    e_field = - np.gradient(potential_array)
    activation = np.gradient(np.gradient(potential_array))

    return potential_array, e_field, activation, x_position



