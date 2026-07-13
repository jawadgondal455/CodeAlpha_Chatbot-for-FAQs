# FAQ Chatbot

A simple NLP-based FAQ chatbot with a desktop GUI. It matches user questions to the most relevant FAQ using TF-IDF vectorization and cosine similarity, then displays the corresponding answer in a chat-style interface.

## Features

- Preprocesses text using NLTK (tokenization, stopword removal, lemmatization)
- Matches user queries to FAQs using TF-IDF + cosine similarity
- Falls back gracefully when no relevant match is found
- Simple, dark-themed Tkinter chat interface
- Easy to customize with your own FAQ dataset

## Project Structure

```
faq_bot/
├── faqs.json          # FAQ dataset (questions and answers)
├── preprocess.py       # Text cleaning and normalization
├── matcher.py           # TF-IDF matching engine
├── chatbot_gui.py       # Tkinter chat interface (entry point)
├── requirements.txt      # Python dependencies
└── README.md
```

## Requirements

- Python 3.8+
- Internet connection (first run only, to download NLTK data)

## Installation

1. Clone or download this project folder.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the chatbot:
```
python chatbot_gui.py
```

On first run, NLTK will automatically download required resources (`punkt`, `stopwords`, `wordnet`). This only happens once.

The GUI will open. Type a question in the input box and press **Enter** or click **Send** to get the best matching answer.

## Customizing FAQs

Edit `faqs.json` to add your own questions and answers, following this format:

```json
[
  {
    "question": "Your question here?",
    "answer": "Your answer here."
  }
]
```

No code changes are needed — the matcher automatically rebuilds its index from the updated file each time it runs.

## How It Works

1. **Preprocessing** (`preprocess.py`): User input and FAQ questions are lowercased, cleaned of punctuation/numbers, tokenized, stripped of stopwords, and lemmatized.
2. **Matching** (`matcher.py`): All FAQ questions are converted into TF-IDF vectors. A user's query is vectorized the same way, and cosine similarity is computed against every FAQ question.
3. **Response**: The FAQ with the highest similarity score is returned as the answer, provided it meets a minimum confidence threshold (default `0.35`). Below that, a fallback message is shown.
4. **Interface** (`chatbot_gui.py`): A Tkinter-based chat window displays the conversation and handles user input.

## Configuration

The similarity threshold can be adjusted in `matcher.py`:

```python
FAQMatcher(faq_path="faqs.json", threshold=0.35)
```

- Lower it if valid questions are being rejected too often.
- Raise it if the bot is returning irrelevant answers.

## Limitations

- Currently supports **English only**. Roman Urdu, Urdu, or other languages are not recognized, since NLTK's stopword list and lemmatizer are English-based.
- Matching quality depends on how closely the FAQ dataset covers real user phrasing — broader datasets give better results.

## Future Improvements

- Add multi-language support via a translation layer (e.g., `deep-translator`)
- Support intent-based matching instead of pure keyword similarity
- Add a web-based interface as an alternative to the desktop GUI
