FROM python:3.11.9-slim-bullseye AS requirements

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PYTHONUNBUFFERED=TRUE

RUN apt-get update && \
    apt-get install --no-install-recommends -y curl libpq-dev && \
    apt-get install -y gcc && \
    apt-get clean && \
    curl -O https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
    python -m venv /home/venv

ENV PATH="/home/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11.9-slim-bullseye AS runtime

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED=TRUE

COPY --from=requirements /home/venv /home/venv
COPY --from=requirements /usr/lib/x86_64-linux-gnu/libpq.so.5 /usr/lib/x86_64-linux-gnu/
COPY --from=requirements /usr/lib/x86_64-linux-gnu/libldap_r-2.4.so.2 /usr/lib/x86_64-linux-gnu/
COPY --from=requirements /usr/lib/x86_64-linux-gnu/liblber-2.4.so.2 /usr/lib/x86_64-linux-gnu/
COPY --from=requirements /usr/lib/x86_64-linux-gnu/libsasl2.so.2 /usr/lib/x86_64-linux-gnu/

ENV PATH="/home/venv/bin:$PATH"

COPY . .

EXPOSE 80
