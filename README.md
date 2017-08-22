# Dependency

Python3.5
- json
- csv
- matplotlib 
- facebook
- datetime 

# Usage 

* To record the number of impression, update the token in fbcrawler.py from [here](https://developers.facebook.com/tools/explorer/), (click 'Get Token' -> 'Get User Access Token' to enable related permissions) and run `python fbcrawler_v2.py`. Data of the newest 25 posts will be updated and saved in `record.son`. 

* To plot the line chart of impression for each post in the `record.son`, run `python myplot.py`.(each post's data within its first 96 hours will be plotted)

# Todos

 - [ ] automatically record data at a given time
 - [ ] automatically update the access token.( or get the long-term token?)
