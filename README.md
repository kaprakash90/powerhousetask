# powerhousetask
Programming task for Powerhouse

# Steps to get the app running
1. Clone the repository
2. Run the app in docker with following commands
```
docker build . -t powerhousetask
docker run -p 8000:8000 powerhousetask
```
3. To run the tests execute ```docker run powerhousetask python manage.py test```
