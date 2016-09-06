FROM python:3-onbuild
EXPOSE 5000
CMD ["gunicorn", "--timeout 120", "-b 0.0.0.0:5000", "application:app"]