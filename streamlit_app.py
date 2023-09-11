import streamlit as st
import requests

st.set_page_config(layout="wide")
PAGE_SIZE = 50


def fetch_results(offset, limit, search_type, essence_title):
    response = requests.get(
        f"http://localhost:8000/essence?search_type={search_type}&essence_title={essence_title}&limit={limit}&offset={offset}"  # noqa
    )

    return response.json() if response.status_code == 200 else []


# Initialize or set the session state
if "offset" not in st.session_state:
    st.session_state["offset"] = 0

# UI elements
st.title("Basalam Product Essence Finder")
st.sidebar.title("Search Settings")

search_type = st.sidebar.radio("Search type:", ["Like", "Exact"])
essence_title = st.sidebar.text_input("Enter Essence Title", "")

if st.sidebar.button("Search"):
    st.session_state["offset"] = 0
    results = fetch_results(
        st.session_state["offset"], PAGE_SIZE, search_type, essence_title
    )

# Pagination buttons
if st.button("Next"):
    st.session_state["offset"] += PAGE_SIZE
    results = fetch_results(
        st.session_state["offset"], PAGE_SIZE, search_type, essence_title
    )

if st.session_state["offset"] > 0 and st.button("Previous"):
    st.session_state["offset"] -= PAGE_SIZE
    results = fetch_results(
        st.session_state["offset"], PAGE_SIZE, search_type, essence_title
    )

with open("style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

# Display results
if "results" in locals():
    paginated_results = results
    if paginated_results:
        col1, col2, col3, col4 = st.columns([1, 6, 2, 3])
        col1.write("#")
        col2.write("Product Title")
        col3.write("Essence")
        col4.write("Product URL")
        st.write("---")
        for idx, result in enumerate(paginated_results):
            col1, col2, col3, col4 = st.columns([1, 6, 2, 3])
            col1.write(f"{idx + 1 + st.session_state['offset']}")
            col2.write(f"{result['product_title']}")
            col3.write(f"{result['essence_title']}")
            col4.write(f"[basalam.com/p/{result['id']}]({result['url']})")
    else:
        st.write("No results found.")
