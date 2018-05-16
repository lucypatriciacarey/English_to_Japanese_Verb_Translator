### CS4744 Project
### Translates English verb into Japanese verbs

import romkan
import csv

special_iku_forms = ["iku"]
special_ru_forms = [
	"taberu", 
	"miru", 
	"miseru",
	"fueru", 
	"oboeru", 
	"oshieru", 
	"shirabeta", 
	"wasureru", 
	"hajimeru", 
	"akeru", 
	"tojiru", 
	"ageru", 
	"kowareru", 
	"neru", 
	"ukeru", 
	"kariru", 
	"ikiru", 
	"tasukeru",
	"mitsukeru",
	"kariru",
	"nageru",
	"nigeru",
	"mazeru",
	"kaeru",
	"shiraberu",
	"okiru"
	]

verb_roots = {
		"eat" : "taberu",
		"drink" : "nomu",
		"buy" : "kau",
		"watch": "miru",
		"look": "miru",
		"see": "miru",
		"put": "oku",
		"write": "kaku",
		"draw": "kaku",
		"show": "miseru",
		"send": "okuru",
		"go": "iku",
		"meet": "au",
		"make": "tsukuru",
		"produce": "tsukuru",
		"return": "kaeru",
		"increase": "fueru",
		"decrease": "heru",
		"learn": "narau",
		"memorize": "oboeru",
		"teach": "oshieru",
		"notify": "oshieru", 
		"check": "shiraberu",
		"forget": "wasureru",
		"escape": "nigeru", 
		"start": "hajimeru", 
		"shoot": "utsu",
		"laugh": "warau",
		"suck": "suu",
		"cry": "naku",
		"finish": "owaru", 
		"open": "akeru", 
		"close": "tojiru",
		"win": "katsu", 
		"talk": "hanasu", 
		"speak": "hanasu", 
		"turn": "magaru", 
		"stop": "tomaru", 
		"stay": "tomaru", 
		"sit": "suwaru", 
		"wash": "arau", 
		"give": "ageru",
		"break": "kowareru", 
		"sleep": "neru",
		"wake": "okiru", 
		"grill": "yaku", 
		"roast": "yaku", 
		"repair": "naosu", 
		"fix": "naosu", 
		"receive": "ukeru", 
		"borrow": "kariru", 
		"rise": "agaru", 
		"wear": "kiru", 
		"swim": "oyogu",
		"live": "ikiru",
		"listen": "kiku",
		"mix": "mazeru",
		"run": "hashiru",
		"dance": "odoru",
		"anger": "okoru",
		"play": "asobu",
		"scowl": "niramu",
		"want": "hoshigaru",
		"stab": "sasu",
		"search": "sagasu",
		"find": "mitsukeru",
		"throw": "nageru",
		"protect": "mamoru",
		"pay": "harau",
		"stand": "tatsu",
		"remember": "oboeru",
		"count": "kazoeru",
		"understand": "wakaru",
		"know": "wakaru",
		"kill": "korosu",
		"swell": "fukuramu",
		"jump": "haneru",
		"step": "fumu",
		"fly": "tobu",
		"sing": "utau",
		"climb": "noboru",
		"die": "shinu",
		"help": "tasukeru",
		"study": "bennkyou+suru", 
		"investigate": "chousa+suru",
		"exchange": "koukann+suru",
		"contact": "rennraku+suru", 
		"oppose": "hanntai+suru",
		"practice": "rennshuu+suru",
		"announce": "happyou+suru",
		"change": "hennka+suru",
		"reply": "hennji+suru", 
		"work": "shigoto+suru",
		"exercise": "unndou+suru",
		"marry": "kekkonn+suru",
		"graduate": "sotsugyou+suru",
		"order": "chuumonn+suru",
		"drive": "unnten+suru",
		"calculate": "keisann+suru",
		"complete": "kannsei+suru",
		"develop": "kaihatsu+suru",
		"report": "houkoku+suru",
		"focus": "shuuchyuu+suru",
		"confess": "kokuhaku+suru",
		"agree": "sannsei+suru",
		"prepare": "jyunnbi+suru",
		"explain": "setsumei+suru",
		"shop": "kaimono+suru",
		"travel": "ryokou+suru",
		"promise": "yakusoku+suru",
		"attend": "shusseki+suru",
		"manage": "kanri+suru",
		"print": "innsatsu+suru",
		"introduce": "shoukai+suru",
		"verify": "kakuninn+suru",
		"clean": "souji+suru",
	}

english_verb_special_past_tense = {
		"ate": "eat",
		"drank": "drink",
		"bought": "buy",
		"saw": "see",
		"wrote": "write",
		"drew": "draw",
		"went": "go",
		"met": "meet",
		"made": "make",
		"taught": "teach",
		"forgot": "forget",
		"won": "win",
		"spoke": "speak",
		"sat": "sit",
		"broke": "break",
		"slept": "sleep",
		"rose": "rise",
		"wore": "wear",
		"drove": "drive",
		"ran": "run",
		"threw": "throw",
		"understood": "understand",
		"flew": "fly",
		"sang": "sing",
		"knew": "know",
		"swam": "swim",
		"gave": "give",
		"sent": "send"
	}

inv_english_verb_special_past_tense  = {v: k for k, v in english_verb_special_past_tense.items()}

property_mapping = {
	"will": ["future"],
	"was": ["past"],
	"have": ["perfect"],
	"had": ["past", "perfect"],
	"not": ["negation"],
	"don't": ["negation"],
	"doesn't": ["present", "negation"],
	"didn't": ["past", "negation"],
	"won't": ["future", "negation"],
	"no": ["negation"],
	"might": ["potential"],
	"may": ["potential"]
}

manual = ("[help|h]\t\t\t\tDisplays keyword help manual\n" +
		  "[translate|trans] [english verb]\tTranslates given verb into Japanese\n" +
		  "[has] [english verb]\t\t\tReturns True if verb ROOT exists in program dictionary\n" +
		  "[create]\t\t\t\tCreates a txt file containg mapping of English VP to Japanese VP\n" +
		  "[quit|q]\t\t\t\tExit Program")  

#=====================================================================
#							FUNCTIONS 
#=====================================================================
def toContinuous(root):
	if root.endswith("ie"):
		root = rreplace(root, "ie", "y")
	elif root.endswith("e") and not root.endswith("ee"):
		root = rreplace(root, "e", "")
	elif len(root) == 3 and root[-1] in "tnm" and root[-2] == "i":
		root = root + root[-1]
	return root + "ing"

def toPast(root):
	if root in inv_english_verb_special_past_tense:
		return inv_english_verb_special_past_tense[root]

	if root.endswith("y"):
		root = rreplace(root, "y", "i")
	elif root.endswith("e"):
		root = rreplace(root, "e", "")

	return root + "ed"

def createMapping(value=None):
	#for each verb root
	table = [["English VP", "Japanese VP"]]
	for root, _ in verb_roots.items():
		phrases = [
			root, 
			toPast(root), 
			"will "+root, 
			"doesn't "+root, 
			"didn't "+root,
			"won't "+root,
			toContinuous(root),
			"was "+toContinuous(root),
			"will be "+toContinuous(root),
			"not "+toContinuous(root),
			"was not "+toContinuous(root),
			"will not be "+toContinuous(root),
			"have "+toPast(root),
			"had "+toPast(root),
			"will have "+toPast(root),
			"have not "+toPast(root),
			"had not "+toPast(root),
			"will have not "+toPast(root),
			"have being "+toContinuous(root),
			"had been "+toContinuous(root),
			"will have been "+toContinuous(root),
			"have not being "+toContinuous(root),
			"had not been "+toContinuous(root),
			"will have not been "+toContinuous(root)
			]
		for phrase in phrases:
			root, properties = parseEnglish(phrase.split())
			output = toJapanese(root, properties)
			table.append([phrase, output])

	with open("English_to_Japanese.txt",'w',encoding='utf8') as f:
		for eng, jap in table:
			f.write(eng+','+jap+'\n')

	#perfect continuous -> have been rooting, had been rooting, will have been rooting + Negation


def printManual(value=None):
	return manual

def rreplace(s, old, new, occurrence=1):
	li = s.rsplit(old, occurrence)
	return new.join(li)

def isVowel(char):
	return char in "aeuio"

def parseEnglish(value):
	if not value:
		return "", ["WARNING: No Value given"]

	properties = set([])
	root = ""
	start = 0
	for i, word in enumerate(value):
		if word in property_mapping:
			for prop in property_mapping[word]:
				properties.add(prop)
		else:
			if root == "":
				tense = ""
				if word.endswith("ing") and word not in inv_english_verb_special_past_tense:
					properties.add("continuous")
					tense = "present"
					if word[:-3] in verb_roots:
						root = word[:-3]
					elif word[:-3]+"e" in verb_roots:
						root = word[:-3]+"e"
					elif word[:-4] in verb_roots:
						root = word[:-4]
					elif word[:-4]+"ie" in verb_roots:
						root = word[:-4]+"ie"
				elif word.endswith("ed"):
					tense = "past"
					if word[:-1] in verb_roots:
						root = word[:-1]
					elif word[:-2] in verb_roots:
						root = word[:-2]
					elif word[:-3] in verb_roots:
						root = word[:-3]
					elif word[:-3]+"y" in verb_roots:
						root = word[:-3]+"y"
				elif word in english_verb_special_past_tense:
					tense = "past"
					root = english_verb_special_past_tense[word]
				elif word in verb_roots:
					tense = "present"
					root = word
				
				if "present" not in properties and "past" not in properties and "future" not in properties and tense:
					properties.add(tense)

				if root:
					print("Analyzing the phrase " + str(value[start:i+1]))
					return root, list(properties)

	return "", ["WARNING: No root/verb found"]

def toJapanese(root, properties):
	print("Properties: " + str(properties))
	verb = verb_roots[root].split("+")
	root = verb[0]
	addon = ""
	if len(verb) > 1:
		addon = verb[1]

	if addon: 
		if "past" in properties:
			addon = rreplace(addon, "su", "shi")
			addon = rreplace(addon, "ru", "ta")
			
		if "continuous" in properties:
			addon = rreplace(addon, "shi", "shite")
			addon = rreplace(addon, "su", "shite")
			addon = rreplace(addon, "ru", "iru")
			addon = rreplace(addon, "ta", "ita")

		if "negation" in properties:
			addon = rreplace(addon, "su", "shi")
			addon = rreplace(addon, "ru", "nai")
			addon = rreplace(addon, "ta", "nakatta")

		if "potential" in properties:
			addon += "kamo"
	else:
		if root.endswith("tsu"):
			addon = root[-3:]
			root = root[:len(root)-3]
		else:
			addon = root[-2:]
			root = root[:len(root)-2]

		tenten = False
		special = False
		if root+addon in special_ru_forms:
			special = True

		if ("past" in properties and not "negation" in properties) or "continuous" in properties:
			if "mu" in addon or "nu" in addon or "bu" in addon or "gu" in addon:
				tenten = True
			addon = rreplace(addon, "tsu", "t")
			addon = rreplace(addon, "su", "shi")
			addon = rreplace(addon, "ku", "i")
			addon = rreplace(addon, "gu", "i")
			#Speical ru -> t cases 
			if special:
				addon = rreplace(addon, "ru", "")
			else:
				addon = rreplace(addon, "ru", "t")
			addon = rreplace(addon, "bu", "nn")
			addon = rreplace(addon, "mu", "nn")
			addon = rreplace(addon, "nu", "nn")
			addon = rreplace(addon, "u", "t")

		#Speical ku -> t cases (only for iku *go*)
		if root+addon == "ii":
			addon = "t"

		if "past" in properties:
			if special:
				addon = rreplace(addon, "ru", "")
			addon+="ta"

		if "continuous" in properties:
			addon+="te"
			if "tate" in addon:
				addon = rreplace(addon, "tate", "teta")
			
			if addon.endswith("ta"):
				addon = rreplace(addon, "ta", "ita")
			else:
				addon+="iru"

		if "negation" in properties:
			addon = rreplace(addon, "iru", "inai")
			if addon.endswith("ta"):
				if len(addon) > 3 and isVowel(addon[-4]) and addon[-3] == "u":
					addon = rreplace(addon, "u", "wa")
				else:
					addon = rreplace(addon, "tsu", "tu")
					addon = rreplace(addon, "u", "a")
				addon = rreplace(addon, "ta", "nakatta")
			else:
				addon = rreplace(addon, "tsu", "tu")
				if isVowel(addon[-2]) and addon[-1] == "u":
					addon = rreplace(addon, "u", "wanai")
				else:
					if special:
						addon = rreplace(addon, "ru", "nai")
					else:
						addon = rreplace(addon, "u", "anai")


		if "potential" in properties:
			addon += "kamo"

		if tenten:
			addon = rreplace(addon, "te", "de")
			if not addon.endswith("ta") or "de" not in addon:
				addon = rreplace(addon, "ta", "da")

	verb = root + addon
	return romkan.to_hiragana(verb) + " (" + verb + ")"

def translate(value=None):
	if not value:
		return "WARNING: No Input Detected"

	root, properties = parseEnglish(value)

	if root:
		return toJapanese(root, properties)

	return properties[0]

def hasWord(value=None):
	if value:
		verb = value[0]
		return str(verb in verb_roots)
	else:
		return "False"

def quit(value=None):
	return None

def doPrompt():
	user_input = input(">>> ").split()
	if user_input:
		key = user_input[0].lower()
		value = user_input[1:]
		return {"key": key, "value": value}
	else:
		return None

def processInput(user_input):
	if user_input["key"] in actions:
		return actions[user_input["key"]](user_input["value"])
	else:
		return "WARNING: Invalid keyword"

#=====================================================================
#							MAIN
#=====================================================================

actions = {
	"help": printManual, 
	"h": printManual, 
	"translate": translate, 
	"trans": translate, 
	"has": hasWord,
	"quit": quit,
	"quit()": quit,
	"q": quit,
	"create": createMapping
}

def main():
	print("---------------------------------------------------\n" + 
		  "Welcome to English Verb to Japanese Verb Translator\n" +
		  "---------------------------------------------------\n" +
		  "Type 'help' for more information.")
	exit = False
	while not exit:
		user_input = doPrompt()
		if not user_input:
			continue
		output = processInput(user_input)
		if not output:
			exit = True
		else:
			print(output)
			print()

if __name__ == "__main__":
	main()