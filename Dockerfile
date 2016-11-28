FROM python:3.5.2
ADD . /bcharts_imgproc
WORKDIR /bcharts_imgproc
RUN pip install -r requirements.txt