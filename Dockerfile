FROM python:3.11-slim

COPY . /app
WORKDIR /app

RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install -r requirements.txt
RUN python load.py