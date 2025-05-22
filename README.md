__❗️vibe-coding project❗️__

# Smart News Feed Parser

A Python-based RSS feed parser that uses semantic search to filter and categorize news articles based on keywords.

## Features

- Automatically collects news from multiple RSS feeds
- Uses BERT-based semantic search to match articles with categories
- Supports custom keyword categories via TSV file
- Runs on a daily schedule (1:00 AM by default)
- Saves filtered articles in JSON format

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure RSS feeds in `config.py`

3. Set up your keywords in `keywords.tsv`:
```
category<TAB>keyword1,keyword2,keyword3
```

## Usage

Run the parser:
```bash
python feed_parser.py
```

The script will:
1. Load keywords from `keywords.tsv`
2. Initialize the BERT model for semantic search
3. Start the scheduler to run daily at 1:00 AM
4. Parse RSS feeds and save matching articles to the `output` directory

## Output

Articles are saved in JSON format in the `output` directory with filenames like `YYYY-MM-DD-news.json`. Each article contains:
- Title
- Categories
- Clean text content
- Image URL (if available)
- Source
- Link
- Publication date

## Configuration

You can modify the following settings in `config.py`:
- RSS feed URLs
- Semantic similarity threshold
- BERT model selection
- Schedule time
- File paths 