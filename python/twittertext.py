# -*- coding: utf-8 -*-
""" Python port of twitter-text
"""
import html
import re
# Escape HTML with html.escape

SPACES = r"\x09-\x0D\x20\x85\xA0\u1680\u180E\u2000-\u200A\u2028\u2029\u202F\u205F\u3000"

INVALID_CHARS = r"\uFFFE\uFEFF\uFFFF\u202A-\u202E"

PUNCT = r"!\"#%&'\(\)*\+,\\\-\.\/:;<=>\?@\[\]\^_{|}~\$"

RTL_CHARS = r"[\u0600-\u06FF]|[\u0750-\u077F]|[\u0590-\u05FF]|[\uFE70-\uFEFF]"

NON_BMP_CODE_PAIRS = r"[\uD800-\uDBFF][\uDC00-\uDFFF]"

LATIN_ACCENT_CHARS = r"\xC0-\xD6\xD8-\xF6\xF8-\xFF\u0100-\u024F\u0253\u0254\u0256\u0257\u0259\u025B\u0263\u0268\u026F\u0272\u0289\u028B\u02BB\u0300-\u036F\u1E00-\u1EFF"

# Generated from unicode_regex/unicode_regex_groups.scala, same as objective c's \p{L}\p{M}
BMP_LETTERS_AND_MARKS = r"A-Za-z\xaa\xb5\xba\xc0-\xd6\xd8-\xf6\xf8-\u02c1\u02c6-\u02d1\u02e0-\u02e4\u02ec\u02ee\u0300-\u0374\u0376\u0377\u037a-\u037d\u037f\u0386\u0388-\u038a\u038c\u038e-\u03a1\u03a3-\u03f5\u03f7-\u0481\u0483-\u052f\u0531-\u0556\u0559\u0561-\u0587\u0591-\u05bd\u05bf\u05c1\u05c2\u05c4\u05c5\u05c7\u05d0-\u05ea\u05f0-\u05f2\u0610-\u061a\u0620-\u065f\u066e-\u06d3\u06d5-\u06dc\u06df-\u06e8\u06ea-\u06ef\u06fa-\u06fc\u06ff\u0710-\u074a\u074d-\u07b1\u07ca-\u07f5\u07fa\u0800-\u082d\u0840-\u085b\u08a0-\u08b2\u08e4-\u0963\u0971-\u0983\u0985-\u098c\u098f\u0990\u0993-\u09a8\u09aa-\u09b0\u09b2\u09b6-\u09b9\u09bc-\u09c4\u09c7\u09c8\u09cb-\u09ce\u09d7\u09dc\u09dd\u09df-\u09e3\u09f0\u09f1\u0a01-\u0a03\u0a05-\u0a0a\u0a0f\u0a10\u0a13-\u0a28\u0a2a-\u0a30\u0a32\u0a33\u0a35\u0a36\u0a38\u0a39\u0a3c\u0a3e-\u0a42\u0a47\u0a48\u0a4b-\u0a4d\u0a51\u0a59-\u0a5c\u0a5e\u0a70-\u0a75\u0a81-\u0a83\u0a85-\u0a8d\u0a8f-\u0a91\u0a93-\u0aa8\u0aaa-\u0ab0\u0ab2\u0ab3\u0ab5-\u0ab9\u0abc-\u0ac5\u0ac7-\u0ac9\u0acb-\u0acd\u0ad0\u0ae0-\u0ae3\u0b01-\u0b03\u0b05-\u0b0c\u0b0f\u0b10\u0b13-\u0b28\u0b2a-\u0b30\u0b32\u0b33\u0b35-\u0b39\u0b3c-\u0b44\u0b47\u0b48\u0b4b-\u0b4d\u0b56\u0b57\u0b5c\u0b5d\u0b5f-\u0b63\u0b71\u0b82\u0b83\u0b85-\u0b8a\u0b8e-\u0b90\u0b92-\u0b95\u0b99\u0b9a\u0b9c\u0b9e\u0b9f\u0ba3\u0ba4\u0ba8-\u0baa\u0bae-\u0bb9\u0bbe-\u0bc2\u0bc6-\u0bc8\u0bca-\u0bcd\u0bd0\u0bd7\u0c00-\u0c03\u0c05-\u0c0c\u0c0e-\u0c10\u0c12-\u0c28\u0c2a-\u0c39\u0c3d-\u0c44\u0c46-\u0c48\u0c4a-\u0c4d\u0c55\u0c56\u0c58\u0c59\u0c60-\u0c63\u0c81-\u0c83\u0c85-\u0c8c\u0c8e-\u0c90\u0c92-\u0ca8\u0caa-\u0cb3\u0cb5-\u0cb9\u0cbc-\u0cc4\u0cc6-\u0cc8\u0cca-\u0ccd\u0cd5\u0cd6\u0cde\u0ce0-\u0ce3\u0cf1\u0cf2\u0d01-\u0d03\u0d05-\u0d0c\u0d0e-\u0d10\u0d12-\u0d3a\u0d3d-\u0d44\u0d46-\u0d48\u0d4a-\u0d4e\u0d57\u0d60-\u0d63\u0d7a-\u0d7f\u0d82\u0d83\u0d85-\u0d96\u0d9a-\u0db1\u0db3-\u0dbb\u0dbd\u0dc0-\u0dc6\u0dca\u0dcf-\u0dd4\u0dd6\u0dd8-\u0ddf\u0df2\u0df3\u0e01-\u0e3a\u0e40-\u0e4e\u0e81\u0e82\u0e84\u0e87\u0e88\u0e8a\u0e8d\u0e94-\u0e97\u0e99-\u0e9f\u0ea1-\u0ea3\u0ea5\u0ea7\u0eaa\u0eab\u0ead-\u0eb9\u0ebb-\u0ebd\u0ec0-\u0ec4\u0ec6\u0ec8-\u0ecd\u0edc-\u0edf\u0f00\u0f18\u0f19\u0f35\u0f37\u0f39\u0f3e-\u0f47\u0f49-\u0f6c\u0f71-\u0f84\u0f86-\u0f97\u0f99-\u0fbc\u0fc6\u1000-\u103f\u1050-\u108f\u109a-\u109d\u10a0-\u10c5\u10c7\u10cd\u10d0-\u10fa\u10fc-\u1248\u124a-\u124d\u1250-\u1256\u1258\u125a-\u125d\u1260-\u1288\u128a-\u128d\u1290-\u12b0\u12b2-\u12b5\u12b8-\u12be\u12c0\u12c2-\u12c5\u12c8-\u12d6\u12d8-\u1310\u1312-\u1315\u1318-\u135a\u135d-\u135f\u1380-\u138f\u13a0-\u13f4\u1401-\u166c\u166f-\u167f\u1681-\u169a\u16a0-\u16ea\u16f1-\u16f8\u1700-\u170c\u170e-\u1714\u1720-\u1734\u1740-\u1753\u1760-\u176c\u176e-\u1770\u1772\u1773\u1780-\u17d3\u17d7\u17dc\u17dd\u180b-\u180d\u1820-\u1877\u1880-\u18aa\u18b0-\u18f5\u1900-\u191e\u1920-\u192b\u1930-\u193b\u1950-\u196d\u1970-\u1974\u1980-\u19ab\u19b0-\u19c9\u1a00-\u1a1b\u1a20-\u1a5e\u1a60-\u1a7c\u1a7f\u1aa7\u1ab0-\u1abe\u1b00-\u1b4b\u1b6b-\u1b73\u1b80-\u1baf\u1bba-\u1bf3\u1c00-\u1c37\u1c4d-\u1c4f\u1c5a-\u1c7d\u1cd0-\u1cd2\u1cd4-\u1cf6\u1cf8\u1cf9\u1d00-\u1df5\u1dfc-\u1f15\u1f18-\u1f1d\u1f20-\u1f45\u1f48-\u1f4d\u1f50-\u1f57\u1f59\u1f5b\u1f5d\u1f5f-\u1f7d\u1f80-\u1fb4\u1fb6-\u1fbc\u1fbe\u1fc2-\u1fc4\u1fc6-\u1fcc\u1fd0-\u1fd3\u1fd6-\u1fdb\u1fe0-\u1fec\u1ff2-\u1ff4\u1ff6-\u1ffc\u2071\u207f\u2090-\u209c\u20d0-\u20f0\u2102\u2107\u210a-\u2113\u2115\u2119-\u211d\u2124\u2126\u2128\u212a-\u212d\u212f-\u2139\u213c-\u213f\u2145-\u2149\u214e\u2183\u2184\u2c00-\u2c2e\u2c30-\u2c5e\u2c60-\u2ce4\u2ceb-\u2cf3\u2d00-\u2d25\u2d27\u2d2d\u2d30-\u2d67\u2d6f\u2d7f-\u2d96\u2da0-\u2da6\u2da8-\u2dae\u2db0-\u2db6\u2db8-\u2dbe\u2dc0-\u2dc6\u2dc8-\u2dce\u2dd0-\u2dd6\u2dd8-\u2dde\u2de0-\u2dff\u2e2f\u3005\u3006\u302a-\u302f\u3031-\u3035\u303b\u303c\u3041-\u3096\u3099\u309a\u309d-\u309f\u30a1-\u30fa\u30fc-\u30ff\u3105-\u312d\u3131-\u318e\u31a0-\u31ba\u31f0-\u31ff\u3400-\u4db5\u4e00-\u9fcc\ua000-\ua48c\ua4d0-\ua4fd\ua500-\ua60c\ua610-\ua61f\ua62a\ua62b\ua640-\ua672\ua674-\ua67d\ua67f-\ua69d\ua69f-\ua6e5\ua6f0\ua6f1\ua717-\ua71f\ua722-\ua788\ua78b-\ua78e\ua790-\ua7ad\ua7b0\ua7b1\ua7f7-\ua827\ua840-\ua873\ua880-\ua8c4\ua8e0-\ua8f7\ua8fb\ua90a-\ua92d\ua930-\ua953\ua960-\ua97c\ua980-\ua9c0\ua9cf\ua9e0-\ua9ef\ua9fa-\ua9fe\uaa00-\uaa36\uaa40-\uaa4d\uaa60-\uaa76\uaa7a-\uaac2\uaadb-\uaadd\uaae0-\uaaef\uaaf2-\uaaf6\uab01-\uab06\uab09-\uab0e\uab11-\uab16\uab20-\uab26\uab28-\uab2e\uab30-\uab5a\uab5c-\uab5f\uab64\uab65\uabc0-\uabea\uabec\uabed\uac00-\ud7a3\ud7b0-\ud7c6\ud7cb-\ud7fb\uf870-\uf87f\uf882\uf884-\uf89f\uf8b8\uf8c1-\uf8d6\uf900-\ufa6d\ufa70-\ufad9\ufb00-\ufb06\ufb13-\ufb17\ufb1d-\ufb28\ufb2a-\ufb36\ufb38-\ufb3c\ufb3e\ufb40\ufb41\ufb43\ufb44\ufb46-\ufbb1\ufbd3-\ufd3d\ufd50-\ufd8f\ufd92-\ufdc7\ufdf0-\ufdfb\ufe00-\ufe0f\ufe20-\ufe2d\ufe70-\ufe74\ufe76-\ufefc\uff21-\uff3a\uff41-\uff5a\uff66-\uffbe\uffc2-\uffc7\uffca-\uffcf\uffd2-\uffd7\uffda-\uffdc"

ASTRAL_LETTERS_AND_MARKS = r"\U00010000-\U0001000b\U0001000d-\U00010026\U00010028-\U0001003a\U0001003c\U0001003d\U0001003f-\U0001004d\U00010050-\U0001005d\U00010080-\U000100fa\U000101fd\U00010280-\U0001029c\U000102a0-\U000102d0\U000102e0\U00010300-\U0001031f\U00010330-\U00010340\U00010342-\U00010349\U00010350-\U0001037a\U00010380-\U0001039d\U000103a0-\U000103c3\U000103c8-\U000103cf\U00010400-\U0001049d\U00010500-\U00010527\U00010530-\U00010563\U00010600-\U00010736\U00010740-\U00010755\U00010760-\U00010767\U00010800-\U00010805\U00010808\U0001080a-\U00010835\U00010837\U00010838\U0001083c\U0001083f-\U00010855\U00010860-\U00010876\U00010880-\U0001089e\U00010900-\U00010915\U00010920-\U00010939\U00010980-\U000109b7\U000109be\U000109bf\U00010a00-\U00010a03\U00010a05\U00010a06\U00010a0c-\U00010a13\U00010a15-\U00010a17\U00010a19-\U00010a33\U00010a38-\U00010a3a\U00010a3f\U00010a60-\U00010a7c\U00010a80-\U00010a9c\U00010ac0-\U00010ac7\U00010ac9-\U00010ae6\U00010b00-\U00010b35\U00010b40-\U00010b55\U00010b60-\U00010b72\U00010b80-\U00010b91\U00010c00-\U00010c48\U00011000-\U00011046\U0001107f-\U000110ba\U000110d0-\U000110e8\U00011100-\U00011134\U00011150-\U00011173\U00011176\U00011180-\U000111c4\U000111da\U00011200-\U00011211\U00011213-\U00011237\U000112b0-\U000112ea\U00011301-\U00011303\U00011305-\U0001130c\U0001130f\U00011310\U00011313-\U00011328\U0001132a-\U00011330\U00011332\U00011333\U00011335-\U00011339\U0001133c-\U00011344\U00011347\U00011348\U0001134b-\U0001134d\U00011357\U0001135d-\U00011363\U00011366-\U0001136c\U00011370-\U00011374\U00011480-\U000114c5\U000114c7\U00011580-\U000115b5\U000115b8-\U000115c0\U00011600-\U00011640\U00011644\U00011680-\U000116b7\U000118a0-\U000118df\U000118ff\U00011ac0-\U00011af8\U00012000-\U00012398\U00013000-\U0001342e\U00016800-\U00016a38\U00016a40-\U00016a5e\U00016ad0-\U00016aed\U00016af0-\U00016af4\U00016b00-\U00016b36\U00016b40-\U00016b43\U00016b63-\U00016b77\U00016b7d-\U00016b8f\U00016f00-\U00016f44\U00016f50-\U00016f7e\U00016f8f-\U00016f9f\U0001b000\U0001b001\U0001bc00-\U0001bc6a\U0001bc70-\U0001bc7c\U0001bc80-\U0001bc88\U0001bc90-\U0001bc99\U0001bc9d\U0001bc9e\U0001d165-\U0001d169\U0001d16d-\U0001d172\U0001d17b-\U0001d182\U0001d185-\U0001d18b\U0001d1aa-\U0001d1ad\U0001d242-\U0001d244\U0001d400-\U0001d454\U0001d456-\U0001d49c\U0001d49e\U0001d49f\U0001d4a2\U0001d4a5\U0001d4a6\U0001d4a9-\U0001d4ac\U0001d4ae-\U0001d4b9\U0001d4bb\U0001d4bd-\U0001d4c3\U0001d4c5-\U0001d505\U0001d507-\U0001d50a\U0001d50d-\U0001d514\U0001d516-\U0001d51c\U0001d51e-\U0001d539\U0001d53b-\U0001d53e\U0001d540-\U0001d544\U0001d546\U0001d54a-\U0001d550\U0001d552-\U0001d6a5\U0001d6a8-\U0001d6c0\U0001d6c2-\U0001d6da\U0001d6dc-\U0001d6fa\U0001d6fc-\U0001d714\U0001d716-\U0001d734\U0001d736-\U0001d74e\U0001d750-\U0001d76e\U0001d770-\U0001d788\U0001d78a-\U0001d7a8\U0001d7aa-\U0001d7c2\U0001d7c4-\U0001d7cb\U0001e800-\U0001e8c4\U0001e8d0-\U0001e8d6\U0001ee00-\U0001ee03\U0001ee05-\U0001ee1f\U0001ee21\U0001ee22\U0001ee24\U0001ee27\U0001ee29-\U0001ee32\U0001ee34-\U0001ee37\U0001ee39\U0001ee3b\U0001ee42\U0001ee47\U0001ee49\U0001ee4b\U0001ee4d-\U0001ee4f\U0001ee51\U0001ee52\U0001ee54\U0001ee57\U0001ee59\U0001ee5b\U0001ee5d\U0001ee5f\U0001ee61\U0001ee62\U0001ee64\U0001ee67-\U0001ee6a\U0001ee6c-\U0001ee72\U0001ee74-\U0001ee77\U0001ee79-\U0001ee7c\U0001ee7e\U0001ee80-\U0001ee89\U0001ee8b-\U0001ee9b\U0001eea1-\U0001eea3\U0001eea5-\U0001eea9\U0001eeab-\U0001eebb\U00020000-\U0002a6d6\U0002a700-\U0002b734\U0002b740-\U0002b81d\U0002f800-\U0002fa1d\U000e0100-\U000e01ef"

# Generated from unicode_regex/unicode_regex_groups.scala, same as objective c's \p{Nd}
BMP_NUMERALS = r"0-9\u0660-\u0669\u06f0-\u06f9\u07c0-\u07c9\u0966-\u096f\u09e6-\u09ef\u0a66-\u0a6f\u0ae6-\u0aef\u0b66-\u0b6f\u0be6-\u0bef\u0c66-\u0c6f\u0ce6-\u0cef\u0d66-\u0d6f\u0de6-\u0def\u0e50-\u0e59\u0ed0-\u0ed9\u0f20-\u0f29\u1040-\u1049\u1090-\u1099\u17e0-\u17e9\u1810-\u1819\u1946-\u194f\u19d0-\u19d9\u1a80-\u1a89\u1a90-\u1a99\u1b50-\u1b59\u1bb0-\u1bb9\u1c40-\u1c49\u1c50-\u1c59\ua620-\ua629\ua8d0-\ua8d9\ua900-\ua909\ua9d0-\ua9d9\ua9f0-\ua9f9\uaa50-\uaa59\uabf0-\uabf9\uff10-\uff19"

ASTRAL_NUMERALS = r"\U000104a0-\U000104a9\U00011066-\U0001106f\U000110f0-\U000110f9\U00011136-\U0001113f\U000111d0-\U000111d9\U000112f0-\U000112f9\U000114d0-\U000114d9\U00011650-\U00011659\U000116c0-\U000116c9\U000118e0-\U000118e9\U00016a60-\U00016a69\U00016b50-\U00016b59\U0001d7ce-\U0001d7ff"

HASHTAG_SPECIAL_CHARS = r"_\u200c\u200d\ua67e\u05be\u05f3\u05f4\uff5e\u301c\u309b\u309c\u30a0\u30fb\u3003\u0f0b\u0f0c\xb7"

# A hashtag must contain at least one unicode letter or mark, as well as numbers, underscores, and select special characters.
HASH_SIGNS = r"[#＃]"

HASHTAG_ALPHA = fr"""
    (?:
        [{BMP_LETTERS_AND_MARKS}]
        |
        (?={NON_BMP_CODE_PAIRS})
        (?:[{ASTRAL_LETTERS_AND_MARKS}])
    )"""

HASHTAG_ALPHA_NUMERIC = fr"""
    (?:
        [{BMP_LETTERS_AND_MARKS}{BMP_NUMERALS}{HASHTAG_SPECIAL_CHARS}]
        |
        (?={NON_BMP_CODE_PAIRS})
        (?:
            [{ASTRAL_LETTERS_AND_MARKS}]
            |
            [{ASTRAL_NUMERALS}]
        )
    )"""

END_HASHTAG_MATCH = fr"^(?: {HASH_SIGNS}|://)"

CODE_POINT = r"(?:[^\uD800-\uDFFF]|[\uD800-\uDBFF][\uDC00-\uDFFF])"

HASHTAG_BOUNDARY = fr"""(?:
  ^ | \uFE0E | \uFE0F | $ | (?! {HASHTAG_ALPHA_NUMERIC} | &) {CODE_POINT}
  )"""

VALID_HASHTAG = re.compile(fr"""
    (?= {HASHTAG_BOUNDARY} )
    (?P<hash> {HASH_SIGNS} )
    (?!\uFE0F|\u20E3)
    (?P<tag>{HASHTAG_ALPHA_NUMERIC}*{HASHTAG_ALPHA}{HASHTAG_ALPHA_NUMERIC}*)
    """, re.I + re.X + re.U)

# Mention related regex collection
VALID_MENTION_PRECEDING_CHARS = r"""(?:
    ^
    |
    [^a-zA-Z0-9_!#$%&*@＠]
    |
    (?: ^ | [^a-zA-Z0-9_+~.-] ) (?: rt | RT | rT | Rt ) :?
   )"""

AT_SIGNS= r"[@＠]"

RE_VALID_MENTION_OR_LIST = re.compile(fr"""
    {VALID_MENTION_PRECEDING_CHARS}                    # Preceding characters
    (?P<at> {AT_SIGNS} )                               # At mark
    (?P<screename>  [a-zA-Z0-9_]{1,20} )               # Screen name
    (?: / (?P<list> [a-zA-Z][a-zA-Z0-9_\-]{0,24} ) ) ? # List
    """, re.X)

RE_VALID_REPLY = re.compile(fr"""
    ^
    (?: [{SPACES}]* )
    (?P<at> {AT_SIGNS} )
    (?P<username> [a-zA-Z0-9_]{{1,20}} )
    """, re.X)

RE_END_METNTION_MATCH = re.compile(fr"""
    ^ (?: {AT_SIGNS} | [{LATIN_ACCENT_CHARS}] | :// )
    """, re.X)

# #  URL related regex collection
VALID_URL_PRECEDING_CHARS = fr"(?:[^A-Za-z0-9@＠$#＃{INVALID_CHARS}]|^)"
INVALID_URL_WITHOUT_PROTOCOL_PRECEDING_CHARS = r"[-_./]$"
INVALID_DOMAIN_CHARS = fr"{PUNCT}{SPACES_GROUP}{INVALID_CHARS}"

# VALID_DOMAIN_CHARS = fr"[^{INVALID_DOMAIN_CHARS}]"
# VALID_SUBDOMAIN = fr"(?:(?:{VALID_DOMAIN_CHARS}(?:[_-]|{VALID_DOMAIN_CHARS})*)?{VALID_DOMAIN_CHARS}\.)"
# VALID_DOMAIN_NAME = fr"(?:(?:{VALID_DOMAIN_CHARS}(?:-|{VALID_DOMAIN_CHARS})*)?{VALID_DOMAIN_CHARS}\.)"
# VALID_GTD = r"(?:(?:" + "|".join((
#     "삼성", "닷컴", "닷넷", "香格里拉", "餐厅", "食品", "飞利浦", "電訊盈科", "集团", "通販", "购物", "谷歌", "诺基亚", "联通", "网络", "网站", "网店", "网址", "组织机构", "移动", "珠宝", "点看", "游戏", "淡马锡", "机构", "書籍", "时尚", "新闻", "政府",
#     "政务", "手表", "手机", "我爱你", "慈善", "微博", "广东", "工行", "家電", "娱乐", "天主教", "大拿", "大众汽车", "在线", "嘉里大酒店", "嘉里", "商标", "商店", "商城", "公益", "公司", "八卦", "健康", "信息", "佛山", "企业", "中文网", "中信", "世界",
#     "ポイント", "ファッション", "セール", "ストア", "コム", "グーグル", "クラウド", "みんな", "คอม", "संगठन", "नेट", "कॉम", "همراه", "موقع", "موبايلي", "كوم", "كاثوليك", "عرب", "شبكة",
#     "بيتك", "بازار", "العليان", "ارامكو", "اتصالات", "ابوظبي", "קום", "сайт", "рус", "орг", "онлайн", "москва", "ком", "католик", "дети",
#     "zuerich", "zone", "zippo", "zip", "zero", "zara", "zappos", "yun", "youtube", "you", "yokohama", "yoga", "yodobashi", "yandex", "yamaxun",
#     "yahoo", "yachts", "xyz", "xxx", "xperia", "xin", "xihuan", "xfinity", "xerox", "xbox", "wtf", "wtc", "wow", "world", "works", "work", "woodside",
#     "wolterskluwer", "wme", "winners", "wine", "windows", "win", "williamhill", "wiki", "wien", "whoswho", "weir", "weibo", "wedding", "wed",
#     "website", "weber", "webcam", "weatherchannel", "weather", "watches", "watch", "warman", "wanggou", "wang", "walter", "walmart",
#     "wales", "vuelos", "voyage", "voto", "voting", "vote", "volvo", "volkswagen", "vodka", "vlaanderen", "vivo", "viva", "vistaprint",
#     "vista", "vision", "visa", "virgin", "vip", "vin", "villas", "viking", "vig", "video", "viajes", "vet", "versicherung",
#     "vermögensberatung", "vermögensberater", "verisign", "ventures", "vegas", "vanguard", "vana", "vacations", "ups", "uol", "uno",
#     "university", "unicom", "uconnect", "ubs", "ubank", "tvs", "tushu", "tunes", "tui", "tube", "trv", "trust", "travelersinsurance",
#     "travelers", "travelchannel", "travel", "training", "trading", "trade", "toys", "toyota", "town", "tours", "total", "toshiba",
#     "toray", "top", "tools", "tokyo", "today", "tmall", "tkmaxx", "tjx", "tjmaxx", "tirol", "tires", "tips", "tiffany", "tienda", "tickets",
#     "tiaa", "theatre", "theater", "thd", "teva", "tennis", "temasek", "telefonica", "telecity", "tel", "technology", "tech", "team", "tdk",
#     "tci", "taxi", "tax", "tattoo", "tatar", "tatamotors", "target", "taobao", "talk", "taipei", "tab", "systems", "symantec", "sydney",
#     "swiss", "swiftcover", "swatch", "suzuki", "surgery", "surf", "support", "supply", "supplies", "sucks", "style", "study", "studio",
#     "stream", "store", "storage", "stockholm", "stcgroup", "stc", "statoil", "statefarm", "statebank", "starhub", "star", "staples",
#     "stada", "srt", "srl", "spreadbetting", "spot", "spiegel", "space", "soy", "sony", "song", "solutions", "solar", "sohu", "software",
#     "softbank", "social", "soccer", "sncf", "smile", "smart", "sling", "skype", "sky", "skin", "ski", "site", "singles", "sina", "silk", "shriram",
#     "showtime", "show", "shouji", "shopping", "shop", "shoes", "shiksha", "shia", "shell", "shaw", "sharp", "shangrila", "sfr", "sexy", "sex",
#     "sew", "seven", "ses", "services", "sener", "select", "seek", "security", "secure", "seat", "search", "scot", "scor", "scjohnson",
#     "science", "schwarz", "schule", "school", "scholarships", "schmidt", "schaeffler", "scb", "sca", "sbs", "sbi", "saxo", "save", "sas",
#     "sarl", "sapo", "sap", "sanofi", "sandvikcoromant", "sandvik", "samsung", "samsclub", "salon", "sale", "sakura", "safety", "safe",
#     "saarland", "ryukyu", "rwe", "run", "ruhr", "rugby", "rsvp", "room", "rogers", "rodeo", "rocks", "rocher", "rmit", "rip", "rio", "ril",
#     "rightathome", "ricoh", "richardli", "rich", "rexroth", "reviews", "review", "restaurant", "rest", "republican", "report",
#     "repair", "rentals", "rent", "ren", "reliance", "reit", "reisen", "reise", "rehab", "redumbrella", "redstone", "red", "recipes",
#     "realty", "realtor", "realestate", "read", "raid", "radio", "racing", "qvc", "quest", "quebec", "qpon", "pwc", "pub", "prudential", "pru",
#     "protection", "property", "properties", "promo", "progressive", "prof", "productions", "prod", "pro", "prime", "press", "praxi",
#     "pramerica", "post", "porn", "politie", "poker", "pohl", "pnc", "plus", "plumbing", "playstation", "play", "place", "pizza", "pioneer",
#     "pink", "ping", "pin", "pid", "pictures", "pictet", "pics", "piaget", "physio", "photos", "photography", "photo", "phone", "philips", "phd",
#     "pharmacy", "pfizer", "pet", "pccw", "pay", "passagens", "party", "parts", "partners", "pars", "paris", "panerai", "panasonic",
#     "pamperedchef", "page", "ovh", "ott", "otsuka", "osaka", "origins", "orientexpress", "organic", "org", "orange", "oracle", "open", "ooo",
#     "onyourside", "online", "onl", "ong", "one", "omega", "ollo", "oldnavy", "olayangroup", "olayan", "okinawa", "office", "off", "observer",
#     "obi", "nyc", "ntt", "nrw", "nra", "nowtv", "nowruz", "now", "norton", "northwesternmutual", "nokia", "nissay", "nissan", "ninja", "nikon",
#     "nike", "nico", "nhk", "ngo", "nfl", "nexus", "nextdirect", "next", "news", "newholland", "new", "neustar", "network", "netflix", "netbank",
#     "net", "nec", "nba", "navy", "natura", "nationwide", "name", "nagoya", "nadex", "nab", "mutuelle", "mutual", "museum", "mtr", "mtpc", "mtn",
#     "msd", "movistar", "movie", "mov", "motorcycles", "moto", "moscow", "mortgage", "mormon", "mopar", "montblanc", "monster", "money",
#     "monash", "mom", "moi", "moe", "moda", "mobily", "mobile", "mobi", "mma", "mls", "mlb", "mitsubishi", "mit", "mint", "mini", "mil", "microsoft",
#     "miami", "metlife", "merckmsd", "meo", "menu", "men", "memorial", "meme", "melbourne", "meet", "media", "med", "mckinsey", "mcdonalds",
#     "mcd", "mba", "mattel", "maserati", "marshalls", "marriott", "markets", "marketing", "market", "map", "mango", "management", "man",
#     "makeup", "maison", "maif", "madrid", "macys", "luxury", "luxe", "lupin", "lundbeck", "ltda", "ltd", "lplfinancial", "lpl", "love", "lotto",
#     "lotte", "london", "lol", "loft", "locus", "locker", "loans", "loan", "lixil", "living", "live", "lipsy", "link", "linde", "lincoln", "limo",
#     "limited", "lilly", "like", "lighting", "lifestyle", "lifeinsurance", "life", "lidl", "liaison", "lgbt", "lexus", "lego", "legal",
#     "lefrak", "leclerc", "lease", "lds", "lawyer", "law", "latrobe", "latino", "lat", "lasalle", "lanxess", "landrover", "land", "lancome",
#     "lancia", "lancaster", "lamer", "lamborghini", "ladbrokes", "lacaixa", "kyoto", "kuokgroup", "kred", "krd", "kpn", "kpmg", "kosher",
#     "komatsu", "koeln", "kiwi", "kitchen", "kindle", "kinder", "kim", "kia", "kfh", "kerryproperties", "kerrylogistics", "kerryhotels",
#     "kddi", "kaufen", "juniper", "juegos", "jprs", "jpmorgan", "joy", "jot", "joburg", "jobs", "jnj", "jmp", "jll", "jlc", "jio", "jewelry", "jetzt",
#     "jeep", "jcp", "jcb", "java", "jaguar", "iwc", "iveco", "itv", "itau", "istanbul", "ist", "ismaili", "iselect", "irish", "ipiranga",
#     "investments", "intuit", "international", "intel", "int", "insure", "insurance", "institute", "ink", "ing", "info", "infiniti",
#     "industries", "immobilien", "immo", "imdb", "imamat", "ikano", "iinet", "ifm", "ieee", "icu", "ice", "icbc", "ibm", "hyundai", "hyatt",
#     "hughes", "htc", "hsbc", "how", "house", "hotmail", "hotels", "hoteles", "hot", "hosting", "host", "hospital", "horse", "honeywell",
#     "honda", "homesense", "homes", "homegoods", "homedepot", "holiday", "holdings", "hockey", "hkt", "hiv", "hitachi", "hisamitsu",
#     "hiphop", "hgtv", "hermes", "here", "helsinki", "help", "healthcare", "health", "hdfcbank", "hdfc", "hbo", "haus", "hangout", "hamburg",
#     "hair", "guru", "guitars", "guide", "guge", "gucci", "guardian", "group", "grocery", "gripe", "green", "gratis", "graphics", "grainger",
#     "gov", "got", "gop", "google", "goog", "goodyear", "goodhands", "goo", "golf", "goldpoint", "gold", "godaddy", "gmx", "gmo", "gmbh", "gmail",
#     "globo", "global", "gle", "glass", "glade", "giving", "gives", "gifts", "gift", "ggee", "george", "genting", "gent", "gea", "gdn", "gbiz",
#     "garden", "gap", "games", "game", "gallup", "gallo", "gallery", "gal", "fyi", "futbol", "furniture", "fund", "fun", "fujixerox", "fujitsu",
#     "ftr", "frontier", "frontdoor", "frogans", "frl", "fresenius", "free", "fox", "foundation", "forum", "forsale", "forex", "ford",
#     "football", "foodnetwork", "food", "foo", "fly", "flsmidth", "flowers", "florist", "flir", "flights", "flickr", "fitness", "fit",
#     "fishing", "fish", "firmdale", "firestone", "fire", "financial", "finance", "final", "film", "fido", "fidelity", "fiat", "ferrero",
#     "ferrari", "feedback", "fedex", "fast", "fashion", "farmers", "farm", "fans", "fan", "family", "faith", "fairwinds", "fail", "fage",
#     "extraspace", "express", "exposed", "expert", "exchange", "everbank", "events", "eus", "eurovision", "etisalat", "esurance",
#     "estate", "esq", "erni", "ericsson", "equipment", "epson", "epost", "enterprises", "engineering", "engineer", "energy", "emerck",
#     "email", "education", "edu", "edeka", "eco", "eat", "earth", "dvr", "dvag", "durban", "dupont", "duns", "dunlop", "duck", "dubai", "dtv", "drive",
#     "download", "dot", "doosan", "domains", "doha", "dog", "dodge", "doctor", "docs", "dnp", "diy", "dish", "discover", "discount", "directory",
#     "direct", "digital", "diet", "diamonds", "dhl", "dev", "design", "desi", "dentist", "dental", "democrat", "delta", "deloitte", "dell",
#     "delivery", "degree", "deals", "dealer", "deal", "dds", "dclk", "day", "datsun", "dating", "date", "data", "dance", "dad", "dabur", "cyou",
#     "cymru", "cuisinella", "csc", "cruises", "cruise", "crs", "crown", "cricket", "creditunion", "creditcard", "credit", "courses",
#     "coupons", "coupon", "country", "corsica", "coop", "cool", "cookingchannel", "cooking", "contractors", "contact", "consulting",
#     "construction", "condos", "comsec", "computer", "compare", "company", "community", "commbank", "comcast", "com", "cologne",
#     "college", "coffee", "codes", "coach", "clubmed", "club", "cloud", "clothing", "clinique", "clinic", "click", "cleaning", "claims",
#     "cityeats", "city", "citic", "citi", "citadel", "cisco", "circle", "cipriani", "church", "chrysler", "chrome", "christmas", "chloe",
#     "chintai", "cheap", "chat", "chase", "channel", "chanel", "cfd", "cfa", "cern", "ceo", "center", "ceb", "cbs", "cbre", "cbn", "cba", "catholic",
#     "catering", "cat", "casino", "cash", "caseih", "case", "casa", "cartier", "cars", "careers", "career", "care", "cards", "caravan", "car",
#     "capitalone", "capital", "capetown", "canon", "cancerresearch", "camp", "camera", "cam", "calvinklein", "call", "cal", "cafe", "cab",
#     "bzh", "buzz", "buy", "business", "builders", "build", "bugatti", "budapest", "brussels", "brother", "broker", "broadway",
#     "bridgestone", "bradesco", "box", "boutique", "bot", "boston", "bostik", "bosch", "boots", "booking", "book", "boo", "bond", "bom", "bofa",
#     "boehringer", "boats", "bnpparibas", "bnl", "bmw", "bms", "blue", "bloomberg", "blog", "blockbuster", "blanco", "blackfriday",
#     "black", "biz", "bio", "bingo", "bing", "bike", "bid", "bible", "bharti", "bet", "bestbuy", "best", "berlin", "bentley", "beer", "beauty",
#     "beats", "bcn", "bcg", "bbva", "bbt", "bbc", "bayern", "bauhaus", "basketball", "baseball", "bargains", "barefoot", "barclays",
#     "barclaycard", "barcelona", "bar", "bank", "band", "bananarepublic", "banamex", "baidu", "baby", "azure", "axa", "aws", "avianca",
#     "autos", "auto", "author", "auspost", "audio", "audible", "audi", "auction", "attorney", "athleta", "associates", "asia", "asda", "arte",
#     "art", "arpa", "army", "archi", "aramco", "arab", "aquarelle", "apple", "app", "apartments", "aol", "anz", "anquan", "android", "analytics",
#     "amsterdam", "amica", "amfam", "amex", "americanfamily", "americanexpress", "alstom", "alsace", "ally", "allstate", "allfinanz",
#     "alipay", "alibaba", "alfaromeo", "akdn", "airtel", "airforce", "airbus", "aigo", "aig", "agency", "agakhan", "africa", "afl",
#     "afamilycompany", "aetna", "aero", "aeg", "adult", "ads", "adac", "actor", "active", "aco", "accountants", "accountant", "accenture",
#     "academy", "abudhabi", "abogado", "able", "abc", "abbvie", "abbott", "abb", "abarth", "aarp", "aaa", "onion"
#   )) + ")(?=[^0-9a-zA-Z@]|$))"
#
#
# VALID_CCTLD = r"(?:(?:" + '|'.join((
#     "한국", "香港", "澳門", "新加坡", "台灣", "台湾", "中國", "中国", "გე", "ไทย", "ලංකා", "ഭാരതം", "ಭಾರತ", "భారత్", "சிங்கப்பூர்", "இலங்கை", "இந்தியா", "ଭାରତ", "ભારત", "ਭਾਰਤ",
#     "ভাৰত", "ভারত", "বাংলা", "भारोत", "भारतम्", "भारत", "ڀارت", "پاکستان", "مليسيا", "مصر", "قطر", "فلسطين", "عمان", "عراق", "سورية", "سودان", "تونس",
#     "بھارت", "بارت", "ایران", "امارات", "المغرب", "السعودية", "الجزائر", "الاردن", "հայ", "қаз", "укр", "срб", "рф", "мон", "мкд", "ею", "бел", "бг", "ελ",
#     "zw", "zm", "za", "yt", "ye", "ws", "wf", "vu", "vn", "vi", "vg", "ve", "vc", "va", "uz", "uy", "us", "um", "uk", "ug", "ua", "tz", "tw", "tv", "tt",
#     "tr", "tp", "to", "tn", "tm", "tl", "tk",
#     "tj", "th", "tg", "tf", "td", "tc", "sz", "sy", "sx", "sv", "su", "st", "ss", "sr", "so", "sn", "sm", "sl", "sk", "sj", "si", "sh", "sg", "se", "sd",
#     "sc", "sb", "sa", "rw", "ru", "rs", "ro",
#     "re", "qa", "py", "pw", "pt", "ps", "pr", "pn", "pm", "pl", "pk", "ph", "pg", "pf", "pe", "pa", "om", "nz", "nu", "nr", "np", "no", "nl", "ni", "ng",
#     "nf", "ne", "nc", "na", "mz", "my", "mx",
#     "mw", "mv", "mu", "mt", "ms", "mr", "mq", "mp", "mo", "mn", "mm", "ml", "mk", "mh", "mg", "mf", "me", "md", "mc", "ma", "ly", "lv", "lu", "lt", "ls",
#     "lr", "lk", "li", "lc", "lb", "la", "kz",
#     "ky", "kw", "kr", "kp", "kn", "km", "ki", "kh", "kg", "ke", "jp", "jo", "jm", "je", "it", "is", "ir", "iq", "io", "in", "im", "il", "ie", "id", "hu",
#     "ht", "hr", "hn", "hm", "hk", "gy", "gw",
#     "gu", "gt", "gs", "gr", "gq", "gp", "gn", "gm", "gl", "gi", "gh", "gg", "gf", "ge", "gd", "gb", "ga", "fr", "fo", "fm", "fk", "fj", "fi", "eu", "et",
#     "es", "er", "eh", "eg", "ee", "ec", "dz",
#     "do", "dm", "dk", "dj", "de", "cz", "cy", "cx", "cw", "cv", "cu", "cr", "co", "cn", "cm", "cl", "ck", "ci", "ch", "cg", "cf", "cd", "cc", "ca", "bz",
#     "by", "bw", "bv", "bt", "bs", "br", "bq",
#     "bo", "bn", "bm", "bl", "bj", "bi", "bh", "bg", "bf", "be", "bd", "bb", "ba", "az", "ax", "aw", "au", "at", "as", "ar", "aq", "ao", "an", "am", "al",
#     "ai", "ag", "af", "ae", "ad", "ac"
#  )) + r")(?=[^0-9a-zA-Z@]|$))"
#
# VALID_PUNYCODE = r"(?:xn--[0-9a-z]+)"
# VALI_SPECIAL_CCTLD = r"(?:(?:co|tv)(?=[^0-9a-zA-Z@]|$))"
# VALID_DOMAIN = fr"(?:{VALID_SUBDOMAIN}*{VALID_DOMAIN_NAME}(?:{VALID_GTLD}|{VALID_CCTLD}|{VALID_PUNYCODE}))"
# RE_VALID_ASCII_DOMAIN = re.compile(fr"(?:(?:[\-a-z0-9{LATIN_ACCENT_CHARS}]+)\.)+(?:{VALID_GTLD}|{VALID_CCTLD}|{VALID_PUNYCODE})", re.I)
# RE_INVALID_SHORT_DOMAIN = re.compile(r"^{VALID_DOMAIN_NAME}{VALID_CCTLD}$", re.I)
# RE_VALID_SPECIAL_SHORT_DOMAIN = re.compile(fr"^{VALID_DOMAIN_NAME}{VALID_SPECIAL_CCTLD}$", re.I)
# VALID_PORT_NUMBER = "[0-9]+"
# CYRILLIC_LETTERS_AND_MARKS = r"\u0400-\u04FF"
# RE_VALID_URL_PATH_CHARS = re.compile(fr"[a-z{CYRILLIC_LETTERS_AND_MARKS}0-9!\*';:=\+,\.\$\/%#\[\]\-\u2013_~@\|&{LATIN_ACCENT_CHARS}]", re.I)
# # Allow URL paths to contain up to two nested levels of balanced parens
# #  1. Used in Wikipedia URLs like /Primer_(film)
# # 2. Used in IIS sessions like /S(dfd346)/
# # 3. Used in Rdio URLs like /track/We_Up_(Album_Version_(Edited))/
# VALID_URL_BALANCED_PARENS = re.compile(fr"""
#   (?i:
#     \(
#        (?:
#         '#{validGeneralUrlPathChars}+
#         |
#         # allow one nested level of balanced parentheses
#         (?:
#           {validGeneralUrlPathChars}*
#         \(
#           {validGeneralUrlPathChars}+
#         \)
#           {validGeneralUrlPathChars}*
#         )
#       )
#     \)
#   )
#   """, re.V + re.I)
# # Valid end-of-path chracters (so /foo. does not gobble the period).
# #  1. Allow =&# for empty URL parameters and other URL-join artifacts
# VALID_URL_PATH_ENDING_CHARS = re.compile(fr"[\+\-a-z{CYRILLIC_LETTERS_AND_MARKS}0-9=_#\/{LATIN_ACCENT_CHARS}]|(?:{VALID_URL_BALANCED_PARENS})")
# #  Allow @ in a url, but only in the middle. Catch things like http://example.com/@user/
# VALID_URL_PATH = re.compile("""(?:
#     (?:
#       {VALID_GENERAL_URL_PATH_CHARS}*
#       (?:{VALID_URL_BALANCED_PARENS}{VALID_GENERAL_URL_PATH_CHARS}*)*
#       {VALID_URL_PATH_CHARS}
#       )|(?:@{VALID_GENERAL_URL_PATH_CHARS}+\/)
#     )""", re.I + re.X)
#
# VALID_URL_QUERY_CHARS = r"(?i:[a-z0-9!?\*'@\(\);:&=\+\$\/%#\[\]\-_\.,~|])"
# VALID_URL_QUERY_ENDING_CHARS = r"(?i:[a-z0-9_&=#\/])"
# RE_EXTRACT_URL = re.compile(fr"""
#       (?P<preceding>{VALID_URL_PRECEDING_CHARS})                                   # 1 Preceeding chracter
#       (?P<url>                                                        # 2 URL
#         (?P<protocol>https?:\/\/)?                                    # 3 Protocol (optional)
#         (?P<domain>{VALID_DOMAIN})                                     # 4 Domain(s)
#         (?P<port>?::({VALID_PORT_NUMBER}))?                             # 5 Port number (optional)
#         (?P<path>\/{VALID_URL_PATH}*)?                                  # 6 URL Path
#         (?P<query>\?{VALID_URL_QUERY_CHARS}*{VALID_URL_QUERY_ENDING_CHARS})? # 7 Query String
#       )""", re.I + re.X)
#
# #   twttr.txt.regexen.validTcoUrl = /^https?:\/\/t\.co\/[a-z0-9]+/i;
# URL_HAS_PROTOCOL = re.compile(r"^https?:\/\/", re.I)
# URL_HAS_HTTPS = re.compile(r"^https:\/\/", re.I)
#
# # cashtag related regex
# CASHTAG = r"(?i:[a-z]{1,6}(?:[._][a-z]{1,2})?)"
# RE_VALID_CASHTAG = re.compile('(^|{SPACES})(\\$)({CASHTAG})(?=$|\\s|[{PUNCT}])', re.I)

# These URL validation pattern strings are based on the ABNF from RFC 3986
  # twttr.txt.regexen.validateUrlUnreserved = /[a-z\u0400-\u04FF0-9\-._~]/i;
  # twttr.txt.regexen.validateUrlPctEncoded = /(?:%[0-9a-f]{2})/i;
  # twttr.txt.regexen.validateUrlSubDelims = /[!$&'()*+,;=]/i;
  # twttr.txt.regexen.validateUrlPchar = regexSupplant('(?:
  #   '#{validateUrlUnreserved}|
  #   '#{validateUrlPctEncoded}|
  #   '#{validateUrlSubDelims}|
  #   '[:|@]
  # ')', 'i');
#
#   twttr.txt.regexen.validateUrlScheme = /(?:[a-z][a-z0-9+\-.]*)/i;
#   twttr.txt.regexen.validateUrlUserinfo = regexSupplant('(?:
#     '#{validateUrlUnreserved}|
#     '#{validateUrlPctEncoded}|
#     '#{validateUrlSubDelims}|
#     ':
#   ')*', 'i');
#
#   twttr.txt.regexen.validateUrlDecOctet = /(?:[0-9]|(?:[1-9][0-9])|(?:1[0-9]{2})|(?:2[0-4][0-9])|(?:25[0-5]))/i;
#   twttr.txt.regexen.validateUrlIpv4 = regexSupplant(/(?:#{validateUrlDecOctet}(?:\.#{validateUrlDecOctet}){3})/i);
#
#   // Punting on real IPv6 validation for now
#   twttr.txt.regexen.validateUrlIpv6 = /(?:\[[a-f0-9:\.]+\])/i;
#
#   // Also punting on IPvFuture for now
#   twttr.txt.regexen.validateUrlIp = regexSupplant('(?:
#     '#{validateUrlIpv4}|
#     '#{validateUrlIpv6}
#   ')', 'i');
#
#   // This is more strict than the rfc specifies
#   twttr.txt.regexen.validateUrlSubDomainSegment = /(?:[a-z0-9](?:[a-z0-9_\-]*[a-z0-9])?)/i;
#   twttr.txt.regexen.validateUrlDomainSegment = /(?:[a-z0-9](?:[a-z0-9\-]*[a-z0-9])?)/i;
#   twttr.txt.regexen.validateUrlDomainTld = /(?:[a-z](?:[a-z0-9\-]*[a-z0-9])?)/i;
#   twttr.txt.regexen.validateUrlDomain = regexSupplant(/(?:(?:#{validateUrlSubDomainSegment}\.)*(?:#{validateUrlDomainSegment}\.)#{validateUrlDomainTld})/i);
#
#   twttr.txt.regexen.validateUrlHost = regexSupplant('(?:
#     '#{validateUrlIp}|
#     '#{validateUrlDomain}
#   ')', 'i');
#
#   // Unencoded internationalized domains - this doesn't check for invalid UTF-8 sequences
#   twttr.txt.regexen.validateUrlUnicodeSubDomainSegment = /(?:(?:[a-z0-9]|[^\u0000-\u007f])(?:(?:[a-z0-9_\-]|[^\u0000-\u007f])*(?:[a-z0-9]|[^\u0000-\u007f]))?)/i;
#   twttr.txt.regexen.validateUrlUnicodeDomainSegment = /(?:(?:[a-z0-9]|[^\u0000-\u007f])(?:(?:[a-z0-9\-]|[^\u0000-\u007f])*(?:[a-z0-9]|[^\u0000-\u007f]))?)/i;
#   twttr.txt.regexen.validateUrlUnicodeDomainTld = /(?:(?:[a-z]|[^\u0000-\u007f])(?:(?:[a-z0-9\-]|[^\u0000-\u007f])*(?:[a-z0-9]|[^\u0000-\u007f]))?)/i;
#   twttr.txt.regexen.validateUrlUnicodeDomain = regexSupplant(/(?:(?:#{validateUrlUnicodeSubDomainSegment}\.)*(?:#{validateUrlUnicodeDomainSegment}\.)#{validateUrlUnicodeDomainTld})/i);
#
#   twttr.txt.regexen.validateUrlUnicodeHost = regexSupplant('(?:
#     '#{validateUrlIp}|
#     '#{validateUrlUnicodeDomain}
#   ')', 'i');
#
#   twttr.txt.regexen.validateUrlPort = /[0-9]{1,5}/;
#
#   twttr.txt.regexen.validateUrlUnicodeAuthority = regexSupplant(
#     '(?:(#{validateUrlUserinfo})@)?'  + // $1 userinfo
#     '(#{validateUrlUnicodeHost})'     + // $2 host
#     '(?::(#{validateUrlPort}))?'        //$3 port
#   , "i");
#
#   twttr.txt.regexen.validateUrlAuthority = regexSupplant(
#     '(?:(#{validateUrlUserinfo})@)? // $1 userinfo
#     '(#{validateUrlHost})'           + // $2 host
#     '(?::(#{validateUrlPort}))?'       // $3 port
#   , "i");
#
#   twttr.txt.regexen.validateUrlPath = regexSupplant(/(\/#{validateUrlPchar}*)*/i);
#   twttr.txt.regexen.validateUrlQuery = regexSupplant(/(#{validateUrlPchar}|\/|\?)*/i);
#   twttr.txt.regexen.validateUrlFragment = regexSupplant(/(#{validateUrlPchar}|\/|\?)*/i);
#
#   // Modified version of RFC 3986 Appendix B
#   twttr.txt.regexen.validateUrlUnencoded = regexSupplant(
#     '^'                               + // Full URL
#     '(?:'                             +
#       '([^:/?#]+):\\/\\/'             + // $1 Scheme
#     ')?'                              +
#     '([^/?#]*)'                       + // $2 Authority
#     '([^?#]*)'                        + // $3 Path
#     '(?:'                             +
#       '\\?([^#]*)'                    + // $4 Query
#     ')?'                              +
#     '(?:'                             +
#       '#(.*)'                         + // $5 Fragment
#     ')?$'
#   , "i");
#
