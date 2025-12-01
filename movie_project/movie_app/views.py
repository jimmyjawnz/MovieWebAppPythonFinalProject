import base64
from io import BytesIO
from random import Random
from django.shortcuts import render
from django.core.paginator import Paginator
import numpy as np
import pandas as pd
from movie_app.models import Movies
import matplotlib.pyplot as mp

# Global Colours
colors = ['blue', 'green', 'red', 'purple', 'yellow', 'orange', 'pink', 'lime','lightblue','dimgray', 'coral', 'cyan']
colors10 = ['blue', 'green', 'red', 'purple', 'yellow', 'orange', 'pink', 'lime','lightblue','cyan']

# Home Page
def home_page(req):
    return render(req, 'index.html', search_processing(req)) # Return base search processing

# Search Page
def search_page(req):
    return render(req, 'search.html', search_processing(req)) # Return base search processing

# Details Page
def details_page(req, show_id):
    # Add check for if the passed id is 'r' or 'random'
    # this will cause a random movie/show to be shown
    if (show_id == 'random' or show_id == 'r'):
        random_id = Random.randint(Random(), 1, 8807)
        record = Movies.objects.all().filter(show_id=f"s{random_id}")[0] # # Grabs the first element of the random id
    else:
        record = Movies.objects.all().filter(show_id=show_id)[0] # Grabs the first element of the matching id
    return render(req, 'details.html', { 'record': record })

# Analytics Page
def analytics_page(req):
    # Collect database data and make it a dataframe
    data = list(Movies.objects.all().values())
    dataframe = pd.DataFrame(data)
    images = [] # for storing the base64 strings for displaying in the DOM

    # Create Graph for Movies/Shows over Time
    records_per_year = dataframe['release_year'].value_counts().sort_index()
    images.append(create_graph(records_per_year.index, records_per_year.values, 'line', 
        'Time (years)', '', 'Movie/Show Release Distribution over Time'))

    # Create Graph for Shows per Age Rating
    records_per_ageRating = dataframe['age_rating'].value_counts().sort_values().nlargest(10)
    images.append(create_graph(records_per_ageRating.values, records_per_ageRating.index, 'pie', 
        '', '', 'Percent of Movies/Shows per Age Rating (Top 10)'))

    # Create Graph for Directors with most Movies
    records_per_director = dataframe['director'].value_counts().sort_values().nlargest(10)
    images.append(create_graph(records_per_director.index, records_per_director.values, 'barh', 
        '', '', 'Directors with most Movies/Shows Directed (Top 10)'))
    
    return render(req, 'graphs.html', { 'images': images})

## Search Process
def search_processing(req):
    # Get all the passed query parameters
    query = req.GET.get('q', '')
    search_by = req.GET.get('search_by', '')
    year_filter = req.GET.get('year', '')
    country_filter = req.GET.get('country', '')
    genre_filter = req.GET.get('genre', '')
    page_num = req.GET.get("page")

    # Get movies from database
    results = Movies.objects.all().order_by('title')

    # Checks if user is searching something specific
    # whether by title, director, or cast
    if query:
        if search_by == "cast":
            results = results.filter(cast__icontains=query)
        elif search_by == "director":
            results = results.filter(director__icontains=query)
        else:
            results = results.filter(title__icontains=query)
    
    # Sets up available years based on query
    years = results.values_list().values_list('release_year', flat=True).distinct().order_by('-release_year')

    # Sets up countries as a filter option based on query
    countries = parse_strings(results, 'country')

    # Sets up genres as a filter option based on the query
    genres = parse_strings(results, 'listed_in')

    # Get and filter based on year, country, and genre
    if year_filter:
        results = results.filter(release_year=year_filter)
    if country_filter:
        results = results.filter(country__icontains=country_filter)
    if genre_filter:
        results = results.filter(listed_in__icontains=genre_filter)

    # Set up pagination of 25 entries per page
    paginator = Paginator(results, 25)
    page_obj = paginator.get_page(page_num)

    # Returns object of response results
    return {
        'results': results,
        'page_obj': page_obj,
        'query': query,
        'years': years,
        'selected_year': year_filter,
        'countries': countries,
        'selected_country': country_filter,
        'search_by': search_by,
        'selected_genre': genre_filter,
        'genres': genres,
    }

## For parsing column results to individual strings for use in filtering
def parse_strings(results, column):
    arr = np.array(list(results.values_list(column, flat=True).distinct()), dtype=str) # Get values from database
    arr = np.char.split(arr, sep=', ')  # Split the multi-values
    arr = np.concatenate(arr) # Join to 1 array
    arr = np.unique(arr) # Get only Unique/Distinct
    arr = arr[arr != 'None'] # Remove any None values
    arr = arr[arr != ''] # Remove any Empty values
    arr.sort() # Order by / Sort
    return arr

## Creates a graph with the given arguments
def create_graph(x, y, gtype, x_label, y_label, title):
    fig, ax = mp.subplots() # Create a figure
    
    # Create a graph based on the type passed (bar, line, pie, etc)
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
    
    # Set Labels and Title
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)

    # Create a tempfile to store the image of the graph in
    # then code it based on base64 for displaying in the dom
    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png', bbox_inches='tight')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    return encoded