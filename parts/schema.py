import graphene
from graphene_django.types import DjangoObjectType
from .models import Part, Samochod

class PartType(DjangoObjectType):
    class Meta:
        model = Part
        fields = "__all__"

class SamochodType(DjangoObjectType):
    class Meta:
        model = Samochod
        fields = "__all__"

class Query(graphene.ObjectType):
    all_parts = graphene.List(PartType)
    all_samochody = graphene.List(SamochodType)

    def resolve_all_parts(root, info):
        return Part.objects.all()

    def resolve_all_samochody(root, info):
        return Samochod.objects.all()

schema = graphene.Schema(query=Query)
