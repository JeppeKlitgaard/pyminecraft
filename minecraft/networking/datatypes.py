"""
Contains the datatypes used by the networking part of `pyminecraft`.
The types are described at http://wiki.vg/Protocol#Data_types
"""

__all__ = ["ENDIANNESS",
           "Datatype",
           "Boolean",
           "Byte", "UnsignedByte",
           "Short", "UnsignedShort",
           "Integer", "UnsignedInteger",
           "Long", "UnsignedLong",
           "LongLong", "UnsignedLongLong",
           "Float",
           "Double"]

import struct

ENDIANNESS = "!"  # Network, big-endian


class Datatype(object):
    """
    Base object for all `pyminecraft` networking datatypes.
    """
    PYTHON_TYPE = None  # The Python equivalent
    FORMAT = ""
    SIZE = 0

    @classmethod
    def read(cls, fileobject):
        bin_data = fileobject.read(cls.SIZE)
        return cls.deserialize(bin_data)

    @classmethod
    def deserialize(cls, data):
        return struct.unpack(ENDIANNESS + cls.FORMAT, data)[0]

    @classmethod
    def serialize(cls, data):
        serialized_data = struct.pack(ENDIANNESS + cls.FORMAT, data)
        return serialized_data


class Boolean(Datatype):
    PYTHON_TYPE = bool
    FORMAT = "?"
    SIZE = 1


class Byte(Datatype):
    PYTHON_TYPE = int
    FORMAT = "b"
    SIZE = 1


class UnsignedByte(Datatype):
    PYTHON_TYPE = int
    FORMAT = "B"
    SIZE = 1


class Short(Datatype):
    PYTHON_TYPE = int
    FORMAT = "h"
    SIZE = 2


class UnsignedShort(Datatype):
    PYTHON_TYPE = int
    FORMAT = "H"
    SIZE = 2


class Integer(Datatype):
    PYTHON_TYPE = int
    FORMAT = "i"
    SIZE = 4


class UnsignedInteger(Datatype):
    PYTHON_TYPE = int
    FORMAT = "I"
    SIZE = 4


class Long(Datatype):
    PYTHON_TYPE = int
    FORMAT = "l"
    SIZE = 4


class UnsignedLong(Datatype):
    PYTHON_TYPE = int
    FORMAT = "L"
    SIZE = 4


class LongLong(Datatype):
    PYTHON_TYPE = int
    FORMAT = "q"
    SIZE = 8


class UnsignedLongLong(Datatype):
    PYTHON_TYPE = int
    FORMAT = "Q"
    SIZE = 8


class Float(Datatype):
    PYTHON_TYPE = float
    FORMAT = "f"
    SIZE = 4


class Double(Datatype):
    PYTHON_TYPE = float
    FORMAT = "d"
    SIZE = 8
