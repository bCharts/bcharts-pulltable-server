from mysql.connector import connection
from datetime import datetime
import uuid
import swiftclient
from io import StringIO

container_name = 'bcharts_images'


def open_object_storage():
    auth_url = 'https://identity.open.softlayer.com/v3'
    user_id = '4dc4d2091827499db4d3b197197c35b3'
    password = 'gA3pn~)&O*LDzy69'
    project_id = 'cf3653a87afe436cb4f98b6719e3c64b'
    region_name = 'dallas'

    conn = swiftclient.Connection(key=password, authurl=auth_url, auth_version='3', os_options={
        'project_id': project_id,
        'user_id': user_id,
        'region_name': region_name
    })

    return conn

def open_mysql():
    cnx = connection.MySQLConnection(user='b15299b76462e8', password='1825c249',
                                     host='us-cdbr-iron-east-04.cleardb.net', database='ad_17e3f5535b971ba')

    return cnx

def insert_new_history(b64_images, b64_csv):
    reqid = str(uuid.uuid4())

    obj_storage = open_object_storage()

    image_ids = []
    for b64_image in b64_images:
        image_id = str(uuid.uuid4())
        image_ids.append(image_id)
        temp_file = StringIO()
        temp_file.write(b64_image)

        obj_storage.put_object(container_name, image_id, temp_file.getvalue())
        temp_file.close()

    csv_id = str(uuid.uuid4())
    temp_file = StringIO()
    temp_file.write(b64_csv)

    obj_storage.put_object(container_name, csv_id, temp_file.getvalue())
    obj_storage.close()

    cur_time = str(datetime.now())

    # DB 저장
    cnx = open_mysql()
    cursor = cnx.cursor()

    query = 'INSERT INTO ad_17e3f5535b971ba.pulltablehistory (reqid, reqtime) VALUES ('
    query += '\'' + reqid + '\','
    query += '\'' + cur_time + '\')'
    cursor.execute(query)

    seq = 1
    for image_id in image_ids:
        query = 'INSERT INTO ad_17e3f5535b971ba.pulltablestepimage (reqid, seq, imgid) VALUES ('
        query += '\'' + reqid + '\','
        query += str(seq) + ','
        query += '\'' + image_id + '\')'
        cursor.execute(query)
        seq += 1

    query = 'INSERT INTO ad_17e3f5535b971ba.pulltablecsv (reqid, csvid) VALUES ('
    query += '\'' + reqid + '\','
    query += '\'' + csv_id + '\')'
    cursor.execute(query)
    cnx.commit()

    cnx.close()


def get_historylist():
    cnx = open_mysql()
    cursor = cnx.cursor()

    query = 'SELECT reqid, reqtime FROM pulltablehistory ORDER BY reqtime DESC'
    cursor.execute(query)

    row = cursor.fetchone()
    if row is None:
        return '{\"history\":[]}'

    ret_val = '{\"history\":['
    while row is not None:
        ret_val += '{\"reqid\":\"' + row[0] + '\", \"reqtime\":\"' + str(row[1]) + '\"},'
        row = cursor.fetchone()
    ret_val = ret_val[:len(ret_val) - 1]
    ret_val += ']}'

    cnx.close()

    return ret_val


def get_history(reqid):
    cnx = open_mysql()
    cursor = cnx.cursor()

    query = 'SELECT imgid FROM pulltablestepimage WHERE reqid=\'' + reqid + '\' ORDER BY seq'
    cursor.execute(query)
    row_imageids = cursor.fetchall()

    query = 'SELECT csvid FROM pulltablecsv WHERE reqid=\'' + reqid + '\''
    cursor.execute(query)
    row_csv = cursor.fetchone()

    cnx.close()

    # 파일 열기
    obj_storage = open_object_storage()

    step_images = []
    for row_imageid in row_imageids:
        step_images.append(obj_storage.get_object(container_name, row_imageid[0])[1])

    csv = obj_storage.get_object(container_name, row_csv[0])[1]

    obj_storage.close()

    ret_val = '{"b64_images":['
    for step_image in step_images:
        ret_val += '"data:image/png;base64,' + step_image.decode('utf-8') + '",'
    ret_val = ret_val[:len(ret_val) - 1]
    ret_val += '],'
    ret_val += '"b64_csv":"' + csv.decode('utf-8') + '"}'

    return ret_val
