# Download All the GIFs from GIPHY

# Overview

Using the GIPHY API, download GIFs from GIPHY.

# Quickstart

<code>python -m get_gifs ./config/giphy.json</code>

# Prerequisites

* GIPHY API Token
* Python 3.8.1

# How To

1. Get a GIPHY API Token
2. Copy that token into the config file (<code>./config/giphy.json</code>)
3. In the config file, update the list of search terms.
4. Run with<br>
<code>python -m get_gifs ./config/giphy.json</code>
	* expect a runtime of about 1 second (by default) per GIF

# Resources

* GIPHY Guide<br>
https://developers.giphy.com/docs/api#quick-start-guide
* GIPHY Documentation<br>
https://developers.giphy.com/docs/resource/
* StackOverflow Help<br>
https://stackoverflow.com/questions/54992629/how-to-save-display-giphy-gif-using-python-api
* i Trick<br>
https://eric.blog/2019/01/12/how-to-download-a-gif-from-giphy/