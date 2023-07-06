from io import open
from sys import float_info

from conllu import parse_incr
from nltk import FreqDist, WittenBellProbDist

# Setup Treebank File Mappings
treebank = {}
treebank['en'] = 'UD_English-GUM/en_gum'
treebank['fr'] = 'UD_French-Rhapsodie/fr_rhapsodie'
treebank['uk'] = 'UD_Ukrainian-IU/uk_iu'


# Set Training Hyperparameters
SOS_TAG = '<s>'
EOS_TAG = '</s>'

TAG_BINS = 100    # No. of Bins used during smoothing of Transition Probabilities
VOCAB_BINS = 1e5  # No. of Bins used during smoothing of Emission Probabilities


# Define Corpus Loading Methods
def train_corpus(lang):
	return treebank[lang] + '-ud-train.conllu'

def test_corpus(lang):
	return treebank[lang] + '-ud-test.conllu'

# Remove contractions such as "isn't".
def prune_sentence(sent):
	return [token for token in sent if type(token['id']) is int]

def conllu_corpus(path):
	data_file = open(path, 'r', encoding='utf-8')
	sents = list(parse_incr(data_file))
	return [prune_sentence(sent) for sent in sents]


## -- Part 1 : Parameter Estimation (Functions) -- ##
def corpus_to_taglist(corpus):
	"""Converts the given corpus to a single list of POS tags."""
	tag_list = []
	for sent in corpus:
		tag_list.append(SOS_TAG)

		for token in sent:
			tag_list.append(token['upos'])
		
		tag_list.append(EOS_TAG)

	return tag_list


def corpus_to_emission_list(corpus, hapax_rule):
	"""Converts the given corpus to a single list of
	   emission tuples and a set of present hapax legeomena."""
	hapaxes = corpus_to_hapaxes(corpus)
	emission_list = []	

	for sent in corpus:
		for word_pos, token in enumerate(sent):
			tag = token['upos']
			word = token['form']

			if word in hapaxes:
				word = hapax_rule.apply_rule(word, word_pos)

			emission_list.append((tag, word))

	return emission_list, hapaxes


def corpus_to_hapaxes(corpus):
	"""Extracts all hapax legomena from the given corpus."""
	word_counts = FreqDist()

	for sent in corpus:
		for token in sent:
			word_counts[token['form']] += 1

	return set(word_counts.hapaxes())


def corpus_to_tagset(corpus):
	"""Extracts all unique tags from the provided corpus."""
	return set([token['upos'] for sent in corpus for token in sent])


def corpus_to_vocab(corpus):
	"""Extracts all unique words from the provided corpus."""
	return set([token['form'] for sent in corpus for token in sent])


def smooth_freq_dists(freq_dists, bins):
	"""
	Smooths a collection of provided frequency distributions 
	using Witten-Bell Smoothing and a specified number of bins.
	"""
	prob_dists = {}

	for key, dist in freq_dists.items():
		prob_dists[key] = WittenBellProbDist(dist, bins=bins) 

	return prob_dists


def get_transition_probs(tag_list, tag_set):
	"""
	Estimates the transition probabilities for an HMM based upon
	the provided set of list of tags.
	"""
	# Transitions Dictionary: Maps Tag to FreqDist of Next Tags
	transitions = dict(
		[(tag, FreqDist()) for tag in set(tag_list)]
	)

	# -- Determine Frequencies of Tag Transitions -- #
	for i in range(len(tag_list)-1):
		tag = tag_list[i]
		next_tag = tag_list[i+1]

		transitions[tag][next_tag] += 1

	# -- Smooth and Return Emission Probabilities -- #
	return smooth_freq_dists(transitions, TAG_BINS)


def get_emission_probs(emission_list, tag_set):
	"""
	Estimates the emission probabilities for an HMM based upon
	the provided list of tag -> word emissions.
	""" 

	# Emission Dictionary: Maps Tag to Current Word
	emissions = dict(
		[(tag, FreqDist()) for tag in tag_set]
	)

	# -- Determine Frequencies of Tag Emissions -- #
	for emission in emission_list:
		tag, word = emission
		emissions[tag][word] += 1

	# -- Return Smoothed Probability Distribution for Emissions -- #
	return smooth_freq_dists(emissions, VOCAB_BINS)


## -- Part 2 : Parameter Estimation (Functions) -- ##
def viterbi(word_list, tag_set, t_probs, e_probs):
	"""
	Given a set of trained transition and emission probabilities,
	the function will predict the associated part-of-speech tags
	for each word within the provided list of words using the
	Viterbi Algorithm.

	Returns a list of POS tags for each word of the input sentence.
	"""

	# -- Build Data Structures -- #
	length = len(word_list)

	v = [dict() for _ in range(length+1)]
	backpointers = [dict() for _ in range(length+1)]
	
	# -- Initialisation Step -- #
	for tag in tag_set:
		v[0][tag] = t_probs[SOS_TAG].logprob(tag) + e_probs[tag].logprob(word_list[0])
		backpointers[0][tag] = SOS_TAG  # TODO Are SOS and EOS Tags needed?

	# -- Forward Propagation Step -- #
	for i in range(1, length):

		for curr_tag in tag_set:
			# Want: Max Prob for Tag, and Prev_Tag that Gives Max Prob
			prob_to_max = lambda prev_tag : (v[i-1][prev_tag]
											+ t_probs[prev_tag].logprob(curr_tag)
											+ e_probs[curr_tag].logprob(word_list[i]))

			v[i][curr_tag], backpointers[i][curr_tag] = prob_and_arg_max(prob_to_max, tag_set)


	# -- Final Step -- #
	prob_to_max = lambda prev_tag : (v[length-1][prev_tag]
									 + t_probs[prev_tag].logprob(EOS_TAG))

	v[length][EOS_TAG], backpointers[length][EOS_TAG] = prob_and_arg_max(prob_to_max, tag_set)

	# -- Return Tags -- #
	return recover_tags(backpointers)


def prob_and_arg_max(prob_to_max, tag_set):
	"""Returns the maximum probability and argument for the given function, and argument domain."""

	# Want: Max Prob for Tag, and Prev_Tag that Gives Max Prob
	max_prob = -float_info.max
	max_tag = None

	for prev_tag in tag_set:

		prob = prob_to_max(prev_tag)

		if (prob > max_prob):
			max_prob = prob
			max_tag = prev_tag

	return max_prob, max_tag


def recover_tags(backpointers):
	"""Constructs a sequence of POS tags from the provided matrix of backpointers."""

	tag_list = []
	curr_tag = EOS_TAG

	# -- Reconstruct POS Tag Sequence from Backpointers -- #
	for i in range(len(backpointers)-1, 0, -1):
		curr_tag = backpointers[i][curr_tag]
		tag_list.insert(0, curr_tag)

	return tag_list


def evaluate_model(transition_probs, emission_probs, tag_set, sentence_lists, true_tag_lists):
	"""Evaluates a trained HMM model based upon a set of provided sentences, and ground-truth labels."""
 
	total_tags = 0
	correct_tags = 0

	sentences_seen = 0
	num_sentences = len(sentence_lists)

	for sentence, true_tags in zip(sentence_lists, true_tag_lists):

		predicted_tags = viterbi(sentence, tag_set, transition_probs, emission_probs)
		for true_tag, predicted_tag in zip(true_tags, predicted_tags):

			total_tags += 1
			if true_tag == predicted_tag:
				correct_tags += 1

		sentences_seen += 1
		print("Progress: {:.2f}%".format(sentences_seen/num_sentences*100), end="\r")

	acc = correct_tags / total_tags
	print("Progress: 100.00%\tAccuracy: {:.3f}%".format(acc*100))

	return acc


def prepare_test_data(test_corpus, train_vocab, hapaxes, hapax_rule):
	"""
	Transforms a test corpus into prepared 2D lists of sentences, and ground-truth tags.

	Appliess the provided hapax rule to all words that were seen 0 or 1 times within the training corpus.
	"""

	word_lists = []
	tag_lists = []

	for sentence in test_corpus:
		words = []
		tags = []

		for word_pos, token in enumerate(sentence):

			tag = token['upos']
			word = token['form']

			if (word not in train_vocab) or (word in hapaxes):
				word = hapax_rule.apply_rule(word, word_pos)

			words.append(word)
			tags.append(tag)

		word_lists.append(words)
		tag_lists.append(tags)

	return word_lists, tag_lists


## -- Part 3 : Unknown Words (Functions) -- ##
from experiments import english_experiments, french_experiments, ukrainian_experiments

# Group Experiments by Language
experiments = {}
experiments['en'] = english_experiments
experiments['fr'] = french_experiments
experiments['uk'] = ukrainian_experiments


## -- MAIN -- ##
def main():

	for lang in ['en', 'fr', 'uk']:

		train_sents = conllu_corpus(train_corpus(lang))
		test_sents = conllu_corpus(test_corpus(lang))

		# -- Part 1,3 : Parameter Estimation with Unknown Words -- #
		tag_set = corpus_to_tagset(train_sents)
		vocab = corpus_to_vocab(train_sents)

		tag_list = corpus_to_taglist(train_sents)
		transition_probs = get_transition_probs(tag_list, tag_set)

		# -- Part 2,3 : Viterbi Algorithm  with Unknown Words -- #
		print("\n\n# -- Experiments for Language: {} -- #".format(lang))
		for hapax_rule in experiments[lang]:

			print("\n{}".format(hapax_rule.name))

			# -- Get Emission Probabilities for Given Hapax Rule-- #
			emission_list, hapaxes = corpus_to_emission_list(train_sents, hapax_rule)
			emission_probs = get_emission_probs(emission_list, tag_set)	

			# -- Evaluate Model for Given Hapax Rule -- #
			test_word_lists, test_tag_lists = prepare_test_data(test_sents, vocab, hapaxes, hapax_rule)
			evaluate_model(transition_probs, emission_probs, tag_set, test_word_lists, test_tag_lists)


if __name__ == '__main__':
	main()
