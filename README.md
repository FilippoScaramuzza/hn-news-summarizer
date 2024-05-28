# News Summary Generator

This project contains scripts to extract the most upvoted news in [Hacker News - Best](https://news.ycombinator.com/best).
The script then generates an LLM-powered summary using the `mistralai/Mistral-7B-Instruct-v0.2` model.

## Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/filipposcaramuzza/hn-news-summarizer.git
    cd hn-news-summarizer
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

- To run the main script, use:

    ```bash
    python src/main.py
    ```
    to get the top nwes and then summarize it, or
    ```bash
    python src/main.py --id <id>
    ```
    to get the summary of a specific news.

    The output should be something like this:

    ```bash
    Processing stories: 100%|███████████████████████████████████████████████████████████████████| 480/480 [00:13<00:00, 35.09it/s]
    Title: Cloudflare took down our website
    Score: 928
    Date: 2024-05-26
    URL: https://robindev.substack.com/p/cloudflare-took-down-our-website
    LLM-Powered Summary:
    {
        "topic": "Cloudflare Forcing Businesses to Upgrade to Enterprise Plan",
        "key_points": [
            "📧 Business received unexpected email from Cloudflare asking to upgrade to Enterprise plan.",
            "💬 Sales team contacted multiple times, but no clear explanation given.",
            "🔒 Domains were suddenly taken down after refusal to upgrade.",
            "💔 Business suffered significant downtime and loss of customer trust.",
            "💡 Tips for dealing with Cloudflare: be prepared to switch, don't use custom caching rules, and make backups."
        ],
        "reading_time": "3 minutes"
    }
    ```


## Contributing

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.

## License

This project is licensed under the MIT License.
