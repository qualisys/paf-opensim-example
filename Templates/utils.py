# Utility functions.
#
# author: Dimitar Stanev <jimstanev@gmail.com>
# https://github.com/mitkof6/opensim_automated_pipeline
##
import scipy.signal
import opensim
import numpy as np
import matplotlib.pyplot as plt # include this when generating plots to verify force filter

def rotate_data_table(table, axis, deg):
    """Rotate OpenSim::TimeSeriesTableVec3 entries using an axis and angle.

    Parameters
    ----------
    table: OpenSim.common.TimeSeriesTableVec3

    axis: 3x1 vector

    deg: angle in degrees

    """
    R = opensim.Rotation(np.deg2rad(deg),
                         opensim.Vec3(axis[0], axis[1], axis[2]))
    for i in range(table.getNumRows()):
        vec = table.getRowAtIndex(i)
        vec_rotated = R.multiply(vec)
        table.setRowAtIndex(i, vec_rotated)

def mm_to_m(table, label):
    """Scale from units in mm for units in m.

    Parameters
    ----------
    label: string containing the name of the column you want to convert

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
    """ 
    Given a signal, its sampling frequency in Hz and filter order

    return the filtered signal

    The defaul filter is a butterworth lowpass filter with given order, which gets applied twice
    """
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

    # validation (uncomment the next block and the figures will be exported in the session folder)
    # signal_val_np = np.zeros((n_frames, 3))
    # for i in range(n_frames):
    #     signal_val_np[i, 0] = signal[i][0]  # extract x component at each time step
    #     signal_val_np[i, 1] = signal[i][1]  # extract y component at each time step
    #     signal_val_np[i, 2] = signal[i][2]  # extract z component at each time step
    # temp = np.array(smooth_signal_list)
    # smooth_signal_np = temp.transpose()
    # plt.figure()
    # plt.plot(signal_val_np[:, 0], label='raw')
    # plt.ylabel(label)
    # plt.xlabel('sample')
    # plt.plot(smooth_signal_np[:, 0], label='filtered')
    # plt.legend()
    # plt.savefig(output_dir + '/{}_x.pdf'.format(label))

    # plt.figure()
    # plt.plot(signal_val_np[:, 1], label='raw')
    # plt.ylabel(label)
    # plt.xlabel('sample')
    # plt.plot(smooth_signal_np[:, 1], label='filtered')
    # plt.legend()
    # plt.savefig(output_dir + '/{}_y.pdf'.format(label))

    # plt.figure()
    # plt.plot(signal_val_np[:, 2], label='raw')
    # plt.ylabel(label)
    # plt.xlabel('sample')
    # plt.plot(smooth_signal_np[:, 2], label='filtered')
    # plt.legend()
    # plt.savefig(output_dir + '/{}_z.pdf'.format(label))
    # plt.close('all')

    return np.array(smooth_signal_list)

def create_opensim_storage(time, data, column_names):
    """Creates a OpenSim::Storage.

    Parameters
    ----------
    time: SimTK::Vector

    data: SimTK::Matrix

    column_names: list of strings

    Returns
    -------
    sto: OpenSim::Storage

    """
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