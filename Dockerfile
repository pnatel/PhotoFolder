# FROM --platform=linux/arm/v7 python:slim
FROM python:slim


LABEL maintainer=pnatel@gmail.com

ENV hostname=photomanager
ENV name=photomanager

# RUN mkdir /source
VOLUME /source

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 23276

CMD ["python3", "./main.py"]

# Health check steps
RUN apt-get update
RUN apt-get install -y curl
HEALTHCHECK --interval=90s --timeout=3s \
  CMD curl -ILfSs http://localhost:23276/ > /dev/null || \
      curl -ILfkSs http://localhost:23276/config > /dev/null || exit 1