# Basalam Product Essence Finder

This project offers a fast and efficient method for users to search and find product essences from the Basalam platform. The backend is powered by FastAPI, while the frontend UI is designed using Streamlit. Both components of the project are lightweight, responsive, and easy to deploy.

## Project Structure

- **Backend**: FastAPI server interfacing with a Postgres database to fetch product essence data.
- **Frontend**: Streamlit application that communicates with the FastAPI backend to display search results in a paginated format.

## Features

- **Search Type**: Allows users to search using exact matches or a "like" method that matches products containing the entered essence.
- **Pagination**: Allows users to navigate through large result sets.
- **Interactive UI**: Enables users to input their search criteria and view the results all within a single page.

## How to Setup and Run

### Backend (FastAPI)

1. Install required packages:

```bash
pip install fastapi[all] asyncpg
```


2. Update `config.py` with the appropriate database configurations.

3. Run the FastAPI server:

```bash
uvicorn your_fastapi_filename:app --reload
```


### Frontend (Streamlit)

1. Install required packages:

```bash
pip install streamlit requests
```


2. Run the Streamlit app:

```bash
streamlit run your_streamlit_filename.py
```

vbnet
Copy code

3. Navigate to the provided local URL in your browser (usually `http://localhost:8501/`).

## Usage

1. Open the Streamlit app in your browser.
2. Use the sidebar to select the type of search ("Like" or "Exact").
3. Enter the essence title you wish to search for.
4. Click on "Search" to view the results.
5. Navigate through the results using the "Next" and "Previous" buttons.

## Contributions

Contributions to improve this project are welcome. Please raise an issue or submit a pull request on the GitHub repository.