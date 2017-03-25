tsv_file =  "mv_sample.tsv"
mv_data = ""
try:
	mv_file = open(tsv_file)
	for each_line in mv_file:
		mv_data = mv_data + each_line.replace("\t", ",")
except IOError as err:
	print("File error" + str(err))
finally:
	if "mv_sample.tsv" in locals():
		mv_file.close()
mv_data

url_file = open("csv_sample.txt", "w")
url_file.write(mv_data)
url_file.close()