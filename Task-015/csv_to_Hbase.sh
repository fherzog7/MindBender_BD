hbase org.apache.hadoop.hbase.mapreduce.ImportTsv -Dimporttsv.separator="," -Dimporttsv.columns="HBASE_ROW_KEY,proff:id,proff:fname,proff:lname,proff:email,personal:gender,personal:city,personal:social" emp_data /test/MOCK_DATA.csv