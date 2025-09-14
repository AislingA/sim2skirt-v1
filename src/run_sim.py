# imports
import time
import gas_file as gf
import source_file as sf
import ski_file as skf
import PTS9.utils as ut
import PTS9.simulation as sm
import PTS9.visual as vs
import PTS9.do

def SimRun(snapshot_path, percentage):
    start_time = time.time()
    print('--- Starting the simulation ---')

    try:
        # Create the gas and source files
        gasFile, x_min, x_max, y_min, y_max, z_min, z_max = gf.GasFile(snapshot_path, percentage)
        srcFile = sf.SrcFile(snapshot_path, percentage)
        print('\n1. SKIRT source and gas files created')

        # Create .ski file
        skiFile = skf.SkiFile(snapshot_path, gasFile, srcFile, x_min, x_max, y_min, y_max, z_min, z_max)
        print('\n2. SKIRT .ski file created')

        # Execute the SKIRT simulation
        skirt = sm.Skirt()
        sim = skirt.execute(skiFile, console='brief')
        print('\n3. SKIRT sim executed')

        # End timing
        end_time = time.time()
        print('--- Ending the simulation ---')
        elapsed_time = end_time - start_time
        print(f"Execution time: {elapsed_time:.2e} seconds")

        return sim
    
    except FileNotFoundError:
        print(f'Error: File {snapshot_path} not found.')
        return None
    
if __name__ == "__main__":
    snapshot_file = 'snapshot_150.hdf5'
    percentage = 0.10
    SimRun(snapshot_file, percentage)