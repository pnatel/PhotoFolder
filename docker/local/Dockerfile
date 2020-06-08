# Dockerfile (DEVELOPMENT) ARM & x86/x64
FROM python:slim

LABEL maintainer=pnatel@gmail.com \
      focus=local-file \
      platform=MULTI_PLATFORM

ENV hostname=photomanager \
    name=photomanager

# Update aptitude and install software 
RUN apt-get update && apt-get install -y curl

VOLUME /source

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 23276

# CMD ["python3", "./photofolder.py"]
CMD ["sh", "./start.sh"]

# Health check steps
HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -ILfSs http://localhost:23276/ > /dev/null || \
      curl -ILfkSs http://localhost:23276/config > /dev/null || exit 1