from django.shortcuts import render
from movie_app.models import Movies

# Home Page
def home_page(req):
    return render(req, 'index.html')

# Search View
def search_population(req):
    query = req.GET.get('q', '')
    year_filter = req.GET.get('year', '')
    country_filter = req.GET.get('country', '')

    results = Movies.objects.all().order_by('title')

    if query:
        results = results.filter(title__icontains=query)
    
    if year_filter:
        results = results.filter(release_year=year_filter)

    if country_filter:
        results = results.filter(country=country_filter)
    
    years = Movies.objects.values_list('release_year', flat=True).distinct().order_by('-release_year')

    # sets up countries as an option
    countries = Movies.objects.values_list('country', flat=True).distinct().order_by('country')
    countries = [word for sentence in countries for word in sentence.replace(',', '').split()]
    countries = set(countries)
    countries = list(countries)
    countries.sort()

    return render(req, 'search.html', {
        'results': results,
        'query': query,
        'years': years,
        'selected_year': year_filter,
        'countries': countries,
        'selected_country': country_filter
    })
