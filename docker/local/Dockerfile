# Build from Dockerfile for ARM
# For x86/64 you can use the prebuilt image on hub.docker.com:
# $ docker pull pnatel/photo_folder_manager
FROM python:slim

LABEL maintainer=pnatel@gmail.com \
      focus=local-file

ENV hostname=photomanager \
    name=photomanager

# Update aptitude and install software 
RUN apt-get update && apt-get install -y curl

VOLUME [ "/data", "/source", "/destination" ]

WORKDIR /app

# COPY requirements.txt ./

# RUN pip install --no-cache-dir -r requirements.txt 

COPY . .

RUN pip install --no-cache-dir -r requirements.txt && \
	rm -r /app/engine/static/destination && \
    ln -s /destination /app/engine/static && \
    mv /app/data /data && \
    ln -s /data /app

EXPOSE 23276

CMD ["sh", "./start.sh"]

# Health check steps
HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -ILfSs http://localhost:23276/ > /dev/null || \
      curl -ILfkSs http://localhost:23276/config > /dev/null || exit 1