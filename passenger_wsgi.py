import mysql.connector

def get_db_connection():
    """
    Tries to connect to the database.
    Returns the connection object if successful, or an error string if failed.
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="wdddzygb_dev",         # e.g., mycpaneluser_myuser
            password="King@2000",
            database="wdddzygb_dev"      # e.g., mycpaneluser_mydb
        )
        return conn
    except mysql.connector.Error as err:
        return f"❌ Database connection failed: {err}"

def application(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain; charset=utf-8')]
    output = ""

    conn = get_db_connection()

    if isinstance(conn, str):
        # Connection failed, conn is an error message
        output = f"There is an issue with the application.\n{conn}"
    else:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()

            output += "✅ Database connection successful.\n\n"
            output += "📄 User Records:\n"
            for row in rows:
                output += str(row) + "\n"

            cursor.close()
            conn.close()

        except Exception as e:
            status = '500 Internal Server Error'
            output = f"There is an issue with the application.\n🔥 Error fetching data: {e}"

    # Final response
    output_bytes = output.encode('utf-8')
    response_headers.append(('Content-Length', str(len(output_bytes))))
    start_response(status, response_headers)
    return [output_bytes]
