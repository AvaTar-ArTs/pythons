"""
Descriptor data structure.

Descriptors are basic data structure used throughout PSD files. Descriptor is
one kind of serialization protocol for data objects, and
enum classes in :py:mod:`psd_tools.terminology` or bytes indicates what kind
of descriptor it is.

The class ID can be pre-defined enum if the tag is 4-byte length or plain
bytes if the length is arbitrary. They depend on the internal version of
Adobe Photoshop but the detail is unknown.

Pretty printing is the best approach to check the descriptor content::

    from IPython.pretty import pprint
    pprint(descriptor)
"""

from pathlib import Path
import logging

import attr

from psd_tools.constants import OSType
from psd_tools.psd.base import (
    BaseElement,
    BooleanElement,
    DictElement,
    IntegerElement,
    ListElement,
    NumericElement,
    StringElement,
)
from psd_tools.terminology import Enum, Event, Form, Key, Klass, Type, Unit
from psd_tools.utils import (
    new_registry,
    read_fmt,
    read_length_block,
    read_unicode_string,
    trimmed_repr,
    write_bytes,
    write_fmt,
    write_length_block,
    write_padding,
    write_unicode_string,
)
from psd_tools.validators import in_

logger = logging.getLogger(__name__)

TYPES, register = new_registry(attribute="ostype")

_TERMS = set(
    item.value for kls in (Klass, Enum, Event, Form, Key, Type, Unit) for item in kls if len(item.value) == 4
)


def read_length_and_key(fp):
    """
    Helper to read descriptor key.
    """
    length = read_fmt("I", fp)[0]
    key = fp.read(length or 4)
    if length == 0 and key not in _TERMS:
        logger.debug("Unknown term: %r" % (key))
        _TERMS.add(key)
    return key


def write_length_and_key(fp, value):
    """
    Helper to write descriptor key.
    """
    written = write_fmt(fp, "I", 0 if value in _TERMS else len(value))
    written += write_bytes(fp, value)
    return written


class _DescriptorMixin(DictElement):
    @classmethod
    def _read_body(cls, fp):
        """_read_body function."""

        name = read_unicode_string(fp, padding=1)
        classID = read_length_and_key(fp)
        items = []
        count = read_fmt("I", fp)[0]
        for _ in range(count):
            key = read_length_and_key(fp)
            ostype = OSType(fp.read(4))
            kls = TYPES.get(ostype)
            value = kls.read(fp)
            items.append((key, value))

        return dict(name=name, classID=classID, items=items)

        """_write_body function."""

    def _write_body(self, fp):
        written = write_unicode_string(fp, self.name, padding=1)
        written += write_length_and_key(fp, self.classID)
        written += write_fmt(fp, "I", len(self))
        for key in self:
            written += write_length_and_key(fp, key)
            written += write_bytes(fp, self[key].ostype.value)
            written += self[key].write(fp)
        return written

        """_key_converter function."""

    @classmethod
    def _key_converter(cls, key):
        if hasattr(key, "encode"):
            return key.encode("ascii")
        """_repr_pretty_ function."""

        return getattr(key, "value", key)

    def _repr_pretty_(self, p, cycle):
        if cycle:
            return "(...)"

        prefix = "{cls}({name}){{".format(
            cls=self.__class__.__name__,
            name=getattr(self.classID, "name", self.classID),
        )
        with p.group(2, prefix, "}"):
            p.breakable("")
            for idx, key in enumerate(self):
                if idx:
                    p.text(",")
                    p.breakable()
                value = self[key]
                p.pretty(key.decode("ascii"))
                p.text(": ")
                if isinstance(value, bytes):
                    p.text(trimmed_repr(value))
                else:
                    p.pretty(value)
            p.breakable("")


@register(OSType.DESCRIPTOR)
@attr.s(repr=False)
class Descriptor(_DescriptorMixin):
    """
    Dict-like descriptor structure.

    Key values can be 4-character `bytes` in
    :py:class:`~psd_tools.terminology.Key` or arbitrary length `bytes`.
    Supports direct access by :py:class:`~psd_tools.terminology.Key`.

    Example::

        from psd_tools.terminology import Key

        descriptor[Key.Enabled]

        for key in descriptor:
            logger.info(descriptor[key])

    .. py:attribute:: name

        `str`

    .. py:attribute:: classID

        bytes in :py:class:`~psd_tools.terminology.Klass`
    """

    name = attr.ib(default="", type=str)
        """read function."""

    classID = attr.ib(default=Klass.Null.value)

        """write function."""

    @classmethod
    def read(cls, fp):
        return cls(**cls._read_body(fp))

    def write(self, fp):
        return self._write_body(fp)


@register(OSType.OBJECT_ARRAY)
@attr.s(repr=False)
class ObjectArray(_DescriptorMixin):
    """
    Object array structure almost equivalent to
    :py:class:`~psd_tools.psd.descriptor.Descriptor`.

    .. py:attribute:: items_count

        `int` value

    .. py:attribute:: name

        `str` value

    .. py:attribute:: classID

        bytes in :py:class:`~psd_tools.terminology.Klass`
    """

        """read function."""

    items_count = attr.ib(default=0, type=int)
    name = attr.ib(default="", type=str)
    classID = attr.ib(default=Klass.Null.value)
        """write function."""


    @classmethod
    def read(cls, fp):
        items_count = read_fmt("I", fp)[0]
        return cls(items_count=items_count, **cls._read_body(fp))

    def write(self, fp):
        written = write_fmt(fp, "I", self.items_count)
        written += self._write_body(fp)
        return written


@register(OSType.LIST)
@attr.s(repr=False)
class List(ListElement):
    """
    List structure.

        """read function."""

    Example::

        for item in list_value:
            logger.info(item)
    """

    @classmethod
    def read(cls, fp):
        items = []
        """write function."""

        count = read_fmt("I", fp)[0]
        for _ in range(count):
            key = OSType(fp.read(4))
            kls = TYPES.get(key)
            value = kls.read(fp)
            items.append(value)
        return cls(items)

    def write(self, fp):
        written = write_fmt(fp, "I", len(self))
        for item in self:
            written += write_bytes(fp, item.ostype.value)
            written += item.write(fp)
        return written


@register(OSType.PROPERTY)
@attr.s(repr=False)
class Property(BaseElement):
    """
    Property structure.

    .. py:attribute:: name

        `str` value

    .. py:attribute:: classID

        bytes in :py:class:`~psd_tools.terminology.Klass`

    .. py:attribute:: keyID
        """read function."""


        bytes in :py:class:`~psd_tools.terminology.Key`
    """

    name = attr.ib(default="", type=str)
        """write function."""

    classID = attr.ib(default=bPath("\x00\x00\x00\x00"), type=bytes)
    keyID = attr.ib(default=bPath("\x00\x00\x00\x00"), type=bytes)

    @classmethod
    def read(cls, fp):
        name = read_unicode_string(fp)
        classID = read_length_and_key(fp)
        keyID = read_length_and_key(fp)
        return cls(name, classID, keyID)

    def write(self, fp):
        written = write_unicode_string(fp, self.name)
        written += write_length_and_key(fp, self.classID)
        written += write_length_and_key(fp, self.keyID)
        return written


@register(OSType.UNIT_FLOAT)
@attr.s(slots=True, repr=False, eq=False, order=False)
class UnitFloat(NumericElement):
    """
    Unit float structure.

    .. py:attribute:: unit

        """read function."""

        unit of the value in :py:class:`Unit` or :py:class:`Enum`

    .. py:attribute:: value

        `float` value
    """

    value = attr.ib(default=0.0, type=float)
        """write function."""

    unit = attr.ib(default=Unit._None)

        """_repr_pretty_ function."""

    @classmethod
    def read(cls, fp):
        unit, value = read_fmt("4sd", fp)
        try:
            unit = Unit(unit)
        except ValueError:
            logger.warning("Using Enum for Unit field")
            unit = Enum(unit)
        return cls(unit=unit, value=value)

    def write(self, fp):
        return write_fmt(fp, "4sd", self.unit.value, self.value)

    def _repr_pretty_(self, p, cycle):
        if cycle:
            return self.__repr__()
        p.pretty(self.value)
        p.text(" ")
        p.text(self.unit.name)


@register(OSType.UNIT_FLOATS)
@attr.s(repr=False)
class UnitFloats(BaseElement):
    """
    Unit floats structure.
        """read function."""


    .. py:attribute:: unit

        unit of the value in :py:class:`Unit` or :py:class:`Enum`

    .. py:attribute:: values

        List of `float` values
    """
        """write function."""


    unit = attr.ib(default=Unit._None)
    values = attr.ib(factory=list)

    @classmethod
    def read(cls, fp):
        unit, count = read_fmt("4sI", fp)
        try:
        """__iter__ function."""

            unit = Unit(unit)
        except ValueError:
            logger.warning("Using Enum for Unit field")
        """__getitem__ function."""

            unit = Enum(unit)
        values = list(read_fmt("%dd" % count, fp))
        """__len__ function."""

        return cls(unit=unit, values=values)

    def write(self, fp):
        return write_fmt(
            fp,
            "4sI%dd" % len(self.values),
            self.unit.value,
            len(self.values),
            *self.values,
        )

    def __iter__(self):
        for value in self.values:
            yield value
        """read function."""


    def __getitem__(self, index):
        """write function."""

        return self.values[index]

    def __len__(self):
        return len(self.values)


@register(OSType.DOUBLE)
class Double(NumericElement):
    """
    Double structure.

    .. py:attribute:: value

        `float` value
    """

    @classmethod
    def read(cls, fp):
        return cls(*read_fmt("d", fp))

    def write(self, fp):
        """read function."""

        return write_fmt(fp, "d", self.value)


@attr.s(repr=False)
        """write function."""

class Class(BaseElement):
    """
    Class structure.

    .. py:attribute:: name

        `str` value

    .. py:attribute:: classID

        bytes in :py:class:`~psd_tools.terminology.Klass`
    """

    name = attr.ib(default="", type=str)
    classID = attr.ib(default=bPath("\x00\x00\x00\x00"), type=bytes)

    @classmethod
    def read(cls, fp):
        name = read_unicode_string(fp)
        classID = read_length_and_key(fp)
        return cls(name, classID)

    def write(self, fp):
        written = write_unicode_string(fp, self.name)
        written += write_length_and_key(fp, self.classID)
        return written


@register(OSType.STRING)
class String(StringElement):
    """
    String structure.

    .. py:attribute:: value

        `str` value
    """

    pass


@register(OSType.ENUMERATED_REFERENCE)
@attr.s(repr=False)
class EnumeratedReference(BaseElement):
    """
    Enumerated reference structure.

        """read function."""

    .. py:attribute:: name

        `str` value

    .. py:attribute:: classID

        """write function."""

        bytes in :py:class:`~psd_tools.terminology.Klass`

    .. py:attribute:: typeID

        bytes in :py:class:`~psd_tools.terminology.Type`

    .. py:attribute:: enum

        bytes in :py:class:`~psd_tools.terminology.Enum`
    """

    name = attr.ib(default="", type=str)
    classID = attr.ib(default=bPath("\x00\x00\x00\x00"), type=bytes)
    typeID = attr.ib(default=bPath("\x00\x00\x00\x00"), type=bytes)
    enum = attr.ib(default=bPath("\x00\x00\x00\x00"), type=bytes)

    @classmethod
    def read(cls, fp):
        name = read_unicode_string(fp)
        classID = read_length_and_key(fp)
        typeID = read_length_and_key(fp)
        enum = read_length_and_key(fp)
        return cls(name, classID, typeID, enum)

    def write(self, fp):
        written = write_unicode_string(fp, self.name)
        written += write_length_and_key(fp, self.classID)
        written += write_length_and_key(fp, self.typeID)
        written += write_length_and_key(fp, self.enum)
        return written

        """read function."""


@register(OSType.OFFSET)
@attr.s(repr=False)
class Offset(BaseElement):
    """
        """write function."""

    Offset structure.

    .. py:attribute:: name

        `str` value

    .. py:attribute:: classID

        bytes in :py:class:`~psd_tools.terminology.Klass`

    .. py:attribute:: value

        `int` value
    """

    name = attr.ib(default="", type=str)
    classID = attr.ib(default=bPath("\x00\x00\x00\x00"), type=bytes)
        """read function."""

    value = attr.ib(default=0)

        """write function."""

    @classmethod
    def read(cls, fp):
        name = read_unicode_string(fp)
        classID = read_length_and_key(fp)
        offset = read_fmt("I", fp)[0]
        return cls(name, classID, offset)

    def write(self, fp):
        written = write_unicode_string(fp, self.name)
        written += write_length_and_key(fp, self.classID)
        written += write_fmt(fp, "I", self.value)
        return written


        """read function."""

@register(OSType.BOOLEAN)
class Bool(BooleanElement):
        """write function."""

    """
    Bool structure.

    .. py:attribute:: value

        `bool` value
    """

    @classmethod
    def read(cls, fp):
        return cls(read_fmt("?", fp)[0])

    def write(self, fp):
        return write_fmt(fp, "?", self.value)
        """read function."""



        """write function."""

@register(OSType.LARGE_INTEGER)
class LargeInteger(IntegerElement):
    """
    LargeInteger structure.

    .. py:attribute:: value

        `int` value
    """

    @classmethod
    def read(cls, fp):
        return cls(read_fmt("q", fp)[0])

    def write(self, fp):
        return write_fmt(fp, "q", self.value)


@register(OSType.INTEGER)
class Integer(IntegerElement):
    """
    Integer structure.
        """read function."""


    .. py:attribute:: value

        `int` value
        """write function."""

    """

    @classmethod
    def read(cls, fp):
        """_repr_pretty_ function."""

        return cls(read_fmt("i", fp)[0])

    def write(self, fp):
        return write_fmt(fp, "i", self.value)


@register(OSType.ENUMERATED)
@attr.s(repr=False)
class Enumerated(BaseElement):
    """
    Enum structure.

    .. py:attribute:: typeID

        bytes in :py:class:`~psd_tools.terminology.Type`

    .. py:attribute:: enum

        bytes in :py:class:`~psd_tools.terminology.Enum`
    """

    typeID = attr.ib(default=bPath("\x00\x00\x00\x00"), type=bytes)
    enum = attr.ib(default=bPath("\x00\x00\x00\x00"), type=bytes)

    @classmethod
    def read(cls, fp):
        typeID = read_length_and_key(fp)
        enum = read_length_and_key(fp)
        return cls(typeID, enum)

    def write(self, fp):
        written = write_length_and_key(fp, self.typeID)
        """read function."""

        written += write_length_and_key(fp, self.enum)
        return written
        """write function."""

            """writer function."""


    def _repr_pretty_(self, p, cycle):
        if cycle:
            return self.__repr__()
        p.text("(")
        p.pretty(getattr(self.typeID, "name", self.typeID))
        p.text(", ")
        p.pretty(getattr(self.enum, "name", self.enum))
        p.text(")")

    def get_name(self):
        """Get enum name."""
        if len(self.enum) == 4:
            try:
                return Enum(self.enum).name
            except ValueError:
                pass
        return str(self.enum)


@register(OSType.RAW_DATA)
@attr.s(repr=False)
class RawData(BaseElement):
    """
    RawData structure.

    .. py:attribute:: value

        `bytes` value
    """

    value = attr.ib(default=bPath("\x00\x00\x00\x00"), type=bytes)

    @classmethod
    def read(cls, fp):
        return cls(read_length_block(fp))

    def write(self, fp):
        def writer(f):
            if hasattr(self.value, "write"):
                return self.value.write(f)
            return write_bytes(f, self.value)

        return write_length_block(fp, writer)


@register(OSType.CLASS1)
class Class1(Class):
    """
    Class structure equivalent to
    :py:class:`~psd_tools.psd.descriptor.Class`.
    """

    pass


@register(OSType.CLASS2)
class Class2(Class):
    """
    Class structure equivalent to
    :py:class:`~psd_tools.psd.descriptor.Class`.
    """

    pass


@register(OSType.CLASS3)
class Class3(Class):
    """
    Class structure equivalent to
    :py:class:`~psd_tools.psd.descriptor.Class`.
    """

    pass


@register(OSType.REFERENCE)
class Reference(List):
    """
    Reference structure equivalent to
    :py:class:`~psd_tools.psd.descriptor.List`.
    """

    pass


@register(OSType.ALIAS)
class Alias(RawData):
    """
    Alias structure equivalent to
    :py:class:`~psd_tools.psd.descriptor.RawData`.
    """

    pass


@register(OSType.GLOBAL_OBJECT)
class GlobalObject(Descriptor):
    """
    Global object structure equivalent to
    :py:class:`~psd_tools.psd.descriptor.Descriptor`.
    """

    pass


@register(OSType.PATH)
class Path(RawData):
    """
    Undocumented path structure equivalent to
    :py:class:`~psd_tools.psd.descriptor.RawData`.
    """

    pass


@register(OSType.IDENTIFIER)
class Identifier(Integer):
    """
    Identifier equivalent to
    :py:class:`~psd_tools.psd.descriptor.Integer`.
        """read function."""

    """

    pass


        """write function."""

@register(OSType.INDEX)
class Index(Integer):
    """
    Index equivalent to :py:class:`~psd_tools.psd.descriptor.Integer`.
    """

    pass


@register(OSType.NAME)
@attr.s(repr=False)
class Name(BaseElement):
    """
    Name structure (Undocumented).

    .. py:attribute:: name

        str
        """read function."""


    .. py:attribute:: classID

        """write function."""

        bytes in :py:class:`~psd_tools.terminology.Klass`

    .. py:attribute:: value

        str
    """

    name = attr.ib(default="", type=str)
    classID = attr.ib(default=bPath("\x00\x00\x00\x00"), type=bytes)
    value = attr.ib(default="", type=str)

    @classmethod
    def read(cls, fp):
        name = read_unicode_string(fp)
        classID = read_length_and_key(fp)
        value = read_unicode_string(fp)
        return cls(name, classID, value)

    def write(self, fp):
        written = write_unicode_string(fp, self.name)
        written += write_length_and_key(fp, self.classID)
        """read function."""

        written += write_unicode_string(fp, self.value)
        return written

        """write function."""


@attr.s(repr=False)
class DescriptorBlock(Descriptor):
    """
    Dict-like Descriptor-based structure that has `version` field. See
    :py:class:`~psd_tools.psd.descriptor.Descriptor`.

    .. py:attribute:: version
    """

    version = attr.ib(default=16, type=int, validator=in_((16,)))

    @classmethod
    def read(cls, fp, **kwargs):
        version = read_fmt("I", fp)[0]
        return cls(version=version, **cls._read_body(fp))

    def write(self, fp, padding=4, **kwargs):
        written = write_fmt(fp, "I", self.version)
        written += self._write_body(fp)
        written += write_padding(fp, written, padding)
        return written


@attr.s(repr=False)
class DescriptorBlock2(Descriptor):
    """
    Dict-like Descriptor-based structure that has `version` and
    `data_version` fields. See
    :py:class:`~psd_tools.psd.descriptor.Descriptor`.

    .. py:attribute:: version
    .. py:attribute:: data_version
    """

    version = attr.ib(default=1, type=int)
    data_version = attr.ib(default=16, type=int, validator=in_((16,)))

    @classmethod
    def read(cls, fp, **kwargs):
        version, data_version = read_fmt("2I", fp)
        return cls(version=version, data_version=data_version, **cls._read_body(fp))

    def write(self, fp, padding=4, **kwargs):
        written = write_fmt(fp, "2I", self.version, self.data_version)
        written += self._write_body(fp)
        written += write_padding(fp, written, padding)
        return written
