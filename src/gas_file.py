#imports
import snap_utils as su
import numpy as np

def GasFile(snapshot_path, percentage):
    _, _, _, _, medium_pos, medium_masses, medium_hsml, medium_temp = su.radius_cut(snapshot_path, percentage)

    # apply gas to dust ratio
    gas_2_dust = 0.01
    dust_mass = medium_masses * gas_2_dust

    gas_data = {
          'x(pc)': medium_pos[:, 0],
          'y(pc)': medium_pos[:, 1],
          'z(pc)': medium_pos[:, 2],
          'h(pc)': medium_hsml,
          'M(Msun)': dust_mass,
          'T(K)': medium_temp,         
    }

    # format the dict for skirt
    gas_skirt = np.column_stack([
          gas_data['x(pc)'],
          gas_data['y(pc)'],
          gas_data['z(pc)'],
          gas_data['h(pc)'],
          gas_data['M(Msun)'],
          gas_data['T(K)']          
    ])

    min_x, max_x = np.min(gas_data["x(pc)"]), np.max(gas_data["x(pc)"])
    min_y, max_y = np.min(gas_data["y(pc)"]), np.max(gas_data["y(pc)"])
    min_z, max_z = np.min(gas_data["z(pc)"]), np.max(gas_data["z(pc)"])

    #print statements
    print(f'--- Medium Data Min and Max Values ---')
    print(f'Min x (pc) coord: {min_x:.2e}, Max x (pc) coord: {max_x:.2e}')
    print(f'Min y (pc) coord: {min_y:.2e}, Max y (pc) coord: {max_y:.2e}')
    print(f'Min z (pc) coord: {min_z:.2e}, Max z (pc) coord: {max_z:.2e}')
    print(f'Min smoothing length (pc): {np.min(gas_data["h(pc)"]):.2e}, Max smoothing length (pc): {np.max(gas_data["h(pc)"]):.2e}')
    print(f'Min dust mass (Msun): {np.min(gas_data["M(Msun)"]):.2e}, Max dust mass (Msun): {np.max(gas_data["M(Msun)"]):.2e}')
    print(f'Min temp (K): {np.min(gas_data["T(K)"]):.2e}, Max temp (K): {np.max(gas_data["T(K)"]):.2e}')   

    header = (
         "# column 1: x(pc)\n"
         "# column 2: y(pc)\n"
         "# column 3: z(pc)\n"
         "# column 4: h(pc)\n"
         "# column 5: M(Msun)\n"
         "# column 6: T(K)"
    )
    filename = snapshot_path.replace('.hdf5', '_gas.txt')
    np.savetxt(filename, gas_skirt, fmt='%.6e', delimiter=' ', header=header, comments='')

    return filename, min_x, max_x, min_y, max_y, min_z, max_z