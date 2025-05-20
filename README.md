# LinkedIn Matchmaker

This project is a co-founder matchmaking tool that compares two LinkedIn profiles and generates a playful, insightful match report. It uses AI to analyze professional backgrounds, generate comparison cards, and suggest startup ideas for potential co-founders.

## Features

- Fetches and analyzes LinkedIn profile data
- Compares profiles on multiple professional and personal dimensions
- Generates witty, scroll-worthy comparison cards
- Suggests creative startup ideas for matched pairs
- Asynchronous, fast, and fun to use

## Requirements

- Python 3.8+
- See `requirements.txt` for dependencies

## Installation

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd linkedin-match
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment variables (see `.env.example` if provided).

## Usage

Run the main agent:

```bash
python agent.py
```

You can modify the code to input different LinkedIn profile names and get match results.

## Project Structure

- `agent.py` — Main logic for fetching, comparing, and matching profiles
- `classes.py` — Data models for profiles, cards, and results
- `requirements.txt` — Python dependencies

## Notes

- This project uses AI models and external APIs. Make sure you have the necessary API keys and access rights.
- For best results, use real LinkedIn profile names.
