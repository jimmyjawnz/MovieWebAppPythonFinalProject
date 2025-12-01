import numpy as np
import pandas as pd
from movie_app.models import Movies

# Loads the Movies/Shows from the netflix titles csv file
# into the database
def load_movie_data():
    df = pd.read_csv("movie_app/netflix_titles.csv")
    df.replace({np.nan: None}, inplace=True)
    df.replace({'nan': None}, inplace=True)
    for _, row in df.iterrows():
        Movies.objects.create(
            show_id=row["show_id"],
            type=row["type"],
            title=row["title"],
            director=row["director"],
            cast=row["cast"],
            country=row["country"],
            date_added=row["date_added"],
            release_year=row["release_year"],
            age_rating=row["rating"],
            duration=row["duration"],
            listed_in=row["listed_in"],
            description=row["description"]
        )
    print("Data Loaded Successfully!")

load_movie_data()