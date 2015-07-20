db = {
    'user': [
        {'id': 1, 'name': 'Chuck Norris', 'rate': 2},
        {'id': 2, 'name': 'Bruce Lee', 'rate': 1},
        {'id': 3, 'name': 'Jackie Chan', 'rate': 3},
    ]
}


ID = 'id'


class BaseMeta(type):
    __data_storage__ = db  # MUST be a dictionary
    __used_id__ = {}
    __tablenames__ = set()

    def __new__(mcs, name, bases, attributes):
        mcs._init_used_id()  # set all available IDs in __used_id__
        mcs._init_tablenames()  # set all available tablenames in __tablenames__
        fields = {}

        tablename = attributes.get('__tablename__', None)

        if tablename is None:
            tablename = name.lower()
            attributes.update({'__tablename__': tablename})

        if tablename not in mcs.__data_storage__:
            mcs.__tablenames__.add(tablename)
            mcs.__used_id__[tablename] = set()
            mcs.__data_storage__[tablename] = []

        for field_name, field_obj in attributes.items():
            if isinstance(field_obj, Field):
                setattr(field_obj, 'name', field_name)
                setattr(field_obj.__class__,
                        '__eq__',
                        lambda self, other: "{}.{} = {}".format(tablename, self.name, str(other)))
                fields[field_name] = field_obj

        attributes.update({
            '__init__': mcs._create_init(fields, tablename),
            'get': mcs._create_get(),
        })

        return super(BaseMeta, mcs).__new__(mcs, name, bases, attributes)

    @classmethod
    def _init_used_id(mcs):
        for name, table in mcs.__data_storage__.items():
            mcs.__used_id__[name] = set()
            for row in table:
                mcs.__used_id__[name].add(row[ID])

    @classmethod
    def _init_tablenames(mcs):
        for tablename in mcs.__data_storage__:
            mcs.__tablenames__.add(tablename)

    @classmethod
    def _create_init(mcs, fields, tablename):
        def init(self, **kwargs):
            if ID in kwargs and kwargs[ID] in mcs.__used_id__[tablename]:
                self.id = kwargs[ID]
            elif ID in kwargs and kwargs[ID] not in mcs.__used_id__[tablename]:
                raise IndexError("You are not allowed to add custom id")
            else:
                self.id = 1 if len(mcs.__used_id__[tablename]) == 0 else max(mcs.__used_id__[tablename]) + 1
                mcs.__used_id__[tablename].add(self.id)
                new_row = {ID: self.id}

                for field_name, field_obj in fields.items():
                    if not isinstance(kwargs[field_name], field_obj.field_type):
                        raise TypeError("field type must be %s not %s" % (field_obj.field_type,
                                                                          type(kwargs[field_name])))
                    new_row[field_name] = kwargs[field_name]

                mcs.__data_storage__[tablename].append(new_row)

            for field_name, field_obj in fields.items():
                setattr(self.__class__,
                        field_name,
                        property(fget=mcs._create_fget(field_name),
                                 fset=mcs._create_fset(field_name, field_obj.field_type)))

                # self.__dict__.update({field_name: property(fget=mcs._create_fget(field_name),
                #                                            fset=mcs._create_fset(field_name, field_obj.field_type))})
        return init

    @classmethod
    def _create_get(mcs):
        def get(cls, obj_id):
            for row in mcs.__data_storage__[cls.__tablename__]:  # TODO optimize searching
                if obj_id == row[ID]:
                    return cls(**row)

        return classmethod(get)

    @classmethod
    def _create_fget(mcs, field_name):
        def fget(self):
            for row in mcs.__data_storage__[self.__class__.__tablename__]:
                if self.id == row[ID]:
                    return row[field_name]

        return fget

    @classmethod
    def _create_fset(mcs, field_name, field_type):
        def fset(self, value):
            if not isinstance(value, field_type):
                raise TypeError("field type must be %s not %s" % (field_type, type(value)))

            for row in mcs.__data_storage__[self.__class__.__tablename__]:
                if self.id == row[ID]:
                    row[field_name] = value

        return fset


class Field:
    pass


class IntegerField(Field):
    field_type = int


class TextField(Field):
    field_type = str


class Entity(metaclass=BaseMeta):
    id = IntegerField()


class User(Entity):
    __tablename__ = 'user'
    name = TextField()
    rate = IntegerField()

if __name__ == '__main__':
    pass