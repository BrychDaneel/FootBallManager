def log(conn, admin, message):
    cursor = conn.cursor()
    cursor.execute("BEGIN api.log({}, '{}'); END;".format(admin, message))
    cursor.close()
    pass
