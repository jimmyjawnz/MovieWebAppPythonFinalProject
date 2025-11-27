from django.shortcuts import render
from movie_app.models import Movies


# Search View
def search_population(req):
    query = req.GET.get('q', '')
    year_filter = req.GET.get('year', '')

    results = Movies.objects.all()

    if query:
        results = results.filter(title__icontains=query)
    
    if year_filter:
        results = results.filter(release_year=year_filter)
    
    years = Movies.objects.values_list('release_year', flat=True).distinct()

    return render(req, 'search.html', {
        'results': results,
        'query': query,
        'years': years,
        'selected_year': year_filter
    })
