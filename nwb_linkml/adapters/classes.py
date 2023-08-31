"""
Adapters to linkML classes
"""
import pdb
import re
from abc import abstractmethod
from typing import List, Optional
from nwb_schema_language import Dataset, Group, ReferenceDtype, CompoundDtype, DTypeType
from nwb_linkml.adapters.adapter import Adapter, BuildResult
from linkml_runtime.linkml_model import ClassDefinition, SlotDefinition
from nwb_linkml.maps import QUANTITY_MAP
from nwb_linkml.lang_elements import Arraylike

CAMEL_TO_SNAKE = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')
"""
Convert camel case to snake case

courtesy of: https://stackoverflow.com/a/12867228
"""

def camel_to_snake(name:str) -> str:
    """
    Convert camel case to snake case

    courtesy of: https://stackoverflow.com/a/12867228
    """
    return CAMEL_TO_SNAKE.sub(r'_\1', name).lower()

class ClassAdapter(Adapter):
    """
    Abstract adapter to class-like things in linkml, holds methods common to
    both DatasetAdapter and GroupAdapter
    """
    cls: Dataset | Group
    parent: Optional['ClassAdapter'] = None

    @abstractmethod
    def build(self) -> BuildResult:
        """
        Make this abstract so it can't be instantiated directly.

        Subclasses call :meth:`.build_base` to get the basics true of both groups and datasets
        """


    def build_base(self, extra_attrs: Optional[List[SlotDefinition]]=None) -> BuildResult:
        """
        Build the basic class and attributes before adding any specific
        modifications for groups or datasets.
        """

        # Build this class
        #name = self._get_full_name()
        if self.parent is not None:
            name = self._get_full_name()
        else:
            name = self._get_attr_name()

        # Get vanilla top-level attributes
        attrs = self.build_attrs(self.cls)
        name_slot = self.build_name_slot()
        attrs.append(name_slot)
        if extra_attrs is not None:
            if isinstance(extra_attrs, SlotDefinition):
                extra_attrs = [extra_attrs]
            attrs.extend(extra_attrs)

        cls = ClassDefinition(
            name = name,
            is_a = self.cls.neurodata_type_inc,
            description=self.cls.doc,
            attributes=attrs,
        )

        slots = []
        if self.parent is not None:
            slots.append(self.build_self_slot())

        res = BuildResult(
            classes = [cls],
            slots = slots
        )

        return res

    def build_attrs(self, cls: Dataset | Group) -> List[SlotDefinition]:
        attrs = [
            SlotDefinition(
                name=attr.name,
                description=attr.doc,
                range=self.handle_dtype(attr.dtype),
            ) for attr in cls.attributes
        ]

        return attrs

    def _get_full_name(self) -> str:
        """The full name of the object in the generated linkml

        Distinct from 'name' which is the thing that's used to define position in
        a hierarchical data setting
        """
        if self.cls.neurodata_type_def:
            name = self.cls.neurodata_type_def
        elif self.cls.name is not None:
            # not necessarily a unique name, so we combine parent names
            name_parts = []
            if self.parent is not None:
                name_parts.append(self.parent._get_full_name())

            name_parts.append(self.cls.name)
            name = '__'.join(name_parts)
        elif self.cls.neurodata_type_inc is not None:
            # again, this is against the schema, but is common
            name = self.cls.neurodata_type_inc
        else:
            raise ValueError('Not sure what our name is!')


        return name

    def _get_attr_name(self) -> str:
        """
        Get the name to use as the attribute name,
        again distinct from the actual name of the instantiated object
        """
        # return self._get_full_name()
        name = None
        if self.cls.neurodata_type_def:
            #name = camel_to_snake(self.cls.neurodata_type_def)
            name = self.cls.neurodata_type_def
        elif self.cls.name is not None:
            # we do have a unique name
            name = self.cls.name
        elif self.cls.neurodata_type_inc:
            #name = camel_to_snake(self.cls.neurodata_type_inc)
            name = self.cls.neurodata_type_inc

        if name is None:
            raise ValueError(f'Class has no name!: {self.cls}')

        return name

    def handle_dtype(self, dtype: DTypeType | None) -> str:
        if isinstance(dtype, ReferenceDtype):
            return dtype.target_type
        elif dtype is None or dtype == []:
            # Some ill-defined datasets are "abstract" despite that not being in the schema language
            return 'AnyType'
        elif isinstance(dtype, list) and isinstance(dtype[0], CompoundDtype):
            # there is precisely one class that uses compound dtypes:
            # TimeSeriesReferenceVectorData
            # compoundDtypes are able to define a ragged table according to the schema
            # but are used in this single case equivalently to attributes.
            # so we'll... uh... treat them as slots.
             # TODO
            return 'AnyType'
            #raise NotImplementedError('got distracted, need to implement')

        else:
            # flat dtype
            return dtype

    def build_name_slot(self) -> SlotDefinition:
        """
        If a class has a name, then that name should be a slot with a
        fixed value.

        If a class does not have a name, then name should be a required attribute

        References:
            https://github.com/NeurodataWithoutBorders/nwb-schema/issues/552#issuecomment-1700319001

        Returns:

        """
        if self.cls.name:
            name_slot = SlotDefinition(
                name='name',
                required=True,
                ifabsent=self.cls.name,
                equals_string=self.cls.name,
                range='string'
            )
        else:
            name_slot = SlotDefinition(
                name='name',
                required=True,
                range='string'
            )
        return name_slot

    def build_self_slot(self) -> SlotDefinition:
        """
        If we are a child class, we make a slot so our parent can refer to us
        """
        return SlotDefinition(
            name=self._get_attr_name(),
            description=self.cls.doc,
            range=self._get_full_name(),
            **QUANTITY_MAP[self.cls.quantity]
        )







