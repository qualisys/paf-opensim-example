# Qualisys PAF – OpenSim Example

## Getting Started
To download this example project to your computer, you can either:

* [Click here](https://github.com/qualisys/paf-opensim-example/archive/refs/heads/main.zip) to download it as a zip file.
<br>_— or —_
* Clone this repository to your computer.

## Video Tutorial
A video tutorial is available in the repository, providing an overview of how to use the PAF – OpenSim example.

## Preparing Qualisys Data for OpenSim Processing

> **Note:** QTM 2025.1 Update 1 introduces new export features for TRC (marker data) and STO (force data) files. Exports can now be performed directly within QTM and through any PAF modules. OpenSim models with Sport, CAST, and IOR marker sets are available in this repository at: `paf-opensim-example-main\Templates\OpenSim`

### Prerequisites
- Install QTM 2025.1 Update 1 or later from [Qualisys website](https://www.qualisys.com)

## Export Options

### Option 1: Export via PAF OpenSim Example
The PAF OpenSim example uses native QTM export functionality:

1. **Start QTM** and open the project 'PAF OpenSim Example'
2. **Create or navigate to data**:
   - Use the Project view (Ctrl+R) to create a person and session , or
   - Navigate to existing example files
3. **Capture or import** .qtm files, or use demo files
4. **Filter marker data** (recommended before export):
   - Open each measurement
   - Select all trajectories in the Labelled Trajectories list
   - Right-click and select **Smooth trajectory (Butterworth)**
   - To change filter frequency: Open Trajectory Editor → Modify Cutoff Frequency → Apply filter
5. **Generate export files**:
   - At session level: **Start Processing** → **Generate .trc and .sto**
   - This generates TRC and STO files for all QTM files in the session
6. **Locate exported files**:
   - Right-click session folder in QTM Project view
   - Select "Open folder in explorer"
   - Find .trc and .mot files

### Option 2: Single Export from QTM Trial
- Open a qtm trial then go to **File** → **Export** → **To TRC…** or **To STO…**

### Option 3: Batch Process Export
1. In QTM: **File** → **Batch Process…**
2. Navigate to folder with QTM files
3. Select multiple files using **Ctrl + click** → **Open**
4. Configure settings:
   - ✓ Enable: **Export to TRC file** and **Export to STO file**
   - ✗ Disable: **Auto-backup files before processing**, **Pre-process 2D data**, **Gap-fill the gaps**, **Track the measurements**
5. Press **OK**
6. Files are exported to same folder as QTM trials

## Using Exported Files in OpenSim

> **Note:** For detailed instructions or to use a different model, please refer to the [OpenSim documentation](https://simtk-confluence.stanford.edu/display/OpenSim).

### Step 1: Setup
1. Start **OpenSim 4.5**
2. Load OpenSim model:
   - Model location for different marker sets: `paf-opensim-example-main\Templates\OpenSim`
   - **File** → **Open Model** → Navigate to `gait2392_simbody_....osim`

### Step 2: Scale the Model
1. **Tools** → **Scale Model**
2. Click folder icon next to "Adjust Model Markers"
3. Navigate to your **Static TRC file** → **Open**
4. Click **Run**
5. Verify: Navigator tab shows new model with `...-scaled` suffix

> **Tip:** Check OpenSim documentation for additional scaling settings and marker fixation options to improve results.

### Step 3: Run Inverse Kinematics
1. **Tools** → **Inverse Kinematics**
2. Click folder icon next to highlighted field
3. Navigate to your **motion .trc file** → **Open**
4. Click **Run**
5. Verify: 
   - Skeleton moves in 3D viewer during processing
   - Navigator tab shows **IKResults**

### Step 4: Run Inverse Dynamics

#### 4.1 Configure External Loads
1. **Tools** → **Inverse Dynamics** → **External Loads** tab
2. Enable **External Loads** checkbox
3. Click note icon with pen
4. Select your **STO trial file**

#### 4.2 Setup Right Leg Forces
1. Click **Add**
2. Configure force parameters:
   - **Force Name**: `Right`
   - **Applied to**: `calcn_r`
3. Set **Force Columns** (assuming right leg on force plate 1, check in QTM for that trial):
   - Column 1: `1_ground_force_vx`
   - Column 2: `1_ground_force_vy`
   - Column 3: `1_ground_force_vz`
4. Set **Point Columns**:
   - Column 1: `1_ground_force_px`
   - Column 2: `1_ground_force_py`
   - Column 3: `1_ground_force_pz`
5. Enable **Applied Torque** and set:
   - Column 1: `1_ground_torque_x`
   - Column 2: `1_ground_torque_y`
   - Column 3: `1_ground_torque_z`

#### 4.3 Setup Left Leg Forces
- Repeat steps above using `2_ground...` prefixes
- **Applied to**: `calcn_l`

> **Important:** Force plate numbers vary based on which plate each foot strikes. Verify in your QTM trial.

#### 4.4 Complete Analysis
1. Click **Save** to save force configuration for the future use
2. Note the **Output directory** in Main Settings tab where you inverse dynamics results will be save as `inverse_dynamics.sto`
3. Click **Run**

#### 4.5 Plot Results
1. **Tools** → **Plot**
2. **Y-Quantity** → **Load File** → Select `inverse_dynamics.sto`
3. Select desired signals (for example ankle_angle_r_moment) → **OK**
4. **X-Quantity** → Select **Time**
5. In **Curves List**: Select figure → **Add**

## EMG in OpenSim

EMG analysis can be integrated with OpenSim. Reference example: [EMG-informed Computed Muscle Control for Dynamic Simulations of Movement](https://simtk.org/projects/emg).

## Additional Resources
- [OpenSim documentation](https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/overview)
- [Tutorial 3 - Scaling, Inverse Kinematics, and Inverse Dynamics](https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/pages/53089741/Tutorial+3+-+Scaling+Inverse+Kinematics+and+Inverse+Dynamics)

## Resources for Qualisys Project Automation Framework (PAF)

The ***Project Automation Framework*** (PAF) streamlines the motion capture process from data collection to final report. This repository demonstrates how PAF implements custom automated data collection in [Qualisys Track Manager (QTM)](http://www.qualisys.com/software/qualisys-track-manager/) and connects QTM to processing engines.

### PAF Documentation
Full documentation for PAF development: [PAF Documentation](https://github.com/qualisys/paf-documentation)

### PAF Examples
Official examples for various processing engines:

- [AnyBody](https://github.com/qualisys/paf-anybody-example)
- [Cleanse](https://github.com/qualisys/paf-cleanse-example)
- [Excel](https://github.com/qualisys/paf-excel-example)
- [Matlab](https://github.com/qualisys/paf-matlab-example)
- [OpenSim](https://github.com/qualisys/paf-opensim-example)
- [Python](https://github.com/qualisys/paf-python-example)
- [Theia Markerless](https://github.com/qualisys/paf-theia-markerless-example)
- [Theia Markerless Comparison](https://github.com/qualisys/paf-theia-markerless-comparison-example)
- [Theia Markerless True Hybrid](https://github.com/qualisys/paf-theia-markerless-true-hybrid-example)
- [Visual3D](https://github.com/qualisys/paf-visual3d-example)

---

> **License Note:** As of QTM version 2.17, official Qualisys PAF examples can be used without additional license. Advanced analysis types require "PAF Framework Developer kit" license (Article number 150300).
