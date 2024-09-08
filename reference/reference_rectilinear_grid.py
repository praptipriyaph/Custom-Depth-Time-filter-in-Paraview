import vtk
import numpy as np
from paraview.vtk.util import numpy_support as ns
from paraview.simple import GetAnimationScene, Render

def RequestData():
    # Get the active source data object
    input_data = self.GetInputDataObject(0, 0)
    output = vtk.vtkRectilinearGrid()

    # Get the animation scene and time steps
    animationScene1 = GetAnimationScene()
    time_steps = animationScene1.TimeKeeper.TimestepValues
    num_time_steps = len(time_steps)
    print(f"Number of time steps: {num_time_steps}")

    # Initialize lists to store the consolidated data
    z_coords = []
    data_arrays = {}

    # Loop through each time step
    for time_step_index in range(num_time_steps):
        # Set the current time step
        time_value = time_steps[time_step_index]
        animationScene1.TimeKeeper.Time = time_value
        Render()  # Update the view to reflect the current time step

        # Fetch the data from the active source
        input_data = self.GetInputDataObject(0, 0)

        # Ensure the input data is vtkPolyData
        if isinstance(input_data, vtk.vtkPolyData):
            # Extract the 'so' array and point coordinates
            points = input_data.GetPoints()
            point_data = input_data.GetPointData()
            salinity_array = point_data.GetArray('so')

            # Check for data presence
            if salinity_array is None or points is None:
                print(f"Warning: No salinity data or points found at time step {time_step_index}")
                continue

            # Convert VTK arrays to numpy arrays
            points_np = ns.vtk_to_numpy(points.GetData())
            salinity_np = ns.vtk_to_numpy(salinity_array)

            # Store the z-coordinates
            if len(z_coords) == 0:
                z_coords = np.unique(points_np[:, 2])

            # Initialize data array storage if not already done
            if 'Salinity' not in data_arrays:
                data_arrays['Salinity'] = np.zeros((num_time_steps, len(z_coords)))

            # Store salinity values for the current time step
            for j in range(points.GetNumberOfPoints()):
                z = points_np[j][2]  # Assuming depth is along the z-axis
                salinity_value = salinity_np[j]
                z_index = np.where(z_coords == z)[0][0]
                data_arrays['Salinity'][time_step_index, z_index] = salinity_value

            print(f"Processed time step {time_step_index} with time value {time_value}")
        else:
            raise RuntimeError("Input data type not supported. Expected vtkPolyData.")

    # Convert lists to numpy arrays
    time_indices = np.arange(num_time_steps)
    z_indices = np.arange(len(z_coords))

    # Create vtkFloatArray for coordinates
    x_vtk_array = ns.numpy_to_vtk(time_indices, deep=True, array_type=vtk.VTK_FLOAT)
    x_vtk_array.SetName("TimeIndices")

    y_vtk_array = ns.numpy_to_vtk(z_indices, deep=True, array_type=vtk.VTK_FLOAT)
    y_vtk_array.SetName("ZIndices")

    # Set coordinates for vtkRectilinearGrid
    output.SetDimensions(len(time_indices), len(z_indices), 1)  # 1 in the z-dimension
    output.SetXCoordinates(x_vtk_array)
    output.SetYCoordinates(y_vtk_array)
    output.SetZCoordinates(ns.numpy_to_vtk(np.zeros(1), deep=True, array_type=vtk.VTK_FLOAT))  # Single plane for 2D

    # Add data arrays to vtkRectilinearGrid
    for name, array in data_arrays.items():
        flattened_array = array.flatten()
        vtk_data_array = ns.numpy_to_vtk(flattened_array, deep=True, array_type=vtk.VTK_FLOAT)
        vtk_data_array.SetName(name)
        output.GetPointData().AddArray(vtk_data_array)
        print(f"Added '{name}' to vtkRectilinearGrid.")

    # Set the output data object
    self.GetOutputDataObject(0).ShallowCopy(output)
    print("Set the output data object.")

try:
    RequestData()
except Exception as e:
    print(f"Error: {e}")
