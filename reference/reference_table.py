import vtk
import numpy as np
from paraview.vtk.util import numpy_support as ns
from paraview.simple import GetAnimationScene, Render

def RequestData():
    # Get the active source data object
    input_data = self.GetInputDataObject(0, 0)
    output = vtk.vtkTable()

    # Get the animation scene and time steps
    animationScene1 = GetAnimationScene()
    time_steps = animationScene1.TimeKeeper.TimestepValues
    num_time_steps = len(time_steps)
    print(f"Number of time steps: {num_time_steps}")

    # Initialize lists to store the consolidated data
    time_steps_list = []
    depths = []
    salinities = []

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

            # Convert VTK arrays to lists
            points_np = ns.vtk_to_numpy(points.GetData())
            salinity_np = ns.vtk_to_numpy(salinity_array)

            # Store the data in the lists
            for j in range(points.GetNumberOfPoints()):
                z = points_np[j][2]  # Assuming depth is along the z-axis
                salinity_value = salinity_np[j]
                time_steps_list.append(time_step_index)
                depths.append(z)
                salinities.append(salinity_value)

            print(f"Processed time step {time_step_index} with time value {time_value}")
        else:
            raise RuntimeError("Input data type not supported. Expected vtkPolyData.")

    # Create columns for the vtkTable
    time_array = ns.numpy_to_vtk(np.array(time_steps_list), deep=True, array_type=vtk.VTK_INT)
    depth_array = ns.numpy_to_vtk(np.array(depths), deep=True, array_type=vtk.VTK_FLOAT)
    salinity_array = ns.numpy_to_vtk(np.array(salinities), deep=True, array_type=vtk.VTK_FLOAT)

    # Set column names
    time_array.SetName("TimeStep")
    depth_array.SetName("Depth")
    salinity_array.SetName("Salinity")

    # Add columns to the vtkTable
    output.AddColumn(time_array)
    output.AddColumn(depth_array)
    output.AddColumn(salinity_array)

    # Set the output data object
    self.GetOutputDataObject(0).ShallowCopy(output)
    print("Set the output data object.")

try:
    RequestData()
except Exception as e:
    print(f"Error: {e}")
