FROM python:3.10-slim
# taken from https://docs.streamlit.io/deploy/tutorials/kubernetes

RUN groupadd --gid 1000 appuser \
    && useradd --uid 1000 --gid 1000 -ms /bin/bash appuser

RUN pip3 install --no-cache-dir --upgrade \
    pip \
    virtualenv

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git

USER appuser
WORKDIR /home/appuser

COPY . /home/appuser/

ENV VIRTUAL_ENV=/home/appuser/venv
RUN virtualenv ${VIRTUAL_ENV}
RUN . ${VIRTUAL_ENV}/bin/activate && pip install -r requirements.txt


EXPOSE 8501

COPY deploy/run.sh /home/appuser
ENTRYPOINT ["./run.sh"]
