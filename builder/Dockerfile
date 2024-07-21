FROM python:3.10

WORKDIR /usr/src/app/builder

COPY . .
RUN apt update && apt upgrade --yes && \
  apt install pipx --yes && apt upgrade pipx --yes && \
  pipx ensurepath && \
  curl -sSL https://install.python-poetry.org | python3 - && export PATH="/root/.local/bin:$PATH" && echo 'export PATH="/root/.local/bin:$PATH"' >> ~/.bashrc && \
  poetry env use 3.10 && poetry install && \
  export WHISPER_ROOT=/usr/src/app/builder/whisper.cpp && apt install ffmpeg --yes && \
  apt-get install -y sqlite3 && sqlite3 db/local.db -init db/init.sql && sqlite3 db/local.db -init db/migration.sql 

#RUN apt install ffmpeg
CMD [ "poetry" , "shell"  ]
