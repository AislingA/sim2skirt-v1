#imports
import snap_utils as su
import numpy as np

def computeTemperature(luminosity, star_radius):
    '''
    Computes the surface temperature of a star using its luminosity, radius, and the Stefan-Boltzmann Law.
    The Stefan-Boltzmann constant (sigma) used is 5.670374419e-5.
    Returns temperature in Kelvin.
    '''
    sigma = 5.670374419e-5
    T_sun = 5777 # k
    return T_sun * (luminosity / star_radius**2)**0.25

def SrcFile(snapshot_path, percentage):
    source_pos, source_hsml, source_radius, source_luminosity, _, _, _, _ = su.radius_cut(snapshot_path, percentage)
    # compute the temps
    source_temp = computeTemperature(source_luminosity, source_radius)

    src_data = {
          'x(pc)': source_pos[:, 0],
          'y(pc)': source_pos[:, 1],
          'z(pc)': source_pos[:, 2],
          'h(pc)': source_hsml,
          'R(km)': source_radius,
          'T(K)': source_temp,
    }

    # format the dict for skirt
    src_skirt = np.column_stack([
          src_data['x(pc)'],
          src_data['y(pc)'],
          src_data['z(pc)'],
          src_data['h(pc)'],
          src_data['R(km)'],
          src_data['T(K)']          
    ])

    #print statements
    print(f'--- Source Data Min and Max Values ---')
    print(f'Min x (pc) coord: {np.min(src_data["x(pc)"]):.2e}, Max x (pc) coord: {np.max(src_data["x(pc)"]):.2e}')
    print(f'Min y (pc) coord: {np.min(src_data["y(pc)"]):.2e}, Max y (pc) coord: {np.max(src_data["y(pc)"]):.2e}')
    print(f'Min z (pc) coord: {np.min(src_data["z(pc)"]):.2e}, Max z (pc) coord: {np.max(src_data["z(pc)"]):.2e}')
    print(f'Min smoothing length (pc): {np.min(src_data["h(pc)"]):.2e}, Max smoothing length (pc): {np.max(src_data["h(pc)"]):.2e}')
    print(f'Min radius (km): {np.min(src_data["R(km)"]):.2e}, Max radius (km): {np.max(src_data["R(km)"]):.2e}')
    print(f'Min temp (K): {np.min(src_data["T(K)"]):.2e}, Max temp (K): {np.max(src_data["T(K)"]):.2e}')

    header = (
         "# x(pc) y(pc) z(pc) h(pc) R(km) T(K)"
    )
    filename = snapshot_path.replace('.hdf5', '_src.txt')
    np.savetxt(filename, src_skirt, fmt='%.6e', delimiter=' ', header=header, comments='')

    return filename