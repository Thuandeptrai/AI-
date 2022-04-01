FROM  arm32v7/python:3.7-slim-buster
WORKDIR /

COPY requirement.txt requirement.txt
RUN pip install --no-cache-dir -r requirement.txt
EXPOSE 5000
COPY . .
CMD [ "python3", "hmm+lstm.py"]

