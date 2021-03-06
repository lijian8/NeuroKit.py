# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

from .bio_ecg import *
from .bio_rsp import *
from .bio_eda import *
from .bio_emg import *


# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
def bio_process(ecg=None, rsp=None, eda=None, emg=None, sampling_rate=1000, age=None, sex=None, position=None, resampling_method="bfill", ecg_quality_model="default", hrv_segment_length=60, use_cvxEDA=True, add=None, emg_names=None, scr_min_amplitude=0.1):
    """
    Automated processing of bio signals. Wrapper for other bio processing functions.

    Parameters
    ----------
    ecg : list or array
        ECG signal array.
    rsp : list or array
        Respiratory signal array.
    eda :  list or array
        EDA signal array.
    emg :  list, array or DataFrame
        EMG signal array. Can include multiple channels.
    sampling_rate : int
        Sampling rate (samples/second).
    age : float
        Subject's age.
    sex : str
        Subject's gender ("m" or "f").
    position : str
        Recording position. To compare with data from Voss et al. (2015), use "supine".
    resampling_method : str
        "mean", "pad" or "bfill", the resampling method used for ECG and RSP heart rate.
    ecg_quality_model : str
        Path to model used to check signal quality. "default" uses the builtin model.
    hrv_segment_length : int
        Number of RR intervals within each sliding window on which to compute frequency-domains power. Particularly important for VLF. Adjust with caution.
    use_cvxEDA : bool
        Use convex optimization (CVXEDA) described in "cvxEDA: a Convex Optimization Approach to Electrodermal Activity Processing" (Greco et al., 2015).
    add : pandas.DataFrame
        Dataframe or channels to add by concatenation to the processed dataframe.
    emg_names : list
        List of EMG channel names.
    scr_min_amplitude : float
        Minimum treshold by which to exclude Skin Conductance Responses (SCRs).

    Returns
    ----------
    processed_bio : dict
        Dict containing processed bio features.

        Contains the ECG raw signal, the filtered signal, the R peaks indexes, HRV characteristics, all the heartbeats, the Heart Rate, and the RSP filtered signal (if respiration provided), respiratory sinus arrhythmia (RSA) features, the EDA raw signal, the filtered signal, the phasic component (if cvxEDA is True), the SCR onsets, peak indexes and amplitudes, the EMG raw signal, the filtered signal and pulse onsets.



    Example
    ----------
    >>> import neurokit as nk
    >>>
    >>> bio_features = nk.bio_process(ecg=ecg_signal, rsp=ecg_signal, eda=eda_signal)

    Notes
    ----------
    *Details*

    - **ECG Features**: See :func:`neurokit.ecg_process()`.
    - **EDA Features**: See :func:`neurokit.eda_process()`.
    - **RSP Features**: See :func:`neurokit.rsp_process()`.
    - **EMG Features**: See :func:`neurokit.emg_process()`.


    *Authors*

    - Dominique Makowski (https://github.com/DominiqueMakowski)

    *Dependencies*

    - pandas

    *See Also*

    - BioSPPY: https://github.com/PIA-Group/BioSPPy
    - hrv: https://github.com/rhenanbartels/hrv
    - cvxEDA: https://github.com/lciti/cvxEDA

    References
    -----------
    - Heart rate variability. (1996). Standards of measurement, physiological interpretation, and clinical use. Task Force of the European Society of Cardiology and the North American Society of Pacing and Electrophysiology. Eur Heart J, 17, 354-381.
    - Voss, A., Schroeder, R., Heitmann, A., Peters, A., & Perz, S. (2015). Short-term heart rate variability—influence of gender and age in healthy subjects. PloS one, 10(3), e0118308.
    - Greco, A., Valenza, G., & Scilingo, E. P. (2016). Evaluation of CDA and CvxEDA Models. In Advances in Electrodermal Activity Processing with Applications for Mental Health (pp. 35-43). Springer International Publishing.
    - Greco, A., Valenza, G., Lanata, A., Scilingo, E. P., & Citi, L. (2016). cvxEDA: A convex optimization approach to electrodermal activity processing. IEEE Transactions on Biomedical Engineering, 63(4), 797-804.
    - Zohar, A. H., Cloninger, C. R., & McCraty, R. (2013). Personality and heart rate variability: exploring pathways from personality to cardiac coherence and health. Open Journal of Social Sciences, 1(06), 32.
    - Smith, A. L., Owen, H., & Reynolds, K. J. (2013). Heart rate variability indices for very short-term (30 beat) analysis. Part 2: validation. Journal of clinical monitoring and computing, 27(5), 577-585.
    - Azevedo, R. T., Garfinkel, S. N., Critchley, H. D., & Tsakiris, M. (2017). Cardiac afferent activity modulates the expression of racial stereotypes. Nature communications, 8.
    - Edwards, L., Ring, C., McIntyre, D., & Carroll, D. (2001). Modulation of the human nociceptive flexion reflex across the cardiac cycle. Psychophysiology, 38(4), 712-718.
    - Gray, M. A., Rylander, K., Harrison, N. A., Wallin, B. G., & Critchley, H. D. (2009). Following one's heart: cardiac rhythms gate central initiation of sympathetic reflexes. Journal of Neuroscience, 29(6), 1817-1825.
    """
    processed_bio = {}
    bio_df = pd.DataFrame({})

    # ECG & RSP
    if ecg is not None:
        ecg = ecg_process(ecg=ecg, rsp=rsp, sampling_rate=sampling_rate, resampling_method=resampling_method, quality_model=ecg_quality_model, hrv_segment_length=hrv_segment_length, age=age, sex=sex, position=position)
        processed_bio["ECG"] = ecg["ECG"]
        if rsp is not None:
            processed_bio["RSP"] = ecg["RSP"]
        bio_df = pd.concat([bio_df, ecg["df"]], axis=1)

    if rsp is not None and ecg is None:
        rsp = rsp_process(rsp=rsp, sampling_rate=sampling_rate, resampling_method=resampling_method)
        processed_bio["RSP"] = rsp["RSP"]
        bio_df = pd.concat([bio_df, rsp["df"]], axis=1)


    # EDA
    if eda is not None:
        eda = eda_process(eda=eda, sampling_rate=sampling_rate, use_cvxEDA=use_cvxEDA, scr_min_amplitude=scr_min_amplitude)
        processed_bio["EDA"] = eda["EDA"]
        bio_df = pd.concat([bio_df, eda["df"]], axis=1)

    # EMG
    if emg is not None:
        emg = emg_process(emg=emg, sampling_rate=sampling_rate, emg_names=emg_names)
        bio_df = pd.concat([bio_df, emg.pop("df")], axis=1)
        for i in emg:
            processed_bio[i] = emg[i]


    if add is not None:
        add = add.reset_index(drop=True)
        bio_df = pd.concat([bio_df, add], axis=1)
    processed_bio["df"] = bio_df

    return(processed_bio)



# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
def bio_ERP(epoch, event_length, sampling_rate=1000, window_post=4):
    """
    Extract event-related bio (EDA, ECG and RSP) changes.

    Parameters
    ----------
    epoch : pandas.DataFrame
        An epoch contains in the epochs dict returned by :function:`neurokit.create_epochs()` on dataframe returned by :function:`neurokit.bio_process()`.
    event_length : int
        In seconds.
    sampling_rate : int
        Sampling rate (samples/second).
    window_post : float
        Post-stimulus window size (in seconds) to include eventual responses (usually 3 or 4).

    Returns
    ----------
    RSP_Response : dict
        Event-locked bio response features.

    Example
    ----------
    >>> import neurokit as nk
    >>> bio = nk.bio_process(RSP=df["RSP"], add=df["Photosensor"])
    >>> df = bio["df"]
    >>> events = nk.find_events(df["Photosensor"], cut="lower")
    >>> epochs = nk.create_epochs(df, events["onsets"], duration=events["durations"]+8000, onset=-4000)
    >>> for epoch in epochs:
    >>>     bio_response = nk.bio_ERP(epoch, event_length=4000)

    Notes
    ----------
    *Details*

    - **ECG Features**

        - **Heart_Rate_Baseline**: mean HR before stimulus onset.
        - **Heart_Rate_Min**: Min HR after stimulus onset.
        - **Heart_Rate_MinDiff**: HR mininum - baseline.
        - **Heart_Rate_MinTime**: Time of minimum.
        - **Heart_Rate_Max**: Max HR after stimulus onset.
        - **Heart_Rate_MaxDiff**: Max HR - baseline.
        - **Heart_Rate_MaxTime**: Time of maximum.
        - **Heart_Rate_Mean**: Mean HR after stimulus onset.
        - **Heart_Rate_MeanDiff**: Mean HR - baseline.
        - **Cardiac_Systole**: Cardiac phase on stimulus onset (1 = systole, 0 = diastole).
        - **Cardiac_Systole_Completion**: Percentage of cardiac phase completion on simulus onset.
        - **HRV**: Returns HRV features. See :func:`neurokit.ecg_hrv()`.
        - **HRV_Diff**: HRV post-stimulus - HRV pre-stimulus.
    - **Respiration Features**

        - **RSP_Rate_Baseline**: mean RSP Rate before stimulus onset.
        - **RSP_Rate_Min**: Min RSP Rate after stimulus onset.
        - **RSP_Rate_MinDiff**: RSP Rate mininum - baseline.
        - **RSP_Rate_MinTime**: Time of minimum.
        - **RSP_Rate_Max**: Max RSP Rate after stimulus onset.
        - **RSP_Rate_MaxDiff**: Max RSP Rate - baseline.
        - **RSP_Rate_MaxTime**: Time of maximum.
        - **RSP_Rate_Mean**: Mean RSP Rate after stimulus onset.
        - **RSP_Rate_MeanDiff**: Mean RSP Rate - baseline.
        - **RSP_Min**: Value in standart deviation (normalized by baseline) of the lowest point.
        - **RSP_MinTime**: Time of RSP Min.
        - **RSP_Max**: Value in standart deviation (normalized by baseline) of the highest point.
        - **RSP_MaxTime**: Time of RSP Max.
        - **RSP_Inspiration**: Respiration phase on stimulus onset (1 = inspiration, 0 = expiration).
        - **RSP_Inspiration_Completion**: Percentage of respiration phase on stimulus onset.
        - **RSP_Cycle_Length**: Mean duration of RSP cycles (inspiration and expiration) after stimulus onset.
        - **RSP_Cycle_Length_Baseline**: Mean duration of RSP cycles (inspiration and expiration) before stimulus onset.
        - **RSP_Cycle_LengthDiff**: mean cycle length after - mean cycle length before stimulus onset.
    - **EDA Features**
        - **Looking for help**: *Experimental*: respiration artifacts correction needs to be implemented.
        - **EDA_Peak**: Max of EDA (in a window starting 1s after the stim onset) minus baseline.
        - **SCR_Amplitude**: Peak of SCR. If no SCR, returns NA.
        - **SCR_Magnitude**: Peak of SCR. If no SCR, returns 0.
        - **SCR_Amplitude_Log**: log of 1+amplitude.
        - **SCR_Magnitude_Log**: log of 1+magnitude.
        - **SCR_PeakTime**: Time of peak.
        - **SCR_Latency**: Time between stim onset and SCR onset.
        - **SCR_RiseTime**: Time between SCR onset and peak.
        - **SCR_Strength**: *Experimental*: peak divided by latency.


    *Authors*

    - Dominique Makowski (https://github.com/DominiqueMakowski)

    *Dependencies*

    - numpy
    - pandas

    *See Also*

    References
    -----------
    - Gomez, P., Stahel, W. A., & Danuser, B. (2004). Respiratory responses during affective picture viewing. Biological Psychology, 67(3), 359-373.
    - Schneider, R., Schmidt, S., Binder, M., Schäfer, F., & Walach, H. (2003). Respiration-related artifacts in EDA recordings: introducing a standardized method to overcome multiple interpretations. Psychological reports, 93(3), 907-920.
    """
    bio_response = {}
    if "ECG_Filtered" in epoch.columns:
        ECG_Response = ecg_ERP(epoch, event_length, sampling_rate, window_post)
        bio_response.update(ECG_Response)
    if "RSP_Filtered" in epoch.columns:
        RSP_Response = rsp_ERP(epoch, event_length, sampling_rate, window_post)
        bio_response.update(RSP_Response)
    if "EDA_Filtered" in epoch.columns:
        EDA_Response = eda_ERP(epoch, event_length, sampling_rate, window_post)
        bio_response.update(EDA_Response)

    return(bio_response)