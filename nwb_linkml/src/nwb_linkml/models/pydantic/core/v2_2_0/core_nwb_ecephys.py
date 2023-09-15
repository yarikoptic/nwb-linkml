from __future__ import annotations
from datetime import datetime, date
from enum import Enum
from typing import List, Dict, Optional, Any, Union
from pydantic import BaseModel as BaseModel, Field
from nptyping import Shape, Float, Float32, Double, Float64, LongLong, Int64, Int, Int32, Int16, Short, Int8, UInt, UInt32, UInt16, UInt8, UInt64, Number, String, Unicode, Unicode, Unicode, String, Bool, Datetime64
from nwb_linkml.types import NDArray
import sys
if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


from .core_nwb_base import (
    NWBDataInterface,
    TimeSeriesSync,
    TimeSeriesStartingTime,
    TimeSeries,
    NWBContainer
)

from ...hdmf_common.v1_1_0.hdmf_common_table import (
    DynamicTableRegion,
    DynamicTable
)


metamodel_version = "None"
version = "2.2.0"

class ConfiguredBaseModel(BaseModel,
                validate_assignment = True,
                validate_default = True,
                extra = 'forbid',
                arbitrary_types_allowed = True,
                use_enum_values = True):
    pass


class ElectricalSeries(TimeSeries):
    """
    A time series of acquired voltage data from extracellular recordings. The data field is an int or float array storing data in volts. The first dimension should always represent time. The second dimension, if present, should represent channels.
    """
    name:str= Field(...)
    data:ElectricalSeriesData= Field(..., description="""Recorded voltage data.""")
    electrodes:ElectricalSeriesElectrodes= Field(..., description="""DynamicTableRegion pointer to the electrodes that this time series was generated from.""")
    channel_conversion:Optional[List[float]]= Field(default_factory=list, description="""Channel-specific conversion factor. Multiply the data in the 'data' dataset by these values along the channel axis (as indicated by axis attribute) AND by the global conversion factor in the 'conversion' attribute of 'data' to get the data values in Volts, i.e, data in Volts = data * data.conversion * channel_conversion. This approach allows for both global and per-channel data conversion factors needed to support the storage of electrical recordings as native values generated by data acquisition systems. If this dataset is not present, then there is no channel-specific conversion factor, i.e. it is 1 for all channels.""")
    description:Optional[str]= Field(None, description="""Description of the time series.""")
    comments:Optional[str]= Field(None, description="""Human-readable comments about the TimeSeries. This second descriptive field can be used to store additional information, or descriptive information if the primary description field is populated with a computer-readable string.""")
    starting_time:Optional[TimeSeriesStartingTime]= Field(None, description="""Timestamp of the first sample in seconds. When timestamps are uniformly spaced, the timestamp of the first sample can be specified and all subsequent ones calculated from the sampling rate attribute.""")
    timestamps:Optional[List[float]]= Field(default_factory=list, description="""Timestamps for samples stored in data, in seconds, relative to the common experiment master-clock stored in NWBFile.timestamps_reference_time.""")
    control:Optional[List[int]]= Field(default_factory=list, description="""Numerical labels that apply to each time point in data for the purpose of querying and slicing data by these values. If present, the length of this array should be the same size as the first dimension of data.""")
    control_description:Optional[List[str]]= Field(default_factory=list, description="""Description of each control value. Must be present if control is present. If present, control_description[0] should describe time points where control == 0.""")
    sync:Optional[TimeSeriesSync]= Field(None, description="""Lab-specific time and sync information as provided directly from hardware devices and that is necessary for aligning all acquired time information to a common timebase. The timestamp array stores time in the common timebase. This group will usually only be populated in TimeSeries that are stored external to the NWB file, in files storing raw data. Once timestamp data is calculated, the contents of 'sync' are mostly for archival purposes.""")
    

class ElectricalSeriesData(ConfiguredBaseModel):
    """
    Recorded voltage data.
    """
    name:Literal["data"]= Field("data")
    unit:Optional[str]= Field(None, description="""Base unit of measurement for working with the data. This value is fixed to 'volts'. Actual stored values are not necessarily stored in these units. To access the data in these units, multiply 'data' by 'conversion' and 'channel_conversion' (if present).""")
    array:Optional[Union[
        NDArray[Shape["* num_times"], Number],
        NDArray[Shape["* num_times, * num_channels"], Number],
        NDArray[Shape["* num_times, * num_channels, * num_samples"], Number]
    ]]= Field(None)
    

class ElectricalSeriesElectrodes(DynamicTableRegion):
    """
    DynamicTableRegion pointer to the electrodes that this time series was generated from.
    """
    name:Literal["electrodes"]= Field("electrodes")
    table:Optional[DynamicTable]= Field(None, description="""Reference to the DynamicTable object that this region applies to.""")
    description:Optional[str]= Field(None, description="""Description of what this table region points to.""")
    

class SpikeEventSeries(ElectricalSeries):
    """
    Stores snapshots/snippets of recorded spike events (i.e., threshold crossings). This may also be raw data, as reported by ephys hardware. If so, the TimeSeries::description field should describe how events were detected. All SpikeEventSeries should reside in a module (under EventWaveform interface) even if the spikes were reported and stored by hardware. All events span the same recording channels and store snapshots of equal duration. TimeSeries::data array structure: [num events] [num channels] [num samples] (or [num events] [num samples] for single electrode).
    """
    name:str= Field(...)
    data:SpikeEventSeriesData= Field(..., description="""Spike waveforms.""")
    timestamps:List[float]= Field(default_factory=list, description="""Timestamps for samples stored in data, in seconds, relative to the common experiment master-clock stored in NWBFile.timestamps_reference_time. Timestamps are required for the events. Unlike for TimeSeries, timestamps are required for SpikeEventSeries and are thus re-specified here.""")
    electrodes:ElectricalSeriesElectrodes= Field(..., description="""DynamicTableRegion pointer to the electrodes that this time series was generated from.""")
    channel_conversion:Optional[List[float]]= Field(default_factory=list, description="""Channel-specific conversion factor. Multiply the data in the 'data' dataset by these values along the channel axis (as indicated by axis attribute) AND by the global conversion factor in the 'conversion' attribute of 'data' to get the data values in Volts, i.e, data in Volts = data * data.conversion * channel_conversion. This approach allows for both global and per-channel data conversion factors needed to support the storage of electrical recordings as native values generated by data acquisition systems. If this dataset is not present, then there is no channel-specific conversion factor, i.e. it is 1 for all channels.""")
    description:Optional[str]= Field(None, description="""Description of the time series.""")
    comments:Optional[str]= Field(None, description="""Human-readable comments about the TimeSeries. This second descriptive field can be used to store additional information, or descriptive information if the primary description field is populated with a computer-readable string.""")
    starting_time:Optional[TimeSeriesStartingTime]= Field(None, description="""Timestamp of the first sample in seconds. When timestamps are uniformly spaced, the timestamp of the first sample can be specified and all subsequent ones calculated from the sampling rate attribute.""")
    control:Optional[List[int]]= Field(default_factory=list, description="""Numerical labels that apply to each time point in data for the purpose of querying and slicing data by these values. If present, the length of this array should be the same size as the first dimension of data.""")
    control_description:Optional[List[str]]= Field(default_factory=list, description="""Description of each control value. Must be present if control is present. If present, control_description[0] should describe time points where control == 0.""")
    sync:Optional[TimeSeriesSync]= Field(None, description="""Lab-specific time and sync information as provided directly from hardware devices and that is necessary for aligning all acquired time information to a common timebase. The timestamp array stores time in the common timebase. This group will usually only be populated in TimeSeries that are stored external to the NWB file, in files storing raw data. Once timestamp data is calculated, the contents of 'sync' are mostly for archival purposes.""")
    

class SpikeEventSeriesData(ConfiguredBaseModel):
    """
    Spike waveforms.
    """
    name:Literal["data"]= Field("data")
    unit:Optional[str]= Field(None, description="""Unit of measurement for waveforms, which is fixed to 'volts'.""")
    array:Optional[Union[
        NDArray[Shape["* num_events, * num_samples"], Number],
        NDArray[Shape["* num_events, * num_samples, * num_channels"], Number]
    ]]= Field(None)
    

class FeatureExtraction(NWBDataInterface):
    """
    Features, such as PC1 and PC2, that are extracted from signals stored in a SpikeEventSeries or other source.
    """
    name:str= Field(...)
    description:List[str]= Field(default_factory=list, description="""Description of features (eg, ''PC1'') for each of the extracted features.""")
    features:FeatureExtractionFeatures= Field(..., description="""Multi-dimensional array of features extracted from each event.""")
    times:List[float]= Field(default_factory=list, description="""Times of events that features correspond to (can be a link).""")
    electrodes:FeatureExtractionElectrodes= Field(..., description="""DynamicTableRegion pointer to the electrodes that this time series was generated from.""")
    

class FeatureExtractionFeatures(ConfiguredBaseModel):
    """
    Multi-dimensional array of features extracted from each event.
    """
    name:Literal["features"]= Field("features")
    array:Optional[NDArray[Shape["* num_events, * num_channels, * num_features"], Float32]]= Field(None)
    

class FeatureExtractionElectrodes(DynamicTableRegion):
    """
    DynamicTableRegion pointer to the electrodes that this time series was generated from.
    """
    name:Literal["electrodes"]= Field("electrodes")
    table:Optional[DynamicTable]= Field(None, description="""Reference to the DynamicTable object that this region applies to.""")
    description:Optional[str]= Field(None, description="""Description of what this table region points to.""")
    

class EventDetection(NWBDataInterface):
    """
    Detected spike events from voltage trace(s).
    """
    name:str= Field(...)
    detection_method:str= Field(..., description="""Description of how events were detected, such as voltage threshold, or dV/dT threshold, as well as relevant values.""")
    source_idx:List[int]= Field(default_factory=list, description="""Indices (zero-based) into source ElectricalSeries::data array corresponding to time of event. ''description'' should define what is meant by time of event (e.g., .25 ms before action potential peak, zero-crossing time, etc). The index points to each event from the raw data.""")
    times:List[float]= Field(default_factory=list, description="""Timestamps of events, in seconds.""")
    

class EventWaveform(NWBDataInterface):
    """
    Represents either the waveforms of detected events, as extracted from a raw data trace in /acquisition, or the event waveforms that were stored during experiment acquisition.
    """
    name:str= Field(...)
    spike_event_series:Optional[List[SpikeEventSeries]]= Field(default_factory=list, description="""SpikeEventSeries object(s) containing detected spike event waveforms.""")
    

class FilteredEphys(NWBDataInterface):
    """
    Electrophysiology data from one or more channels that has been subjected to filtering. Examples of filtered data include Theta and Gamma (LFP has its own interface). FilteredEphys modules publish an ElectricalSeries for each filtered channel or set of channels. The name of each ElectricalSeries is arbitrary but should be informative. The source of the filtered data, whether this is from analysis of another time series or as acquired by hardware, should be noted in each's TimeSeries::description field. There is no assumed 1::1 correspondence between filtered ephys signals and electrodes, as a single signal can apply to many nearby electrodes, and one electrode may have different filtered (e.g., theta and/or gamma) signals represented. Filter properties should be noted in the ElectricalSeries.
    """
    name:str= Field(...)
    electrical_series:List[ElectricalSeries]= Field(default_factory=list, description="""ElectricalSeries object(s) containing filtered electrophysiology data.""")
    

class LFP(NWBDataInterface):
    """
    LFP data from one or more channels. The electrode map in each published ElectricalSeries will identify which channels are providing LFP data. Filter properties should be noted in the ElectricalSeries description or comments field.
    """
    name:str= Field(...)
    electrical_series:List[ElectricalSeries]= Field(default_factory=list, description="""ElectricalSeries object(s) containing LFP data for one or more channels.""")
    

class ElectrodeGroup(NWBContainer):
    """
    A physical grouping of electrodes, e.g. a shank of an array.
    """
    name:str= Field(...)
    description:Optional[str]= Field(None, description="""Description of this electrode group.""")
    location:Optional[str]= Field(None, description="""Location of electrode group. Specify the area, layer, comments on estimation of area/layer, etc. Use standard atlas names for anatomical regions when possible.""")
    position:Optional[Any]= Field(None, description="""stereotaxic or common framework coordinates""")
    

class ClusterWaveforms(NWBDataInterface):
    """
    DEPRECATED The mean waveform shape, including standard deviation, of the different clusters. Ideally, the waveform analysis should be performed on data that is only high-pass filtered. This is a separate module because it is expected to require updating. For example, IMEC probes may require different storage requirements to store/display mean waveforms, requiring a new interface or an extension of this one.
    """
    name:str= Field(...)
    waveform_filtering:str= Field(..., description="""Filtering applied to data before generating mean/sd""")
    waveform_mean:ClusterWaveformsWaveformMean= Field(..., description="""The mean waveform for each cluster, using the same indices for each wave as cluster numbers in the associated Clustering module (i.e, cluster 3 is in array slot [3]). Waveforms corresponding to gaps in cluster sequence should be empty (e.g., zero- filled)""")
    waveform_sd:ClusterWaveformsWaveformSd= Field(..., description="""Stdev of waveforms for each cluster, using the same indices as in mean""")
    

class ClusterWaveformsWaveformMean(ConfiguredBaseModel):
    """
    The mean waveform for each cluster, using the same indices for each wave as cluster numbers in the associated Clustering module (i.e, cluster 3 is in array slot [3]). Waveforms corresponding to gaps in cluster sequence should be empty (e.g., zero- filled)
    """
    name:Literal["waveform_mean"]= Field("waveform_mean")
    array:Optional[NDArray[Shape["* num_clusters, * num_samples"], Float32]]= Field(None)
    

class ClusterWaveformsWaveformSd(ConfiguredBaseModel):
    """
    Stdev of waveforms for each cluster, using the same indices as in mean
    """
    name:Literal["waveform_sd"]= Field("waveform_sd")
    array:Optional[NDArray[Shape["* num_clusters, * num_samples"], Float32]]= Field(None)
    

class Clustering(NWBDataInterface):
    """
    DEPRECATED Clustered spike data, whether from automatic clustering tools (e.g., klustakwik) or as a result of manual sorting.
    """
    name:str= Field(...)
    description:str= Field(..., description="""Description of clusters or clustering, (e.g. cluster 0 is noise, clusters curated using Klusters, etc)""")
    num:List[int]= Field(default_factory=list, description="""Cluster number of each event""")
    peak_over_rms:List[float]= Field(default_factory=list, description="""Maximum ratio of waveform peak to RMS on any channel in the cluster (provides a basic clustering metric).""")
    times:List[float]= Field(default_factory=list, description="""Times of clustered events, in seconds. This may be a link to times field in associated FeatureExtraction module.""")
    


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
ElectricalSeries.model_rebuild()
ElectricalSeriesData.model_rebuild()
ElectricalSeriesElectrodes.model_rebuild()
SpikeEventSeries.model_rebuild()
SpikeEventSeriesData.model_rebuild()
FeatureExtraction.model_rebuild()
FeatureExtractionFeatures.model_rebuild()
FeatureExtractionElectrodes.model_rebuild()
EventDetection.model_rebuild()
EventWaveform.model_rebuild()
FilteredEphys.model_rebuild()
LFP.model_rebuild()
ElectrodeGroup.model_rebuild()
ClusterWaveforms.model_rebuild()
ClusterWaveformsWaveformMean.model_rebuild()
ClusterWaveformsWaveformSd.model_rebuild()
Clustering.model_rebuild()
    