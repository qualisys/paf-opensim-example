# Qualisys PAF – OpenSim example

## Getting started
To download this example project to your computer, you can either:

* [Click here](https://github.com/qualisys/paf-opensim-example/archive/refs/heads/main.zip) to download it as a zip file.
<br>_— or —_
* Clone this repository to your computer.


## Video Tutorial
A video tutorial is available in the repository, providing an overview of how to use the PAF – OpenSim example. Please note, the video may become outdated in the future, but it still offers useful guidance if you encounter complications while converting *.c3d files to *.trc and *.mot files.

## Preparing Qualisys Data for OpenSim Processing
### Preparation
1. Install Miniconda from [here](https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe).
 - During installation, ensure to check 'Add Miniconda3 to my PATH environment variable'.
 > **Note:** If any other Python versions are installed in the future and added to the PATH list, which can shift Miniconda3's position in the list not to be the first, it may cause issues with activating environments. To resolve this, open the PATH list, move Miniconda3 to the first position, and then restart QTM. Or use manual conversion as described in the section 'Converting files from Anaconda Prompt' below.
2. Install the opensim-example environment and libraries:
 - Open the Anaconda Prompt (miniconda3) by pressing start and typing `miniconda`.
 - Navigate to your downloaded `paf-opensim-example` project folder, where the `environment.yml` file is located.
 - Change to the project directory in Anaconda Prompt (miniconda3) by typing:
```
cd "path to your paf-opensim-example project"
```
 - Prepare the environment and install all required libraries by running:
```
conda env create -f environment.yml
```
3. Test the installation by activating the environment and trying to import OpenSim:
 ```
 conda activate opensim_example
 ```
 and then
 ```
 python -c "import opensim"
 ```
  If there is no error, the installation was successful. Close the Anaconda Prompt (miniconda3) window.

4. Re-start QTM in case it is open

### Converting files using QTM Project Automation Framework
1. Start QTM and open the project 'OpenSim Example' in QTM
2. Use the Project view in QTM (Ctrl+R) to create a person and session or navigate to example files.
3. Capture or import .qtm files, or use demo files.
4. Make sure Project Options -> C3D Export -> Zero Force Baseline is activated
2. It is recommended to filter marker data prior to exporting it:
   1. Open each measurement
   2. Select all trajectories in the Labelled Trajectories list
   3. Right-click and select Smooth trajectory (Butterworth)
   4. To change the filter frequency, open the Trajectory Editor and change the Cutoff Frequency before applying the filter
3. Click Start Processing to run the Generate .trc and .mot Analysis.
4. Right-click the session folder in the QTM Project view, select "Open folder in explorer" and locate .trc and .mot files.
5. If the files are not generated, run the processing from the command line to get full error outputs (see next section).

### Converting files from Anaconda Prompt
An alternative way is converting *.c3d files from Anaconda Prompt (miniconda3).

#### Step 1: Activate the OpenSim-Example Environment
1. Open the Anaconda Prompt (miniconda3).
2. Activate the OpenSim-Example environment by running:
````
conda activate opensim_example
````
3. In Anaconda Prompt (miniconda3) navigate to the Templates folder where the python script qtm2opensim.py is located by typing
````
cd "path to your Templates folder in paf-opensim-example project"
````
4. Then you can run qtm2opensim.py script and add the path where your *.c3d files to convert them to trc and mot files. To do that run in Anaconda Prompt (miniconda3) this command:
````
python qtm2opensim.py --c3d_dir "add path here where your c3d files located"
````

### Using the exported files in OpenSim
For detailed instructions or if you would like to use a different model, please refer to the OpenSim documentation.
1. Start OpenSim
2. Review data for one of the measurements:
   1. Select File -> Preview Experimental Data and load .trc file (marker data)
   2. Repeat for .mot file (force data)
   3. Extend the ExperimentalData nodes, use Ctrl+click to select .trc and .mot data and select Sync motions
   4. Play files to confirm that marker and force data are aligned as expected.
   5. OpenSim 4.4 will offset the forces and markers in the Visualizer window so that they are not on top of each other. This display offset is a display only property. The model itself is never affected by the changes to the display offset but you can remove this offset by right-clicking on the second ExperimentalData node then select Display -> Model Offset 
   6. Note: to change the orientation of the data, you can modify the settings for rotate_data_table in qtm2opensim.py
3. Use data in OpenSim:
   1. Use File -> Open Model and load the example models from OpenSim Example\Templates\OpenSim. Examples for CAST and IOR marker sets are included.
   2. Select Tools -> Scale model:
      1. Enter the subject's mass
      2. Check the box *Marker data for measurements* and select the .trc file for the static trial
      3. Check the box *Adjust Model markers* and sekect the .trc for the static trial
      4. Adjust Scale Factors and Static Pose Weights as desired
      5. Click Run
      6. You can now right-click and close the original model and use the -scaled model instead
   3. Select Tools -> Inverse Kinematics
      1. Load .trc file for dynamic file
      2. Adjust weights as desired
      3. Click Run
   4. Select Tools -> Inverse Dynamics
      1. In the *Main settings* tab, select *Loaded Motion* and choose *IKResults*. Check the *Filter coordinates* box and enter a cutoff frequency for your kinematic data.  
      Note or change the path of the *Output* directory where the results of the Inverse Dynamics step are written
      2. In the *External Loads* tab, click on the edit icon to open the External Forces window
      3. Load the .mot file in *Force data file*
      4. Click on *Add...* and enter a name for the right foot force assignment, ie "Right", and select *calcn_r* in the list of segments next to *Applied to*. Check *Applies Force* (*Point Force*) and *Applies Torque*. In the various drop downs, select the components ('_v' suffix components for Force, '_p' suffix components for Point and '_torque' suffix components for Torque) of the correct force plate that is in contact with the right foot. Click on *OK*
      5. Replicate the previous step for the left foot force assignment (use *calcn_l*)
      6. Click on *Save* to save your external forces setup
      7. Save your Inverse Dynamics Tool setup (optional) and click on Run
      8. You can now plot results of your Inverse Dynamics procedure by going to Tools -> Plot. Click on *Y-Quantity* and *Load File* to select the inverse_dynamics.sto output file that contains the results of the Inverse Dynamics step (path set in the *Main settings* tab). Select the signals you want to plot and click *OK*. Click on *X_Quantity* and select *Time*. Finally click on your figure in the *Curves List* and then click on *Add* to see the curve in the graph
      9. For more details please refer to the OpenSim documentation, for example https://simtk-confluence.stanford.edu/display/OpenSim/How+to+Use+the+Inverse+Dynamics+Tool and https://simtk-confluence.stanford.edu/display/OpenSim/Tutorial+3+-+Scaling%2C+Inverse+Kinematics%2C+and+Inverse+Dynamics

## Resources for using the Qualisys Project Automation Framework (PAF)

The purpose of the ***Project Automation Framework*** (PAF) is to streamline the motion capture process from data collection to the final report. This repository contains an example project that illustrate how PAF can be used to implement custom automated data collection in [Qualisys Track Manager (QTM)](http://www.qualisys.com/software/qualisys-track-manager/), and how QTM can be connected to a processing engine. 

### PAF Documentation

The full documentation for PAF development is available here: [PAF Documentation](https://github.com/qualisys/paf-documentation).


### PAF Examples

Our official examples for various processing engines:

- [Excel](https://github.com/qualisys/paf-excel-example)
- [Matlab](https://github.com/qualisys/paf-matlab-example)
- [OpenSim](https://github.com/qualisys/paf-opensim-example)
- [Python](https://github.com/qualisys/paf-python-example)
- [Theia Markerless](https://github.com/qualisys/paf-theia-markerless-example)
- [Theia Markerless Comparison](https://github.com/qualisys/paf-theia-markerless-comparison-example)
- [Theia Markerless True Hybrid](https://github.com/qualisys/paf-theia-markerless-true-hybrid-example)
- [Visual3D](https://github.com/qualisys/paf-visual3d-example)


### EMG in OpenSim

The EMG analysis can be added into OpenSim. For reference, there is an example repository with EMG analysis: [EMG-informed Computed Muscle Control for Dynamic Simulations of Movement]( https://simtk.org/projects/emg). To get an idea of the EMG format and data, you can examine the file  walk2EMG_filtered_normCMC.sto .
Following the repository's guidelines, the basic steps to prepare a .sto file with EMG data: use the latest PAF OpenSim example, after generating the .mot and .trc files the EMG data will also be exported in the TSV format, normalize the EMG signal, filter the EMG signal, organize the data in the proper sequence, ensuring headers are correctly set in a TXT file and save it as an .sto file extension.


_As of QTM version 2.17, the official Qualisys PAF examples can be used without any additional license. Note that some more advanced analysis types require a license for the "PAF Framework Developer kit" (Article number 150300)._
