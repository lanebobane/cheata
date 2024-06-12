# Documentation

## About

If you have used Strava or similar public leaderboard apps for timed sports, you have likely encountered some clearly bogus entries. The services usually have a "report suspicious" feature, but some of the entries are so clearly bogus it made me wonder how easy it would be to manipulate and post bogus data. This repository comprise the tools I built to test this out. 

## Usage

You can enter a shell environment by running: 

`python3 -i test_shell.py`

from within the repo. This will open an interactive shell with some test data initialized. You can then import and interact with whatever other data you specify via the file path. 

## Roadmap

1. Add GPS randomization to prevent similarity between reference file and output file. 
2. Create command flags to prevent need for interactive shell. 
3. Recreate some core functionality offered by other similar tools (timing, segments, other stats).