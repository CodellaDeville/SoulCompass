# SoulCompass

SoulCompass is an AI-powered application inspired by The Law of One material, offering channeled insights through two main features:

1. **Ra Chatbot** - An AI trained on The Law of One that responds to questions in a Ra-like manner
2. **Energy Reading Journal** - A tool to log emotions, dreams, and synchronicities and receive insights based on The Law of One

## Features

- Multi-page Streamlit application with intuitive navigation
- Dark mode theme with blues, purples, and dark rusts
- Ra Chatbot with natural language understanding
- Energy Reading Journal with tabbed interface for different entry types
- Comprehensive information about The Law of One material
- Direct integration with lawofone.info content database

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
streamlit run Home.py
```

## Deploying to Streamlit Cloud (Free Account)

1. Fork this repository to your GitHub account
2. Log in to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click "New app"
4. Select your forked repository
5. Select the main branch
6. Set the "Main file path" to `Home.py`
7. Click "Deploy"

**Note**: The first run may take a few minutes as the app builds the Law of One database cache by scraping content from lawofone.info. Subsequent runs will be faster as the database will be cached.

## About The Law of One

The Law of One material consists of 106 conversations, called sessions, between Don Elkins, a professor of physics and UFO investigator, and Ra, speaking through Carla Rueckert. Ra states that it/they are a sixth-density social memory complex that formed on Venus about 2.6 billion years ago.

The Law of One states that there is only one, and that one is the Infinite Creator. All things, all life, all of the creation is part of one original thought.

For more information, visit [lawofone.info](https://www.lawofone.info/).

## Credits

This application is inspired by The Law of One material and is not affiliated with L/L Research or the original authors of The Law of One material.

The Law of One material is copyright 1982, 1984, 1998 L/L Research. The Ra Contact books are copyright 2018 L/L Research and Tobey Wheelock.
