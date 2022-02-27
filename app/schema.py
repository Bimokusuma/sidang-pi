import graphene
from graphene_django import DjangoObjectType
from .models import Record


class RecordType(DjangoObjectType):
    class Meta:
        model = Record
        fields = (
            'id',
            'user',
            'score',
            'score_addition',
            'score_substraction',
            'score_multiplication',
            'score_division',
            'date',
        )
        
class Query(graphene.ObjectType):
    records = graphene.List(RecordType)

    def resolve_records(root, info, **kwargs):
        return Record.objects.all()

schema = graphene.Schema(query=Query)
