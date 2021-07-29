from sqlalchemy import text
import os

##### Main #####
def build_dw(sql_path, db_session):
    """Running SQL script to create DW table"""

    sql_scripts = get_sql_scripts(sql_path)
    for sql in sql_scripts:
        with db_session() as db:
            script = text(sql)
            db.execute(script)

##### Utils #####
def get_sql_scripts(path):
    """Get list of SQL raw string from files"""

    list_file = [os.path.join(path, filename) for filename in os.listdir(path)]
    sql_scripts = []
    for file_dir in list_file:
        with open(file_dir, "r", encoding="utf-8") as file:
            script = "\n".join(file.readlines())
            sql_scripts.append(script)
    return sql_scripts
