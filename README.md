# NBA Prop Predictor ⛹️‍♂️:

*Learning to predict play props with Monte Carlo Simulations*

A Discord bot that predicts NBA player performance in their next game using linear regression and Monte Carlo simulation. Users can request a projection for a specific player and statistic, and the bot will provide an interactive visualization with the predicted value and probability distribution.

![donny](https://user-images.githubusercontent.com/96222805/231003184-85800a96-1ebf-41a2-8406-d35fdb23d44f.jpeg)

*Donovan Mitchell after historic 71 point game*

#### Features

- Fetches NBA player data using the NBA API
- Performs linear regression on a player's recent game statistics
- Runs Monte Carlo simulations to generate a probability distribution of predicted performance
- Generates interactive visualizations for the projected statistics and probability distribution
- Provides a Discord command to request player projections

#### Installation and setup

Clone this repository to your local machine.
Install the required dependencies using pip install -r requirements.txt.
Create a .env file in the root directory and add your Discord bot token:

```python
DISCORD_TOKEN=your_bot_token
```

Run the bot with python nbaprops.py

#### Usage

Invite the bot to your Discord server and use the !project_stat command followed by the player's full name, the statistic abbreviation, and optionally, the number of recent games to base the prediction on (default is 5).

Example command:

```python
!project_stat "Draymond Green" P 9
```

Supported statistics abbreviations:

P: Points (PTS)

R: Rebounds (REB)

A: Assists (AST)

PA: Points + Assists (PTS_AST)

PR: Points + Rebounds (PTS_REB)

3P: Three-Point Field Goals Made (FG3M)

The bot will respond with a message containing the predicted performance, probability distribution, and visualizations of the projection and Monte Carlo simulation results.

<img width="440" alt="Screen Shot 2023-03-27 at 10 09 56 AM" src="https://user-images.githubusercontent.com/96222805/228015525-31835d67-8232-4a2b-bd5c-68e878f8bc76.png">

(Draymond Green's Actual Stats This Game: 12 Points)

## Update Log

**APRIL 9TH, 2023**

<img width="872" alt="Screen Shot 2023-04-09 at 8 05 46 PM" src="https://user-images.githubusercontent.com/96222805/230980474-2be169de-6958-4c96-9911-68923528b20f.png">

Updating bot parameters with 2023 NBA Playoff Stats. Predictions expanded from only prop values to team W/L and series scoring predictions.

#### Contributing

Contributions are welcome! Please feel free to open a pull request or create an issue to report bugs or suggest improvements.

I am still actively working on this project and looking to make improvements, feel free to drop any ideas.

https://medium.com/@ethanwchen/nba-sportsbetting-with-data-science-f030ce2327ee
