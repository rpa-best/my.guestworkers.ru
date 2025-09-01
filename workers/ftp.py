import os, io
import pandas as pd
from ftplib import FTP, Error

HOST = os.getenv("FTP_HOST")
USER = os.getenv("FTP_HOST_USER")
PASSWORD = os.getenv("FTP_HOST_PASSWORD")


def get_workers():
    with FTP(HOST, USER, PASSWORD) as ftp:
        ftp.cwd('/httpdocs/upload/csv1c/back/')
        # file_name = sorted(filter(lambda x: str(x).endswith('.csv'), ftp.nlst()), key=lambda x: ftp.voidcmd(f"MDTM {x}"))[-1]
        file_name = 'sotrudniki.csv'
        with io.BytesIO() as file:
            try:
                ftp.retrbinary(f'RETR {file_name}', file.write)
            except Error:
                file_name = sorted(filter(lambda x: str(x).endswith('.csv'), ftp.nlst()), key=lambda x: ftp.voidcmd(f"MDTM {x}"))[-1]
                ftp.retrbinary(f'RETR {file_name}', file.write)
            df = pd.read_csv(io.StringIO(file.getvalue().decode()), sep=';', encoding='utf8')
            return df.astype(object).where(pd.notnull(df), None).to_dict(orient="records")
