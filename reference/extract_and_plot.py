#This script creates a CSV file by extracting time-varying salinity and depth data from a ParaView source, then reads the data and renders a scatter plot of salinity over time and depth in ParaView's Python View using Matplotlib.

import csv
import os
import numpy as np
import matplotlib.pyplot as plt
from paraview.simple import *
from paraview import python_view

# Function to create the CSV file from the source
def create_csv(output_directory, csv_file_name="salinity_data.csv"):
    try:
        print("Starting CSV creation process...")

        # Get the active source (assuming ExtractTimeSteps1 is already active)
        plotDataOverTime1 = GetActiveSource()
        if plotDataOverTime1 is None:
            print("Error: No active source found.")
            return None
        SetActiveSource(plotDataOverTime1)
        print("Active source set.")

        # Get the time information
        time_steps = plotDataOverTime1.TimestepValues
        if not time_steps:
            print("No time steps found in the data.")
            return None

        print(f"Found {len(time_steps)} time steps.")

        # Prepare to store data
        all_data = []

        # Loop through each time step
        for time_step_index, time_step_value in enumerate(time_steps):
            print(f"Processing time step {time_step_index + 1}/{len(time_steps)}: {time_step_value}")

            # Set the current time step
            plotDataOverTime1.UpdatePipeline(time_step_value)
            
            # Fetch data from the active source
            output_data = servermanager.Fetch(plotDataOverTime1)
            if output_data is None:
                print(f"Error: No output data for time step {time_step_index}.")
                continue
            
            # Extract 'so' and depth arrays
            salinity_array = output_data.GetPointData().GetArray("so")
            if not salinity_array:
                print(f"No salinity data found in time step {time_step_index}.")
                continue
            
            points = output_data.GetPoints()
            if not points:
                print(f"No point coordinates found in time step {time_step_index}.")
                continue
            
            # Convert VTK arrays to lists
            num_points = points.GetNumberOfPoints()
            for i in range(num_points):
                salinity_value = salinity_array.GetValue(i)
                depth_value = points.GetPoint(i)[2]  # Assuming depth is along the z-axis
                
                data_entry = {
                    "TimeStep": time_step_value,
                    "Depth": depth_value,
                    "so": salinity_value
                }
                all_data.append(data_entry)
            print(f"Time step {time_step_index + 1}: Processed {num_points} points.")

        # Create the CSV file
        csv_file_path = os.path.join(output_directory, csv_file_name)
        with open(csv_file_path, 'w', newline='') as csv_file:
            fieldnames = ["TimeStep", "Depth", "so"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_data)

        print(f"Data extraction complete. CSV file saved at: {csv_file_path}")
        return csv_file_path
    except Exception as e:
        print(f"Error during CSV creation: {e}")
        return None

# Function to read and process data from CSV
def read_csv_data(csv_path):
    try:
        print(f"Reading CSV data from: {csv_path}")
        time_steps = []
        depths = []
        salinity_values = []

        with open(csv_path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            for row in reader:
                time_steps.append(float(row[0]))
                depths.append(float(row[1]))
                salinity_values.append(float(row[2]))

        # Convert lists to numpy arrays
        time_steps = np.array(time_steps)
        depths = np.array(depths)
        salinity_values = np.array(salinity_values)

        print(f"Read {len(time_steps)} rows from CSV.")

        return time_steps, depths, salinity_values
    except Exception as e:
        print(f"Error reading CSV data: {e}")
        return None, None, None

# Function to render the plot in ParaView's Python View
def render_in_python_view(csv_path):
    try:
        print(f"Rendering plot in Python View with data from: {csv_path}")

        # Read data from CSV
        time_steps, depths, salinity_values = read_csv_data(csv_path)
        if time_steps is None or depths is None or salinity_values is None:
            print("Error: Failed to read CSV data.")
            return

        print("CSV data read successfully.")

        # Get the active Python view in ParaView
        view = GetActiveViewOrCreate('PythonView')
        if view is None:
            print("Error: No active Python View found.")
            return

        print("Active Python View set.")

        # Define the Python script for rendering
        script = f"""
import numpy as np
import matplotlib.pyplot as plt
from paraview import python_view

def setup_data(view):
    pass

def render(view, width, height):
    print("Rendering started.")
    # Create a figure and axes
    fig, ax = plt.subplots(figsize=(8, 6))  # Adjust size as needed

    # Create a scatter plot
    time_steps = np.array({time_steps.tolist()})
    depths = np.array({depths.tolist()})
    salinity_values = np.array({salinity_values.tolist()})

    scatter = ax.scatter(time_steps, depths, c=salinity_values, cmap='viridis', marker='.')
    fig.colorbar(scatter, label='Salinity (so)')
    ax.set_title('Scatter Plot of Salinity over Time and Depth')
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Depth')
    ax.invert_yaxis()  # Invert y-axis to have depth increasing downwards
    print("Rendering completed.")

    return python_view.figure_to_image(fig)
"""

        # Assign the script to the Python view and render
        view.Script = script
        Render()

        print("Rendering complete.")
    except Exception as e:
        print(f"Error during rendering: {e}")

# Path to the output directory
output_directory = '/home/toshit/Desktop/praptii'

# Create the CSV file
csv_file_path = create_csv(output_directory)

# If the CSV file was created successfully, render the plot
if csv_file_path:
    render_in_python_view(csv_file_path)
