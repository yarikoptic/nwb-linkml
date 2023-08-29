from __future__ import annotations
from datetime import datetime, date
from enum import Enum
from typing import List, Dict, Optional, Any, Union
from pydantic import BaseModel as BaseModel, Field
from nptyping import NDArray, Shape, Float, Float32, Double, Float64, LongLong, Int64, Int, Int32, Int16, Short, Int8, UInt, UInt32, UInt16, UInt8, UInt64, Number, String, Unicode, Unicode, Unicode, String, Bool, Datetime64
import sys
if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


from .hdmf_common_table import (
    DynamicTableRegion,
    DynamicTable,
    VectorIndex,
    VectorData
)

from .nwb_language import (
    Arraylike
)


metamodel_version = "None"
version = "None"

class WeakRefShimBaseModel(BaseModel):
   __slots__ = '__weakref__'

class ConfiguredBaseModel(WeakRefShimBaseModel,
                validate_assignment = True,
                validate_all = True,
                underscore_attrs_are_private = True,
                extra = 'forbid',
                arbitrary_types_allowed = True,
                use_enum_values = True):
    pass


class AbstractFeatureSeriesData(ConfiguredBaseModel):
    """
    Values of each feature at each time.
    """
    unit: Optional[str] = Field(None, description="""Since there can be different units for different features, store the units in 'feature_units'. The default value for this attribute is \"see 'feature_units'\".""")
    array: Optional[NDArray[Shape["* num_times, * num_features"], Number]] = Field(None)
    

class AbstractFeatureSeriesDataArray(Arraylike):
    
    num_times: float = Field(...)
    num_features: Optional[float] = Field(None)
    

class AbstractFeatureSeriesFeatureUnits(ConfiguredBaseModel):
    """
    Units of each feature.
    """
    feature_units: Optional[List[str]] = Field(default_factory=list, description="""Units of each feature.""")
    

class AbstractFeatureSeriesFeatures(ConfiguredBaseModel):
    """
    Description of the features represented in TimeSeries::data.
    """
    features: List[str] = Field(default_factory=list, description="""Description of the features represented in TimeSeries::data.""")
    

class AnnotationSeriesData(ConfiguredBaseModel):
    """
    Annotations made during an experiment.
    """
    resolution: Optional[float] = Field(None, description="""Smallest meaningful difference between values in data. Annotations have no units, so the value is fixed to -1.0.""")
    unit: Optional[str] = Field(None, description="""Base unit of measurement for working with the data. Annotations have no units, so the value is fixed to 'n/a'.""")
    data: List[str] = Field(default_factory=list, description="""Annotations made during an experiment.""")
    

class IntervalSeriesData(ConfiguredBaseModel):
    """
    Use values >0 if interval started, <0 if interval ended.
    """
    resolution: Optional[float] = Field(None, description="""Smallest meaningful difference between values in data. Annotations have no units, so the value is fixed to -1.0.""")
    unit: Optional[str] = Field(None, description="""Base unit of measurement for working with the data. Annotations have no units, so the value is fixed to 'n/a'.""")
    data: List[int] = Field(default_factory=list, description="""Use values >0 if interval started, <0 if interval ended.""")
    

class DecompositionSeriesData(ConfiguredBaseModel):
    """
    Data decomposed into frequency bands.
    """
    unit: Optional[str] = Field(None, description="""Base unit of measurement for working with the data. Actual stored values are not necessarily stored in these units. To access the data in these units, multiply 'data' by 'conversion'.""")
    array: Optional[NDArray[Shape["* num_times, * num_channels, * num_bands"], Number]] = Field(None)
    

class DecompositionSeriesDataArray(Arraylike):
    
    num_times: Optional[float] = Field(None)
    num_channels: Optional[float] = Field(None)
    num_bands: Optional[float] = Field(None)
    

class DecompositionSeriesSourceChannels(DynamicTableRegion):
    """
    DynamicTableRegion pointer to the channels that this decomposition series was generated from.
    """
    table: Optional[DynamicTable] = Field(None, description="""Reference to the DynamicTable object that this region applies to.""")
    description: Optional[str] = Field(None, description="""Description of what this table region points to.""")
    array: Optional[NDArray[Shape["* dim0, * dim1, * dim2, * dim3"], ]] = Field(None)
    

class DecompositionSeriesBands(DynamicTable):
    """
    Table for describing the bands that this series was generated from. There should be one row in this table for each band.
    """
    band_name: Optional[List[str]] = Field(default_factory=list, description="""Name of the band, e.g. theta.""")
    band_limits: DecompositionSeriesBandsBandLimits = Field(..., description="""Low and high limit of each band in Hz. If it is a Gaussian filter, use 2 SD on either side of the center.""")
    band_mean: DecompositionSeriesBandsBandMean = Field(..., description="""The mean Gaussian filters, in Hz.""")
    band_stdev: DecompositionSeriesBandsBandStdev = Field(..., description="""The standard deviation of Gaussian filters, in Hz.""")
    colnames: Optional[str] = Field(None, description="""The names of the columns in this table. This should be used to specify an order to the columns.""")
    description: Optional[str] = Field(None, description="""Description of what is in this dynamic table.""")
    id: DynamicTableId = Field(..., description="""Array of unique identifiers for the rows of this dynamic table.""")
    VectorData: Optional[List[VectorData]] = Field(default_factory=list, description="""Vector columns, including index columns, of this dynamic table.""")
    

class DecompositionSeriesBandsBandLimits(VectorData):
    """
    Low and high limit of each band in Hz. If it is a Gaussian filter, use 2 SD on either side of the center.
    """
    description: Optional[str] = Field(None, description="""Description of what these vectors represent.""")
    array: Optional[NDArray[Shape["* dim0, * dim1, * dim2, * dim3"], ]] = Field(None)
    

class DecompositionSeriesBandsBandMean(VectorData):
    """
    The mean Gaussian filters, in Hz.
    """
    description: Optional[str] = Field(None, description="""Description of what these vectors represent.""")
    array: Optional[NDArray[Shape["* dim0, * dim1, * dim2, * dim3"], ]] = Field(None)
    

class DecompositionSeriesBandsBandStdev(VectorData):
    """
    The standard deviation of Gaussian filters, in Hz.
    """
    description: Optional[str] = Field(None, description="""Description of what these vectors represent.""")
    array: Optional[NDArray[Shape["* dim0, * dim1, * dim2, * dim3"], ]] = Field(None)
    

class UnitsSpikeTimesIndex(VectorIndex):
    """
    Index into the spike_times dataset.
    """
    target: Optional[VectorData] = Field(None, description="""Reference to the target dataset that this index applies to.""")
    description: Optional[str] = Field(None, description="""Description of what these vectors represent.""")
    array: Optional[NDArray[Shape["* dim0, * dim1, * dim2, * dim3"], ]] = Field(None)
    

class UnitsSpikeTimes(VectorData):
    """
    Spike times for each unit in seconds.
    """
    resolution: Optional[float] = Field(None, description="""The smallest possible difference between two spike times. Usually 1 divided by the acquisition sampling rate from which spike times were extracted, but could be larger if the acquisition time series was downsampled or smaller if the acquisition time series was smoothed/interpolated and it is possible for the spike time to be between samples.""")
    description: Optional[str] = Field(None, description="""Description of what these vectors represent.""")
    array: Optional[NDArray[Shape["* dim0, * dim1, * dim2, * dim3"], ]] = Field(None)
    

class UnitsObsIntervalsIndex(VectorIndex):
    """
    Index into the obs_intervals dataset.
    """
    target: Optional[VectorData] = Field(None, description="""Reference to the target dataset that this index applies to.""")
    description: Optional[str] = Field(None, description="""Description of what these vectors represent.""")
    array: Optional[NDArray[Shape["* dim0, * dim1, * dim2, * dim3"], ]] = Field(None)
    

class UnitsObsIntervals(VectorData):
    """
    Observation intervals for each unit.
    """
    description: Optional[str] = Field(None, description="""Description of what these vectors represent.""")
    array: Optional[NDArray[Shape["* dim0, * dim1, * dim2, * dim3"], ]] = Field(None)
    

class UnitsElectrodesIndex(VectorIndex):
    """
    Index into electrodes.
    """
    target: Optional[VectorData] = Field(None, description="""Reference to the target dataset that this index applies to.""")
    description: Optional[str] = Field(None, description="""Description of what these vectors represent.""")
    array: Optional[NDArray[Shape["* dim0, * dim1, * dim2, * dim3"], ]] = Field(None)
    

class UnitsElectrodes(DynamicTableRegion):
    """
    Electrode that each spike unit came from, specified using a DynamicTableRegion.
    """
    table: Optional[DynamicTable] = Field(None, description="""Reference to the DynamicTable object that this region applies to.""")
    description: Optional[str] = Field(None, description="""Description of what this table region points to.""")
    array: Optional[NDArray[Shape["* dim0, * dim1, * dim2, * dim3"], ]] = Field(None)
    

class UnitsWaveformMean(VectorData):
    """
    Spike waveform mean for each spike unit.
    """
    sampling_rate: Optional[float] = Field(None, description="""Sampling rate, in hertz.""")
    unit: Optional[str] = Field(None, description="""Unit of measurement. This value is fixed to 'volts'.""")
    description: Optional[str] = Field(None, description="""Description of what these vectors represent.""")
    array: Optional[NDArray[Shape["* dim0, * dim1, * dim2, * dim3"], ]] = Field(None)
    

class UnitsWaveformSd(VectorData):
    """
    Spike waveform standard deviation for each spike unit.
    """
    sampling_rate: Optional[float] = Field(None, description="""Sampling rate, in hertz.""")
    unit: Optional[str] = Field(None, description="""Unit of measurement. This value is fixed to 'volts'.""")
    description: Optional[str] = Field(None, description="""Description of what these vectors represent.""")
    array: Optional[NDArray[Shape["* dim0, * dim1, * dim2, * dim3"], ]] = Field(None)
    

class UnitsWaveforms(VectorData):
    """
    Individual waveforms for each spike on each electrode. This is a doubly indexed column. The 'waveforms_index' column indexes which waveforms in this column belong to the same spike event for a given unit, where each waveform was recorded from a different electrode. The 'waveforms_index_index' column indexes the 'waveforms_index' column to indicate which spike events belong to a given unit. For example, if the 'waveforms_index_index' column has values [2, 5, 6], then the first 2 elements of the 'waveforms_index' column correspond to the 2 spike events of the first unit, the next 3 elements of the 'waveforms_index' column correspond to the 3 spike events of the second unit, and the next 1 element of the 'waveforms_index' column corresponds to the 1 spike event of the third unit. If the 'waveforms_index' column has values [3, 6, 8, 10, 12, 13], then the first 3 elements of the 'waveforms' column contain the 3 spike waveforms that were recorded from 3 different electrodes for the first spike time of the first unit. See https://nwb-schema.readthedocs.io/en/stable/format_description.html#doubly-ragged-arrays for a graphical representation of this example. When there is only one electrode for each unit (i.e., each spike time is associated with a single waveform), then the 'waveforms_index' column will have values 1, 2, ..., N, where N is the number of spike events. The number of electrodes for each spike event should be the same within a given unit. The 'electrodes' column should be used to indicate which electrodes are associated with each unit, and the order of the waveforms within a given unit x spike event should be in the same order as the electrodes referenced in the 'electrodes' column of this table. The number of samples for each waveform must be the same.
    """
    sampling_rate: Optional[float] = Field(None, description="""Sampling rate, in hertz.""")
    unit: Optional[str] = Field(None, description="""Unit of measurement. This value is fixed to 'volts'.""")
    description: Optional[str] = Field(None, description="""Description of what these vectors represent.""")
    array: Optional[NDArray[Shape["* dim0, * dim1, * dim2, * dim3"], ]] = Field(None)
    

class UnitsWaveformsIndex(VectorIndex):
    """
    Index into the waveforms dataset. One value for every spike event. See 'waveforms' for more detail.
    """
    target: Optional[VectorData] = Field(None, description="""Reference to the target dataset that this index applies to.""")
    description: Optional[str] = Field(None, description="""Description of what these vectors represent.""")
    array: Optional[NDArray[Shape["* dim0, * dim1, * dim2, * dim3"], ]] = Field(None)
    

class UnitsWaveformsIndexIndex(VectorIndex):
    """
    Index into the waveforms_index dataset. One value for every unit (row in the table). See 'waveforms' for more detail.
    """
    target: Optional[VectorData] = Field(None, description="""Reference to the target dataset that this index applies to.""")
    description: Optional[str] = Field(None, description="""Description of what these vectors represent.""")
    array: Optional[NDArray[Shape["* dim0, * dim1, * dim2, * dim3"], ]] = Field(None)
    


# Update forward refs
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/
AbstractFeatureSeriesData.update_forward_refs()
AbstractFeatureSeriesDataArray.update_forward_refs()
AbstractFeatureSeriesFeatureUnits.update_forward_refs()
AbstractFeatureSeriesFeatures.update_forward_refs()
AnnotationSeriesData.update_forward_refs()
IntervalSeriesData.update_forward_refs()
DecompositionSeriesData.update_forward_refs()
DecompositionSeriesDataArray.update_forward_refs()
DecompositionSeriesSourceChannels.update_forward_refs()
DecompositionSeriesBands.update_forward_refs()
DecompositionSeriesBandsBandLimits.update_forward_refs()
DecompositionSeriesBandsBandMean.update_forward_refs()
DecompositionSeriesBandsBandStdev.update_forward_refs()
UnitsSpikeTimesIndex.update_forward_refs()
UnitsSpikeTimes.update_forward_refs()
UnitsObsIntervalsIndex.update_forward_refs()
UnitsObsIntervals.update_forward_refs()
UnitsElectrodesIndex.update_forward_refs()
UnitsElectrodes.update_forward_refs()
UnitsWaveformMean.update_forward_refs()
UnitsWaveformSd.update_forward_refs()
UnitsWaveforms.update_forward_refs()
UnitsWaveformsIndex.update_forward_refs()
UnitsWaveformsIndexIndex.update_forward_refs()
