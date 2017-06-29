FROM python:2.7.13

RUN echo "America/Los_Angeles" > /etc/timezone

RUN dpkg-reconfigure -f noninteractive tzdata

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["/app/app.py"]