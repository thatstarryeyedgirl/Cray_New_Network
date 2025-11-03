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
        # feteched the news by id and ensures only the original author can edit it or return a 403 error if not authorized
        news = get_object_or_404(News, pk=pk)

       
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
        # fetch the news by news id or return 404 if not found
        news_item = get_object_or_404(News, pk=pk)

        # only the author or a staff/admin can delete the news
        if not (news_item.author == request.user or request.user.is_staff or request.user.is_superuser): # checks if the logged-in 
            # user is either the author of the news or has admin/staff privileges
            return Response({"detail": "You do not have permission to delete this news."},
                            status=status.HTTP_403_FORBIDDEN)

        # perform delete
        news_item.delete()
        return Response({"message": "News deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    
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
    
