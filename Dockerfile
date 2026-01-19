FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        git \
        git-lfs \
        openssh-client \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --no-cache-dir --upgrade pip uv

COPY hub-mirror /app/hub-mirror
RUN uv sync --project /app/hub-mirror --frozen

ENV PATH="/app/hub-mirror/.venv/bin:$PATH"

CMD ["hubmirror"]
