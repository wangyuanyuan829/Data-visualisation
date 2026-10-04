# Process

### Design Idea
Traditional data charts focus on reading values. As a designer, I wanted to explore how weather data can create atmosphere and emotional feeling.
The core question: What does this weather feel like?

### Data & Visual Mapping Decision
I selected rainfall from Hong Kong Observatory.
- No axes or number-heavy diagram. I removed chart borders to keep immersive atmosphere.
- Low rainfall: warm, sparse particles, bright background → calm sunny mood
- Heavy rainfall: dark background, massive falling particles → heavy, wet atmosphere

## Tools
- Data source: Hong Kong Observatory rainfall data
- AI assistance: ChatGPT, Doubao (豆包), Gemini — used for brainstorming visual metaphors,
  drafting data-mapping logic, and debugging Python scripts
- Processing & rendering: Python (fetch.py for data collection, plot.py for visualization)
- Version control: Git / GitHub

## Kept
- No axes, no numeric labels — the piece reads as atmosphere, not a data table
- Removed all chart borders and frames to keep the scene immersive
- Particle density and color temperature directly encode rainfall intensity

## Rejected
- Standard bar / line charts — too focused on exact values, killed the mood
- Showing axes ticks, legends, or precise mm readings — broke the immersion
- Color-coding rainfall by a sequential blue scale (looks like every other weather viz) 
