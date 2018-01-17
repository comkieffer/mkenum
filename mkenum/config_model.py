
# TODO: Add required=True where needed

OutputFileSchema = {
    'type': 'dict',
    'required': True,
    'schema': {
        'filename': { 'type': 'string', 'required': True }, 
        'system_includes': { 'type': 'list', 'keyschema': { 'type': 'string' } }, 
        'local_includes': { 'type': 'list', 'keyschema': { 'type': 'string' } }, 
    }
}

EnumerationItem = {
    'type': 'dict',
    'schema': {
        'identifier': { 'type': 'string', 'required': True },
        'value': { 'type': 'string' },
    }
}

EnumerationValueMappingSchema = {
    'type': 'dict',
    'schema': {
        'from': { 'type': 'string', 'required': True },
        'to': { 'type': 'string', 'required': True },
        'name': { 'type': 'string', 'required': True },
        'input_type': { 'type': 'string', 'required': True },
        'return_type': { 'type': 'string', 'required': True },
    }
}

EnumerationSchema = {
    'type': 'dict',
    'schema':  {
        'name': { 'type': 'string', 'required': True },
        'namespace': { 
            'type': 'list',
            'keyschema': { 'type': 'string' },
        },
        'doc_comment': { 'type': 'string' },
        'values': {
            'type': 'list',
            'required': True,
            'anyof_keyschema': [ { 'type': 'string' }, EnumerationItem ],
        },
        'mappings': {
            'type': 'list',
            'keyschema': EnumerationValueMappingSchema
        }
    }
}

ConfigSchema = {
    'outputs': {
        'type': 'dict',
        'schema': {
            'header': OutputFileSchema,
            'source': OutputFileSchema,
        }, 
    }, 

    'enumerations': {
        'type': 'list',
        'required': True,
        'schema': EnumerationSchema
    }
} 