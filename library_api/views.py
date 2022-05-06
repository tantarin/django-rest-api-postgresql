from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from library_api.models import Book, Author
from library_api.serializers import BookSerializer, AuthorSerializer


@api_view(["GET"])
@csrf_exempt
def welcome(request):
    content = {"message": "Welcome to the BookStore!"}
    return JsonResponse(content)


@api_view(["GET"])
@csrf_exempt
def get_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return JsonResponse({'books': serializer.data}, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
@csrf_exempt
def get_authors(request):
    authors = Author.objects.all()
    serializer = AuthorSerializer(authors, many=True)
    return JsonResponse({'authors': serializer.data}, safe=False, status=status.HTTP_200_OK)


@api_view(["POST"])
@csrf_exempt
def add_book(request):
    payload = json.loads(request.body)
    user = request.user
    try:
        author = Author.objects.get(id=payload["author"])
        book = Book.objects.create(
            title=payload["title"],
            description=payload["description"],
            author=author
        )
        serializer = BookSerializer(book)
        return JsonResponse({'books': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PUT"])
@csrf_exempt
def update_book(request, book_id):
    payload = json.loads(request.body)
    try:
        book_item = Book.objects.filter(id=book_id)
        # returns 1 or 0
        book_item.update(**payload)
        book = Book.objects.get(id=book_id)
        serializer = BookSerializer(book)
        return JsonResponse({'book': serializer.data}, safe=False, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["DELETE"])
@csrf_exempt
def delete_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        book.delete()
        return JsonResponse(status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something went wrong'}, safe=False,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)