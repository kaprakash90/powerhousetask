FROM python
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8000
ENV DEBUG_ENABLED False
CMD python manage.py runserver 0.0.0.0:8000
