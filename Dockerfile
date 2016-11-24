FROM python:3.4.5
ADD . /bcharts_imgproc
WORKDIR /bcharts_imgproc
RUN pip install -r requirements.txt