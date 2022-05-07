from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from django.views.decorators.csrf import csrf_exempt
from library_api.models import Book, Author
from library_api.serializers import BookSerializer, AuthorSerializer


@api_view(["GET"])
@csrf_exempt
def get_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response({'books': serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
@csrf_exempt
def get_authors(request):
    authors = Author.objects.all()
    serializer = AuthorSerializer(authors, many=True)
    return Response({'authors': serializer.data}, status=status.HTTP_200_OK)


@api_view(["POST", "GET"])
@parser_classes([JSONParser])
@csrf_exempt
def add_book(request):
    if request.method == "POST":
        book = Book.objects.create(
            title=request.data["title"],
            description=request.data["description"],
        )
        serializer = BookSerializer(data=request.data)
        print(serializer)
        if not serializer.is_valid():
            return Response(
                data= serializer.errors,
                status=status.HTTP_404_NOT_FOUND
            )
        return Response({'books': serializer.data}, status=status.HTTP_201_CREATED)
    if request.method == "GET":
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response({'books': serializer.data}, status=status.HTTP_200_OK)


@api_view(["PUT"])
@parser_classes([JSONParser])
@csrf_exempt
def update_book(request, book_id):
    try:
        book_item = Book.objects.filter(id=book_id)
        book_item.update(**request.data)
        book = Book.objects.get(id=book_id)
        serializer = BookSerializer(book)
        return Response({'book': serializer.data}, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response({'error': 'Something terrible went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
@csrf_exempt
def delete_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
