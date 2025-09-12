    def SimRun(self):
        '''
        Manages the entire SKIRT simulation process.
        Calls methods to read snapshot information, create gas and source data files, generate the .ski configuration file, and execute the SKIRT simulation.
        Includes a timing method to measure total simulation runtime.
        
        Steps:
            1. Attempts to open and read the snapshot file using `self.SnapInfo()`.
            2. Creates the SKIRT-formatted source file using `self.SrcFile()`.
            3. Creates the SKIRT-formatted gas file using `self.GasFile()`.
            4. Generates the .ski file using `self.SkiFile()`, providing paths for the gas and source files.
            5. Executes the SKIRT simulation using the generated .ski file.
        
        Returns:
            gas_data (dict): The processed gas data dictionary.
            src_data (dict): The processed source data dictionary.
            sim: The SKIRT simulation result.
        '''
        start_time = time.time() #start timing
        print('Starting timing for simulation.')

        try:
            print(f'Attempting to open snapshot file: {self.snapshot}')
            self.SnapInfo()
            print('File was opened successfully.')
            # get src file
            srcFile = self.SrcFile()
            # get gas file
            gasFile = self.GasFile()
            print('SKIRT source and gas files created')
            #create the ski file from the template
            skiFile = self.SkiFile(gasFile, srcFile) 
            print('SKIRT .ski file created.')
            #execute simulation
            skirt = sm.Skirt()
            sim = skirt.execute(skiFile, console='brief')
            print('SKIRT sim executed.')

            end_time = time.time()  # End timing
            print("Ending timing.")
            elapsed_time = end_time - start_time
            print(f"Execution time: {elapsed_time:.2e} seconds")
                
            return self.gas_data, self.src_data, sim

        except FileNotFoundError:
            print(f'Error: File {self.snapshot} not found.')
            return None, None, None
#process the snapshot file
if __name__ == "__main__":
    snapshot_file = 'snapshot_150.hdf5' 
    percentage = 1
    sim = SkirtSim(snapshot_file, r_extract_percent=percentage)
    gas_data, source_data, sim_result = sim.SimRun()