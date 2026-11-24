"""
Text summarization utility using sumy library.
"""
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import os
import logging # Added this line

# Download required NLTK data on first import
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    try:
        print("NLTK 'punkt' tokenizer not found, attempting to download...")
        nltk.download('punkt', quiet=True)
        print("NLTK 'punkt' tokenizer downloaded successfully.")
    except Exception as e:
        print(f"ERROR: Failed to download NLTK 'punkt' tokenizer: {e}")
        # Summarization functions will need to handle potential downstream errors
        # if the tokenizer is truly missing.

LANGUAGE = "english"
SENTENCES_COUNT = 3  # Number of sentences in summary


def summarize_text(text: str, sentences_count: int = SENTENCES_COUNT) -> str:
    """
    Summarize text using LSA (Latent Semantic Analysis) algorithm.
    
    Args:
        text: The text to summarize
        sentences_count: Number of sentences to include in summary
        
    Returns:
        Summarized text as a string
    """
    if not text or len(text.strip()) < 50:
        return text  # Return original if too short
    
    try:
        parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
        stemmer = Stemmer(LANGUAGE)
        summarizer = LsaSummarizer(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)
        
        summary_sentences = summarizer(parser.document, sentences_count)
        summary = " ".join(str(sentence) for sentence in summary_sentences)
        
        return summary if summary else text
    except Exception as e:
        # If summarization fails, return original text
        logging.error(f"Summarization error: {e}")
        return text


def generate_summary_from_url(url: str, title: str = "") -> str:
    """
    Generate a basic summary from URL and title.
    This is a fallback when full text is not available.
    
    Args:
        url: The URL of the content
        title: The title of the content
        
    Returns:
        A simple summary string
    """
    if title:
        return f"Article: {title}"
    return f"Content from: {url}"
