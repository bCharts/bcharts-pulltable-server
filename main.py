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
from TableDetection import tbdetection
from TableDetection import tbdutil
import cv2
import numpy as np
import historymanager
import settingsmanager

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


@app.route('/pulltable', methods=['POST'])
def pull_table():
    crop_top = int(request.values['top'])
    crop_left = int(request.values['left'])
    crop_width = int(request.values['width'])
    crop_height = int(request.values['height'])

    full_imagesrc = request.values['imagesrc']
    imagesrc = full_imagesrc.split(',', 1)[1]

    image_byte = base64.b64decode(imagesrc)
    file_bytes = np.fromstring(image_byte, dtype=np.uint8)
    org_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    crop_right = crop_width + crop_left
    crop_bottom = crop_height + crop_top

    # Crop image
    cropped_image = org_image[crop_top:crop_bottom, crop_left:crop_right]

    ret_result_code = 'ok'

    ret, result_csv, result_images = tbdetection.get_csv(cropped_image)
    if ret != 'ok':
        ret_result_code = 'table_detection_err'
        return json.dumps({'result': ret_result_code, 'msg': ''})

    print(result_csv)

    resp = Response('')
    resp.headers['Content-Type'] = 'text/plain'
    ret, rd_url = csvup.uploade_csv(result_csv)
    if ret != 'ok':
        ret_result_code = 'upload_csv_err'

    step_images = []
    for result_image in result_images:
        # tbdutil.show_img_plot(result_image)
        ret, buf = cv2.imencode('.PNG', result_image)
        b64_image = base64.b64encode(buf)
        step_images.append(b64_image.decode('utf-8'))

    b64_result_csv = base64.standard_b64encode(bytearray(result_csv.encode('utf-8'))).decode('utf-8')

    historymanager.insert_new_history(step_images, b64_result_csv)

    return json.dumps({
        'result': ret_result_code,
        'url': rd_url,
        'csv': b64_result_csv,
        'images': {
            'step1': 'data:image/png;base64,' + step_images[0],
            'step2': 'data:image/png;base64,' + step_images[1],
            'step3': 'data:image/png;base64,' + step_images[2],
            'step4': 'data:image/png;base64,' + step_images[3],
            'step5': 'data:image/png;base64,' + step_images[4],
            'step6': 'data:image/png;base64,' + step_images[5]
        }
    })


@app.route('/gethistorylist', methods=['GET'])
def get_historylist():
    return historymanager.get_historylist()


@app.route('/gethistory', methods=['GET'])
def get_history():
    reqid = request.values['reqid']
    return historymanager.get_history(reqid)


@app.route('/getsettings', methods=['GET'])
def get_settings():
    print(settingsmanager.get_settinglist())
    return settingsmanager.get_settinglist()


@app.route('/setsettings', methods=['POST'])
def set_settings():
    req_param = json.loads(base64.b64decode(request.values['q']).decode('utf-8'))
    update_data = json.loads(req_param)

    vline_gap = update_data['vline_gap']
    hline_gap = update_data['hline_gap']
    hough_manual_thr = update_data['hough_manual_thr']
    hough_manual_thr_val = update_data['hough_manual_thr_val']
    allowed_hnoise = update_data['allowed_hnoise']
    allowed_vnoise = update_data['allowed_vnoise']
    hblank_gap = update_data['hblank_gap']
    mono_thr = update_data['mono_thr']

    settingsmanager.set_settings('vline_gap', vline_gap)
    settingsmanager.set_settings('hline_gap', hline_gap)
    settingsmanager.set_settings('hough_manual_thr', hough_manual_thr)
    settingsmanager.set_settings('hough_manual_thr_val', hough_manual_thr_val)
    settingsmanager.set_settings('allowed_hnoise', allowed_hnoise)
    settingsmanager.set_settings('allowed_vnoise', allowed_vnoise)
    settingsmanager.set_settings('hblank_gap', hblank_gap)
    settingsmanager.set_settings('mono_thr', mono_thr)

    return 'ok', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=srv_port)
