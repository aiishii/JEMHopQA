import re
import json
import pandas as pd
import argparse

def tsv_to_pred_format(in_file, out_file):
	triple_format = re.compile(r'[（\(]\s*(.+?)\s*[,，]\s*(.+?)\s*[,，]\s*(.+?)\s*[）\)]')
	# qid\tpredicted_answer\tpredicted_derivations
	df =pd.read_table(in_file)
	pred_format_dic = {"answer":{}, "derivations":{}}

	for i, r in df.iterrows():
		pred_format_dic["answer"][r.qid] = r.predicted_answer
		triples = []
		if type(r.predicted_derivations) is str:
			for d_str in r.predicted_derivations.split(';'):
				try:
					res = triple_format.findall(d_str)
				except Exception as e:
					print(e)
					res = None
				
				if not res: 
					print('error triples format:'+ str(r.predicted_derivations))
				else:
					sbj, relation, obj = res[0]
					triples.append([sbj, relation, obj.split('、')])
		pred_format_dic["derivations"][r.qid] = triples
						
	with open(out_file, mode="w") as f_out:
		f_out.write(json.dumps(pred_format_dic, ensure_ascii=False))

if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument(
		'-tsv', '--tsv_file_name', required=True,
		help="Model prediction tsv file.")
	parser.add_argument(
		'-out', '--out_json_file_name', required=True,
		help="Output json file.")

	args = parser.parse_args()

	tsv_to_pred_format(args.tsv_file_name , args.out_json_file_name)
	
