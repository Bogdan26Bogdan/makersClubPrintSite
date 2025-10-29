# MakersClubPrintSite

A simple site to allow members to submit their files to be printed and to make it easier for the executives to manage all of the prints.

## Running demo

After installing the requirements, navigate to the flask-server folder and run `python app.py`

## Requirements

### Python requirements

Can be installed by running `pip install -r requirements.txt`

- Flask
- Sqlalchemy
- Talisman
- Flask-login
- python-dotenv

### Tailwindcss + Flowbite requirements

The basics can be taken from flowbites flask guide at: https://flowbite.com/docs/getting-started/flask/
A output.css is included for convenience.

Commands in order to generate a new output.css:

1. `npm install tailwindcss @tailwindcss/cli --save-dev`
2. Make sure the static/src/input.css exists
3. `npm install flowbite --save`
4. `npx @tailwindcss/cli -i ./static/src/input.css -o ./static/dist/output.css --watch`

## Tests

Tests can be run by running `python -m unittest discover` while in the flask server folder
