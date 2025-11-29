from django.shortcuts import render
from movie_app.models import Movies

# Home Page
def home_page(req):
    return render(req, 'index.html', search_processing(req))

# Search Page
def search_page(req):
    return render(req, 'search.html', search_processing(req))

# Search Process
def search_processing(req):
    query = req.GET.get('q', '')
    year_filter = req.GET.get('year', '')
    country_filter = req.GET.get('country', '')

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

    return {
        'results': results,
        'query': query,
        'years': years,
        'selected_year': year_filter,
        'countries': countries,
        'selected_country': country_filter
    }
