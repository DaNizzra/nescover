import streamlit as st
import requests

# Sayfa Konfigürasyonu
st.set_page_config(page_title="Nescover", page_icon="🎬", layout="wide")

# Özel CSS ile biraz şıklık katalım (Butonlar ve kartlar için)
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stTextInput input {
        border-radius: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Oturum Durumu (State) - Kullanıcı postları ve listeleri kaybolmasın diye hafıza
if "posts" not in st.session_state:
    st.session_state.posts = [
        {"user": "Nexus", "category": "Anime", "content": "Berserk'in yeni mangası ne zaman çıkacak bilen var mı?", "likes": 12},
        {"user": "Danz", "category": "Movies", "content": "Interstellar sinemada tekrar izlenir, başyapıt.", "likes": 25}
    ]

if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

# --- SIDEBAR (Menü) ---
st.sidebar.title("🚀 Nescover Hub")
st.sidebar.markdown("Negotiate, Score and Discover")
menu = st.sidebar.radio("Navigation", ["Discover", "Community Posts", "My Score & Watchlist"])

TMDB_API_KEY = "c8c434316d3f3f50889211333d45f435"

# --- 1. DISCOVER SAYFASI ---
if menu == "Discover":
    st.title("🔥 Discover Movies, TV Shows & Anime")
    st.write("Search anything globally and explore details instantly.")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("Search...", placeholder="Type a movie, anime or series name...")
    with col2:
        category_filter = st.selectbox("Category", ["All", "Movie", "TV Series"])

    if search_query:
        url = f"https://api.themoviedb.org/3/search/multi?api_key={TMDB_API_KEY}&query={search_query}"
        response = requests.get(url)
        data = response.json()
        results = data.get("results", [])
        
        if results:
            st.success(f"Found {len(results)} results!")
            cols = st.columns(4)
            for i, item in enumerate(results[:12]):
                with cols[i % 4]:
                    title = item.get("title") or item.get("name") or "No Title"
                    poster_path = item.get("poster_path")
                    vote = item.get("vote_average", 0)
                    media_type = item.get("media_type", "unknown")
                    
                    if poster_path:
                        st.image(f"https://image.tmdb.org/t/p/w500{poster_path}", use_column_width=True)
                    else:
                        st.image("https://via.placeholder.com/300x450?text=No+Image", use_column_width=True)
                        
                    st.markdown(f"**{title}**")
                    st.caption(f"Type: {media_type.upper()} | ⭐ {vote}")
                    
                    # Watchlist'e Ekleme Butonu
                    if st.button(f"Add to Watchlist", key=f"add_{item.get('id')}"):
                        if title not in st.session_state.watchlist:
                            st.session_state.watchlist.append(title)
                            st.toast(f"Added '{title}' to your watchlist!")
        else:
            st.warning("No results found.")

# --- 2. COMMUNITY POSTS (Sosyal Akış & Chat) ---
elif menu == "Community Posts":
    st.title("💬 Nescover Community Feed")
    st.write("Share your thoughts, reviews or theories with other users.")
    
    # Post Atma Formu
    with st.form("post_form"):
        username = st.text_input("Your Username", placeholder="e.g. Danni zra")
        post_category = st.selectbox("Topic Category", ["Anime", "Movies", "TV Series", "General Discussion"])
        post_content = st.text_area("What's on your mind?", placeholder="Write your review, question or thought here...")
        submitted = st.form_submit_button("Post to Community")
        
        if submitted and username and post_content:
            st.session_state.posts.insert(0, {"user": username, "category": post_category, "content": post_content, "likes": 0})
            st.success("Post published successfully!")
        elif submitted:
            st.error("Please fill in both your username and message.")

    st.markdown("---")
    st.subheader("Recent Posts")
    
    # Postları Listeleme
    for i, p in enumerate(st.session_state.posts):
        with st.container():
            st.markdown(f"**@{p['user']}** &nbsp;·&nbsp; `#{p['category']}`")
            st.write(p['content'])
            col_l, col_r = st.columns([1, 10])
            with col_l:
                if st.button(f"❤️ {p['likes']}", key=f"like_{i}"):
                    st.session_state.posts[i]['likes'] += 1
                    st.rerun()
            st.markdown("---")

# --- 3. SCORE & WATCHLIST (Puanlama ve Listeler) ---
elif menu == "My Score & Watchlist":
    st.title("⭐ My Watchlist & Scores")
    st.write("Manage what you want to watch or track your scored content.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📌 Your Watchlist")
        if st.session_state.watchlist:
            for item in st.session_state.watchlist:
                st.markdown(f"- 🎬 {item}")
        else:
            st.info("Your watchlist is empty. Go to Discover and add some items!")
            
    with col2:
        st.subheader("📊 Rate a Title")
        rated_title = st.text_input("Title Name you want to rate")
        user_score = st.slider("Your Score (1 to 10)", 1, 10, 8)
        if st.button("Save Score"):
            st.success(f"Successfully rated '{rated_title}' as {user_score}/10!")
