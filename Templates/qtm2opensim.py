import os
import argparse
import scipy.signal
import opensim
import opensim as osim
import numpy as np

def convert_c3d(c3d_dir, c3d_file):

    FORCE_THRESHOLD = 10 # Force data will be set to zero if below threshold

    # Read c3d file
    adapter = osim.C3DFileAdapter()
    adapter.setLocationForForceExpression(1)
    tables = adapter.read(os.path.join(c3d_dir, c3d_file))

    # Get marker data from c3d file
    markers = adapter.getMarkersTable(tables)

    # Rotate marker data
    rotate_data_table(markers, [1, 0, 0], -90) # Assumes that z is pointing up vertically in QTM
        
    # Write marker data to .trc file
    trcAdapter = osim.TRCFileAdapter()
    trcAdapter.write(markers, os.path.join(c3d_dir, c3d_file.replace('.c3d','.trc')))
            
    # Get force data from c3d file
    forces = adapter.getForcesTable(tables)
    t = forces.getIndependentColumn()
    labels = forces.getColumnLabels()

    # create index of samples where force is below threshold
    numFPs = int(forces.getNumColumns()/3)
    r = len(t)
    below = np.full((numFPs,r), False)
    for fpID in range(numFPs):
        f = forces.getDependentColumn('f' + str(fpID + 1))
        fz = np.zeros(r)
        for i in range(r):
            fz[i] = f[i][2]
        below[fpID,:]=fz<FORCE_THRESHOLD

    # set force to zero where fz < threshold
    for i in range(r):
        vec = forces.getRowAtIndex(i)
        if below[0,i]:
            for j in range(3):
                vec[j]=osim.Vec3(0,0,0)
        if below[1,i]:
            for j in range(3,6):
                vec[j]=osim.Vec3(0,0,0)
        forces.setRowAtIndex(i,vec)

     # Rotate forces (Assumes that z is pointing up vertically in QTM)
    rotate_data_table(forces, [1, 0, 0], 90)
    rotate_data_table(forces, [0, 1, 0], 180)
    rotate_data_table(forces, [0, 0, 1], 180)

    # conversion of unit (f -> N, p -> mm, tau -> Nmm)
    mm_to_m(forces, 'p1')
    mm_to_m(forces, 'p2')
    mm_to_m(forces, 'm1')
    mm_to_m(forces, 'm2')

    # interpolate and fit splines to smooth the data
    list_mat = list()
    sample_rate = 1/(t[1]-t[0])
    for label in labels:
        f = forces.getDependentColumn(label)
        list_mat.append(lowpass_filter(f, label, sample_rate, order=2, cutoff=10, padtype="odd", output_dir=c3d_dir))

    # construct the matrix of the forces (forces, moments, torques / right and left)
    # (type opensim.Matrix)
    forces_task_np = np.array(list_mat)
    forces_task_mat = osim.Matrix(len(t), 18)
    for n in range(6):
        for j in range(3):
            for i in range(len(t)):
                forces_task_mat.set(i, 3 * n + j, forces_task_np[n, j, i])

    # export forces
    labels_list = ['ground_force_vx', 'ground_force_vy', 'ground_force_vz',
                'ground_force_px', 'ground_force_py', 'ground_force_pz',
                'ground_torque_x', 'ground_torque_y', 'ground_torque_z',
                '1_ground_force_vx', '1_ground_force_vy', '1_ground_force_vz',
                '1_ground_force_px', '1_ground_force_py', '1_ground_force_pz',
                '1_ground_torque_x', '1_ground_torque_y', '1_ground_torque_z']
    force_sto = create_opensim_storage(t, forces_task_mat, labels_list)
    force_sto.setName('GRF')
    force_sto.printResult(force_sto, c3d_file.replace('.c3d',''), c3d_dir, 0.001, '.mot')

def rotate_data_table(table, axis, deg):
    """
    Efficiently rotate data in an OpenSim Table.
    """
    R = opensim.Rotation(np.deg2rad(deg), opensim.Vec3(axis[0], axis[1], axis[2]))
    for i in range(table.getNumRows()):
        vec = table.getRowAtIndex(i)
        vec_rotated = R.multiply(vec)
        table.setRowAtIndex(i, vec_rotated)

def mm_to_m(table, label):
    """
    Convert measurements from millimeters to meters in an OpenSim Table.
    """
    c = table.updDependentColumn(label)
    for i in range(c.size()):
        c[i] = opensim.Vec3(c[i][0] * 0.001, c[i][1] * 0.001, c[i][2] * 0.001)

def get_valid_padlen(signal, A, B):
    """ if signal is too short the defaultpadlen needs to change in order for the scipy filtfilt to work with padding """
    padlen = 3 * max(len(A), len(B))  # from scipy default
    signal_length = len(signal)
    if signal_length <= padlen:
        padlen = signal_length - 1
    return padlen

def lowpass_filter(signal, label, sampling_freq, order=4, cutoff=12, padtype="odd", output_dir='.'):
     
    # instantiate variables
    n_frames = signal.nrow()
    signal_np = np.zeros((n_frames))
    smooth_signal_list = []
    # filter settings
    nyq = 0.5 * sampling_freq
    # The double filter should have 1/sqrt(2) transfer at cutoff, so we need correction for filter order
    cutoff = cutoff / (np.sqrt(2) - 1) ** (0.5 / order)
    Wn = cutoff / nyq
    B, A = scipy.signal.butter(order, Wn, output="ba")
    # convert Vec3 into np.array
    for i in range(3):
        for j in range(n_frames):
            signal_np[j] = signal[j][i]  # extract component at each time step
        
        # padding
        padlen = get_valid_padlen(signal_np, A, B)

        # smoothing
        smooth_signal_list.append(scipy.signal.filtfilt(B, A, signal_np, padtype=padtype, padlen=padlen))


    return np.array(smooth_signal_list)

def create_opensim_storage(time, data, column_names):

    sto = opensim.Storage()
    sto.setColumnLabels(list_to_osim_array_str(['time'] + column_names))
    for i in range(data.nrow()):
        row = opensim.ArrayDouble()
        for j in range(data.ncol()):
            row.append(data.get(i, j))

        sto.append(time[i], row)

    return sto

def list_to_osim_array_str(list_str):
    """Convert Python list of strings to OpenSim::Array<string>."""
    arr = opensim.ArrayStr()
    for element in list_str:
        arr.append(element)

    return arr
# start convert_c3d when running directly from command line


def main():
    parser = argparse.ArgumentParser(description="Process C3D files with OpenSim.")
    parser.add_argument('--c3d_dir', type=str, required=True, help="Directory containing C3D files")
    args = parser.parse_args()

    c3d_dir = args.c3d_dir

    # Your existing code to process C3D files
    for file_name in os.listdir(c3d_dir):
        if file_name.endswith('.c3d'):
            convert_c3d(c3d_dir, file_name)

# Ensure your existing functions like convert_c3d are included here

if __name__ == '__main__':
    main()