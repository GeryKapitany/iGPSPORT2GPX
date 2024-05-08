FROM python:3.12

ADD config.py .
ADD iGPSPORT2GPX.py .
ADD requirements.txt .

RUN pip install -r requirements.txt

RUN mkdir /export

CMD ["python", "./iGPSPORT2GPX.py"]