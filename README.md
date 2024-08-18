# Depth vs Time Plotting with Custom Filter in ParaView

## Overview
This project involves a ParaView pipeline designed to visualize salinity data as a depth vs time plot. The pipeline has been saved as a custom filter named `CustomDepthTimePlot`, which allows for easy application to any NetCDF file. This README provides instructions on how to use the filter and a technical explanation of the code and its complexity.

## Pipeline in ParaView
The pipeline used to create the depth vs time plot consists of the following steps:
1. **NetCDF File**: The input dataset containing salinity data.
2. **Slice 1**: Cuts through the dataset at a specified plane.
3. **Slice 2**: Further slices the data to focus on the desired region i.e. slices the data again to get the data along a line.
4. **ExtractTimeSteps**: Extracts the time steps of interest from the dataset.
5. **GroupTimeSteps**: Groups the extracted time steps for processing.
6. **Programmable Filter**: Processes the data to create a `vtkRectilinearGrid` representing the depth vs time plot.

## Using the Custom Filter

The entire pipeline has been saved as a custom filter named `CustomDepthTimePlot`. This filter can be directly applied to a NetCDF file to generate the desired depth vs time plot.

### Steps to Load the Custom Filter into ParaView:

1. **Go to Tools**: Open ParaView and navigate to `Tools` in the menu bar.
2. **Manage Custom Filters**: Select `Manage Custom Filters...` from the dropdown menu.
3. **Import the Filter**: Click `Import...` and select the `CustomDepthTimePlot.cpd` file.
4. **Apply the Filter**: Once imported, select your NetCDF file in the pipeline, and choose the `CustomDepthTimePlot` filter to generate the plot.

## Define Inputs and Outputs
- **Input**: The input for the `CustomDepthTimePlot` filter is a NetCDF file containing salinity data across various time steps.
- **Output**: The output is a `vtkRectilinearGrid` representing the salinity values plotted against depth and time, which can be visualized directly in ParaView.

## Time and Space Complexity

- **Time Complexity**: The time complexity of the code is `O(n * m)`, where `n` is the number of partitions (time steps) and `m` is the number of depth points. The complexity arises from the need to process each depth point at each time step.

- **Space Complexity**: The space complexity is `O(n * m)`, due to storing the salinity values in a 2D array with dimensions corresponding to the number of time steps and depth points. This array is then used to populate the `vtkRectilinearGrid`.

## Conclusion
This custom filter simplifies the process of visualizing depth vs time plots in ParaView. By following the steps provided, you can easily import and apply the `CustomDepthTimePlot` filter to your NetCDF data, enabling quick and efficient analysis.

Feel free to explore and modify the custom filter to suit your specific needs!

<img width="1440" alt="Screenshot 2024-08-18 at 10 29 34 PM" src="https://github.com/user-attachments/assets/f580de01-e063-4b86-8e58-560f780210e6">

<img width="1440" alt="Screenshot 2024-08-19 at 2 36 07 AM" src="https://github.com/user-attachments/assets/b3348d9f-02c6-402d-af16-01e5d7c3f8c5">

![18 aug](https://github.com/user-attachments/assets/f34e0c2a-1c9a-493e-84b1-8f787fa56fba)

