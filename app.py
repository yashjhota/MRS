import streamlit as st
import pickle
import requests
import gzip


def fetch_poster(movie_id):
    Response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=762367469701e86cdde3795179d022e3&language=en-US'.format(movie_id))
    data=Response.json()
    poster_path=data['poster_path']
    return "https://image.tmdb.org/t/p/w500"+ poster_path



# Define the recommend function
def recommend(movie):
    try:
        # Find the index of the movie
        movie_index = movies_df[movies_df['title'] == movie].index[0]
        distances = similarity[movie_index]
        
        # Get the indices of the top 5 similar movies
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        
        # Retrieve movie titles
        recommended_movies = []
        recommended_movies_poster=[]
        for i in movies_list:
            movie_id=movies_df.iloc[i[0]].id
               
            recommended_movies.append(movies_df.iloc[i[0]].title)
            #fetch poster from api
            recommended_movies_poster.append(fetch_poster(movie_id))
        return recommended_movies ,recommended_movies_poster
    except IndexError:
        return ["Movie not found in dataset"]

# Load the data
movies_df = pickle.load(open('movie.pkl', 'rb'))  # Ensure this contains a DataFrame with a 'title' column
with gzip.open('compressed.pkl.gz', 'rb') as ifp:
    uncompressed_model = pickle.load(ifp)  # Ensure this is a similarity matrix
similarity =uncompressed_model

# Streamlit UI
st.title("Movie Recommender System")

# Dropdown for selecting movies
option = st.selectbox(
    "Recommend movies based on:",
    movies_df['title'].values,  # Pass the list of titles
)

# Button for recommendations
if st.button("Recommend"):
    names,posters = recommend(option)
    
    col1, col2, col3 ,col4,col5= st.columns(5,vertical_alignment="center")

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
