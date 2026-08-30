from rest_framework import viewsets

from .models import Document
from .serializers import DocumentSerializer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser


class DocumentViewSet(viewsets.ModelViewSet):
    #Create an API controller for Documents. Give it the standard CRUD operations provided by Django REST Framework. When it needs data, work with all Document records in the database. When data needs to move between the API and those records, use DocumentSerializer.

    queryset = Document.objects.all().order_by("-created_at")
    #You're basically configuring the ViewSet: "When you're dealing with documents, use this set of database records."
    # "The database objects this API is working with are all the Document objects."
    # it's like "SELECT * FROM document;" in SQL
    # note that "objects" is a django interface which has methods like "all", "get", "filter", "create" and deals with application's model items.

    serializer_class = DocumentSerializer
    #Use DocumentSerializer to convert between my Django/Python objects and API data

    # by inheritance this class has :
  #  | HTTP | URL | Operation |
 #   | -------- | --------------- | ---------------------------- |
#    | `GET` | ` / documents / ` | Get all documents |
  #  | `POST` | ` / documents / ` | Create   a    document |
    #| `GET` | ` / documents / 5 / ` | Get document  # 5              |
  #  | `PUT` | ` / documents / 5 / ` | Replace document  # 5          |
#    | `PATCH` | ` / documents / 5 / ` | Partially update  document  # 5 |
 #   | `DELETE` | ` / documents / 5 / ` | Delete    document  # 5           |

    parser_classes = [
        JSONParser,
        FormParser,
        MultiPartParser,
    ]
#    Model
#    ↓
#    Serializer
#    ↓
#    JSON
#    response
