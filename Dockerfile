# Project pins Python 3.9 (see environment.yaml / README)
FROM python:3.9-slim

# Unbuffered stdout so print() progress shows up immediately in `docker run` / `docker compose`
ENV PYTHONUNBUFFERED=1

# Chromium and chromedriver from the same Debian repo, so their versions match.
# --no-install-recommends keeps the layer smaller; apt lists are removed in the same layer.
RUN apt-get update \
    && apt-get install -y --no-install-recommends chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# project3.py reads these to use the system browser/driver instead of webdriver-manager,
# which cannot detect Chromium's version and would try to download a driver at runtime.
ENV CHROME_BIN=/usr/bin/chromium \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Ollama is NOT in this container; the ollama client reads OLLAMA_HOST to find the
# server on the host machine (host.docker.internal works on Docker Desktop).
ENV OLLAMA_HOST=http://host.docker.internal:11434

# Run as a non-root user
RUN useradd --create-home --uid 1000 app
WORKDIR /app

# Copy requirements first so the pip layer is cached until dependencies change.
# requirements-dev.txt adds pytest so the `test` compose service can use this same image.
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY --chown=app:app . .
# Pre-create the output dir owned by app so the non-root user can write results there
RUN mkdir -p /app/output && chown app:app /app /app/output
USER app

# Write results into a directory that docker-compose bind-mounts to ./output on the host
ENV OUTPUT_FILE=/app/output/results.csv

ENTRYPOINT ["python", "project3.py"]
