
CONSONANT_DATA = ["ㄱ", "ㄴ", "ㄷ", "ㅁ", "ㅂ", "ㅅ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ",
                  "ㅍ", "ㅎ", "ㄲ", "ㄸ", "ㅃ", "ㅆ", "ㅉ"]

TRAILING_CONSONANT_DATA = ["ㄲ", "ㄳ", "ㄵ", "ㄶ", "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅄ",
                           "ㅆ", "ㄱ", "ㄴ", "ㄷ", "ㅁ", "ㅂ", "ㅅ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]

VOWEL_DATA = ["ㅏ", "ㅑ", "ㅓ", "ㅕ", "ㅗ", "ㅛ", "ㅜ", "ㅠ", "ㅡ", "ㅣ", "ㅐ",
              "ㅒ", "ㅔ", "ㅖ", "ㅘ", "ㅙ", "ㅚ", "ㅝ", "ㅞ", "ㅟ", "ㅢ"]

JOSA_KEYS = ["JKC", "JKG", "JKO", "JKB", "JKV", "JKQ", "JC", "JKS", "JX"]

VOWEL_CONVERGE_CHECK = {"ㅐ": ["ㅏ", "ㅏ"], "ㅙ":["ㅚ","ㅓ"], "ㅣ":["ㅣ","ㅓ"]}

SPACING_ADD_DIC = ["XSN", "XSV", "XSA"]

SPACING_DEL_DIC = {"NNG": ["MAG", "VV"], "NP": ["NNG"], "MAG": ["VV", "XR", "MAG", "NR"], "MAJ": ["NP", "NR", "NNG"], "MM": ["NNG", "NNB", "NNBC"], "EC":["NNG", "VV", "MAG", "VA"], "ETM":["MAG", "NNB", "NNG", "NNBC"]}

DUEN_SORI_DIC = {"ㄲ": "ㄱ", "ㄸ": "ㄷ", "ㅃ": "ㅂ", "ㅆ": "ㅅ", "ㅉ": "ㅈ"}

CATEGORY_LABEL = {"JS": "josa_error", "BS":"busa_error", "AF":"affix_error", "S_ADD":"spacing_add_error", "S_DEL":"spacing_del_error", "G2P":"grapheme_to_phonem_error", "CO":"consonant_error", "VO":"vowel_error"}

ASPECT_LABEL = {"OM":"om_error", "MIF":"mif_error", "REP":"rep_error", "ADD":"add_error", "S_ADD":"s_add_error", "S_DEL":"s_del_error"}

JOSA_CONVERT_LIST = [["은", "는"], ["이", "가", "께서"], ["을", "를"], ["와", "과"], ["이여","여"] ,
                     ["으로","로"], ["이라","라"], ["이냐","냐"], ["이고","고"], ["이여","여"], ["이면""면"], ["이랑","랑"],["에","에게", "께", "의"], ["처럼","마냥"], ["로서","로써", "으로써"] ]

FINAL_CONSONANT_CONVERT_DIC = {"ㄱ":["ㄲ"], "ㄷ":["ㅈ","ㅊ", "ㅌ", "ㅅ", "ㅆ"], "ㅂ":["ㅍ","ㅁ"]}

MAX_ERROR = 4

SENTENCE_ERROR_MAX = 4
