ARG PYTHON_VERSION=3.12.7
FROM python:${PYTHON_VERSION}-alpine3.20 as base

WORKDIR /backend

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

COPY ./backend /backend

# Copy aioredis fix for python 3.12
COPY ./fix_aioredis_python3.12/exceptions.py /usr/local/lib/python3.12/site-packages/aioredis/.

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8000", "--proxy-headers", "--workers=4"]