FROM continuumio/miniconda3

LABEL author="Simas Janusas, <simjanusas@gmail.com>" description="A text clustering Flask app."

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8080

ENTRYPOINT [ "python3" ]

CMD ["app.py"]