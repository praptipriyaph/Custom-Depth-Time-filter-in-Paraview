# Depth vs. Time Analysis Using ParaView
This ParaView Programmable Filter script extracts data from a vtkPolyData dataset and maps it onto a vtkRectilinearGrid. It processes multiple time steps, extracts salinity values at various depths, and stores them in a 2D array to populate the vtkRectilinearGrid, which can then be visualized in ParaView.

## Functionality

- **Data Extraction:** The script extracts point coordinates and salinity values along a defined line from a `vtkPolyData` input over multiple time steps.
- **Grid Mapping:** The extracted data is organized into a 2D array, where the x-axis represents time and the y-axis represents depth.
- **Output Generation:** The 2D array is used to populate a `vtkRectilinearGrid`, which is ideal for generating depth vs. time plots in ParaView.

## ParaView Pipeline

To create a depth vs. time plot using this script in ParaView, use the following pipeline:

1. **NetCDF File:** The source dataset containing the necessary data arrays.
2. **Slice 1:** A slice filter to isolate a specific plane in the dataset.
3. **Slice 2:** Another slice filter, to further refine the region of interest - to get the data along a line.
4. **ExtractTimeSteps:** A filter that isolates data for specific time steps.
5. **GroupTimeSteps:** Combines data from different time steps into a single output.
6. **Programmable Filter:** This custom script processes the grouped time steps, extracting and mapping salinity values along the line onto a `vtkRectilinearGrid`.

## Script Details

The script operates as follows:

1. **Initialization:** Initializes lists to store depth coordinates and salinity values for each time step.
2. **Data Processing:** For each time step, it extracts salinity values along the line of interest, sorting them based on depth and storing them in the 2D array.
3. **Grid Construction:** Maps the time and depth indices to the 2D array, filling it with the extracted salinity values.
4. **Output:** The `vtkRectilinearGrid` is then set as the output, allowing for the creation of depth vs. time plots.

## Usage

To use this script for depth vs. time analysis in ParaView:

1. Set up the pipeline as described.
2. Load the NetCDF file containing the dataset.
3. Use the slice filters to define the line along which the analysis will be performed.
4. Apply the `ExtractTimeSteps` and `GroupTimeSteps` filters to manage the time dimension.
5. Use the Programmable Filter with this script to extract and visualize salinity changes over time and depth.

The final output is a `vtkRectilinearGrid`, perfect for generating depth vs. time plots that can reveal temporal and vertical patterns in salinity within the dataset. The `vtkRectilinearGrid` can be further analysed in Paraview using VTK. 

![18 aug](https://github.com/user-attachments/assets/7e7f6de1-ae15-451b-a3d0-e031e66794f3)
Depth Vs Salinity plot of BoB dataset


## Time and Space Complexity Analysis

### Time Complexity

1. **Partition Loop:** The script iterates over `num_partitions`, where each partition corresponds to a different time step. This results in a linear complexity of `O(P)`, where `P` is the number of partitions (time steps).

2. **Dataset Loop:** Within each partition, the script loops through `num_datasets`, which is usually a constant (often 1 in many cases), so the complexity is `O(D)` where `D` is the number of datasets per partition.

3. **Points Loop:** For each dataset, the script iterates through the points (`points.GetNumberOfPoints()`). The complexity for this loop is `O(N)`, where `N` is the number of points in the dataset.

4. **Overall Time Complexity:** The overall time complexity of the script is `O(P * D * N)`, where:
   - `P` is the number of partitions (time steps).
   - `D` is the number of datasets per partition.
   - `N` is the number of points in each dataset.

### Space Complexity

1. **Z-coordinates:** The space required to store `z_coords` is `O(M)`, where `M` is the number of unique z-coordinates (depth values).

2. **Data Arrays:** The space required to store the salinity data in `data_arrays` is `O(P * M)`, where:
   - `P` is the number of partitions (time steps).
   - `M` is the number of unique z-coordinates.

3. **Output Grid:** The output `vtkRectilinearGrid` has dimensions corresponding to the number of time steps and z-coordinates, resulting in a space complexity of `O(P * M)`.

4. **Overall Space Complexity:** The overall space complexity is `O(P * M)`, primarily due to storing the salinity data and the rectilinear grid output.

### Summary

- **Time Complexity:** `O(P * D * N)`
- **Space Complexity:** `O(P * M)`

Where `P` is the number of partitions (time steps), `D` is the number of datasets per partition, `N` is the number of points in each dataset, and `M` is the number of unique z-coordinates.
