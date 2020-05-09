FROM python:slim

LABEL maintainer=pnatel@gmail.com

ENV hostname=photomanager
ENV name=photomanager
ENV source=/source

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 88

CMD ["python3", "./main.py"]