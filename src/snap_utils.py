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
    header, pt0, pt5: 
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
    center = np.median(medium_pos,axis=0)
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
