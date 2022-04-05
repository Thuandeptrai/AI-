FROM   arm32v7/python:3.7-slim
WORKDIR /

COPY requirement.txt requirement.txt
RUN pip install --index-url=https://www.piwheels.org/simple --no-cache-dir -r requirement.txt
EXPOSE 5000
COPY . .
CMD [ "python3", "hmm+lstm.py"]

