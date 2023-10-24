from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Question
from .serializers import QuestionSerializer
import openai  
from decouple import config
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View


# class QuestionListCreateView(generics.ListCreateAPIView):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]


#     def create(self, request, *args, **kwargs):
#         question = request.data.get('query')
#         # Ask the OpenAI model
#         response = ask_openai_model(question)
#         # Use the serializer to create and validate the object
#         serializer = self.get_serializer(data={
#             'query': question,
#             'response': response,
#         })
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)

#         return Response(serializer.data, status=status.HTTP_201_CREATED)
        

    
    
#     def perform_create(self, serializer):
#         serializer.save()



from rest_framework import generics
from .models import Question
from .serializers import QuestionSerializer
from django.shortcuts import render



class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        query = request.data.get('query')

        if query:
            # Ask the OpenAI model
            response = ask_openai_model(query)
            # Create a new question with the query and response
            question = Question(query=query, response=response)
            question.save()

            return Response({'message': 'Question created successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Query is required.'}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save()

    def list(self, request, *args, **kwargs):
        # Fetch all existing questions and their responses
        queryset = Question.objects.all()
        # questions = self.queryset
        # question_responses = [{'query': question.query, 'response': question.response} for question in questions]
        context = {'questions': queryset}

        # Render the 'questionlistcreate.html' template with the context
        return render(request, 'question_list_create.html',context)




def ask_openai_model(question):
    openai.api_key = config('OPENAI_API_KEY')  # Get the API key from environment variables

    response = openai.Completion.create(
        engine="davinci",  # Choose the OpenAI model engine
        prompt=question,
        max_tokens=50,  # Adjust the response length as needed
        temperature=0.7  # Adjust the temperature for creativity
    )

    return response.choices[0].text.strip()

class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]



class UserRegistrationView(View):
    template_name = 'registration/register.html'

    def get(self, request):
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('question-list-create')
        return render(request, self.template_name, {'form': form})
