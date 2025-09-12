def SkiFile(snapshot_path, gasFile, srcFile):
        '''
        Generates the SKIRT configuration file (.ski) by updating a template file with simulation parameters and data filenames.
        
        Args:
            gasFile (str): Filename of the processed gas data for SKIRT configuration.
            srcFile (str): Filename of the processed source data for SKIRT configuration.
        
        Reads the template .ski file and replaces placeholders.
        The updated .ski file is then written.
        '''
        filename = snapshot_path.replace('.hdf5', '')

        # read the SKIRT template file
        skitemp = 'template.ski'
        with open(skitemp, 'r') as f:
            filedata = f.read()
    
        filedata = filedata.replace('"SOURCEFILE"', f'"{srcFile}"')
        filedata = filedata.replace('"GASFILE"', f'"{gasFile}"')


        header = self.snap_head
        boxsize = header['BoxSize (pc)']
        center = header['Center (pc)']
        x_min, x_max = header['x_min'], header['x_max']
        y_min, y_max = header['y_min'], header['y_max']
        z_min, z_max = header['z_min'], header['z_max']

    
        #read the SKIRT template file
        skitemp = "template.ski" 
        with open(skitemp, 'r') as f:
            filedata = f.read()
    
        #replacing min and max bounds for X, Y, and Z based on the simulation box size
        filedata = filedata.replace('"XMIN"', f'"{x_min} pc"')
        filedata = filedata.replace('"XMAX"', f'"{x_max} pc"')
        filedata = filedata.replace('"YMIN"', f'"{y_min} pc"')
        filedata = filedata.replace('"YMAX"', f'"{y_max} pc"')
        filedata = filedata.replace('"ZMIN"', f'"{z_min} pc"')
        filedata = filedata.replace('"ZMAX"', f'"{z_max} pc"')
    
        # Update field of view based on new box size
        field_of_view_x = x_max - x_min
        field_of_view_y = y_max - y_min
        filedata = filedata.replace('"FOVX"', f'"{field_of_view_x} pc"')
        filedata = filedata.replace('"FOVY"', f'"{field_of_view_y} pc"')
    
        #write the new SKIRT configuration file
        skifile = filename + '.ski'
        with open(skifile, 'w') as f:
            f.write(filedata)
    
        return skifile