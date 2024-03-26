# Seavu
This Python web application is designed for Gebler Tooth Architect's and the management of their IT assets and software using Django running on Heroku.
## Live
Find this application at https://seavu-2d7f288cf2f6.herokuapp.com/inventory
## Local
You can run the application locally on Windows at `http://127.0.0.1:5001/` using the Heroku CLI:
`heroku local --port 5001 -f Procfile.windows`
## Testing
At the project source, for testing run `python manage.py test`.
### Coverage
At the project source, for testing coverage run `coverage  run  --source='.'  manage.py  test` and then run `coverage report`.
## Other
To create a superuser run the following at the project source, `python manage.py createsuperuser`.