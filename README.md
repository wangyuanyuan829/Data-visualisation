# Kowloon‑Rainfall Interactive Rain Curtain Visualisation
This project is an artistic data visualisation of historical daily rainfall records in Hong Kong, built following the artist’s path for assignment 2.
It translates real measured rainfall numbers into an interactive web‑based rain‑curtain animation. The amount of rainfall controls background colour, raindrop count and falling speed, so users can perceive different rainfall moods by selecting historical dates.

<img width="2560" height="1418" alt="image" src="https://github.com/user-attachments/assets/bad28877-8d77-484d-8472-882bd47d97c8" />


## Data source
Raw data comes from **Hong Kong Observatory (HKO) open weather dataset**.
Official open‑data portal: https://data.weather.gov.hk

The original CSV file, saved unchanged inside the `data/` folder, contains daily weather observations. Each row represents one calendar date, including date string and daily total rainfall measured in millimetres (mm). The dataset includes hundreds of daily historical records. The Python script `fetch.py` fetches the source file once and stores the original CSV locally; the program can work fully offline without internet after the first download.

## What this visualisation shows
This artwork maps rainfall values to visual attributes:
- 0 mm (no rain): bright pale background, very few faint raindrops
- 0‑10 mm light rain: soft blue‑toned background, moderate‑quantity slow‑falling raindrops
- 10‑30 mm heavy rain: deeper cool‑blue background, more raindrops with faster falling speed
- ≥30 mm storm: dark gloomy blue background, dense fast‑moving raindrops

Visitors can pick year‑month‑day from dropdown menus to switch between historical weather records, and move the mouse over the rain‑curtain lines to create interactive distortion effects.

### Information discarded during transformation
This visualisation prioritises artistic emotional expression. It discards many original data fields such as temperature, humidity and wind readings. Time‑series continuous trend is not presented; users view only one single day’s data at a time. Exact millimetre values are shown in text label but not encoded precisely into drop‑size, for better visual aesthetic experience.

## Online live demo
Interactive web page hosted by GitHub Pages:
`https://wangyuanyuan829.github.io/Data-visualisation/`

## How to run locally
1. Install uv for python script management
2. Fetch and save raw HKO rainfall source data:
```bash
uv run fetch.py
