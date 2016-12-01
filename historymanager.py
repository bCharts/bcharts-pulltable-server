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


def insert_new_history(b64_images, b64_csv):
    cnx = connection.MySQLConnection(user='b15299b76462e8', password='1825c249',
                                     host='us-cdbr-iron-east-04.cleardb.net', database='ad_17e3f5535b971ba')

    cursor = cnx.cursor()

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

    query = 'INSERT INTO ad_17e3f5535b971ba.pulltablehistory (reqid, step1_name, step2_name, step3_name, step4_name, step5_name, step6_name, csv_name, reqtime) VALUES ('
    query += '\'' + reqid + '\','
    for image_id in image_ids:
        query += '\'' + image_id + '\','
    query += '\'' + csv_id + '\','
    query += '\'' + cur_time + '\')'

    cursor.execute(query)
    cnx.commit()
    cnx.close()


def get_historylist():
    cnx = connection.MySQLConnection(user='b15299b76462e8', password='1825c249',
                                     host='us-cdbr-iron-east-04.cleardb.net', database='ad_17e3f5535b971ba')

    cursor = cnx.cursor()

    query = 'SELECT reqid, reqtime FROM pulltablehistory ORDER BY reqtime DESC'

    cursor.execute(query)

    row = cursor.fetchone()
    ret_val = '{\"history\":['
    while row is not None:
        ret_val += '{\"reqid\":\"' + row[0] + '\", \"reqtime\":\"' + str(row[1]) + '\"},'
        row = cursor.fetchone()
    ret_val = ret_val[:len(ret_val)-1]
    ret_val += ']}'

    cnx.close()

    return ret_val


def get_history(reqid):
    cnx = connection.MySQLConnection(user='b15299b76462e8', password='1825c249',
                                     host='us-cdbr-iron-east-04.cleardb.net', database='ad_17e3f5535b971ba')

    cursor = cnx.cursor()

    query = 'SELECT step1_name, step2_name, step3_name, step4_name, step5_name, step6_name, csv_name FROM pulltablehistory WHERE reqid=\'' + reqid + '\''

    cursor.execute(query)
    row = cursor.fetchone()
    cnx.close()

    obj_storage = open_object_storage()

    step_images = []
    step_images.append(obj_storage.get_object(container_name, row[0])[1])
    step_images.append(obj_storage.get_object(container_name, row[1])[1])
    step_images.append(obj_storage.get_object(container_name, row[2])[1])
    step_images.append(obj_storage.get_object(container_name, row[3])[1])
    step_images.append(obj_storage.get_object(container_name, row[4])[1])
    step_images.append(obj_storage.get_object(container_name, row[5])[1])

    csv = obj_storage.get_object(container_name, row[6])[1]

    obj_storage.close()

    ret_val = '{'
    step_image_cnt = 1
    for step_image in step_images:
        ret_val += '\"b64_step' + str(step_image_cnt) + '\":\"data:image/png;base64,' + step_image.decode('utf-8') + '\",'
        step_image_cnt += 1
    ret_val += '\"b64_csv\":\"' + csv.decode('utf-8') + '\"}'

    return ret_val