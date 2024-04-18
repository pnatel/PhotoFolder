# dockerfile for the REPO
# Or you can use the prebuilt image on hub.docker.com:
# $ docker push pnatel/photo_folder_manager
FROM python:slim

LABEL maintainer=pnatel@gmail.com

ENV hostname=photomanager \
    name=photomanager

# Update aptitude and install software 
RUN apt-get update && apt-get install -y \
    curl \
    git \
# Pillow Pre-requirements
    gcc \
    libjpeg-dev \
    zlib1g-dev

VOLUME [ "/data", "/source", "/destination", "/app" ]

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt && \
    ln -s /destination /app/engine/static && \
    # mv /app/data /data && \
    # ln -s /data /app

EXPOSE 23276

CMD ["sh", "./deploy.sh"]

# Health check steps
HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -ILfSs http://localhost:23276/ > /dev/null || \
      curl -ILfkSs http://localhost:23276/config > /dev/null || exit 1