from random import Random
from django.shortcuts import render
from django.core.paginator import Paginator
from movie_app.models import Movies

# Home Page
def home_page(req):
    return render(req, 'index.html', search_processing(req))

# Search Page
def search_page(req):
    return render(req, 'search.html', search_processing(req))

# Details Page
def details_page(req, show_id):
    # Add check for if the passed id is 'r' or 'random'
    # this will cause a random movie/show to be shown
    if (show_id == 'random' or show_id == 'r'):
        random_id = Random.randint(Random(), 1, 8807)
        record = Movies.objects.all().filter(show_id=f"s{random_id}")[0]
    else:
        record = Movies.objects.all().filter(show_id=show_id)[0] # Grabs the first element of the matching id
    return render(req, 'details.html', { 'record': record })

# Search Process
def search_processing(req):
    query = req.GET.get('q', '')
    year_filter = req.GET.get('year', '')
    country_filter = req.GET.get('country', '')
    page_num = req.GET.get("page")

    results = Movies.objects.all().order_by('title')

    if query:
        results = results.filter(title__icontains=query)
    
    # Sets up available years based on query
    years = results.values_list().values_list('release_year', flat=True).distinct().order_by('-release_year')

    # Sets up countries as a filter option based on query
    countries = results.values_list('country', flat=True).distinct() # Get countries from database
    countries = [word for sentence in countries for word in sentence.replace(',', '').split()] # Split the multi-country values
    countries = set(countries) # Remove duplicates
    countries = list(countries) # Transform to a list
    countries.sort() # Order by / sort

    if year_filter:
        results = results.filter(release_year=year_filter)

    if country_filter:
        results = results.filter(country__icontains=country_filter)

    paginator = Paginator(results, 25)
    page_obj = paginator.get_page(page_num)
    return {
        'results': results,
        'page_obj': page_obj,
        'query': query,
        'years': years,
        'selected_year': year_filter,
        'countries': countries,
        'selected_country': country_filter
    }
