import streamlit as st
import requests

# Sayfa Ayarları
st.set_page_config(page_title="Nescover", page_icon="🎬", layout="wide")

st.title("🎬 Nescover - Discover & Score")
st.write("Your ultimate hub for movies, TV series, and anime.")

# Arama Çubuğu
search_query = st.text_input("Search for a movie, TV show, or anime...")

if search_query:
    # TMDB API (Ücretsiz test anahtarı veya kendi API key'in)
    url = f"https://api.themoviedb.org/3/search/multi?api_key=c8c434316d3f3f50889211333d45f435&query={search_query}"
    response = requests.get(url)
    data = response.json()
    
    results = data.get("results", [])
    
    if results:
        # Sonuçları yan yana şık kartlar halinde gösterelim
        cols = st.columns(4)
        for i, item in enumerate(results[:8]): # İlk 8 sonucu göster
            with cols[i % 4]:
                title = item.get("title") or item.get("name") or "No Title"
                poster_path = item.get("poster_path")
                vote = item.get("vote_average", 0)
                
                if poster_path:
                    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                    st.image(poster_url, use_column_width=True)
                
                st.subheader(title)
                st.write(f"⭐ Score: {vote}")
    else:
        st.warning("No results found. Try another search!")
