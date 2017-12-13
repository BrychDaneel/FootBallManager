def log(conn, admin, message):
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO changes(admin, `time`, `text`) VALUES ({}, NOW(), "{}")
                   """.format(admin, message))
    cursor.close()
