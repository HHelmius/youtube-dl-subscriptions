# youtube-dl-subscriptions

Downloads all new videos from your YouTube subscription feeds.


## Requirements

This script requires python3. Additional dependencies can be found in the `requirements.txt` file.


## Usage

Clone the repository

    git clone https://github.com/mewfree/youtube-dl-subscriptions

Install the requirements

    pip install -r requirements.txt

Go to `https://takeout.google.com/takeout/custom/youtube` and export the subsciption data only. Extract it and save it as `subscriptions.csv` in this folder

You can then run the script

    python3 dl.py

A `last.txt` file will be created in order to avoid downloading the same videos on the next run.
