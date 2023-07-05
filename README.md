# InfoSage Question and Answering Large Language Model
This repository contains code for an application called "InfoSage" that implements a Question and Answering (Q&A) model using the Retriever-Reader approach. The application is built using the Streamlit framework and utilizes several modules and functionalities.

## MainApp.py
* The load_lottieurl function is used to load Lottie animations from a given URL.
* The SessionState class is a custom class used for storing and managing user session information.
* The get_session function retrieves the current user session or creates a new one if it doesn't exist.
* The encrypt_password function takes a password as input and returns its hashed version using the SHA-256 algorithm. This encrypted password is stored in the database.
* The login function handles the login and account creation process. It provides a user interface for entering a username and password, checking their validity, and displaying appropriate messages based on the login status.
* The main function is the main entry point of the application. It first checks if a user session exists and if the user is already logged in. If not, it calls the login function to handle the login process. If the user is logged in, it displays the main application interface.
* The main interface allows users to choose between the "Generative" or "Reader" model type and provides options for entering a URL or uploading a file. Depending on the chosen model type and input source, the code performs scraping, text extraction, or PDF preprocessing to obtain the relevant text data.
* After obtaining the text data, the interface allows users to enter a question and set hyperparameters for the chosen model type. Once the user submits the question and hyperparameters, the corresponding model pipeline is executed, and the answers are displayed.
Finally, the interface provides an option for users to give feedback on the response received. The feedback includes rating the response on a scale of 0-10 and submitting it to the database.
If the user is not logged in, the login function is called to handle the login process and display the login interface.

## Scraper.py
This module contains functions for scraping text data from web pages. It utilizes the requests library to send HTTP GET requests to a given URL and the BeautifulSoup library to parse the HTML content of the web page.
* semmer(ARTICLE, chunk_size): This function takes an article (text) and a chunk size as input. It splits the article into chunks of the specified size, ensuring that the chunks do not split sentences. The function returns a list of chunked text.
* scrap(URL, chunk_size): This function takes a URL and a chunk size as input. It sends a GET request to the URL, retrieves the HTML content of the web page, and uses BeautifulSoup to extract paragraphs `<p> tags` from the content. It then processes the extracted text by removing unnecessary characters and splitting it into chunks using the semmer function. The function returns a pandas DataFrame containing the chunked text and unique IDs for each chunk.

## PDFPreprocess.py
This module provides functions for preprocessing PDF documents. It uses the PyPDF2 library to extract text content from PDF files.
* pdf_reader(file, chunk_size): This function takes a PDF file path and a chunk size as input. It uses the UnstructuredPDFLoader from the langchain.document_loaders module to load the PDF data. Then, it uses a CharacterTextSplitter from the langchain.text_splitter module to split the PDF text into chunks of the specified size. The function returns a pandas DataFrame containing the chunked text and unique IDs for each chunk.

## RetrieverReader.py
This module implements the Retriever-Reader model for question answering using the Haystack library. It includes functions for uploading text data, creating the Retriever and Reader pipelines, and generating answers.
* text_uploader(df): This function takes a pandas DataFrame (df) as input, which contains the text data and unique IDs. It prepares the data for uploading to the Elasticsearch document store by converting each text chunk into a dictionary with the content and metadata. The function writes the documents to the document store and updates the document embeddings using a DensePassageRetriever.
* extractive_pipeline(): This function creates an ExtractiveQAPipeline using a DensePassageRetriever for retrieval and an FARMReader for reading. It configures the models and returns the pipeline.
* generative_pipeline(): This function creates a generative pipeline for question answering. It uses a DensePassageRetriever for retrieval and a PromptNode with a language model for generation. The function configures the pipeline and returns it.

## DatabaseManager.py
This module provides functions for managing user accounts and feedback data using a database implemented using MySQL.
* The logininfo table contains usernames along with their encrypted passwords.
* The prompts table contains usernames, the prompt they entered i.e their question along with their feedback for the answer provided by our model.