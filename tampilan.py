import graphene
import json
from flask import Flask
from flask_graphql import GraphQLView

app = Flask(__name__)

data = [
    {"id":"1", "title":"buku 1"},
    {"id":"2", "title":"buku 2"},
    {"id":"3", "title":"buku 3"},
    {"id":"4", "title":"buku 4"},
    {"id":"5", "title":"buku 5"},
    {"id":"6", "title":"buku 6"},
    {"id":"7", "title":"buku 7"},
    {"id":"8", "title":"buku 8"}
]

class Book(graphene.ObjectType):
    id = graphene.ID()
    title = graphene.String()

class Query(graphene.ObjectType):
    book = graphene.Field(Book)
    books = graphene.List(Book)
    book_by_id = graphene.Field(Book, id=graphene.ID())
    book_by_title = graphene.Field(Book, title=graphene.String())

    def resolve_book(self, info):
        return Book(id=data[1]['id'], title=data[1]['title'])
    
    def resolve_books(self,info):
        return [Book(id=i['id'], title=i['title']) for i in data]
    
    def resolve_book_by_id(self, info, id):
         for i in data:
             if i["id"] == id:
                 return Book(id=i["id"], title=i['title'])
             
    def resolve_book_by_title(self, info, title):
         for i in data:
             if i["title"] == title:
                 return Book(id=i["id"], title=i['title'])
        
class BookInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()

class CreateBook(graphene.Mutation):
    class Arguments:
        book = graphene.Argument(BookInput)
    
    book = graphene.Field(Book)

    def mutate(self, info, book):
        new_book = {"id": book.id, "title": book.title}
        data.append(new_book)
        return CreateBook(book=Book(id=new_book["id"], title=new_book["title"]))

class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()



schema = graphene.Schema(query=Query, mutation=Mutation)

#a = '''
#{
#    bookById(id: "3") {
#        id
#        title
#   }
#
#    bookByTitle(title: "buku 6") {
#        id
#        title
#    }
#}
#'''
#
#result = schema.execute(a)
#output = json.dumps(result.data,  indent=3)
#print(output)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))


if __name__== '__main__':
    app.run(debug=True)