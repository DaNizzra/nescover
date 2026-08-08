import streamlit as st
import requests

# Sayfa Konfigürasyonu
st.set_page_config(
    page_title="Nescover | Discover & Social",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MODERN VE ŞIK UI İÇİN ÖZEL CSS ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
    }
    .film-card {
        background: #161b22;
        border: 1px solid #30363d;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .stTextInput input, .stSelectbox select, .stTextArea textarea {
        background-color: #1f2937 !important;
        color: white !important;
        border-radius: 8px !important;
        border: 1px solid #374151 !important;
    }
    .stButton button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        padding: 0.5rem 1rem;
        box-shadow: 0 2px 4px rgba(99, 102, 241, 0.4);
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE (HAFIZA) BAŞLATMA ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "posts" not in st.session_state:
    st.session_state.posts = []  # Sahte postlar silindi, tertemiz başladı!
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []
if "ratings" not in st.session_state:
    st.session_state.ratings = {}

TMDB_API_KEY = "c8c434316d3f3f50889211333d45f435"

# --- 1. GİRİŞ VE HESAP EKRANI (AUTH) ---
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center;'>🎬 NESCOVER</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #9ca3af;'>Negotiate, Score and Discover</p>", unsafe_allow_html=True)
        
        tab_login, tab_guest = st.tabs(["🚀 Sign Up / Log In", "👤 Continue as Guest"])
        
        with tab_login:
            user_input = st.text_input("Username", placeholder="Choose a cool username...")
            pass_input = st.text_input("Password", type="password", placeholder="Password...")
            if st.button("Enter Nescover", use_container_width=True):
                if user_input.strip():
                    st.session_state.logged_in = True
                    st.session_state.username = user_input.strip()
                    st.rerun()
                else:
                    st.error("Please enter a valid username.")
                    
        with tab_guest:
            st.write("Just want to explore quickly without an account?")
            if st.button("Enter as Guest", use_container_width=True):
                st.session_state.logged_in = True
                st.session_state.username = "Guest_" + str(randint := 4829)
                st.rerun()
    st.stop()

# --- 2. ANA UYGULAMA (GİRİŞ YAPILDIKTAN SONRA) ---
st.sidebar.title("🌟 Nescover Hub")
st.sidebar.write(f"Logged in as: **@{st.session_state.username}**")

menu = st.sidebar.radio("Navigation", ["🔍 Discover", "💬 Community Feed", "⭐ My Watchlist & Scores"])

if st.sidebar.button("Log Out"):
    st.session_state.logged_in = False
    st.rerun()

# --- DISCOVER BÖLÜMÜ ---
if menu == "🔍 Discover":
    st.title("🔥 Discover Movies, TV Shows & Anime")
    st.markdown("Search through millions of titles powered by live global databases.")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input("Search bar", placeholder="Type e.g. Interstellar, Berserk, Breaking Bad...")
    with col2:
        media_filter = st.selectbox("Filter Type", ["All", "Movie", "TV Series"])

    if query:
        url = f"https://api.themoviedb.org/3/search/multi?api_key={TMDB_API_KEY}&query={query}"
        try:
            response = requests.get(url)
            data = response.json()
            results = data.get("results", [])
            
            if results:
                st.success(f"Found {len(results)} results for '{query}'")
                cols = st.columns(4)
                for i, item in enumerate(results[:12]):
                    with cols[i % 4]:
                        title = item.get("title") or item.get("name") or "No Title"
                        poster_path = item.get("poster_path")
                        vote = item.get("vote_average", 0)
                        media_type = item.get("media_type", "unknown").upper()
                        release_date = item.get("release_date") or item.get("first_air_date") or "N/A"
                        
                        # Şık Kart Yapısı
                        st.markdown("<div class='film-card'>", unsafe_allow_html=True)
                        if poster_path:
                            st.image(f"https://image.tmdb.org/t/p/w500{poster_path}", use_column_width=True)
                        else:
                            st.image("https://via.placeholder.com/300x450?text=No+Poster", use_column_width=True)
                            
                        st.markdown(f"**{title}**")
                        st.caption(f"{media_type} | ⭐ {vote:.1f} | 📅 {release_date[:4]}")
                        
                        if st.button("➕ Watchlist", key=f"w_{item.get('id')}"):
                            if title not in st.session_state.watchlist:
                                st.session_state.watchlist.append(title)
                                st.toast(f"Added '{title}' to watchlist!")
                        st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning("No results found on TMDB. Check your spelling.")
        except Exception as e:
            st.error(f"Connection error: {e}")

# --- COMMUNITY FEED BÖLÜMÜ ---
elif menu == "💬 Community Feed":
    st.title("💬 Nescover Community Feed")
    st.markdown("Share thoughts, reviews, or ask recommendations from others.")
    
    # Post Gönderme Kutusu
    with st.form("new_post_form", clear_on_submit=True):
        category = st.selectbox("Topic", ["General", "Anime Review", "Movie Discussion", "Recommendations"])
        content = st.text_area("What's on your mind?", placeholder="Write your thoughts here...")
        submitted = st.form_submit_button("Publish Post")
        
        if submitted:
            if content.strip():
                st.session_state.posts.insert(0, {
                    "user": st.session_state.username,
                    "category": category,
                    "content": content,
                    "likes": 0
                })
                st.success("Post successfully published!")
            else:
                st.error("Post content cannot be empty.")

    st.markdown("---")
    st.subheader("Recent Community Posts")
    
    if not st.session_state.posts:
        st.info("No posts yet. Be the first one to write something!")
    else:
        for idx, post in enumerate(st.session_state.posts):
            with st.container():
                st.markdown(f"**@{post['user']}** &nbsp;·&nbsp; `#{post['category']}`")
                st.write(post['content'])
                
                col_like, col_space = st.columns([1, 10])
                with col_like:
                    if st.button(f"❤️ {post['likes']}", key=f"like_post_{idx}"):
                        st.session_state.posts[idx]['likes'] += 1
                        st.rerun()
                st.markdown("---")

# --- WATCHLIST & SCORES BÖLÜMÜ ---
elif menu == "⭐ My Watchlist & Scores":
    st.title("⭐ My Personal Hub")
    st.markdown("Track your saved titles and personal scoring history.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📌 Your Watchlist")
        if st.session_state.watchlist:
            for item in st.session_state.watchlist:
                st.markdown(f"- 🎬 **{item}**")
        else:
            st.info("Your watchlist is empty. Go to Discover and add some titles!")
            
    with col2:
        st.subheader("📊 Rate a Title")
        rate_title = st.text_input("Title name to rate", placeholder="e.g. Attack on Titan")
        score_val = st.slider("Score (1 to 10)", 1, 10, 8)
        
        if st.button("Save Rating"):
            if rate_title.strip():
                st.session_state.ratings[rate_title.strip()] = score_val
                st.success(f"Rated '{rate_title}' as {score_val}/10 successfully!")
            else:
                st.error("Please enter a title name.")
                
        if st.session_state.ratings:
            st.markdown("#### Your Rated Titles:")
            for t, s in st.session_state.ratings.items():
                st.markdown(f"- **{t}**: ⭐ {s}/10")
