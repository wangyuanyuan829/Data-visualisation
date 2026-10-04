## Data source

Raw data comes from the Hong Kong Observatory (HKO) open weather dataset. Official open-data portal: [https://data.weather.gov.hk](https://data.weather.gov.hk)

The original CSV file, stored unchanged inside the `data/` folder, contains daily weather observations. Each row represents one calendar date, including date information and daily total rainfall measured in millimetres (mm). The dataset includes hundreds of daily historical records.
The Python script `fetch.py` downloads the source file once and saves the original CSV locally; the program can run fully offline without internet access after the initial download.

## What this visualisation shows

This artwork maps rainfall values to visual attributes, guided by colour psychology to express weather mood:

- 0 mm (no rain): bright pale background, very faint raindrops
- 0–10 mm light rain: soft blue-toned background, moderate quantity of slow-falling raindrops
- 10–30 mm heavy rain: deeper cool-blue background, more raindrops with faster falling speed
- ≥30 mm storm: dark gloomy blue background, dense fast-moving raindrops

Visitors can pick year-month-day from dropdown menus to switch between historical weather records, and move the mouse over the rain-curtain lines to create interactive distortion effects.

## Information discarded during transformation

This visualisation prioritises artistic emotional expression. It discards many original data fields such as temperature, humidity and wind readings. Continuous time-series trends are not presented; users view only one single day’s data at a time. Exact millimetre values are shown in a text label but not encoded precisely into drop size, for a better visual aesthetic experience.

## Online live demo

Interactive web page hosted by GitHub Pages: [https://wangyuanyuan829.github.io/Data-visualisation/](https://wangyuanyuan829.github.io/Data-visualisation/)

## How to run locally

1. Install uv for python script management
2. Fetch and save raw HKO rainfall source data:

```
uv run fetch.py
```

3. Generate processed rainfall JSON for web visualisation:

```
uv run plot.py
```

4. Open `docs/index.html` in a web browser to view the interactive artwork.
