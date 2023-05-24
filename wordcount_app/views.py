from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from urllib.parse import urlencode
from django.http import JsonResponse
import requests
import json
from bs4 import BeautifulSoup
from django.http import HttpResponse
from urllib.parse import urlparse


def get_word_frequencies(request):
    # Get the URL from the request
    url = request.POST.get('url', request.GET.get('url', ''))
    
    # If the URL is not provided, return an error
    if not url:
        return render(request, 'wordcount.html', {'url': url})
        #return JsonResponse({'error': 'Missing  URL parameter'})
    
    # Check if the URL has a scheme, if not, add it and make the URL valid
    if not urlparse(url).scheme:
        url = 'https://' + url if url.startswith('www.') else 'https://www.' + url
    
    # Make a request to the URL and get the response
    response = requests.get(url)
    
    # If the response is not OK, return an error
    if response.status_code != 200:
        return JsonResponse({'error': 'Could not get the URL'})
    
    # Extract the HTML from the response
    html = response.text
    
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract the text from the HTML
    text = soup.get_text()
    
    # Split the text into words
    words = text.split()
    
    # Create a dictionary to store the words and their frequencies
    word_frequencies = {}
    
    # Loop through the words
    for word in words:
        # If the word is not in the dictionary, add it with a frequency of 0
        if word not in word_frequencies:
            word_frequencies[word] = 0
        # Increment the frequency of the word by 1
        word_frequencies[word] += 1
    
    # Return the word frequencies as JSON
    return JsonResponse(word_frequencies)







