# feedbackcontent

Minimal API for Toxic comments


### Usage
    $ gunicorn -w 2 --timeout 90 --bind '0.0.0.0:5000' "feedbackcontent:setup_app()"

### Run tests
    $ nosetests
