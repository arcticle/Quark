from future.utils import viewitems

_schema = {
    "$required" : ["id", "name", "dir"],
    "$unique" : ["id", "name", "dir"],
    "$fields": {
        "id" : {
            "$type" : int
        },
        "name" : {
            "$type" : str
        },
        "dir" : {
            "$type" : str
        }
    }
}


class Validator(object):
    def __init__(self, schema):
        self.schema = schema
        
        self._validator_funcs = {
            "CollectionObject" : self._validate_collection_object 
        }

        self._validation_funcs = {
            "$required" : self._required_validation,
            "$unique" : self._uniqueness_validation,
            "$fields" : self._field_validation,
            "$type" : self._type_validation
        }


    def validate(self, data, storage_object):
        object_type = type(storage_object).__name__
        func = self._validator_funcs[object_type]
        return func(data, storage_object)

    def _validate_collection_object(self, data, storage_object):
        result = ValidationResult()

        for validation, constraint in viewitems(self.schema):
            func = self._validation_funcs[validation]
            func(data, constraint, storage_object, result)
        
        return result

    def _uniqueness_validation(self, data, constraint, storage_object, result):
        fields = {}
        
        for field in constraint:
            if field in data:
                fields[field] = data[field]

        query = {"$or": fields}

        obj = storage_object.find_one(query)

        if obj:
            result.add_error("Uniqueness validation failed for fields {}. Existing entry: {}".format(fields, obj))

    def _required_validation(self, data, constraint, storage_object, result):
        for field in constraint:
            if field not in data:
                result.add_error("Required validation failed for field \"{}\".".format(field))

    def _field_validation(self, data, constraint, storage_object, result):
        for field in constraint:
            for validation, constr in viewitems(constraint[field]):
                func = self._validation_funcs[validation]
                if field in data:
                    func(data[field], constr, storage_object, result)

    def _type_validation(self, data, constraint, storage_object, result):
        if not isinstance(data, constraint):
            try:
                # Try type casting to test if the value can be converted
                constraint(data)
            except:
                result.add_error("Type validation failed for \"{}\". Expected \"{}\"".format(data, constraint.__name__))

class ValidationResult(object):
    def __init__(self):
        self.errors = []

    def add_error(self, error):
        self.errors.append(error)

    @property
    def has_error(self):
        return len(self.errors) > 0