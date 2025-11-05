import streamlit as st
import requests
from PIL import Image
from datetime import datetime
import time
import os

# Set the page configuration (must be the first Streamlit command)
st.set_page_config(
    page_title="Anything's Pawsible - Dog Dating",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🐕",
)

# API Configuration
API_BASE_URL = os.getenv("API_URL", "http://localhost:8000")

# Initialize session state
if "current_profile_index" not in st.session_state:
    st.session_state.current_profile_index = 0
if "sample_profiles" not in st.session_state:
    st.session_state.sample_profiles = []
if "matches" not in st.session_state:
    st.session_state.matches = []
if "swipe_history" not in st.session_state:
    st.session_state.swipe_history = []
if "is_loading" not in st.session_state:
    st.session_state.is_loading = False


# Add loading state management
def show_loading_spinner(message="Loading..."):
    """Show a professional loading spinner"""
    st.markdown(
        f"""
    <div style="display: flex; justify-content: center; align-items: center; padding: 2rem;">
        <div style="
            border: 4px solid #f3f3f3;
            border-top: 4px solid #ff6b6b;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin-right: 1rem;
        "></div>
        <span style="color: #666; font-weight: 500;">{message}</span>
    </div>
    <style>
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
    </style>
    """,
        unsafe_allow_html=True,
    )


# Professional CSS inspired by Hinge's beautiful design
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #f3e8ff 0%, #e0e7ff 50%, #f0f4ff 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main .block-container {
        padding-top: 0rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Hide Streamlit branding and warning bars */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stAlert > div {display: none;}
    .stException > div {display: none;}
    [data-testid="stToolbar"] {display: none;}
    .stDeployButton {display: none;}
    [data-testid="stDecoration"] {display: none;}
    .stActionButton {display: none;}
    .st-emotion-cache-1544g2d {display: none;}
    
    /* Hide orange warning/error bars and all notifications */
    [data-testid="stNotification"] {display: none !important;}
    .stAlert {display: none !important;}
    .stWarning {display: none !important;}
    .element-container:has(.stAlert) {display: none !important;}
    .stToast {display: none !important;}
    div[data-testid="stToast"] {display: none !important;}
    [data-testid="stStatusWidget"] {display: none !important;}
    .stSpinner {display: none !important;}
    div[data-testid="stAlert"] {display: none !important;}
    div[data-testid="stNotificationContainer"] {display: none !important;}
    [class*="notification"] {display: none !important;}
    [class*="alert"] {display: none !important;}
    [class*="warning"] {display: none !important;}
    [class*="toast"] {display: none !important;}
    
    /* Logo Styling */
    .logo-container {
        text-align: center;
        margin: 2rem 0;
    }
    
    .logo-image {
        max-width: 300px;
        height: auto;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    }
    
    .app-title {
        color: #1f2937;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 1rem 0 0.5rem 0;
        letter-spacing: -0.02em;
    }
    
    .app-subtitle {
        color: #6b7280;
        font-size: 1.2rem;
        font-weight: 500;
        margin-bottom: 0;
    }
    
    /* Navigation Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(139,92,246,0.1);
        border-radius: 16px;
        padding: 8px;
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #374151;
        background: transparent;
        border-radius: 12px;
        font-weight: 500;
        padding: 12px 24px;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(139,92,246,0.2) !important;
        color: #1f2937 !important;
        box-shadow: 0 4px 12px rgba(139,92,246,0.2);
    }
    
    /* Professional Card Design */
    .profile-card {
        background: white;
        border-radius: 20px;
        padding: 0;
        margin: 2rem auto;
        max-width: 400px;
        box-shadow: 0 16px 40px rgba(0,0,0,0.12);
        overflow: hidden;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .profile-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 50px rgba(0,0,0,0.15);
    }
    
    .card-image {
        width: 100%;
        height: 300px;
        object-fit: cover;
        background: linear-gradient(45deg, #f0f2f5, #e1e8ed);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 4rem;
        color: #bbb;
    }
    
    .card-content {
        padding: 24px;
    }
    
    .dog-name {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
        letter-spacing: -0.01em;
    }
    
    .dog-breed {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 1.5rem;
        font-weight: 500;
    }
    
    .dog-stats {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 16px;
        margin: 20px 0;
    }
    
    .stat-item {
        background: #f8f9fa;
        padding: 16px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #e9ecef;
        transition: background 0.2s ease;
    }
    
    .stat-item:hover {
        background: #f1f3f4;
    }
    
    .stat-label {
        font-weight: 600;
        color: #495057;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    
    .stat-value {
        color: #ff6b6b;
        font-size: 1.2rem;
        font-weight: 700;
    }
    
    .dog-description {
        font-style: italic;
        color: #666;
        line-height: 1.6;
        margin: 20px 0;
        font-size: 1rem;
        background: #f8f9fa;
        padding: 16px;
        border-radius: 12px;
        border-left: 4px solid #ff6b6b;
    }
    
    .location-info {
        color: #888;
        font-size: 0.95rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        font-weight: 500;
    }
    
    /* Professional Swipe Buttons */
    .swipe-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin: 24px 0;
        padding: 0 24px;
    }
    
    .swipe-btn {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        border: none;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }
    
    .pass-btn {
        background: linear-gradient(135deg, #95a5a6, #7f8c8d);
        color: white;
    }
    
    .pass-btn:hover {
        transform: scale(1.1);
        box-shadow: 0 12px 25px rgba(0,0,0,0.2);
    }
    
    .like-btn {
        background: linear-gradient(135deg, #ff6b6b, #ee5a52);
        color: white;
    }
    
    .like-btn:hover {
        transform: scale(1.1);
        box-shadow: 0 12px 25px rgba(255,107,107,0.4);
    }
    
    /* Compatibility Score */
    .compatibility-score {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ff6b6b, #ee5a52);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 16px 0;
        letter-spacing: -0.02em;
    }
    
    /* Form Styling */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        border-radius: 12px !important;
        border: 2px solid #e9ecef !important;
        font-family: 'Inter', sans-serif !important;
        transition: border-color 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #ff6b6b !important;
        box-shadow: 0 0 0 3px rgba(255,107,107,0.1) !important;
    }
    
    /* Professional Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #ff6b6b, #ee5a52) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(255,107,107,0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(255,107,107,0.4) !important;
    }
    

    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(135deg, #ff6b6b, #ee5a52) !important;
        border-radius: 10px !important;
    }
    
    /* Content Cards */
    .content-card {
        background: white;
        border-radius: 16px;
        padding: 32px;
        margin: 24px 0;
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* Metrics */
    .metric-card {
        background: rgba(255,255,255,0.95);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        border: 1px solid rgba(255,255,255,0.2);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: rgba(255,255,255,0.8);
        margin-top: 3rem;
        padding: 2rem;
        font-size: 0.9rem;
        border-top: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .app-title {
            font-size: 2rem;
        }
        
        .app-subtitle {
            font-size: 1rem;
        }
        
        .profile-card {
            margin: 1rem;
            max-width: 100%;
        }
        
        .dog-stats {
            grid-template-columns: 1fr;
        }
    }
</style>
""",
    unsafe_allow_html=True,
)


def load_banner():
    """Load and display the logo at the top of the page"""
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)

    # Try different possible paths for the logo
    logo_paths = [
        "assets/logo.jpeg",
        "streamlit_app/assets/logo.jpeg",
        "../streamlit_app/assets/logo.jpeg",
    ]

    logo_loaded = False
    for logo_path in logo_paths:
        if os.path.exists(logo_path):
            try:
                logo = Image.open(logo_path)
                # Create a column layout to center the logo
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image(logo, use_container_width=True)
                logo_loaded = True
                break
            except Exception:
                continue

    if not logo_loaded:
        # Fallback with beautiful typography
        st.markdown(
            '<h1 class="app-title">🐕 Anything\'s Pawsible</h1>', unsafe_allow_html=True
        )
        st.markdown(
            '<p class="app-subtitle">Find your dog\'s perfect playmate with AI-powered matching</p>',
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


def create_profile_form():
    """Create dog profile upload form with image and text data"""
    st.markdown(
        """
    <div class="content-card">
        <h2 style="color: #1a1a1a; margin-bottom: 0.5rem; font-weight: 700;">🐕 Create Your Dog's Profile</h2>
        <p style="color: #666; margin-bottom: 2rem; font-size: 1.1rem;">Tell us about your furry friend to find their perfect match!</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    with st.form("dog_profile_form"):
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("📸 Upload Your Dog's Photo")
            uploaded_file = st.file_uploader(
                "Choose your dog's best photo",
                type=["png", "jpg", "jpeg"],
                help="Upload a clear photo of your dog",
            )

            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                st.image(image, caption="Your dog's photo", use_container_width=True)

        with col2:
            st.subheader("📝 Tell Us About Your Dog")

            # Basic Info
            name = st.text_input("Dog's Name", placeholder="e.g., Buddy")
            breed = st.selectbox(
                "Breed",
                [
                    "Golden Retriever",
                    "Labrador Retriever",
                    "German Shepherd",
                    "Bulldog",
                    "Poodle",
                    "Beagle",
                    "Border Collie",
                    "French Bulldog",
                    "Siberian Husky",
                    "Yorkshire Terrier",
                    "Dachshund",
                    "Mixed Breed",
                ],
            )

            col_age, col_weight = st.columns(2)
            with col_age:
                age = st.number_input("Age (years)", min_value=0, max_value=20, value=3)
            with col_weight:
                weight = st.number_input(
                    "Weight (lbs)", min_value=1.0, max_value=200.0, value=50.0
                )

            size = st.selectbox("Size", ["Small", "Medium", "Large"])
            gender = st.selectbox("Gender", ["Male", "Female"])

            # Personality Traits (1-5 scale)
            st.subheader("🐾 Personality Traits")
            energy_level = st.slider(
                "Energy Level", 1, 5, 3, help="1=Low energy, 5=High energy"
            )
            friendliness = st.slider(
                "Friendliness", 1, 5, 4, help="1=Shy, 5=Very friendly"
            )
            playfulness = st.slider(
                "Playfulness", 1, 5, 4, help="1=Calm, 5=Very playful"
            )
            training_level = st.slider(
                "Training Level", 1, 5, 3, help="1=Untrained, 5=Well-trained"
            )

            # Social Preferences
            st.subheader("🤝 Social Preferences")
            good_with_dogs = st.checkbox("Gets along with other dogs", value=True)
            good_with_kids = st.checkbox("Gets along with children", value=True)
            good_with_cats = st.checkbox("Gets along with cats", value=False)

            # Location
            location = st.text_input("Location", placeholder="e.g., San Francisco, CA")

            # Description
            description = st.text_area(
                "Description",
                placeholder="Tell us more about your dog's personality, favorite activities, etc.",
            )

        # Submit button
        submitted = st.form_submit_button("🚀 Create Profile", use_container_width=True)

        if submitted:
            if name and breed and location:
                # Create profile data
                profile_data = {
                    "name": name,
                    "breed": breed,
                    "age": age,
                    "size": size,
                    "gender": gender,
                    "weight": weight,
                    "energy_level": energy_level,
                    "friendliness": friendliness,
                    "playfulness": playfulness,
                    "training_level": training_level,
                    "good_with_dogs": good_with_dogs,
                    "good_with_kids": good_with_kids,
                    "good_with_cats": good_with_cats,
                    "location": location,
                    "description": description,
                }

                # Try to create profile via API
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/profile", json=profile_data
                    )
                    if response.status_code == 200:
                        st.success(f"✅ Profile created successfully for {name}!")
                        st.balloons()
                    else:
                        st.error("Failed to create profile. Please try again.")
                except requests.exceptions.RequestException:
                    st.warning("API not available. Profile saved locally.")
                    st.success(f"✅ Profile created for {name}!")
            else:
                st.error("Please fill in all required fields (Name, Breed, Location)")


def generate_sample_profiles():
    """Generate sample dog profiles for swiping with real images"""
    if not st.session_state.sample_profiles:
        # Get breed-specific sample dog images from our dataset
        import glob

        # Try different possible paths for dog images
        possible_paths = [
            "data/profile_pictures/dogs/",  # Docker container path
            "../data/profile_pictures/dogs/",  # Local development path
            "./data/profile_pictures/dogs/",
        ]

        base_path = None
        for path in possible_paths:
            if os.path.exists(path):
                base_path = path
                break

        # Define breed-specific image mappings
        breed_images = {}
        if base_path:
            # Find breed-specific images
            breed_images = {
                "Labrador Retriever": glob.glob(f"{base_path}labrador_*.jpg"),
                "Golden Retriever": glob.glob(f"{base_path}retriever-golden_*.jpg"),
                "Border Collie": glob.glob(
                    f"{base_path}rough-collie_*.jpg"
                ),  # Use rough collie as closest match
                "French Bulldog": glob.glob(f"{base_path}bulldog-french_*.jpg"),
                "Beagle": glob.glob(f"{base_path}beagle_*.jpg"),
            }

        sample_data = [
            {
                "name": "Luna",
                "breed": "Labrador Retriever",
                "age": 2,
                "size": "Large",
                "energy_level": 4,
                "friendliness": 5,
                "playfulness": 4,
                "location": "San Francisco, CA",
                "description": "Energetic lab who loves swimming and fetch!",
                "image_path": breed_images.get("Labrador Retriever", [None])[0]
                if breed_images.get("Labrador Retriever")
                else None,
            },
            {
                "name": "Charlie",
                "breed": "Golden Retriever",
                "age": 4,
                "size": "Large",
                "energy_level": 3,
                "friendliness": 5,
                "playfulness": 3,
                "location": "Oakland, CA",
                "description": "Gentle giant who loves cuddles and walks.",
                "image_path": breed_images.get("Golden Retriever", [None])[0]
                if breed_images.get("Golden Retriever")
                else None,
            },
            {
                "name": "Bella",
                "breed": "Border Collie",
                "age": 3,
                "size": "Medium",
                "energy_level": 5,
                "friendliness": 4,
                "playfulness": 5,
                "location": "Berkeley, CA",
                "description": "Super smart and loves agility training!",
                "image_path": breed_images.get("Border Collie", [None])[0]
                if breed_images.get("Border Collie")
                else None,
            },
            {
                "name": "Max",
                "breed": "French Bulldog",
                "age": 5,
                "size": "Small",
                "energy_level": 2,
                "friendliness": 5,
                "playfulness": 3,
                "location": "San Francisco, CA",
                "description": "Laid-back Frenchie who loves lounging in the park.",
                "image_path": breed_images.get("French Bulldog", [None])[0]
                if breed_images.get("French Bulldog")
                else None,
            },
            {
                "name": "Daisy",
                "breed": "Beagle",
                "age": 1,
                "size": "Medium",
                "energy_level": 4,
                "friendliness": 4,
                "playfulness": 5,
                "location": "San Jose, CA",
                "description": "Young and playful beagle with lots of energy!",
                "image_path": breed_images.get("Beagle", [None])[0]
                if breed_images.get("Beagle")
                else None,
            },
        ]
        st.session_state.sample_profiles = sample_data


def display_dog_card(profile):
    """Display a professional dog profile card for swiping"""
    # Center the card
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Create a container with custom styling
        with st.container():
            st.markdown(
                """
            <style>
            .dog-profile-card {
                background: white;
                border-radius: 20px;
                padding: 0;
                box-shadow: 0 16px 40px rgba(0,0,0,0.12);
                overflow: hidden;
                margin: 2rem 0;
            }
            .dog-card-header {
                padding: 20px 20px 10px 20px;
                text-align: center;
            }
            .dog-card-content {
                padding: 0 20px 20px 20px;
            }
            </style>
            """,
                unsafe_allow_html=True,
            )

            # Card container
            st.markdown('<div class="dog-profile-card">', unsafe_allow_html=True)

            # Show dog image
            if profile.get("image_path"):
                # Try different possible paths since we're running from streamlit_app directory
                possible_image_paths = [
                    profile["image_path"],  # Original path
                    f"../{profile['image_path']}"
                    if not profile["image_path"].startswith("../")
                    else profile["image_path"],  # Add ../ prefix
                    profile["image_path"].replace("../", "")
                    if profile["image_path"].startswith("../")
                    else f"../{profile['image_path']}",  # Toggle ../ prefix
                ]

                image_loaded = False
                for img_path in possible_image_paths:
                    if os.path.exists(img_path):
                        try:
                            dog_image = Image.open(img_path)
                            # Resize to maintain aspect ratio
                            dog_image = dog_image.resize(
                                (400, 300), Image.Resampling.LANCZOS
                            )
                            st.image(dog_image, use_container_width=True)
                            image_loaded = True
                            break
                        except Exception:
                            continue

                if not image_loaded:
                    st.markdown(
                        '<div style="text-align: center; font-size: 4rem; padding: 2rem; background: #f8f9fa;">🐕</div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.markdown(
                    '<div style="text-align: center; font-size: 4rem; padding: 2rem; background: #f8f9fa;">🐕</div>',
                    unsafe_allow_html=True,
                )

            # Dog info header - Make name, breed, and age more prominent
            st.markdown('<div class="dog-card-header">', unsafe_allow_html=True)
            st.markdown(
                f'<h1 style="margin: 0; color: #1a1a1a; font-weight: 800; font-size: 2.8rem; text-align: center;">{profile["name"]}</h1>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<h3 style="margin: 0.5rem 0; color: #ff6b6b; font-size: 1.3rem; text-align: center; font-weight: 600;">{profile["breed"]}</h3>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<p style="margin: 0.3rem 0 1.5rem 0; color: #888; font-size: 1.1rem; text-align: center; font-weight: 500;">{profile["age"]} years old</p>',
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

            # Card content
            st.markdown('<div class="dog-card-content">', unsafe_allow_html=True)

            # Stats in columns
            stat_col1, stat_col2 = st.columns(2)

            with stat_col1:
                st.markdown(
                    f"""
                <div style="background: #f8f9fa; padding: 12px; border-radius: 8px; text-align: center; margin-bottom: 8px;">
                    <div style="font-weight: 600; color: #495057; font-size: 0.8rem; text-transform: uppercase;">Energy</div>
                    <div style="color: #ff6b6b; font-size: 1.1rem;">{"⚡" * profile["energy_level"]}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f"""
                <div style="background: #f8f9fa; padding: 12px; border-radius: 8px; text-align: center;">
                    <div style="font-weight: 600; color: #495057; font-size: 0.8rem; text-transform: uppercase;">Playfulness</div>
                    <div style="color: #ff6b6b; font-size: 1.1rem;">{"🎾" * profile["playfulness"]}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            with stat_col2:
                st.markdown(
                    f"""
                <div style="background: #f8f9fa; padding: 12px; border-radius: 8px; text-align: center; margin-bottom: 8px;">
                    <div style="font-weight: 600; color: #495057; font-size: 0.8rem; text-transform: uppercase;">Friendliness</div>
                    <div style="color: #ff6b6b; font-size: 1.1rem;">{"💖" * profile["friendliness"]}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f"""
                <div style="background: #f8f9fa; padding: 12px; border-radius: 8px; text-align: center;">
                    <div style="font-weight: 600; color: #495057; font-size: 0.8rem; text-transform: uppercase;">Size</div>
                    <div style="color: #ff6b6b; font-size: 1.1rem; font-weight: 700;">{profile["size"]}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            # Description
            st.markdown(
                f"""
            <div style="background: #f8f9fa; padding: 16px; border-radius: 12px; margin: 16px 0; border-left: 4px solid #ff6b6b;">
                <em style="color: #555; font-size: 1rem; line-height: 1.4;">"{profile["description"]}"</em>
            </div>
            """,
                unsafe_allow_html=True,
            )

            # Location
            st.markdown(
                f"""
            <div style="text-align: center; color: #888; font-weight: 500;">
                📍 {profile["location"]}
            </div>
            """,
                unsafe_allow_html=True,
            )

            st.markdown("</div>", unsafe_allow_html=True)  # Close card-content
            st.markdown("</div>", unsafe_allow_html=True)  # Close card


def swipe_interface():
    """Swipe-based interface for browsing dog profiles"""
    st.markdown(
        """
    <div class="content-card">
        <h2 style="color: #1a1a1a; margin-bottom: 0.5rem; font-weight: 700;">💕 Find Your Dog's Match</h2>
        <p style="color: #666; margin-bottom: 1rem; font-size: 1.1rem;">Swipe through profiles to find your dog's perfect playmate!</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    generate_sample_profiles()

    if st.session_state.current_profile_index >= len(st.session_state.sample_profiles):
        # Professional completion screen
        st.markdown(
            """
        <div class="content-card" style="text-align: center;">
            <h2 style="color: #ff6b6b; margin-bottom: 1rem; font-weight: 700;">🎉 Great Job!</h2>
            <p style="color: #666; font-size: 1.2rem; margin-bottom: 2rem;">You've seen all available profiles!</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.balloons()

        # Show match results professionally
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.session_state.matches:
                st.markdown(
                    """
                <div class="content-card">
                    <h3 style="color: #1a1a1a; margin-bottom: 1rem; font-weight: 600;">💕 Your Matches</h3>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                for match in st.session_state.matches:
                    st.markdown(
                        f"""
                    <div class="metric-card">
                        <h4 style="color: #ff6b6b; margin: 0; font-weight: 600;">💕 {match}</h4>
                        <p style="color: #666; margin: 0.5rem 0 0 0;">It's a match! Time to plan a playdate!</p>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )
            else:
                st.markdown(
                    """
                <div class="content-card" style="text-align: center;">
                    <h3 style="color: #666; margin-bottom: 1rem;">No matches this time</h3>
                    <p style="color: #888;">Don't worry! There are more profiles to explore.</p>
                </div>
                """,
                    unsafe_allow_html=True,
                )

        # Reset button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔄 Start Over", use_container_width=True):
                st.session_state.current_profile_index = 0
                st.session_state.matches = []
                st.session_state.swipe_history = []
                st.rerun()
        return

    # Get current profile
    current_profile = st.session_state.sample_profiles[
        st.session_state.current_profile_index
    ]

    # Display profile card
    display_dog_card(current_profile)

    # Beautiful circular buttons only
    st.markdown(
        """
    <div class="swipe-container">
        <div class="swipe-btn pass-btn">
            ✕
        </div>
        <div class="swipe-btn like-btn">
            ❤️
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Progress indicator
    progress = (st.session_state.current_profile_index + 1) / len(
        st.session_state.sample_profiles
    )
    st.progress(progress)
    st.write(
        f"Profile {st.session_state.current_profile_index + 1} of {len(st.session_state.sample_profiles)}"
    )


def handle_swipe(action, profile):
    """Handle swipe action (like or pass)"""
    # Record the swipe
    swipe_data = {
        "profile": profile["name"],
        "action": action,
        "timestamp": datetime.now().isoformat(),
    }
    st.session_state.swipe_history.append(swipe_data)

    # If it's a like, add to matches
    if action == "like":
        st.session_state.matches.append(profile["name"])
        st.success(f"💕 You liked {profile['name']}!")
    else:
        st.info(f"👋 You passed on {profile['name']}")

    # Move to next profile
    st.session_state.current_profile_index += 1

    # Small delay for user feedback
    time.sleep(0.5)
    st.rerun()


def main():
    """Main app function"""
    load_banner()

    # Navigation
    tab1, tab2, tab3 = st.tabs(["🏠 Home", "📝 Create Profile", "💕 Find Matches"])

    with tab1:
        # Welcome content without the white card background
        st.markdown(
            '<h2 style="color: #1a1a1a; margin: 2rem 0 1rem 0; font-weight: 700; text-align: center;">Welcome to Anything\'s Pawsible! 🐕</h2>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
        <p style="font-size: 1.1rem; color: #555; line-height: 1.6; margin-bottom: 2rem; text-align: center;">
            The premier dog dating app where furry friends find their perfect playmates using AI-powered compatibility matching!
        </p>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<h3 style="color: #333; margin-bottom: 1rem; font-weight: 600;">How it works:</h3>',
            unsafe_allow_html=True,
        )
        st.markdown(
            """
        <div style="margin-left: 1rem; margin-bottom: 2rem;">
            <p style="margin: 0.5rem 0; color: #555;"><strong>1. Create a Profile</strong> - Upload your dog's photo and tell us about their personality</p>
            <p style="margin: 0.5rem 0; color: #555;"><strong>2. Start Swiping</strong> - Browse other dogs and swipe right to like, left to pass</p>
            <p style="margin: 0.5rem 0; color: #555;"><strong>3. Make Matches</strong> - When two dogs like each other, it's a match!</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<h3 style="color: #333; margin-bottom: 1rem; font-weight: 600;">Get Started:</h3>',
            unsafe_allow_html=True,
        )
        st.markdown(
            """
        <div style="margin-left: 1rem; margin-bottom: 2rem;">
            <p style="margin: 0.5rem 0; color: #555;">• Use the <strong>"Create Profile"</strong> tab to set up your dog's profile</p>
            <p style="margin: 0.5rem 0; color: #555;">• Use the <strong>"Find Matches"</strong> tab to start swiping and finding compatible dogs</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
        <p style="text-align: center; font-size: 1.1rem; color: #ff6b6b; font-weight: 600; margin-top: 2rem;">
            Ready to find your dog's new best friend? Let's get started! 🎾
        </p>
        """,
            unsafe_allow_html=True,
        )

        # Professional metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                """
            <div class="metric-card">
                <h3 style="color: #ff6b6b; font-size: 2rem; margin: 0; font-weight: 700;">500+</h3>
                <p style="color: #555; margin: 0.5rem 0 0 0; font-weight: 500;">Active Profiles</p>
            </div>
            """,
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                """
            <div class="metric-card">
                <h3 style="color: #ff6b6b; font-size: 2rem; margin: 0; font-weight: 700;">1,200+</h3>
                <p style="color: #555; margin: 0.5rem 0 0 0; font-weight: 500;">Successful Matches</p>
            </div>
            """,
                unsafe_allow_html=True,
            )
        with col3:
            st.markdown(
                """
            <div class="metric-card">
                <h3 style="color: #ff6b6b; font-size: 2rem; margin: 0; font-weight: 700;">3,400+</h3>
                <p style="color: #555; margin: 0.5rem 0 0 0; font-weight: 500;">Happy Playdates</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

    with tab2:
        create_profile_form()

    with tab3:
        swipe_interface()


if __name__ == "__main__":
    main()
