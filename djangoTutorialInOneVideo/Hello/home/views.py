from django.shortcuts import render
from datetime import datetime
from home.models import Contact
from django.contrib import messages
from django.shortcuts import HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import nltk  # noqa: F401
from nltk.corpus import stopwords  # noqa: F401
from nltk.tokenize import sent_tokenize
from transformers import pipeline
from django.http import JsonResponse

# Create your views here.
def index(request):
    context = {
        "variable1":"Harry is great",
        "variable2":"Rohan is great"
    } 
    return render(request, 'index.html', context)
    # return HttpResponse("this is homepage")

def about(request):
    return render(request, 'about.html') 

def services(request):
    return render(request, 'services.html')
 

def contact(request):
    if request.method == "POST":
        
        desc = request.POST.get('desc')
        contact = Contact(desc=desc, date = datetime.today())
        contact.save()
        messages.success(request, 'Your message has been sent!')
    return render(request, 'contact.html')
 



def summarize_paragraph(paragraph):
    # Split the paragraph into smaller chunks of sentences
    sentences = sent_tokenize(paragraph)
    chunk_size = 3  # Number of sentences per chunk, adjust as needed

    # Initialize an empty list to store the summarized chunks
    summarized_chunks = []

    # Process each chunk of sentences
    for i in range(0, len(sentences), chunk_size):
        chunk = ' '.join(sentences[i:i+chunk_size])  # Concatenate sentences to form a chunk

        # Use BERT for extractive summarization
        summarization_pipeline = pipeline("summarization")
        summary = summarization_pipeline(chunk, min_length=50, max_length=100)[0]['summary_text']

        summarized_chunks.append(summary)

    # Concatenate the summarized chunks to form the final summary
    final_summary = ' '.join(summarized_chunks)

    return final_summary

# Django view function to handle summarization requests
def summary(request):
    if request.method == 'POST':
        paragraph = request.POST.get('paragraph')
        # Call the summarize_paragraph function
        summary = summarize_paragraph(paragraph)
        # Return the summary as JSON response
        return JsonResponse({'summary': summary})

    return render(request, 'summary.html')


@login_required(login_url='login')
def HomePage(request):
    return render (request,'index.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        



    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')