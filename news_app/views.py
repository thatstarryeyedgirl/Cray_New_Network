from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import NewsSerializer
from .models import News
from django.shortcuts import get_object_or_404

ChiefEditor = get_user_model() # gets the currently active user model which is ChiefEditor in this case


# Create your views here.
class PostNewsView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # only logged-in ChiefEditors/Users can post

    def post(self, request, *args, **kwargs):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": f"Upload failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class EditNewsView(APIView):
    permission_classes = [permissions.IsAuthenticated] # only logged-in ChiefEditors/Users can edit

    def put(self, request, pk):
        # fetch the news by id or return custom message if not found
        try:
            news = News.objects.get(pk=pk)
        except News.DoesNotExist:
            return Response({"error": "Story not found."}, status=status.HTTP_404_NOT_FOUND)

       
        if news.author != request.user:
            return Response(
                {"error": "You are not allowed to edit this news."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = NewsSerializer(news, data=request.data)
        if serializer.is_valid():
            serializer.save() # updates the news in the database (overwrites the old version with new data)
            return Response({"message": "News updated successfully.", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class DeleteNewsView(APIView):
    permission_classes = [permissions.IsAuthenticated] # only logged-in ChiefEditors/Users can delete

    def delete(self, request, pk, *args, **kwargs):
        try:
            news_item = News.objects.get(pk=pk)
        except News.DoesNotExist:
            return Response({"error": "No story found to delete."}, status=status.HTTP_404_NOT_FOUND)

        # only the author can delete the news
        if news_item.author != request.user:
            return Response({"error": "You can only delete news you created."},
                            status=status.HTTP_403_FORBIDDEN)

        # perform delete
        news_item.delete()
        return Response({"message": "News deleted successfully."}, status=status.HTTP_200_OK)
    
    
class NewsListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    # Public endpoint — shows all available news in descending order of creation
    queryset = News.objects.all().order_by("-created_at") # "-" before the created_at means descending order (newest first)
    # gets all the records from the News table (ChiefEditor model)and orders them by creation date
    serializer_class = NewsSerializer # this line tells DRF that when converting News objects to JSON (or receiving JSON), 
    # use the NewsSerializer
    
    
class NewsSearchView(APIView):
    permission_classes = [permissions.AllowAny] # anyone can search news (no authentication needed)

    def get(self, request, *args, **kwargs):
        title = request.query_params.get("title") # gets the title from query parameters e.g. /news/search/?title=some_title

        if title and title.strip():
            title = title.strip() # removes any extra/unwanted spaces before and after the title
            # Search by title or by first letter of title
            if len(title) == 1:
                queryset = News.objects.filter(title__istartswith=title) # search by first letter
            else:
                queryset = News.objects.filter(title__icontains=title) # search within title
        else:
            queryset = News.objects.all() # if no title is provided, return all news

        # Check if any results found
        if not queryset.exists():
            return Response({"message": "No news found matching your search."}, status=status.HTTP_404_NOT_FOUND)
        
        # returns the serialized news data as a JSON response
        serializer = NewsSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
