#imports
import h5py
import numpy as np

def create_snapshot_data(snapshot_path):
    """
    Reads in a snapshot file and creates the header and particle data variables

    Parameters
    ----------
    snapshot_path: str
        The file path for the snapshot

    Returns
    --------
    header, pto, pt5: 
    """
    with h5py.File(snapshot_path, 'r') as f:
        header = f['Header'].attrs
        pt0 = f['PartType0']
        pt5 = f['PartType5']

    return header, pt0, pt5

def center_data(snapshot_path):
    """
      
    """
    header, pt0, pt5 = create_snapshot_data(snapshot_path)

    # get the boxsize
    box_size = header['BoxSize']
    print(f'Full box size from the snapshot header: {box_size:.2f} pc.')

    # do centering
    medium_pos = pt0['Coordinates'][:]
    center = np.median(gas_pos,axis=0)
    print(f'Center is: {center}')
    medium_pos -= center

    return box_size, medium_pos, center

def radius_cut(snapshot_path, percentage):
    header, pt0, pt5 = create_snapshot_data(snapshot_path)
    box_size, medium_pos, center  = center_data(snapshot_path)

    # defining r_extract as a percentage of the boxsize
    r_extract = percentage * (box_size / 2)
    radius_cut = np.sum(medium_pos*medium_pos, axis=1) < r_extract * r_extract

    # apply radius cut to parameters needed for simulation

    # source parameters
    source_pos = pt5['Coordinates'][:]
    source_hsml = pt5['BH_AccretionLength'][:]
    source_radius = pt5['ProtoStellarRadius_inSolar'][:]
    source_luminosity = pt5['StarLuminosity_Solar'][:]
    print(f'Number of sources prior the radius cut: {len(source_luminosity)}')

    source_pos, source_hsml, source_radius, source_luminosity = source_pos[radius_cut], source_hsml[radius_cut], source_radius[radius_cut], source_luminosity[radius_cut] 
    print(f'Number of sources after the radius cut: {len(source_luminosity)}')

    # medium parameters
    medium_masses = pt0['Masses'][:]
    medium_hsml = pt0['SmoothingLength'][:]
    medium_temp = pt0['Temperature'][:]

    medium_pos, medium_masses, medium_hsml, medium_temp = medium_pos[radius_cut], medium_masses[radius_cut], medium_hsml[radius_cut], medium_temp[radius_cut]

    return source_pos, source_hsml, source_radius, source_luminosity, medium_pos, medium_masses, medium_hsml, medium_temp

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
    source_pos, source_hsml, source_radius, source_luminosity, _, _, _, _ = radius_cut(snapshot_path, percentage)
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
        
def GasFile(snapshot_path, percentage):
    _, _, _, _, medium_pos, medium_masses, medium_hsml, medium_temp = radius_cut(snapshot_path, percentage)

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

    #print statements
    print(f'--- Medium Data Min and Max Values ---')
    print(f'Min x (pc) coord: {np.min(gas_data["x(pc)"]):.2e}, Max x (pc) coord: {np.max(gas_data["x(pc)"]):.2e}')
    print(f'Min y (pc) coord: {np.min(gas_data["y(pc)"]):.2e}, Max y (pc) coord: {np.max(gas_data["y(pc)"]):.2e}')
    print(f'Min z (pc) coord: {np.min(gas_data["z(pc)"]):.2e}, Max z (pc) coord: {np.max(gas_data["z(pc)"]):.2e}')
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

    return filename 

