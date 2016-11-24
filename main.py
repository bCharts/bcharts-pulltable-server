from flask import Flask
from flask import Response
from flask import request
import os
import googlevision
import base64
from io import BytesIO
from PIL import Image
import csvup
import pandas
import ocrwebservice
import json

app = Flask(__name__)
srv_port = int(os.getenv('PORT', 8000))

@app.route('/', methods=['GET'])
def index():
    return 'Running OK'

@app.route('/pulltableocrwebservice', methods=['POST'])
def pull_table_ocrwebservice():
    crop_upper = float(request.values['top'])
    crop_left = float(request.values['left'])
    crop_width = float(request.values['width'])
    crop_height = float(request.values['height'])

    full_imagesrc = request.values['imagesrc']
    imagesrc = full_imagesrc.split(',', 1)[1]

    image_byte = BytesIO(base64.b64decode(imagesrc))
    org_image = Image.open(image_byte)

    crop_right = crop_width + crop_left
    crop_lower = crop_height + crop_upper

    # Crop image
    cropped_image = org_image.crop((crop_left, crop_upper, crop_right, crop_lower))

    # Resize image
    rs_cropped_image = cropped_image.resize((cropped_image.size[0] * 4, cropped_image.size[1] * 4), Image.ANTIALIAS)

    # Turn image into grayscale
    gr_rs_cropped_image = rs_cropped_image.convert('L')

    # Monochromize image
    bw_rs_cropped_image = gr_rs_cropped_image.point(lambda x: 0 if x < 200 else 255, '1')

    binary_image = BytesIO()
    bw_rs_cropped_image.save(binary_image, format='PNG')

    result_excel_link = ocrwebservice.pull_table(binary_image.getvalue())

    result_code = 'ok'
    result_msg = ''

    resp = Response('')
    resp.headers['Content-Type'] = 'text/plain'
    try:
        xd = pandas.read_excel(result_excel_link, header=None)
        csv = xd.to_csv(header=False, index=False, na_rep='null')
    except OSError:
        result_code = 'error'
        result_msg = 'Excel file is not existed. sample_bcharts.csv file will be substituted.'
        csv_file = open('sample_bcharts.csv', 'r')
        csv = csv_file.read()

    rd_url = csvup.uploade_csv(csv)

    return json.dumps({'result': result_code, 'msg': result_msg, 'url': rd_url})

@app.route('/pulltablegoogle', methods=['POST'])
def pull_table_google():
    crop_upper = float(request.values['top'])
    crop_left = float(request.values['left'])
    crop_width = float(request.values['width'])
    crop_height = float(request.values['height'])

    full_imagesrc = request.values['imagesrc']
    imagesrc = full_imagesrc.split(',', 1)[1]

    image_byte = BytesIO(base64.b64decode(imagesrc))
    org_image = Image.open(image_byte)

    crop_right = crop_width + crop_left
    crop_lower = crop_height + crop_upper

    # Crop image
    cropped_image = org_image.crop((crop_left, crop_upper, crop_right, crop_lower))

    # Resize image
    rs_cropped_image = cropped_image.resize((cropped_image.size[0] * 4, cropped_image.size[1] * 4), Image.ANTIALIAS)

    # Turn image into grayscale
    gr_rs_cropped_image = rs_cropped_image.convert('L')

    # Monochromize image
    bw_rs_cropped_image = gr_rs_cropped_image.point(lambda x: 0 if x < 200 else 255, '1')
    bw_rs_cropped_image.show()

    binary_image = BytesIO()
    bw_rs_cropped_image.save(binary_image, format='PNG')
    bw_rs_cropped_image.save('C:\\Users\\bruce\\Desktop\\source.png', format='PNG')

    result_data = googlevision.analyze_image(binary_image.getvalue())
    result_data[1].save('C:\\Users\\bruce\\Desktop\\result.png', format='PNG')

    resp = Response('')
    resp.headers['Content-Type'] = 'text/plain'
    resp.data = result_data[0]

    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=srv_port)
