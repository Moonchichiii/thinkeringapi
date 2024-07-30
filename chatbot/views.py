import re
from decouple import config
from django.db.models import Q
from django.middleware.csrf import get_token
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from posts.models import Post
from posts.serializers import PostSerializer
from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from openai import OpenAI


# Create your views here.

# Initialize the OpenAI client
openai_api_key = config('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)

class ChatbotView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_message = request.data.get('message')
        user = request.user

        if not user_message:
            return Response({"error": "No message provided"}, status=status.HTTP_400_BAD_REQUEST)

        context = (
            "You are an assistant for a social media platform. "
            "You can help the user search for posts, update their profile, or create a new post."
        )

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=150
            )
            chatbot_reply = response.choices[0].message.content.strip()

            if "search posts" in user_message.lower():
                query = user_message.split("search posts", 1)[1].strip()
                if query:
                    search_results = self.search_posts(query)
                    chatbot_reply += "\n\nSearch Results:\n" + "\n".join([post.title for post in search_results])
                else:
                    chatbot_reply += "\n\nNo search query provided."
                    return Response({"response": chatbot_reply}, status=status.HTTP_400_BAD_REQUEST)

            elif "update profile" in user_message.lower():
                if not user.is_authenticated:
                    return Response({"error": "Authentication required to update profile"}, status=status.HTTP_401_UNAUTHORIZED)
                data = self.extract_profile_data(user_message)
                if data['bio']:
                    profile_update_response = self.update_profile(user, data)
                    if profile_update_response.status_code == status.HTTP_200_OK:
                        chatbot_reply += f"\n\n{profile_update_response.data['message']}"
                    else:
                        chatbot_reply += "\n\nFailed to update profile."
                        return profile_update_response
                else:
                    chatbot_reply += "\n\nNo valid profile data provided."
                    return Response({"response": chatbot_reply}, status=status.HTTP_400_BAD_REQUEST)

            elif "create post" in user_message.lower():
                if not user.is_authenticated:
                    return Response({"error": "Authentication required to create post"}, status=status.HTTP_401_UNAUTHORIZED)
                data = self.extract_post_data(user_message)
                if data['title'] and data['content']:
                    post_create_response = self.create_post(user, data)
                    if post_create_response.status_code == status.HTTP_201_CREATED:
                        chatbot_reply += f"\n\nPost created: {post_create_response.data['title']}"
                    else:
                        chatbot_reply += "\n\nFailed to create post."
                        return post_create_response
                else:
                    chatbot_reply += "\n\nMissing title or content for the post."
                    return Response({"response": chatbot_reply}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"response": chatbot_reply}, status=status.HTTP_200_OK)
        except Exception:
            # Handle any unexpected errors gracefully
            return Response({"error": "An internal error occurred. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def search_posts(self, query):
        return Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))

    def extract_profile_data(self, message):
        bio_match = re.search(r'bio:\s*([^,]+)', message)
        bio = bio_match.group(1).strip() if bio_match else ''
        return {"bio": bio}

    def extract_post_data(self, message):
        title_match = re.search(r'title:\s*([^,]+)', message)
        content_match = re.search(r'content:\s*([^,]+)', message)
        title = title_match.group(1).strip() if title_match else ''
        content = content_match.group(1).strip() if content_match else ''
        return {"title": title, "content": content}

    def update_profile(self, user, data):
        try:
            profile = Profile.objects.get(user=user)
            serializer = ProfileSerializer(profile, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

    def create_post(self, user, data):
        data['author'] = user.profile.id
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

