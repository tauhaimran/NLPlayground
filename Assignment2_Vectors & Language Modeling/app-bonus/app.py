"""Streamlit app for comparing extractive vs abstractive summaries

Usage:
	cd "Assignment2_Vectors & Language Modelling"
	pip install streamlit nltk numpy scikit-learn
	streamlit run app-bonus/app.py

The app loads `outputs/final_summaries_fixed.jsonl` (if present) or
`outputs/final_summaries.jsonl` and `outputs/ocr_data_complete.json` and
lets you inspect individual cases, highlight the sentences chosen by the
extractive summarizer, show the abstractive rewrite, and compute simple
ROUGE-1 and BLEU scores comparing abstractive -> extractive (treating
extractive as the reference). This is intended as a lightweight review tool
for manual grading and comparison.
"""
from pathlib import Path
import json
import streamlit as st
from nltk.tokenize import sent_tokenize, word_tokenize
import numpy as np
from collections import Counter
import math


def load_jsonl(path: Path):
	out = []
	if not path.exists():
		return out
	with open(path, 'r', encoding='utf-8') as f:
		for line in f:
			line = line.strip()
			if not line:
				continue
			try:
				out.append(json.loads(line))
			except Exception:
				continue
	return out


def load_json(path: Path):
	if not path.exists():
		return []
	try:
		with open(path, 'r', encoding='utf-8') as f:
			return json.load(f)
	except Exception:
		return []


def rouge_1_f(reference: str, hypothesis: str):
	"""Compute ROUGE-1 precision/recall/f1 between two texts using token overlap."""
	r_tokens = word_tokenize(reference.lower())
	h_tokens = word_tokenize(hypothesis.lower())
	if not r_tokens or not h_tokens:
		return 0.0, 0.0, 0.0
	r_counts = Counter(r_tokens)
	h_counts = Counter(h_tokens)
	overlap = sum((r_counts & h_counts).values())
	prec = overlap / max(1, len(h_tokens))
	rec = overlap / max(1, len(r_tokens))
	if prec + rec == 0:
		f1 = 0.0
	else:
		f1 = 2 * prec * rec / (prec + rec)
	return prec, rec, f1


def lcs_length(a_tokens, b_tokens):
	# classic DP for LCS length
	n, m = len(a_tokens), len(b_tokens)
	if n == 0 or m == 0:
		return 0
	dp = [[0] * (m + 1) for _ in range(n + 1)]
	for i in range(n - 1, -1, -1):
		for j in range(m - 1, -1, -1):
			if a_tokens[i] == b_tokens[j]:
				dp[i][j] = 1 + dp[i + 1][j + 1]
			else:
				dp[i][j] = max(dp[i + 1][j], dp[i][j + 1])
	return dp[0][0]


def rouge_l_f(reference: str, hypothesis: str):
	r_tokens = word_tokenize(reference.lower())
	h_tokens = word_tokenize(hypothesis.lower())
	if not r_tokens or not h_tokens:
		return 0.0
	lcs = lcs_length(r_tokens, h_tokens)
	prec = lcs / len(h_tokens)
	rec = lcs / len(r_tokens)
	if prec + rec == 0:
		f1 = 0.0
	else:
		f1 = 2 * prec * rec / (prec + rec)
	return f1


def bleu_score(reference: str, hypothesis: str):
	# simple unigram BLEU with brevity penalty using counts
	r_tokens = word_tokenize(reference.lower())
	h_tokens = word_tokenize(hypothesis.lower())
	if not h_tokens or not r_tokens:
		return 0.0
	r_counts = Counter(r_tokens)
	h_counts = Counter(h_tokens)
	overlap = sum(min(h_counts[t], r_counts.get(t, 0)) for t in h_counts)
	precision = overlap / len(h_tokens)
	# brevity penalty
	bp = 1.0
	if len(h_tokens) < len(r_tokens):
		bp = math.exp(1 - (len(r_tokens) / len(h_tokens)))
	return bp * precision


def highlight_sentences(text, sentences_to_highlight):
	# sentences_to_highlight: set of sentence strings (exact match)
	sents = sent_tokenize(text)
	out_html = []
	for s in sents:
		cls = ''
		if s.strip() in sentences_to_highlight:
			cls = 'background-color: #fff2a8; padding:2px; border-radius:3px;'
			out_html.append(f"<div style=\"{cls}\">{s}</div>")
		else:
			out_html.append(f"<div>{s}</div>")
	return '\n'.join(out_html)


def main():
	st.set_page_config(page_title='Summary Compare (extractive vs abstractive)', layout='wide')
	st.title('Compare Extractive vs Abstractive Summaries')

	base = Path('..') if (Path.cwd() / 'app-bonus').exists() else Path('.')
	# try fixed first
	final_fixed = Path('outputs/final_summaries_fixed.jsonl')
	final_orig = Path('outputs/final_summaries.jsonl')
	ocr_path = Path('outputs/ocr_data_complete.json')

	if final_fixed.exists():
		records = load_jsonl(final_fixed)
	elif final_orig.exists():
		records = load_jsonl(final_orig)
	else:
		st.error('Could not find final summaries. Run the notebook first to produce `outputs/final_summaries.jsonl`.')
		return

	case_ids = [r.get('case_id') for r in records if r.get('case_id')]
	case_ids = sorted(case_ids)

	col1, col2 = st.columns([2, 1])
	with col2:
		st.subheader('Select case')
		sel = st.selectbox('Case ID', ['(none)'] + case_ids)
		if sel != '(none)':
			rec = next((r for r in records if r.get('case_id') == sel), None)
		else:
			rec = None

		st.markdown('---')
		st.write('Records available:', len(records))
		st.write('Using fixed file:' if final_fixed.exists() else 'Using original file:')

	with col1:
		if not rec:
			st.info('Select a case from the right to inspect its OCR text and summaries.')
			return

		st.header(f"{rec.get('case_id')}")
		# Load OCR text
		ocr = load_json(ocr_path)
		ocr_map = {r.get('case_id'): r for r in ocr}
		o = ocr_map.get(rec.get('case_id'))
		ocr_text = o.get('ocr_text', '') if o else ''

		ext = (rec.get('extractive_summary') or '').strip()
		abstr = (rec.get('abstractive_summary') or '').strip()
		used_fallback = rec.get('used_fallback', False)

		st.subheader('Summaries')
		st.write('Used TF–IDF fallback:' , used_fallback)
		s1, s2 = st.columns(2)
		with s1:
			st.markdown('**Extractive Summary**')
			st.write(ext)
		with s2:
			st.markdown('**Abstractive Summary**')
			st.write(abstr)

		# Highlight extractive sentences in OCR text
		st.subheader('OCR Text (sentences highlighted if selected by extractive)')
		if ocr_text:
			# build set of sentences that appear in extractive (exact match by sentence)
			try:
				ext_sents = set(sent_tokenize(ext))
			except Exception:
				ext_sents = set()
			html = highlight_sentences(ocr_text, ext_sents)
			st.markdown(html, unsafe_allow_html=True)
		else:
			st.warning('No OCR text available for this case.')

		# Metrics
		st.subheader('Automatic comparison metrics (abstractive vs extractive)')
		if not ext:
			st.warning('No extractive summary to use as reference for metrics.')
		else:
			p, r, f1 = rouge_1_f(ext, abstr)
			rl = rouge_l_f(ext, abstr)
			bl = bleu_score(ext, abstr)
			st.metric('ROUGE-1 F1', f'{f1:.3f}')
			st.metric('ROUGE-L F1', f'{rl:.3f}')
			st.metric('BLEU (simple)', f'{bl:.3f}')


if __name__ == '__main__':
	main()

#to run
#pip install streamlit nltk numpy scikit-learn
#streamlit run "app-bonus/app.py"