from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random

#add quotes & imgs to global scope
quotes = [
    "My life is the road, man. I need to keep moving.",
    "The best advice comes from people who don't give advice.",
    "There's two sorts of fear: one you embrace and one you should listen to and turn the other way.",
    "There are three things, to my account, that I need each day. One of them is something to look up to, another is something to look forward to, and another is someone to chase."
    ]

images = [
        "https://cs-people.bu.edu/ralzaid/hw3/static/src/matthew1.jpg",
        "https://cs-people.bu.edu/ralzaid/hw3/static/src/matthew2.jpg",
        "https://cs-people.bu.edu/ralzaid/hw3/static/src/matthew3.jpg",
        "https://cs-people.bu.edu/ralzaid/hw3/static/src/matthew4.jpg"
    ]

def home(request):

    template_name = "quotes/home.html"

    quote = random.choice(quotes)
    image = random.choice(images)

    return render(request, template_name, {'quote': quote, 'image': image})

def random_quote(request):
    return home(request)

def show_all(request):
    context = {
        'quotes': quotes,
        'images': images
    }
    return render(request, 'quotes/show_all.html', context)

def about(request):
    
    template_name = "quotes/about.html"

    context = {
        'person_name': 'Matthew McConaughey',
        'person_bio': (
            'Matthew McConaughey is an American actor and producer, '
            'known for his roles in movies such as "Dallas Buyers Club", '
            '"Interstellar", and "True Detective". He has won numerous awards, '
            'including an Academy Award for Best Actor.'
        )
    }
    return render(request, template_name, context)