FROM python:3.9-slim-buster
ARG PAT
COPY . .

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip install --upgrade --extra-index-url https://Quarter-Lib-Old:${PAT}@pkgs.dev.azure.com/viertel/Quarter-Lib-Old/_packaging/Quarter-Lib-Old/pypi/simple/ quarter-lib-old

EXPOSE 8060
ENV IS_CONTAINER=True

CMD ["python", "index.py"]




