from rest_framework.serializers import Field



class RelatedObjectSerializerField(Field):
    serializer_class = None
    pks = []

    def __init__(self, **kwargs):
        self.serializer_class = kwargs.pop('serializer_class')
        self.pks = kwargs.pop('pks', [])

        super().__init__(**kwargs)

    @property
    def instance(self):

        init_source = [self.source]
        if self.parent:
            parent = self.parent
            while True:
                parent_source = parent.source
                if parent_source:
                    init_source.append(parent_source)
                else:
                    break
                parent = parent.parent
        init_source = "_".join(init_source[::-1])

        instance = None
        if self.root.instance:
            instance = getattr(self.root.instance, init_source)

        return instance

    def to_internal_value(self, data):

        for pk in self.pks:
            if hasattr(self.parent, pk):
                data.update({pk: getattr(self.parent, pk)})

        serializer = self.serializer_class(self.instance, data=data, context=self.context, partial=self.root.partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        setattr(self.parent, self.source, instance.id)
        return instance

    def to_representation(self, value):
        return self.serializer_class(value, context=self.context).data
