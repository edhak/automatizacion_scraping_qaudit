import urllib
import sqlalchemy as sa

def datain_db():
    azure_dev = {
        'server' :'conection server 27 analytics',
        'database' :'xxxxxxxxxxxxxxxxx',
        'username' : 'xxxxxxxxxxxxxxxxxxxxxxxx',
        'password' : 'xxxxxxxxxxxxxxxxxxxxxxxx'
    }
    return azure_dev

def create_engine_db(s,b,u,p):
    d='ODBC Driver 17 for SQL Server'
    connection_string = f'DRIVER={{{d}}};SERVER={s};DATABASE={b};UID={u};PWD={p};Trusted_Connection=no;UseFMTONLY=yes;'
    connection_uri = f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(connection_string)}"
    #print(connection_uri)
    return sa.create_engine(connection_uri, fast_executemany=True, encoding='utf8') 

def main():
    azure_dev = datain_db()
    db = create_engine_db(azure_dev['server'],azure_dev['database'],azure_dev['username'],azure_dev['password'])
    print(type(db))

if __name__=='__main__':
    main()
