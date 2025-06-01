# FPL Prediction Dashboard

Fantasy Premier League (FPL) is a massive online fantasy football game with millions of players globally. Despite its popularity, a significant number of teams become "inactive" towards the end of each season, meaning no transfers were made in 5 or more gameweeks. Around 63.1% of teams were deemed inactive by the end of the 2019-2020 season. Many users abandon their squads due to the overwhelming nature of keeping up with matches, analyzing player statistics, and understanding the intricate nuances of football.


This project introduces the FPL Transfer Recommender, an intuitive and user-friendly web application designed to assist casual FPL players in making optimal transfer decisions. Our goal is to simplify the complex process of squad management, allowing users to remain engaged with the league without being bogged down by extensive data analysis or performance reports.

## Getting Started
To launch and run the FPL Transfer Recommender, you will need to:

1. Open two terminals: These can be in VSCode, cmd, or your operating system's equivalent.
2. Install project dependencies: In one terminal, navigate to the main project folder and run `npm install` to install project dependencies.
3. Run the Flask backend: In the same terminal, execute `flask --app backend run` to run the Python Flask backend.
4. Start the Svelte frontend: In the second terminal, `cd` into the folder called `frontend-svelte`, and run `npm run dev`. This will start the frontend server and display the port it's running on; click the displayed link to open the web application.
5. Use the web app: You can now use the web app to enter a squad of players and get transfer recommendations.

**Note**: Paths may need to be configured depending on your environment for both the ML part and the website.

## How to Use?
The FPL Transfer Recommender provides a streamlined experience for FPL managers:

1. Squad Input: Easily input your current 15-player FPL squad, with built-in validation for FPL rules (e.g., 2 goalkeepers, 5 defenders, max 3 players from a single Premier League team).
2. Bank Balance Entry: Specify your available in-game bank balance to ensure realistic transfer recommendations.
3. Top 3 Transfer Recommendations: Receive three optimal player swap suggestions for your squad.
4. Suggested Starting 11: After applying a recommended transfer, the application suggests an ideal 11-player lineup for the upcoming gameweek based on predicted points.

## How it Works?
The FPL Transfer Recommender operates on a robust backend system that leverages machine learning and a sophisticated recommendation algorithm.

- Data Acquisition: The backend fetches real-time player data from the `fantasy.premierleague.com/api/bootstrap-static/` API. This data is then organized into easily usable Python dictionaries and lists.
- ML Model for Point Prediction: A neural network model, trained on historical FPL player data from the 2021-2022, 2022-2023, and 2023-2024 seasons, predicts the future FPL points for each player in the upcoming gameweek. This model utilizes various features including player statistics (minutes played, goals, assists, cards), intrinsic FPL metrics (influence, creativity, threat, ICT Index), bonus points system data, and FPL-specific stats (transfers in/out, total points).
- Optimal Recommendation Algorithm: Our custom algorithm uses the predicted FPL points from the ML model to generate transfer suggestions. It simulates potential player swaps, considering FPL constraints such as position limits, budget, and the maximum of three players from the same Premier League team. The algorithm prioritizes transfers that offer the highest percentage increase in predicted points for your squad.

## Data source

Data source: https://github.com/vaastav/Fantasy-Premier-League/tree/master

This github repository contains historical data obtained from the official API mentioned above.

Bibtex reference of data source:
```
@misc{anand2016fantasypremierleague,
  title = {{FPL Historical Dataset}},
  author = {Anand, Vaastav},
  year = {2022},
  howpublished = {Retrieved August 2022 from \url{https://github.com/vaastav/Fantasy-Premier-League/}}
}
```

## Project Structure
- `backend.py`: Contains the Flask backend code, including the ML model and recommendation algorithm.
- `frontend-svelte/`: Houses the Svelte frontend application.
- `data/`: Contains historical FPL data from the official FPL API.
- `models/`: Contains trained ML models
- `model_training.ipynb`: Contains model training script

## Challenges Faced
Throughout the development of this project, we encountered several challenges:

- ML Model Stability: Initial attempts with a baseline neural network model resulted in unstable training, necessitating the development of a more robust model.
- Data Inconsistencies: Discrepancies between historical data from the GitHub repository used for training and live data from the official FPL API presented challenges in feature utilization.
- Nuanced FPL Constraints: Implementing complex FPL rules and player statistics (e.g., injury reports, player form) into the recommendation algorithm proved difficult.
- Algorithm Validation: Accurately gauging whether the algorithm consistently provides the "absolute best" transfers is challenging due to the nuanced nature of FPL strategy and user preference.
- UI/UX Design: Ensuring a visually appealing and intuitive user interface required significant trial and error with HTML/CSS to prevent unpredictable component shifting and maintain consistent spacing.

## Future Enhancements
- Advanced Transfer Algorithm: Incorporate more nuanced FPL statistics and user preferences (e.g., best points/cost player, position-specific recommendations) into the recommendation algorithm.
- Improved UI/UX: Enhance the visual design to align more closely with the official FPL color scheme (purple and white) and potentially include direct links to the official FPL website for supplementary material.
- Continuous Model Improvement: Further fine-tune the ML model to achieve even lower error rates in point predictions

## Acknowledgements

We thank the teaching staff of CS 4365/6365 (Spring 2025) for giving us the opportunity to work on this project and supporting us along the way.