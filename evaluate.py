"""
	JEMHopQA evaluation script
	!pip install sudachipy sudachidict_full chikkarpy
	!chikkarpy build -i userdic_sample.txt -o user.dic
"""
import argparse
import logging
import numpy as np
import collections
import re

import pulp
import Levenshtein


import json
import string
from tqdm import tqdm

from chikkarpy import Chikkar
from chikkarpy.dictionarylib import Dictionary as chikkardict
from sudachipy import Dictionary, SplitMode

chikkar = Chikkar()
chikkar.add_dictionary(chikkardict())
chikkar.add_dictionary(chikkardict("user.dic"))
chikkar.enable_verb()

tokenizer = Dictionary(dict="full").create(mode=SplitMode.C)
def get_token_list(text, normalize=False):
	token_list = []
	morphemes = tokenizer.tokenize(text)
	# if '年' in text or '月' in text or '日' in text:
	skip_flg = False
	for i, m in enumerate(morphemes):
		if skip_flg:
			skip_flg = False
			continue
		if m.part_of_speech()[0] in ['空白','補助記号','助詞','助動詞']: continue
		# print(m.surface(), m.normalized_form(), chikkar.find(m.surface()))#
		if i < len(morphemes)-1 and m.part_of_speech()[1] == '数詞' and '助数詞' in morphemes[i+1].part_of_speech()[2]:
			token_list.append([re.sub(r'^0', '', m.surface())+morphemes[i+1].surface()])
			skip_flg = True
		elif m.part_of_speech()[1] == '数詞' and m.surface()[0] == '0':
			token_list.append([re.sub(r'^0', '', m.surface())])
		else:
			token_list.append([m.surface(),m.normalized_form()]+chikkar.find(m.surface()))
	return token_list

def white_space_fix(text):
	return ' '.join(text.split())
def remove_brackets(text):
	text = re.sub(r'\s*[\(（].+?[\)）]\s*', '', text)
	return re.sub(r'[『』「」]', '', text)

def normalize_answer(s):
	if s == 'はい': s = 'YES'
	elif s == 'いいえ': s = 'NO'

	return white_space_fix(remove_brackets(s))

def editdist(p_pred, p_gold):
	norm_p_pred = normalize_answer(p_pred)
	norm_p_gold = normalize_answer(p_gold)

	if norm_p_pred in ['Yes', 'No'] and norm_p_pred != norm_p_gold:
		return 0.0
	if norm_p_gold in ['Yes', 'No'] and norm_p_gold != norm_p_gold:
		return 0.0

	replace_char_list = list(string.ascii_lowercase)
	replace_char_idx = 0
	pred_tokens = get_token_list(norm_p_pred)
	gold_tokens = get_token_list(norm_p_gold)

	pred_char_list = [''] * len(pred_tokens)
	gold_char_list = [''] * len(gold_tokens)
	for i, g_t in enumerate(gold_tokens):
		for j, p_t in enumerate(pred_tokens):
			if set(p_t) & set(g_t) and not pred_char_list[j]:
				gold_char_list[i] = replace_char_list[replace_char_idx]
				pred_char_list[j] = replace_char_list[replace_char_idx]
				replace_char_idx += 1
				break


	for i, g_c in enumerate(gold_char_list):
		if not g_c: 
			gold_char_list[i] = replace_char_list[replace_char_idx]
			replace_char_idx += 1

	for i, p_c in enumerate(pred_char_list):
		if not p_c: 
			pred_char_list[i] = replace_char_list[replace_char_idx]
			replace_char_idx += 1

	levenshtein_ratio = Levenshtein.ratio(''.join(gold_char_list), ''.join(pred_char_list))

	return levenshtein_ratio

def print_alignment(pred, true, a_pred, a_true):
	for k in a_pred:
		print(a_pred[k][1], pred[k], "<=>", true[a_pred[k][0]] if a_pred[k][0] is not None else None)

	for k in a_true:
		if a_true[k][0] is not None:
			continue

		print(a_true[k][1], pred[a_true[k][0]] if a_true[k][0] is not None else None, "<=>", true[k])


out_scores = { 'a_em': [], 'a_score': [],
			'e_p': [], 'e_r': [], 'e_f': [],
			'r_p': [], 'r_r': [], 'r_f': [],
			'er_p': [], 'er_r': [], 'er_f': []}

class Evaluator:
	def __init__(self, args, dim):
		self.args = args
		self.sim = editdist
		self.dim = dim

	def evaluate_ans(self, pred, true):
		ems, scores = [], []

		def em_score(p_pred, p_gold):
			em = 1.0 if  (normalize_answer(p_pred) == normalize_answer(p_gold)) else 0.0
			return em
		
		for t in tqdm(list(true)):
			k = t["qid"]
			if self.args.ignore_missing and k not in pred["answer"]:
				continue

			y_pred = pred["answer"][k]
			if not y_pred or not type(y_pred) is str:
				em, sim_score = 0.0, 0.0
			else:
				y_true = t["answer"]
				em = em_score(y_pred, y_true)
				sim_score = self.sim(y_pred, y_true)
			if self.args.verbose == 1:
				print("-" * 3)
				print("pred:", y_pred, "gold:", y_true)
				print("EM:", em, "SIM:", sim_score)
			
			ems += [em]
			scores += [sim_score]

		out_scores["a_em"] = ems
		out_scores["a_score"] = scores

		return {"em": np.mean(ems), "score": np.mean(scores)}
	
	def evaluate(self, pred, true):
		precs, recalls, fs = [], [], []

		for t in tqdm(list(true)):
			k = t["qid"]
			if self.args.ignore_missing and k not in pred["derivations"]:
				continue

			y_pred = []
			for rf in pred["derivations"][k]:
				for obj in rf[2]:
					y_pred.append([rf[0], rf[1], obj])

			y_true = []
			for rf in t["derivations"]:
				for obj in rf[2]:
					y_true.append([rf[0], rf[1], obj])

			num_cor, a_pred, a_true = self.best_alignment(y_pred, y_true)
			prec, recall = num_cor / len(y_pred) if len(y_pred) > 0 else 0, num_cor / len(y_true) if len(y_true) > 0 else 0
			f = (2 * prec * recall) / (prec + recall) if prec + recall > 0 else 0

			if self.args.verbose == 1:
				print("-" * 3)
				print("P:", prec, "R:", recall, "F:", f)
				print("Pred:", y_pred)
				print("True:", y_true)
				print("Alignment:")
				print_alignment(y_pred, y_true, a_pred, a_true)

			precs += [prec]
			recalls += [recall]
			fs += [(2 * prec * recall) / (prec + recall) if prec + recall > 0 else 0]

		out_scores[self.dim+"_p"] = precs
		out_scores[self.dim+"_r"] = recalls
		out_scores[self.dim+"_f"] = fs

		return {"prec": np.mean(precs), "recall": np.mean(recalls), "f1": np.mean(fs)}
	
	def best_alignment(self, di, dj):
		problem = pulp.LpProblem("Problem-1", pulp.LpMaximize)

		# Variable
		alignment = [[pulp.LpVariable("align_{}_{}".format(i, j), 0, 1, pulp.LpBinary) for j in range(len(dj))] for i in
					range(len(di))]

		#
		# Constraints

		# Each node has one out going edge
		for i in range(len(di)):
			y = 0

			if len(dj) == 0:
				continue

			for j in range(len(dj)):
				y += alignment[i][j]

			problem.addConstraint(y <= 1)

		# Each node has one out going edge
		for i in range(len(dj)):
			y = 0

			if len(di) == 0:
				continue

			for j in range(len(di)):
				y += alignment[j][i]

			problem.addConstraint(y <= 1)

		# Set objective function.
		obj_vars = []
		obj_coefs = collections.defaultdict(dict)

		for i in range(len(di)):
			for j in range(len(dj)):
				coefs = []

				if "e" in self.dim: coefs += [self.sim(di[i][0], dj[j][0]), self.sim(di[i][2], dj[j][2])]
				if "r" in self.dim: coefs += [self.sim(di[i][1], dj[j][1])]

				coef = np.mean(coefs)

				obj_coefs[i][j] = coef

				if coef > 0.0:
					obj_vars += [coef * alignment[i][j]]

		if len(obj_vars) == 0:
			return 0.0, {}, {}

		problem.setObjective(sum(obj_vars))
		problem.solve()

		alignment_pred, alignment_true = {}, {}

		for i in range(len(di)):
			alignment_pred[i] = None, 0.0

			for j in range(len(dj)):
				if pulp.value(alignment[i][j]) == 1.0:
					alignment_pred[i] = j, obj_coefs[i][j]

		for i in range(len(dj)):
			alignment_true[i] = None, 0.0

			for j in range(len(di)):
				if pulp.value(alignment[j][i]) == 1.0:
					alignment_true[i] = j, obj_coefs[j][i]

		num_cor = pulp.value(problem.objective)
		return num_cor, alignment_pred, alignment_true


def main(args):
	preds = json.load(open(args.prediction))
	labels = json.load(open(args.label))


	out = {}

	eva = Evaluator(args, dim="a")
	ret = eva.evaluate_ans(preds, labels)
	out["a"] = ret

	for k in ["e", "r", "er"]:
		eva = Evaluator(args, dim=k)
		ret = eva.evaluate(preds, labels)
		out[k] = ret

	print(json.dumps(out))

	if args.output_score_file:
		qids = [t["qid"] for t in labels]
		with open(args.output_score_file, mode="w") as out_f:
			header = list(out_scores.keys())
			out_f.write('\t'.join(["qid"] + header) + '\n')
			for i in range(len(qids)):
				out_f.write('\t'.join([qids[i]] +[str(out_scores[h][i]) for h in header]) + '\n')

if __name__ == "__main__":
	logging.basicConfig(
		format='%(asctime)s- %(name)s - %(levelname)s - %(message)s')

	parser = argparse.ArgumentParser()

	parser.add_argument(
		'-pred', '--prediction', required=True,
		help="Model prediction.")
	parser.add_argument(
		'-label', '--label', required=True,
		help="Gold-standard reasoning steps.")
	parser.add_argument(
		'-ig', '--ignore-missing', action="store_true",
		help="Ignore missing predictions.")
	parser.add_argument(
		'-v', '--verbose', type=int, default=0,
		help="Verbose level.")
	parser.add_argument(
		'-o', '--output_score_file',
		help="File name for output score.")
	args = parser.parse_args()

	main(args)
