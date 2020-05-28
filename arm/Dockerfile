# ARM Dockerfile (tested on Raspberry Pi 4)
FROM python:slim

LABEL maintainer=pnatel@gmail.com

ENV hostname=photomanager
ENV name=photomanager

# Update aptitude with new repo
RUN apt-get update

# Install software 
RUN apt-get install -y git
RUN apt-get install -y curl
# Pillow Pre-requirements
RUN apt-get install -y gcc
RUN apt-get install -y libjpeg-dev
RUN apt-get install -y zlib1g-dev

RUN git clone https://github.com/pnatel/PhotoFolder.git &&  mv /PhotoFolder /app

VOLUME /source

WORKDIR /app

# COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 23276

CMD ["python3", "./main.py"]

# Health check steps
HEALTHCHECK --interval=90s --timeout=3s \
  CMD curl -ILfSs http://localhost:23276/ > /dev/null || \
      curl -ILfkSs http://localhost:23276/config > /dev/null || exit 1
