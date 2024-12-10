FROM python:3.11-slim



RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu


COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN python load.py