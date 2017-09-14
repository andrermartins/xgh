#!/usr/bin/env python
import sys
import os
import psycopg2

def dump_table(table_name, conn):
    query = "SELECT * FROM "+table_name+" LIMIT 1"
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    description = cur.description
    columns = "'INSERT INTO "+table_name+" VALUES ('"
    for desc in description:
        columns += "||CASE WHEN "+desc.name+" IS NULL THEN 'NULL' ELSE ''''||"+desc.name+"::VARCHAR||'''' END ||','"
    columns = columns[0:len(columns)-3]
    columns += "')'"
    print "SELECT "+columns+" FROM "+table_name

def update_flex_version(vl_flex_version, hostname, conn):
    if (hostname == "alpha"):
        hostname = "alpha-asset.valebroker.com.br"
    else:
        hostname = "alpha-asset-"+hostname+".valebroker.com.br"
    cur = conn.cursor()
    cur.execute("UPDATE tb_contract_host SET vl_flex_version = %s WHERE hostname = %s", (vl_flex_version, hostname))
    conn.commit()
    print "Host "+hostname+" updated to Flex version "+vl_flex_version

def show_error(conn):
    cur = conn.cursor()
    cur.execute("SELECT stack_trace, detail FROM tb_log_error WHERE id_investor = 5801 ORDER BY dt_error DESC LIMIT 1")
    rows = cur.fetchall()
    print rows[0][0]
    print rows[0][1]

def get_connection():
    postgres_database = os.environ['postgres_database']
    postgres_user = os.environ['postgres_user']
    postgres_password = os.environ['postgres_password']
    postgres_host = os.environ['postgres_host']
    postgres_port = os.environ['postgres_port']
    return psycopg2.connect(database=postgres_database, user=postgres_user, password=postgres_password, host=postgres_host, port=postgres_port)

# def set_enviroment_vars():
#     f = open('/tmp/envs.conf')
#     for line in f:

def init(args):
    conn = get_connection()
    # docker-compose up
    if (os.environ['action'] == "dump_table"):
        # docker-compose run dump_table tb_asset_operation
        dump_table(args[0], conn)
    if (os.environ['action'] == "update_flex_version"):
        # docker-compose run update_flex_version 4324 alpha/rf/support
        update_flex_version(args[0], args[1], conn)
    if (os.environ['action'] == "show_error"):
        # docker-compose run show_error
        show_error(conn)
    conn.close()

if __name__ == "__main__":
    init(sys.argv[1:])
