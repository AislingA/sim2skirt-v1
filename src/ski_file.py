# imports


def SkiFile(snapshot_path, srcFile, gasFile, x_min, x_max, y_min, y_max, z_min, z_max):
     filename = snapshot_path.replace('.hdf5', '')

     #read the template file
     skitemp = 'template.ski'
     with open(skitemp, 'r') as f:
          filedata = f.read()

     # replacing items in the template ski file
     filedata = filedata.replace('"SOURCEFILE"', f'"{srcFile}"')
     filedata = filedata.replace('"GASFILE"', f'"{gasFile}"')
     filedata = filedata.replace('"XMIN"', f'"{x_min} pc"')
     filedata = filedata.replace('"XMAX"', f'"{x_max} pc"')
     filedata = filedata.replace('"YMIN"', f'"{y_min} pc"')
     filedata = filedata.replace('"YMAX"', f'"{y_max} pc"')
     filedata = filedata.replace('"ZMIN"', f'"{z_min} pc"')
     filedata = filedata.replace('"ZMAX"', f'"{z_max} pc"')

     # updating field of view based on new box size
     field_of_view_x = x_max - x_min
     field_of_view_y = y_max - y_min
     filedata = filedata.replace('"FOVX"', f'"{field_of_view_x} pc"')
     filedata = filedata.replace('"FOVY"', f'"{field_of_view_y} pc"')

     # write the new SKIRT config file
     skifile = filename + '.ski'
     with open(skifile, 'w') as f:
          f.write(filedata)

     return skifile