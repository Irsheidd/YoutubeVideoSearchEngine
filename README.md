# YouTube Video Search Engine

A simple Information Retrieval system written in Python, built for the exercise
"Ex1: Build a Search Engine Using YouTube Video Data". The full assignment text is in
[Docs/Ex1_BuildASearchEngineUsingYouTubeVideoData.pdf](Docs/Ex1_BuildASearchEngineUsingYouTubeVideoData.pdf).

## What the project is

The goal is to collect a dataset of YouTube videos and build a search engine over
their titles and descriptions. The engine is a Boolean one: a query such as
`(machine OR deep) AND learning` returns the videos that match it.

The assignment is split into eight activities:

| # | Activity | What it produces | Status |
|---|---|---|---|
| 1 | Collect the document collection | A dataset of at least 200 videos | Done (400 videos) |
| 2 | Text processing | A cleaned collection of documents | In progress |
| 3 | Inverted index | For every word, the sorted list of video IDs that contain it, plus its document frequency | Not started |
| 4 | Query parser | A parser for `AND`, `OR`, `NOT` and parentheses that rejects invalid queries | Not started |
| 5 | Boolean search | Query results: matching video IDs, their count, titles and URLs | Not started |
| 6 | Query optimization and skip pointers | Faster `AND` queries, with a comparison count with and without skip pointers | Not started |
| 7 | Biword index | Exact two-word phrase search, such as `"machine learning"` | Not started |
| 8 | Evaluation | A short report based on at least 10 test queries | Not started |

### Rules from the assignment

- The core algorithms (inverted index, query parser, Boolean search, skip pointers,
  biword index) must be implemented by hand. Libraries may be used for reading
  files, handling text and displaying results, but not an existing search engine
  or inverted-index library.
- The query parser must be a real parser. Splitting the query on spaces is not accepted.
- Operator precedence is: parentheses, then `NOT`, then `AND`, then `OR`.
- The final submission is a Jupyter Notebook (`.ipynb`) containing the code,
  explanations and outputs, together with the original dataset.
- Groups of up to 4 students are allowed.
- Deadline stated in the PDF: Thursday, November 12.

## Folder structure

```
ProjectFolder/
├── README.md
├── .gitignore
├── Docs/
│   ├── Dataset.json                                      the video dataset
│   ├── Ex1_BuildASearchEngineUsingYouTubeVideoData.pdf   the assignment
│   └── textprocessing.py                                 Activity 2 code
└── ir/                                                   the virtual environment (not shared, see Setup)
```

## The dataset

`Docs/Dataset.json` is a list of 400 YouTube videos on the theme of Artificial
Intelligence, from 216 different channels. Every video has the same six fields:

| Field | Description |
|---|---|
| `video_id` | Unique YouTube video ID. Used as the document ID throughout the project. |
| `title` | Video title |
| `description` | Short description snippet, usually cut off with `...` |
| `channel` | Channel name |
| `published_date` | Publication date as `YYYY-MM-DD` |
| `url` | Link to the video |

The file is encoded as UTF-8 and contains non-English text, so it must always be
opened with `encoding="utf-8"`. Without it, Python on Windows fails with a
`UnicodeDecodeError`.

## Setup

The virtual environment folder `ir/` is listed in `.gitignore`, so it is not
shared with the project. Everyone who works on the project creates their own.

You need Python 3.14 (the environment was built with 3.14.3).

Run these commands in PowerShell from inside `ProjectFolder`:

```powershell
# 1. Create the virtual environment in a folder named "ir"
python -m venv ir

# 2. Activate it
ir\Scripts\Activate.ps1

# 3. Install the packages
python -m pip install --upgrade pip
pip install nltk spacy pandas ipykernel

# 4. Download the spaCy English model
python -m spacy download en_core_web_sm
```

When the environment is active, the prompt starts with `(ir)`.

On macOS or Linux, step 2 is `source ir/bin/activate`. The other steps are the same.

### If activation is blocked

PowerShell may refuse to run `Activate.ps1` with the message "running scripts is
disabled on this system". Allow scripts for the current window only, then
activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### Selecting the environment in VS Code

VS Code must use the Python inside `ir/`, not the system Python. Otherwise the
script fails with `ModuleNotFoundError: No module named 'nltk'`.

1. Press `Ctrl+Shift+P`.
2. Choose **Python: Select Interpreter**.
3. Pick `ProjectFolder\ir\Scripts\python.exe`.

### Packages

| Package | Version in use | Used for |
|---|---|---|
| `nltk` | 3.10.4 | Text processing helpers (stop words, tokenizer, stemmer) |
| `spacy` and `en_core_web_sm` | 3.8.18 and 3.8.0 | Installed, not used by the code yet |
| `pandas` | 3.1.1 | Installed, not used by the code yet |
| `ipykernel` | 7.4.0 | Running Jupyter notebooks inside the environment |

## Running the code

With the environment active, from inside `ProjectFolder`:

```powershell
python Docs\textprocessing.py
```

The first run needs an internet connection: the script downloads the NLTK data
packages `punkt`, `stopwords` and `wordnet` into your user folder. Later runs
only check that they are up to date.

The script finds `Dataset.json` relative to its own location, so it works from
any folder as long as the two files stay in the same folder.

## Current state of the text processing (Activity 2)

| Step | Status | How it is done |
|---|---|---|
| 1. Read titles and descriptions | Done | `json.load` on `Dataset.json` |
| 2. Convert to lowercase | Done | `str.lower()` |
| 3. Remove punctuation | Done | Every character that is not a letter, digit, underscore or whitespace is replaced with a space |
| 4. Split into words | Done | `str.split()` on whitespace |
| 5. Handle repeated words | Not done | |
| 6. Keep a consistent document ID | Done | Each cleaned video keeps its `video_id` |

The script currently prints the word lists of the first five titles.

Things to know about the current behaviour:

- Punctuation is replaced with a space, so a word is split where the punctuation
  was: `humanity's` becomes `humanity` and `s`, and a URL breaks into several
  small words.
- The `channel` field is cleaned and split in the same way as the title and
  description, although the assignment only asks for those two.
- The cleaned data exists only in memory while the script runs. Nothing is
  written to disk, and `Dataset.json` is never modified.
- The word lists keep their original order and their repeated words. Activity 7
  (biword index) needs that order, so step 5 should add a separate collection of
  unique words and leave the ordered lists as they are.
