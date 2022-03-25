FROM continuumio/miniconda3

LABEL author="Simas Janusas, <simjanusas@gmail.com>" description="A text clustering Flask app."

WORKDIR /app

COPY . /app

# install requirements
RUN pip install -r requirements.txt

# exposing flask port
EXPOSE 5000

ENTRYPOINT [ "python3" ]

CMD ["app.py"]
