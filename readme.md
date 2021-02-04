# Brawl Companion

Brawl Companion is a collection of programs that can help you plan your strategy in playing brawl stars.

## Available Feature

### 1. Trophy League Tracker

Provides information about total trophy after the trophy league ends and trophy details from brawlers who will be affected by the trophy league reset.

### 2. Brawler Recommendation

Provides information about the suitable brawler for a particular map.

## Step-by-step To Run The Program

1. Create virtual environtment

    `python -m venv env`

2. Activate virtual environtment

    `source env/bin/activate`

3. Install requirements

    `pip install -r requirements.txt`

4. Create .env file with token and player_tag variable

    Token can be obtained from the brawl stars API key. Further information about brawl stars API key can be found at https://developer.brawlstars.com/. While player_tag can be obtained from brawl stars player profile.

    The following is an example of an .env file.

    >token = "bearer {token}"<br>
    >player_tag = "{player_tag}"

5. Run program

    `python feature/{script}.py`

    The following is a list of related scripts and features.

    > 1. trophy_league_tracker.py - Trophy League Tracker Feature
    > 2. brawler_recommendation.py - Brawler Recommendation Feature