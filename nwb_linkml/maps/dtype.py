

flat_to_linkml = {
    "float" : "float",
    "float32" : "float",
    "double" : "double",
    "float64" : "double",
    "long" : "integer",
    "int64" : "integer",
    "int" : "integer",
    "int32" : "integer",
    "int16" : "integer",
    "short" : "integer",
    "int8" : "integer",
    "uint" : "integer",
    "uint32" : "integer",
    "uint16" : "integer",
    "uint8" : "integer",
    "uint64" : "integer",
    "numeric" : "float",
    "text" : "string",
    "utf" : "string",
    "utf8" : "string",
    "utf_8" : "string",
    "ascii" : "string",
    "bool" : "boolean",
    "isodatetime" : "datetime"
}
"""
Map between the flat data types and the simpler linkml base types
"""

flat_to_npytyping = {
    "float": "Float",
    "float32": "Float32",
    "double": "Double",
    "float64": "Float64",
    "long": "LongLong",
    "int64": "Int64",
    "int": "Int",
    "int32": "Int32",
    "int16": "Int16",
    "short": "Short",
    "int8": "Int8",
    "uint": "UInt",
    "uint32": "UInt32",
    "uint16": "UInt16",
    "uint8": "UInt8",
    "uint64": "UInt64",
    "numeric": "Number",
    "text": "String",
    "utf": "Unicode",
    "utf8": "Unicode",
    "utf_8": "Unicode",
    "ascii": "String",
    "bool": "Bool",
    "isodatetime": "Datetime64",
    'AnyType': 'Any'
}