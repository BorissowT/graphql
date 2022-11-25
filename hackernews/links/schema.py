import graphene
from graphene_django import DjangoObjectType
from users.schema import UserType
from graphql import GraphQLError

from links.models import Link, Vote


class LinkType(DjangoObjectType):
    class Meta:
        model = Link


class VoteType(DjangoObjectType):
    class Meta:
        model = Vote


class Query(graphene.ObjectType):
    links = graphene.List(LinkType)
    votes = graphene.List(VoteType)

    def resolve_links(self, info, **kwargs):
        return Link.objects.all()

    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()

#1: Defines a mutation class. Right after, you define the output of the mutation,
# the data the server can send back to the client. The output is defined field by field for learning purposes.
# In the next mutation you’ll define them as just one.

#2: Defines the data you can send to the server, in this case, the links’ url and description.

#3: The mutation method: it creates a link in the database using the data sent by the user,
# through the url and description parameters. After, the server returns the CreateLink class
# with the data just created. See how this matches the parameters set on #1.


#4: Creates a mutation class with a field to be resolved, which points to our mutation defined before.


# ...code
# 1
class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()
    posted_by = graphene.Field(UserType)

    class Arguments:
        url = graphene.String()
        description = graphene.String()

    def mutate(self, info, url, description):
        user = info.context.user or None

        link = Link(
            url=url,
            description=description,
            posted_by=user,
        )
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
            posted_by=link.posted_by,
        )


#4
class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()


class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    link = graphene.Field(LinkType)

    class Arguments:
        link_id = graphene.Int()

    def mutate(self, info, link_id):
        user = info.context.user
        if user.is_anonymous:
            #1
            raise GraphQLError('You must be logged to vote!')

        link = Link.objects.filter(id=link_id).first()
        if not link:
            #2
            raise Exception('Invalid Link!')

        Vote.objects.create(
            user=user,
            link=link,
        )

        return CreateVote(user=user, link=link)


class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
    create_vote = CreateVote.Field()


