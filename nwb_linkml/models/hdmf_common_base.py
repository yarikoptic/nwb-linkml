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



metamodel_version = "None"
version = "None"

class ConfiguredBaseModel(BaseModel,
                validate_assignment = True,
                validate_default = True,
                extra = 'forbid',
                arbitrary_types_allowed = True,
                use_enum_values = True):
    pass


class Data(ConfiguredBaseModel):
    """
    An abstract data type for a dataset.
    """
    name: str = Field(...)
    

class Container(ConfiguredBaseModel):
    """
    An abstract data type for a group storing collections of data and metadata. Base type for all data and metadata containers.
    """
    name: str = Field(...)
    

class SimpleMultiContainer(Container):
    """
    A simple Container for holding onto multiple containers.
    """
    name: str = Field(...)
    Data: Optional[List[Data]] = Field(default_factory=list, description="""Data objects held within this SimpleMultiContainer.""")
    container: Optional[List[Container]] = Field(default_factory=list, description="""Container objects held within this SimpleMultiContainer.""")
    


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Data.model_rebuild()
Container.model_rebuild()
SimpleMultiContainer.model_rebuild()
    