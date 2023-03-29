from rest_framework.serializers import Serializer



class RelatedObjectsUtilsMixinSerializer(Serializer):

    def update_or_create_related(self, serializer_class, field, validated_data, extra_data={}):
        data = validated_data.pop(field, {})
        instance = getattr(self.instance, f"{field}") if self.instance else None

        if data:
            if extra_data:
                data.update(extra_data)
            if 'account' in data:
                data.update({"account": str(data.get("account").uuid)})
            serializer = serializer_class(data=data, instance=instance, context=self.context, partial=self.partial)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()

        validated_data.update({f"{field}_id": instance.id})