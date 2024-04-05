import pymysql
import pandas as pd

import glob
from pathlib import Path

import sys

import shutil

import argparse

def main():


# 인자값을 받을 수 있는 인스턴스 생성
    parser = argparse.ArgumentParser(description='Prepare CEL files')

# 입력받을 인자값 등록
    parser.add_argument('--analysis_id', required=True, help='example: 146')
    parser.add_argument('--path', required=True, help='example: /data04/project/inseokh/BioProject/CEL_FILE_Maker')
    args = parser.parse_args()

    analysis_id = args.analysis_id
    project_path = args.path
    cel_path = f"{project_path}/CEL_FILE"
    Path(cel_path).mkdir(parents=True, exist_ok=True)


    # Connect to the database
    connection = pymysql.connect(host='mew.ptbio.kr',
                                 user='camole_readonly',
                                 password='camole_readonly',
                                 database='camole',
                                 cursorclass=pymysql.cursors.DictCursor)
    sql = """
        SELECT p.name AS `프로젝트명`
        , s.idx AS `서비스번호`
        , ag.idx AS `분석작업번호`
        , CONCAT(rg.barcode, '_', r.location) AS `CEL_ID`
        , sp.delivery_name AS `고객검체명`
        FROM project p
        JOIN service s ON s.fk_project_idx = p.idx
        JOIN analysis_group ag ON ag.fk_service_idx = s.idx AND ag.status IN ('대기','진행','완료','오류')
        JOIN analysis_analysis_group aag ON aag.fk_analysis_group_idx = ag.idx
        JOIN analysis a ON a.idx = aag.fk_analysis_idx
        JOIN run_analysis ra ON ra.fk_analysis_idx = a.idx
        JOIN run r ON r.idx = ra.fk_run_idx
        JOIN run_run_group rrg ON rrg.fk_run_idx = r.idx
        JOIN run_group rg ON rg.idx = rrg.fk_run_group_idx
        JOIN library l ON l.idx = r.fk_library_idx
        JOIN sample_qc_library sqcl ON sqcl.fk_library_idx = l.idx
        JOIN sample_sample_qc ssq ON ssq.fk_sample_qc_idx = sqcl.fk_sample_qc_idx
        JOIN sample sp ON sp.idx = ssq.fk_sample_idx
        WHERE ag.idx = %s"""
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, analysis_id)
            result = cursor.fetchall()
            df = pd.DataFrame(result)
            print(df.columns)

#Construct path to CEL files
    with open(f'{project_path}/sample.id', 'w') as f:
        for idx, row in df.iterrows():
            cel_file_path = glob.glob(f'/chipdata/*/cel/{row["CEL_ID"]}.CEL')
            if len(cel_file_path) > 0:
                cel_file_path = cel_file_path[0]
                shutil.copy2(cel_file_path, f'{cel_path}/{row["CEL_ID"]}.CEL')
               # f.write(f'{row["고객검체명"]}\t{row["CEL_ID"]}.CEL\n')
                f.write(f'{row["CEL_ID"]}.CEL\t{row["고객검체명"]}\n')

if __name__ == '__main__':
    main()
