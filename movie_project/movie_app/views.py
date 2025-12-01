import base64
from io import BytesIO
from random import Random
from django.shortcuts import render
from django.core.paginator import Paginator
import pandas as pd
from movie_app.models import Movies
import matplotlib.pyplot as mp

# Global Colours
colors = ['#FFB950', '#FFAD33', '#FF931F', '#FF7E33', '#FA5E1F', '#EC3F13', '#B81702', '#A50104','#8E0103','#7A0103']
colors10 = ['#FFB950', '#FFAD33', '#FF931F', '#FF7E33', '#FA5E1F', '#EC3F13', '#B81702', '#A50104','#8E0103','#7A0103']

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

# Analytics Page
def analytics_page(req):
    data = list(Movies.objects.all().values())
    dataframe = pd.DataFrame(data).replace('nan', None)
    images = []

    # Create Graph for Shows per Age Rating
    records_per_ageRating = dataframe['age_rating'].value_counts().sort_values().nlargest(10)
    images.append(create_graph(records_per_ageRating.values, records_per_ageRating.index, 'pie', 
        '', '', 'Percent of Shows per Age Rating (Top 10)'))
    
    # Create Graph for Shows over Time
    records_per_year = dataframe['release_year'].value_counts().sort_index()
    images.append(create_graph(records_per_year.index, records_per_year.values, 'line', 
        'Time (years)', '', 'Movie/Show Release Distribution over Time'))

    records_per_director = dataframe['director'].value_counts().sort_values().nlargest(10)
    images.append(create_graph(records_per_director.index, records_per_director.values, 'barh', 
        '', '', 'Directors with most Movies Directed (Top 10)'))
    
    return render(req, 'graphs.html', { 'images': images})

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

    # Set up pagination of 25 entries
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

def create_graph(x, y, gtype, x_label, y_label, title, y2 = []):
    fig, ax = mp.subplots()
    
    match gtype:
        case 'bar':
            ax.bar(x, y)
        case 'barh':
            ax.barh(x, y, color=colors10)
            ax.set_xticks([0, 5, 10, 15, 20])
            ax.invert_yaxis()
        case 'pie':
            ax.pie(x, labels=y, colors=colors, autopct='%1.1f%%')
        case 'hist':
            ax.hist(x, bins=y)
        case _:
            ax.plot(x, y)
            # if (y2.len <= 0):
            #     ax.plot(x, y2)                
                
    
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)

    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png', bbox_inches='tight')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    return encoded