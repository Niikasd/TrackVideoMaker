# TrackVideoMaker
[![Video Demonstration](https://i.imgur.com/85QDRiI.png)](https://www.youtube.com/embed/0fi65QKyT2E  "Video Demonstration")
Trackvideomaker is a tool I made inspired by the genre of graph progress videos such as 'Chess Elo Rating Over time'.

What it does is that it takes the user submitted data from CrashTeamRanking and converts them into individual video frames that can then be merged into a video.

It uses the Pycairo library to draw the frames.

# How to Set Up

I have included the database as of 9.7.2022, as well as current username list and other necessary data to have it run as is.

Prerequisites:
1. Python 3
2. Pycairo (Installing pycairo may require some further prerequisites, read more here: https://pycairo.readthedocs.io/en/latest/getting_started.html)

How to run:
1. Open a command line and move to the directory.
2. Run ```python trackvideomaker.py```.
3. The frames will start appearing in the 'Frames' folder.

NOTE: The program takes hours to finish, as creating the frames is very time intensive.

Customization:
- To change which track or between course and lap records, open "list of track IDs' and change the track ID on line 12.
- Country colors can be modified by opening 'Names_colors' and editing the list with the RGB codes. (Open "List of country IDs" to find which ID is which country).
