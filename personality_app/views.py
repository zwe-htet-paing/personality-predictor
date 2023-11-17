from django.shortcuts import render
from .models import TwitterUser

def predict_personality(request):
    if request.method == 'POST':
        # Get Twitter username from the form
        username = request.POST['username']

        # Perform personality prediction using your SVM models
        # Replace the following lines with your actual prediction code
        # For simplicity, I'm assuming you have a function predict_personality(username)
        # that returns a dictionary of personality traits
        personality_traits = predict_personality(username)

        # Save the prediction to the database
        TwitterUser.objects.create(
            username=username,
            openness=personality_traits['openness'],
            conscientiousness=personality_traits['conscientiousness'],
            extraversion=personality_traits['extraversion'],
            agreeableness=personality_traits['agreeableness'],
            neuroticism=personality_traits['neuroticism']
        )

        # Display the results
        return render(request, 'result_.html', {'personality_traits': personality_traits})

    return render(request, 'predict.html')


from django.http import JsonResponse
from . preprocess import clean_text
from . svm_model import predict_traits

def predict_text(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        
        text = clean_text(text)
        prediction = predict_traits(text)
        # Return the prediction as JSON
        # return JsonResponse(prediction)
        return render(request, 'predict_result.html', {'prediction': prediction})
    else:
        return render(request, 'predict_text.html')  # Create a template


def home(request):
    return render(request, 'predict_text.html')

def result(request):
    return render(request, 'base_result.html')

def login(request):
    return render(request, 'login.html')
