# ⚽ SoccerLysis | UEFA Euro 2024 Shot Analysis

An interactive **Streamlit** dashboard for exploring shot data, expected goals (xG), and finishing performance from **UEFA Euro 2024**, built with `pandas`, `matplotlib`, and `mplsoccer`.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B)
![License](https://img.shields.io/badge/License-MIT-green)

## Overview

SoccerLysis lets you filter Euro 2024 shot event data by team, player, and shot outcome, then visualizes:

- A **vertical pitch shot map**, with marker size scaled to xG and color indicating goals vs. non-goals
- Key performance **KPIs**: shots, goals, total xG, average xG per shot, and conversion rate
- A **goals vs. expected goals** snapshot showing over/under-performance relative to xG
- A **shot outcome breakdown** table
- A **player shooting leaderboard** ranked by goals, xG, and shot volume

## Features

- 🎯 Interactive filters for team, player, and shot outcome
- 📊 Real-time KPI cards (shots, goals, xG, conversion rate)
- 🟢 Vertical half-pitch shot map with goal/non-goal color coding
- 📈 Finishing performance snapshot (goals minus xG)
- 🏆 Sortable player leaderboard
- 🎨 Custom dark-themed UI styling

## Demo

<!-- Add a screenshot or GIF of the app here -->
![SoccerLysis Screenshot](https://github.com/XeNoX36/SoccerLysis/blob/main/Soccerlysis.png)

View App: https://soccerlysis-app.streamlit.app/

## Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/<your-username>/soccerlysis.git
   cd soccerlysis
   ```

2. Install the required dependencies:

   ```bash
   pip install streamlit pandas matplotlib mplsoccer
   ```

3. Place the dataset in the project root (see [Data](#data) below).

### Running the App

```bash
streamlit run SoccerLysis_ShotMap_Improved.py
```

The app will open automatically in your browser at `http://localhost:8501`.

## Data

This app expects a CSV file named **`euros_2024_shot_map.csv`** in the same directory as the script (or inside a `Sport_Analysis/` subfolder).

```
your-project/
├── SoccerLysis_ShotMap_Improved.py
└── euros_2024_shot_map.csv
```

The dataset should contain StatsBomb-style shot event data with (at minimum) the following columns:

| Column                | Description                                  |
|-----------------------|-----------------------------------------------|
| `type`                | Event type (filtered to `"Shot"`)              |
| `team`                | Team name                                     |
| `player`              | Player name                                   |
| `location`            | Shot coordinates as a list/array, e.g. `[x, y]` |
| `shot_statsbomb_xg`   | Expected goals (xG) value for the shot         |
| `shot_outcome`        | Outcome of the shot (e.g. `Goal`, `Saved`, `Off T`) |

> If you don't have access to the original dataset, StatsBomb's open Euro 2024 event data is a good starting point.

## Project Structure

```
soccerlysis/
├── SoccerLysis_ShotMap_Improved.py   # Main Streamlit application
├── euros_2024_shot_map.csv           # Shot event dataset (not included)
└── README.md
```

## Tech Stack

- [Streamlit](https://streamlit.io/) — app framework and UI
- [pandas](https://pandas.pydata.org/) — data loading and aggregation
- [matplotlib](https://matplotlib.org/) — plotting backend
- [mplsoccer](https://mplsoccer.readthedocs.io/) — football pitch visualization

## Roadmap

- [ ] Add shot map filtering by match/stage
- [ ] Export filtered data as CSV
- [ ] Add xG timeline / shot sequence view
- [ ] Deploy to Streamlit Community Cloud

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m "Add my feature"`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a pull request

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- Shot event data structure inspired by [StatsBomb](https://statsbomb.com/) open data
- Pitch visualizations powered by [mplsoccer](https://github.com/andrewRowlinson/mplsoccer)
