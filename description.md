Great — then we’ll include the keyword ingestion from a `.tsv` file in the architecture description. Here's an **updated version of the architecture** with that requirement included:

---

## 📰 Project Overview: Smart News Feed Parser with Semantic Search

This project is a **cron-based RSS news parser** that collects and filters news articles daily from a curated list of RSS feeds. The parser performs **semantic keyword matching** using transformer-based embeddings (e.g., BERT), allowing it to detect relevant news articles even when keywords appear in different forms or contexts.

---

## 📐 System Architecture

### 1. **Scheduler (Cron Job)**

* Runs automatically **every day at 1:00 AM**.
* Launches the news parsing workflow.

### 2. **Keyword Loader from TSV**

* Keywords are loaded from a `.tsv` file with the following format:

  ```
  category<TAB>keyword1,keyword2,keyword3
  economy<TAB>inflation,interest rate,market
  ai<TAB>artificial intelligence,neural networks,deep learning
  ```

* Each row represents a category.

* Keywords are **split by commas**, and grouped by their category.

* These keywords are used to generate **semantic embeddings**.

### 3. **RSS Feed Collector**

* Uses `feedparser` to retrieve news entries from multiple RSS sources, such as:

  * NV.biz
  * Reuters
  * Forbes
  * Bloomberg
  * TechCrunch
  * Wired
* Extracts:

  * `title`
  * `summary` or `description`
  * `categories` (if available)
  * `image` (if present in HTML content)

### 4. **Smart Semantic Filter (BERT Embeddings)**

* Embeds all loaded keywords using `sentence-transformers` (e.g., `all-MiniLM-L6-v2`).
* Embeds each article title.
* Computes **cosine similarity** between each title and the keyword vectors.
* Articles are included if **any similarity > threshold (e.g., 0.6)**.
* Can optionally record which category matched for further use.

### 5. **News Formatter**

* Strips HTML from summaries.
* Extracts the first image URL from content.
* Formats each article into a standardized JSON structure:

```json
{
  "title": "Example News Headline",
  "categories": ["ai", "business"],
  "text": "Clean summary text with optional image",
  "image": "https://example.com/image.jpg"
}
```

### 6. **JSON Storage**

* Saves all relevant filtered articles into a `.json` file.
* File can be named by date (e.g., `2025-05-22-news.json`).

---

## 🧠 Technology Stack

| Component     | Technology                         |
| ------------- | ---------------------------------- |
| Language      | Python                             |
| RSS Parsing   | `feedparser`                       |
| HTML Parsing  | `beautifulsoup4`                   |
| Embeddings    | `sentence-transformers` (BERT)     |
| TSV Reader    | `csv` module with `delimiter='\t'` |
| Scheduling    | `cron` or `APScheduler`            |
| Output Format | JSON                               |

---

## 🔍 Example Keyword File (`keywords.tsv`)

```
politics	Trump,Biden,Putin
finance	gold,money,investments
ai	artificial intelligence,deep learning,neural networks
```

If the title is:
**"Trump said that new artificial intelligent tools help gold miners find money"**
→ It will match the categories: `politics`, `finance`, and `ai`.