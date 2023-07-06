# CS5012 P1 : Experiments for Unknown Words
#
# The following file defines the set of experiments to be run upon execution of p1.py

# Rule Flags : Used to specify behaviour of Hapax Rules
ALL_CAPS_FLAG = "ALL_CAPS_FLAG"
CATCHALL_FLAG = "CATCHALL_FLAG"
CHECK_CAPS_FLAG = "CHECK_CAPS_FLAG"
CONTAINS_AT_FLAG = "CONTAINS_AT_FLAG"
FIRST_WORD_FLAG = "FIRST_WORD_FLAG"
GROUP_SUFFIXES_FLAG = "GROUP_SUFFIXES_FLAG"
GROUP_PREFIXES_FLAG = "GROUP_PREFIXES_FLAG"
NUMBER_FLAG = "NUMBER_FLAG"
URL_FLAG = "URL_FLAG"


class HapaxRule():
	"""Container class representing a sequence of rules to be applied
	   to all encountered hapax legomena."""

	def __init__(self, name, suffixes, prefixes, other_flags):
		self.name = name
		self.suffixes = suffixes
		self.prefixes = prefixes
		self.other_flags = other_flags

	def apply_rule(self, word, word_pos):
		"""Transform given word based on specified transformation rules."""

		# -- Check Suffixes -- #
		for suffix_list, group in self.suffixes:
			for suffix in suffix_list:
				if word.endswith(suffix):
					return group if GROUP_SUFFIXES_FLAG in self.other_flags else "UNK-" + suffix

		# -- Check Prefixes -- #
		for prefix_list, group in self.prefixes:
			for prefix in prefix_list:
				if word.startswith(prefix):
					return group if GROUP_PREFIXES_FLAG in self.other_flags else prefix + "-UNK"


		# -- Check Other Number -- #
		if NUMBER_FLAG in self.other_flags:

			# Clean String for Number Check
			num = word
			for c in ['.',',',':','+','#']:
				num = num.replace(c, '')
			 
			if num.isnumeric():
				return "UNK_NUM"

		# -- Check URL -- #
		if URL_FLAG in self.other_flags:
			if "://" in word:
				return "UNK_URL"

		# -- Check All Capitals -- #
		if ALL_CAPS_FLAG in self.other_flags:
			if word.isupper():
				return "UNK_ALLCAPS"

		# -- Check Capitalisation -- #
		if CHECK_CAPS_FLAG in self.other_flags:
			if word_pos != 0 and word[0].isupper():
				return "UNK_CAPS"

		# -- Convert Word to Lower Case if First in Sentence -- #
		if FIRST_WORD_FLAG in self.other_flags:
			if word_pos == 0:
				return word.lower()

		# -- Catchall Case -- #
		if CATCHALL_FLAG in self.other_flags:
			return "UNK"

		# -- Base Case : No Transformation -- #
		return word


# -- General Rules -- #
hapax_rule_none = HapaxRule(
	"Standard: No Additional Tags",
	[], [], []
)

hapax_rule_caps = HapaxRule(
	"UNK: Check Capitalisation",
	[], [], [CHECK_CAPS_FLAG]
)

hapax_rule_catchall = HapaxRule(
	"UNK: Catchall Only",
	[], [], [CATCHALL_FLAG]
)

hapax_rule_num = HapaxRule(
	"UNK: Number Tag",
	[], [], [NUMBER_FLAG]
)

hapax_rule_allcaps = HapaxRule(
	"UNK: All Caps Tag",
	[], [], [ALL_CAPS_FLAG]
)

hapax_rule_decap_first_word = HapaxRule(
	"Per Sentence, Set First Word to Lower-Case",
	[], [], [FIRST_WORD_FLAG]
)

hapax_rule_decap_first_word_catchall = HapaxRule(
	"Per Sentence, Set First Word to Lower-Case; with Catchall",
	[], [], [FIRST_WORD_FLAG, CATCHALL_FLAG]
)

# -- English Rules -- #
en_hapax_rule_ing = HapaxRule(
	"UNK: Suffix -ing",
	[(("ing"), "UNK_VERB")], [], []
)

en_hapax_rule_suffixes = HapaxRule(
	"UNK: Suffixes {-ing, -ly, -ed, -ify} ",
	[(("ing","ly","ed", "ify"),"NOGROUP")], [], []
)

en_hapax_rule_full = HapaxRule(
 	"UNK: FULL",
	[(("ing", "ly", "ed", "ify", "al"), "NO_GROUP")], [], [NUMBER_FLAG, CHECK_CAPS_FLAG]
)

en_hapax_rule_full_catchall = HapaxRule(
 	"UNK: FULL with Catchall",
	[(("ing", "ly", "ed", "ify", "al"), "NO_GROUP")], [], [NUMBER_FLAG, CHECK_CAPS_FLAG, CATCHALL_FLAG]
)

en_hapax_rule_full_decap_first_word = HapaxRule(
 	"UNK: FULL with Decapitalisation",
	[(("ing", "ly", "ed", "ify", "al"), "NO_GROUP")], [], [NUMBER_FLAG, CHECK_CAPS_FLAG, FIRST_WORD_FLAG]
)

# Comment Experiment Lines to Remove during Execution of p1.py
english_experiments = [
	hapax_rule_none,
	hapax_rule_caps,
	hapax_rule_catchall,
	hapax_rule_num,
	hapax_rule_allcaps,

	en_hapax_rule_ing,
	en_hapax_rule_suffixes,
	en_hapax_rule_full,
	en_hapax_rule_full_catchall,

	hapax_rule_decap_first_word,
	hapax_rule_decap_first_word_catchall,
	en_hapax_rule_full_decap_first_word,
]


# -- French Rules -- #
fr_hapax_rule_suffixes = HapaxRule(
	"UNK: Suffixes {-er, -ez, -ent, -ont, -ent}",
	[(("er","ez", "ent","ont","ent"),"UNK_VERB")],
	[], []
)

fr_hapax_rule_prefixes = HapaxRule(
	"UNK: Prefixes {-re, -dé}",
	[],
	[(("re", "dé"),"NO_GROUP")],
	[]
)

fr_hapax_rule_full = HapaxRule(
	"UNK: Full",
	[(("er","ez", "ent","ont","ent"),"UNK_VERB")],
	[(("re", "dé"),"NO_GROUP")],
	[NUMBER_FLAG, CHECK_CAPS_FLAG]
)

fr_hapax_rule_full_catchall = HapaxRule(
	"UNK: Full with Catchall",
	[(("er","ez", "ent","ont","ent"),"UNK_VERB")],
	[(("re", "dé"),"NO_GROUP")],
	[NUMBER_FLAG, CHECK_CAPS_FLAG, CATCHALL_FLAG]
)

fr_hapax_rule_full_decap_first_word = HapaxRule(
	"UNK: Full with Decapitalisation",
	[(("er","ez", "ent","ont","ent"),"UNK_VERB")],
	[(("re", "dé"),"NO_GROUP")],
	[NUMBER_FLAG, CHECK_CAPS_FLAG, FIRST_WORD_FLAG]
)

# Comment Experiment Lines to Remove during Execution of p1.py
french_experiments = [
	hapax_rule_none,
	hapax_rule_caps,
	hapax_rule_catchall,
	hapax_rule_num,
	hapax_rule_allcaps,

	fr_hapax_rule_suffixes,
	fr_hapax_rule_prefixes,
	fr_hapax_rule_full,
	fr_hapax_rule_full_catchall,

	hapax_rule_decap_first_word,
	hapax_rule_decap_first_word_catchall,
	fr_hapax_rule_full_decap_first_word,
]

# -- Ukrainian Rules -- #
uk_hapax_rule_suffixes = HapaxRule(
	"UNK: Multiple Suffixes",
	[
		(("ання","яння", "ення", "єння"), "UNK_NOUN"),
		(("ної", "ої"), "UNK_GROUP"),
		(("ний","ий"), "UNK_ADJ")
	],
	[],[]
)

uk_hapax_rule_full = HapaxRule(
	"UNK: Full",
	[
		(("яння", "ення", "єння"), "UNK_NOUN"),
		(("ної", "ої"), "UNK_GROUP"),
		(("ний","ий"), "UNK_ADJ")
	],
	[],
	[NUMBER_FLAG, CHECK_CAPS_FLAG]
)

uk_hapax_rule_full_catchall = HapaxRule(
	"UNK: Full with Catchall",
	[
		(("яння", "ення", "єння"), "UNK_NOUN"),
		(("ної", "ої"), "UNK_GROUP"),
		(("ний","ий"), "UNK_ADJ")
	],
	[],
	[NUMBER_FLAG, CHECK_CAPS_FLAG, CATCHALL_FLAG]
)

uk_hapax_rule_full_decap_first_word = HapaxRule(
	"UNK: Full with Decapitalisation",
	[
		(("яння", "ення", "єння"), "UNK_NOUN"),
		(("ної", "ої"), "UNK_GROUP"),
		(("ний","ий"), "UNK_ADJ")
	],
	[],
	[NUMBER_FLAG, CHECK_CAPS_FLAG, FIRST_WORD_FLAG]
)

# Comment Experiment Lines to Remove during Execution of p1.py
ukrainian_experiments = [
	hapax_rule_none,
	hapax_rule_caps,
	hapax_rule_catchall,
	hapax_rule_num,
	hapax_rule_allcaps,

	uk_hapax_rule_suffixes,
	uk_hapax_rule_full,
	uk_hapax_rule_full_catchall,

	hapax_rule_decap_first_word,
	hapax_rule_decap_first_word_catchall,
	uk_hapax_rule_full_decap_first_word,
]