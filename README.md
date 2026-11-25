# YouTube Video Search Engine

A simple Information Retrieval system written in Python, built for the exercise
"Ex1: Build a Search Engine Using YouTube Video Data". The full assignment text is in
[assignment/Ex1_BuildASearchEngineUsingYouTubeVideoData.pdf](assignment/Ex1_BuildASearchEngineUsingYouTubeVideoData.pdf).

## What the project is

The goal is to collect a dataset of YouTube videos and build a search engine over
their titles and descriptions. The engine is a Boolean one: a query such as
`(machine OR deep) AND learning` returns the videos that match it.

The assignment is split into eight activities:

| # | Activity | What it produces | Status |
|---|---|---|---|
| 1 | Collect the document collection | A dataset of at least 200 videos | Done (400 videos) |
| 2 | Text processing | A cleaned collection of documents | In progress (step 5 has a bug, see Current state) |
| 3 | Inverted index | For every word, the sorted list of video IDs that contain it, plus its document frequency | Written, cannot run until Activity 2 is fixed |
| 4 | Query parser | A parser for `AND`, `OR`, `NOT` and parentheses that rejects invalid queries | In progress (some invalid queries are accepted) |
| 5 | Boolean search | Query results: matching video IDs, their count, titles and URLs | Written, cannot run until Activity 2 is fixed |
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
├── assignment/
│   └── Ex1_BuildASearchEngineUsingYouTubeVideoData.pdf   the assignment
├── data/
│   └── Dataset.json           the video dataset (Activity 1)
├── src/
│   ├── textprocessing.py      Activity 2
│   ├── inverted_index.py      Activity 3
│   ├── query_parser.py        Activity 4
│   └── boolean_search.py      Activity 5
├── notebooks/                 the submission notebook (not created yet)
└── ir/                        the virtual environment (not shared, see Setup)
```

- All Python modules go in `src/`. They import each other by file name, so they
  must stay in the same folder.
- The dataset stays in `data/`, where the code in `src/` looks for it.
- The Jupyter notebook for the final submission goes in `notebooks/`.

## The dataset

`data/Dataset.json` is a list of 400 YouTube videos on the theme of Artificial
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

Run these commands in PowerShell from inside the project folder:

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
3. Pick `ir\Scripts\python.exe` inside the project folder.

### Packages

| Package | Version in use | Used for |
|---|---|---|
| `nltk` | 3.10.4 | Imported by `textprocessing.py`, which downloads its data packages. None of its text functions are called yet |
| `spacy` and `en_core_web_sm` | 3.8.18 and 3.8.0 | Installed, not used by the code yet |
| `pandas` | 3.1.1 | Installed, not used by the code yet |
| `ipykernel` | 7.4.0 | Running Jupyter notebooks inside the environment |

## Running the code

With the environment active, from inside the project folder:

```powershell
python src\textprocessing.py    # Activity 2
python src\inverted_index.py    # Activity 3
python src\query_parser.py      # Activity 4
python src\boolean_search.py    # Activity 5
```

| Module | Imports from |
|---|---|
| `textprocessing.py` | none of the other modules |
| `inverted_index.py` | `textprocessing.py` |
| `query_parser.py` | none of the other modules |
| `boolean_search.py` | `textprocessing.py`, `inverted_index.py`, `query_parser.py` |

Only `query_parser.py` runs to the end at the moment. The other three stop with
`KeyError: 'unique_words'` (see Current state).

The first run needs an internet connection: `textprocessing.py` downloads the NLTK
data packages `punkt`, `stopwords` and `wordnet` into your user folder. Later runs
only check that they are up to date.

The code finds `data/Dataset.json` relative to its own location, so it works from
any folder as long as `src/` and `data/` stay next to each other.

## Current state

### Text processing (Activity 2)

| Step | Status | How it is done |
|---|---|---|
| 1. Read titles and descriptions | Done | `json.load` on `Dataset.json` |
| 2. Convert to lowercase | Done | `str.lower()` |
| 3. Remove punctuation | Done | Every character that is not a letter, digit, underscore or whitespace is replaced with a space |
| 4. Split into words | Done | `str.split()` on whitespace |
| 5. Handle repeated words | Has a bug | `dict.fromkeys` keeps each word of the title and description once, in `unique_words` |
| 6. Keep a consistent document ID | Done | Each cleaned video keeps its `video_id` |

**Known bug in step 5:** the lines that create `unique_words` are outside the loop,
so they run only for the last video. That video is also added to the collection
twice. The script then stops with `KeyError: 'unique_words'`, and so does every
module that imports it.

Things to know about the current behaviour:

- Punctuation is replaced with a space, so a word is split where the punctuation
  was: `humanity's` becomes `humanity` and `s`, and a URL breaks into several
  small words.
- The `channel` field is cleaned and split in the same way as the title and
  description, although the assignment only asks for those two. It is not part of
  `unique_words`, so it is not searchable.
- The cleaned data exists only in memory while the script runs. Nothing is
  written to disk, and `Dataset.json` is never modified.
- The word lists keep their original order and their repeated words. Activity 7
  (biword index) needs that order.

### Inverted index (Activity 3)

Maps each term to its document frequency (`df`) and its sorted list of video IDs
without duplicates (`doc_ids`). `show_inverted_index` displays chosen terms, or the
10 most frequent ones.

### Query parser (Activity 4)

Converts a query to postfix form with the Shunting-Yard algorithm. Operators are
recognized in upper or lower case.

Known limitations:

- Only mismatched parentheses are rejected by the parser itself. Other errors, such
  as `artificial AND` or two words with no operator, are only caught later by the
  Boolean search.
- Some invalid queries are accepted, such as `artificial NOT` and
  `artificial machine AND`.
- The valid query `NOT NOT data` is rejected during the search.
- Quotation marks are ignored, so phrases are not recognized.

### Boolean search (Activity 5)

Evaluates the postfix query with a stack. `AND`, `OR` and `NOT` each walk through
the sorted posting lists with two pointers. The results show the query, the number
of matches, and the ID, title and URL of each matching video.
