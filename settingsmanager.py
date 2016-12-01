from mysql.connector import connection


def get_settings(key):
    cnx = connection.MySQLConnection(user='b15299b76462e8', password='1825c249',
                                     host='us-cdbr-iron-east-04.cleardb.net', database='ad_17e3f5535b971ba')

    cursor = cnx.cursor()
    query = 'SELECT set_value FROM pulltablesettings WHERE set_name=\'' + key + '\''
    cursor.execute(query)
    row = cursor.fetchone()
    cnx.close()

    if row is None:
        return None

    return str(row[0])


def set_settings(key, value):
    cnx = connection.MySQLConnection(user='b15299b76462e8', password='1825c249',
                                     host='us-cdbr-iron-east-04.cleardb.net', database='ad_17e3f5535b971ba')

    cursor = cnx.cursor()
    query = 'UPDATE pulltablesettings SET set_value = \'' + str(value) + '\' WHERE set_name=\'' + key + '\''
    cursor.execute(query)
    cnx.commit()
    cnx.close()


def get_settinglist():
    cnx = connection.MySQLConnection(user='b15299b76462e8', password='1825c249',
                                     host='us-cdbr-iron-east-04.cleardb.net', database='ad_17e3f5535b971ba')

    cursor = cnx.cursor()
    query = 'SELECT set_name, set_value, datatype, comment FROM pulltablesettings'
    cursor.execute(query)
    row = cursor.fetchone()
    if row is None:
        return None

    ret_val = '{\"settings\":['
    while row is not None:
        ret_val += '{\"set_name\":\"' + row[0] + '\", \"set_value\":\"' + row[1] + '\",\"datatype\":\"' + row[2] + '\",\"comment\":\"' + row[3] + '\"},'
        row = cursor.fetchone()
    ret_val = ret_val[:len(ret_val) - 1]
    ret_val += ']}'
    cnx.close()

    return ret_val
