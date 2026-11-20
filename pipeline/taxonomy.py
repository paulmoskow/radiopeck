"""RadioPeck tag taxonomy: the dictionary used by normalize_tags.py.

This is a STARTER dictionary written by hand. It is meant to be extended from
the "Top unmapped tags" section of the report: add a synonym to the right list,
re-run, and the coverage numbers show the effect.

Matching is done on a normalised key (lower case, accents and punctuation
removed, see normalize_tags.norm_key), so "Música Clásica", "musica clasica"
and "música-clásica" are the same entry. You do not need to list spelling
variants that differ only by case, accents or punctuation.
"""

# Words that are removed from the START and END of a tag before lookup:
# "pop music" -> "pop", "radio rock" -> "rock", "online radio" -> (nothing left).
GENERIC_WORDS = {
    "music", "musica", "musik", "musique", "muzyka", "muzika", "музыка",
    "radio", "radios", "radyo", "rádio", "радио", "fm", "am", "station", "stations",
    "estacion", "emisora", "sender", "online", "web", "webradio", "internet",
    "stream", "streaming",
}

# Whole tags that carry no information for search.
GENERIC_TAGS = [
    "hits", "hit", "best", "top", "the best", "best of", "lo mejor", "free", "live",
    "en vivo", "directo", "24 7", "24h", "247", "hd", "mp3", "aac", "stereo",
    "entretenimiento", "entertainment", "unterhaltung", "divertissement",
    "intrattenimento", "entretenimento", "programa", "program", "programacion",
    "programming", "broadcast", "broadcasting", "emision", "emisiones", "transmision",
    "favorites", "favourites", "favoritos", "greatest hits", "top hits", "new", "nuevo",
    "nueva", "novedades", "estrenos", "sound", "sounds", "audio", "international",
    "internacional", "internazionale", "internationale", "global", "worldwide", "all",
    "todo", "general", "the", "a", "fm radio", "am radio", "hot", "hot hits",
    "online only", "exclusive", "exclusivo", "misc", "tv", "television", "mainstream",
    "contemporary", "discography", "programas envivo", "programas en vivo", "envivo",
    "social", "ai",
]

# canonical genre -> synonyms (any language)
GENRES = {
    "pop": [
        "pop", "top 40", "top40", "chr", "pop hits", "pop international",
        "pop internacional", "europop", "synthpop", "synth pop", "teen pop", "mandopop",
        "cantopop", "c pop", "cpop", "pop moderno", "流行", "流行音乐", "поп", "попса",
        "juvenil", "contemporary hits", "charts", "top charts", "top 100", "top 40 hits",
        "hit parade", "hitparade",
    ],
    "rock": [
        "rock", "classic rock", "hard rock", "alternative rock", "indie rock", "punk rock",
        "punk", "grunge", "hardcore", "progressive rock", "prog rock", "soft rock",
        "rock and roll", "rockabilly", "rock alternativo", "rock en espanol",
        "rock espanol", "rock clasico", "rock classique", "garage rock",
        "psychedelic rock", "post rock", "рок", "摇滚", "搖滾", "ロック", "록",
    ],
    "alternative": [
        "alternative", "alt", "indie", "indie pop", "indie folk", "independent",
        "alternativo", "shoegaze", "britpop", "emo", "new wave",
    ],
    "metal": [
        "metal", "heavy metal", "death metal", "black metal", "thrash metal",
        "power metal", "doom metal", "metalcore", "nu metal", "symphonic metal",
        "метал", "металл",
    ],
    "jazz": [
        "jazz", "smooth jazz", "acid jazz", "swing", "bebop", "big band", "jazz fusion",
        "free jazz", "latin jazz", "cool jazz", "jazzy", "gypsy jazz", "dixieland",
        "nu jazz", "vocal jazz", "jazz vocal", "contemporary jazz", "джаз", "爵士",
        "爵士乐", "ジャズ", "재즈",
    ],
    "blues": ["blues", "delta blues", "chicago blues", "electric blues", "блюз", "布鲁斯"],
    "classical": [
        "classical", "klassik", "klassisch", "klassische", "classique", "clasica",
        "classica", "classico", "opera", "baroque", "barock", "symphony", "symphonic",
        "orchestra", "orchestral", "chamber", "chamber music", "string quartet",
        "contemporary classical", "early music", "классика",
        "классическая", "古典", "古典音乐", "古典乐", "クラシック", "클래식",
    ],
    "electronic": [
        "electronic", "electronica", "electro", "edm", "techno", "house", "deep house",
        "tech house", "progressive house", "trance", "psytrance", "goa",
        "drum and bass", "dnb", "drum n bass", "dubstep", "electronic dance", "idm",
        "minimal", "minimal techno", "hardstyle", "breakbeat", "electro house",
        "future house", "tropical house", "elektronik", "elektronisch", "electronique",
        "trip hop", "synthwave", "электронная", "электроника", "电子", "电子音乐",
        "エレクトロニック",
    ],
    "dance": [
        "dance", "club", "eurodance", "disco", "dancefloor", "dance hits", "nu disco",
        "italo disco", "euro disco", "dance classics", "tanz", "danse", "danza",
        "танцевальная", "舞曲", "dj", "party",
    ],
    "hip hop": [
        "hip hop", "hiphop", "rap", "trap", "gangsta rap", "old school hip hop",
        "french rap", "boom bap", "drill", "grime", "cloud rap", "хип хоп", "рэп",
        "说唱",
    ],
    "r&b/soul": [
        "rnb", "soul", "neo soul", "funk", "motown", "urban", "contemporary rnb",
        "rhythm and blues", "ритм энд блюз",
    ],
    "country": [
        "country", "country and western", "country western", "western", "americana",
        "bluegrass", "outlaw country", "honky tonk",
    ],
    "folk": [
        "folk", "folklore", "folklor", "folclore", "folclor", "folklorico",
        "singer songwriter", "traditional", "tradicional", "volksmusik", "volkstumlich",
        "trad", "celtic", "irish folk", "народная", "фолк", "民谣", "民歌",
    ],
    "reggae": [
        "reggae", "ska", "dancehall", "dub", "roots reggae", "rocksteady", "ragga",
        "raggamuffin",
    ],
    "latin": [
        "latin", "latino", "latina", "latin pop", "latin hits", "salsa", "bachata",
        "merengue", "cumbia", "reggaeton", "tropical", "banda", "norteno", "ranchera",
        "rancheras", "regional mexicano", "regional mexicana", "mariachi", "vallenato",
        "tejano", "corridos", "corrido", "grupera", "urbano", "urbana", "latin urban",
        "bolero", "tango", "flamenco", "rumba", "son cubano", "timba", "champeta",
        "mambo", "pop latino", "regional mexican", "mexican", "mexicana", "mexicano",
        "mexican regional", "popular mexicana", "musica popular mexicana",
        "tradicional mexicana", "traditional mexican", "grupero", "banda nortena",
        "nortena",
    ],
    "brazilian": [
        "sertanejo", "samba", "pagode", "forro", "mpb", "axe", "brazilian", "brasileira",
        "funk carioca", "funk brasileiro",
    ],
    "schlager": [
        "schlager", "deutsche schlager", "partyschlager", "discofox", "german schlager",
    ],
    "oldies": [
        "oldies", "oldie", "golden oldies", "classic hits", "retro", "vintage",
        "nostalgia", "nostalgie", "evergreens", "evergreen", "golden hits", "golden age",
        "classic", "classics", "clasicos", "retro hits", "musica del recuerdo",
        "del recuerdo", "recuerdo", "recuerdos",
    ],
    "ambient": [
        "ambient", "chillout", "chill out", "chill", "lounge", "downtempo",
        "easy listening", "new age", "relaxation", "relax", "relaxing", "meditation",
        "spa", "background", "muzak", "smooth", "calm", "sleep", "cafe", "coffee",
        "chilled", "atmospheric", "space music", "nature sounds", "relajante",
    ],
    "world": [
        "world", "ethnic", "weltmusik", "world beat", "afrobeat", "afrobeats", "african",
        "afro", "middle eastern", "oriental", "balkan", "caribbean", "calypso", "soca",
        "hawaiian", "afro pop", "highlife", "kizomba", "kuduro", "semba",
        "coupe decale", "amapiano", "gqom",
    ],
    "indian": [
        "bollywood", "filmi", "bhangra", "indian", "hindustani", "carnatic", "ghazal",
        "qawwali", "bhajan", "kirtan", "desi", "tollywood", "kollywood",
        "indian classical",
    ],
    "asian pop": [
        "kpop", "k pop", "jpop", "j pop", "anime", "jrock", "j rock", "krock",
        "thai pop", "vpop", "v pop", "city pop", "visual kei", "idol", "idols",
    ],
    "instrumental": ["instrumental", "instrumentals", "piano", "guitar"],
    "soundtrack": [
        "soundtrack", "soundtracks", "film music", "film scores", "movie music", "ost",
        "video game", "game music", "film", "cinema", "bande originale", "bso",
    ],
    "seasonal": [
        "christmas", "xmas", "weihnachten", "navidad", "noel", "natale", "natal",
        "holiday", "holidays", "halloween", "easter", "villancicos",
    ],
    "variety": [
        "variety", "eclectic", "mixed", "various", "mix", "all genres", "varied",
        "variado", "variada", "variados", "variedades", "diverse", "diverso",
        "multi genre", "multigenre", "genre mix", "all styles", "everything",
        "miscellaneous", "random", "vielfalt", "gemischt", "divers", "varie",
        "crossover", "full service",
    ],
    "romantic": [
        "romantic", "romantica", "romantico", "love songs", "baladas", "balada",
        "balada pop", "ballads", "ballad", "power ballads",
    ],
    "experimental": [
        "experimental", "avant garde", "avantgarde", "noise", "sound art",
    ],
    "adult contemporary": [
        "adult contemporary", "ac", "hot ac", "soft ac", "adult hits", "lite", "mor",
        "middle of the road", "adult alternative",
    ],
}

# one tag -> several values ("category:value")
MULTI = {
    "pop rock": ["genre:pop", "genre:rock"],
    "pop and rock": ["genre:pop", "genre:rock"],
    "rock and pop": ["genre:rock", "genre:pop"],
    "blues rock": ["genre:blues", "genre:rock"],
    "country rock": ["genre:country", "genre:rock"],
    "folk rock": ["genre:folk", "genre:rock"],
    "jazz and blues": ["genre:jazz", "genre:blues"],
    "bossa nova": ["genre:jazz", "genre:brazilian"],
    "lofi": ["genre:ambient", "genre:hip hop"],
    "lo fi": ["genre:ambient", "genre:hip hop"],
    "chillhop": ["genre:ambient", "genre:hip hop"],
    "news talk": ["format:news", "format:talk"],
    "news and talk": ["format:news", "format:talk"],
    "news and information": ["format:news"],
    "sports talk": ["format:sports", "format:talk"],
    "hip hop and rnb": ["genre:hip hop", "genre:r&b/soul"],
    "hip hop rnb": ["genre:hip hop", "genre:r&b/soul"],
    "pop dance": ["genre:pop", "genre:dance"],
    "dance pop": ["genre:pop", "genre:dance"],
    "local news": ["format:news", "format:local"],
    "noticias locales": ["format:news", "format:local"],
    "local information": ["format:news", "format:local"],
    "localtalk": ["format:talk", "format:local"],
    "local talk": ["format:talk", "format:local"],
    "sports news": ["format:sports", "format:news"],
    "noticias nacionales": ["format:news"],
    "greek pop": ["genre:pop", "language:greek"],
    "greek folk": ["genre:folk", "language:greek"],
}

# canonical format -> synonyms. A format is what a station DOES (news, talk,
# sports, religion) or WHO runs it (public, community, campus), not a music genre.
FORMATS = {
    "news": [
        "news", "noticias", "noticia", "nachrichten", "actualites", "actualite",
        "notizie", "noticiero", "noticiarios", "noticiario", "informativo",
        "informativa", "journal", "telejornal", "jornal", "jornalismo", "current affairs",
        "aktuell", "aktuelles", "actualidad", "atualidades", "новости", "новини",
        "information", "informacion", "informations",
        "新闻", "新聞", "ニュース", "뉴스",
    ],
    "talk": [
        "talk", "talk show", "talkshow", "hablada", "palabra", "gesprach", "discussion",
        "debate", "interview", "interviews", "phone in", "call in", "politics",
        "politik", "politica", "politique", "politiek", "opinion", "entrevistas",
        "spoken", "spoken word", "speech", "wort", "parole", "conversation",
        "conversacion", "tertulia", "ток", "ток шоу", "разговорное", "脱口秀",
    ],
    "sports": [
        "sport", "sports", "deporte", "deportes", "deportivo", "deportiva", "esporte",
        "esportes", "fussball", "football", "soccer", "futbol", "futebol", "calcio",
        "basketball", "baseball", "nfl", "nba", "mlb", "nhl", "cricket", "rugby",
        "tennis", "motorsport", "formula 1", "f1", "golf", "hockey", "olympics",
        "racing", "ciclismo", "cycling", "boxing", "спорт", "体育", "スポーツ", "스포츠",
        "live sports",
    ],
    "religion": [
        "religion", "religious", "religioso", "religiosa", "religiosos", "religios",
        "religieux", "religieuse", "religione", "christian", "gospel", "catholic",
        "catholique", "catolica", "catolico", "cattolica", "katholisch", "islam",
        "islamic", "muslim", "quran", "koran", "coran", "bible", "biblia", "bibel",
        "worship", "praise", "praise and worship", "ccm", "christian contemporary",
        "evangelical", "evangelica", "evangelico", "evangelisch", "jesus", "jesus christ",
        "jesucristo", "god", "dios", "gott", "church", "iglesia", "kirche", "eglise",
        "igreja", "orthodox", "orthodoxe", "ortodoxa", "buddhist", "buddhism", "hindu",
        "spiritual", "spirituality", "espiritual", "sermon", "sermons", "prayer",
        "oracion", "gebet", "cristiana", "cristiano", "cristianas", "christlich",
        "chretien", "chretienne", "adventist", "adventista", "pentecostal", "baptist",
        "lutheran", "protestant", "protestante", "ministerio", "ministry",
        "православное", "православие", "христианское", "христианство", "ислам",
        "молитва", "宗教", "基督教", "佛教", "christian preaching", "christian teaching",
        "preaching", "sunnah", "hadith",
    ],
    "kids": [
        "kids", "kid", "children", "childrens", "ninos", "infantil", "infantiles",
        "enfants", "enfant", "kinder", "kindermusik", "criancas", "infanzia", "bambini",
        "дети", "детское", "儿童", "child", "baby", "bedtime",
    ],
    "community": [
        "community", "comunitaria", "comunitario", "communautaire", "gemeinschaft",
        "burgerfunk", "comunidade", "free radio",
        "radio libre", "radio libera", "freies radio", "grassroots", "associative",
        "associatif",
    ],
    "local": [
        "local", "locale", "lokal", "lokaal", "regional", "regionale", "regionales",
        "regionaal",
    ],
    "campus": [
        "campus", "college", "university", "universidad", "universitaria",
        "universitario", "universite", "universitat", "universidade", "student",
        "students", "estudiantil", "etudiant", "school", "high school", "colegio",
        "escuela", "ecole", "schule", "universityradio", "collegeradio",
    ],
    "public": [
        "public", "public service", "public broadcasting", "public broadcaster", "npr",
        "pbs", "bbc", "publica", "publico", "publique", "offentlich", "service public",
        "servizio pubblico", "state radio", "estatal", "ard", "ndr", "wdr", "swr", "rtve",
        "rtbf", "orf", "srf",
    ],
    "culture": [
        "culture", "cultural", "cultura", "kultur", "arts", "arte", "art", "literature",
        "literatura", "theater", "theatre", "teatro", "history", "historia", "geschichte",
        "science", "ciencia", "wissenschaft", "education", "educational", "educacion",
        "educativa", "educativo", "bildung", "learning", "language learning",
        "aprendizaje", "podcast", "podcasts", "documentary", "documentaries",
        "documentales", "audiobooks", "audiobook", "books", "libros", "radio drama",
        "horspiel", "drama", "old time radio", "otr",
    ],
    "comedy": [
        "comedy", "humor", "humour", "comedia", "humoristico", "comique", "komodie",
        "funny", "satire", "stand up", "standup",
    ],
    "service": [
        "weather", "tiempo", "wetter", "meteo", "meteorologia", "traffic", "trafico",
        "verkehr", "trafic",
    ],
}

# Spoken-word names of decades that the "80s" regex cannot see.
DECADE_WORDS = {
    "sesentas": "1960s", "setentas": "1970s", "ochentas": "1980s", "noventas": "1990s",
    "oitentas": "1980s", "anos oitenta": "1980s", "anos noventa": "1990s",
}

# canonical language (as Radio Browser names them, English, lower case) ->
# names a tag may use. Language names that already appear in the stations'
# own `language` field are also picked up automatically from the data.
LANGUAGES = {
    "english": ["english", "ingles", "englisch", "anglais", "inglese", "английский",
                "英语", "英語", "영어"],
    "spanish": ["spanish", "espanol", "castellano", "spanisch", "espagnol", "spagnolo",
                "espanhol", "испанский", "西班牙语", "西班牙語"],
    "german": ["german", "deutsch", "aleman", "allemand", "tedesco", "alemao",
               "deutschsprachig", "немецкий", "德语", "德語"],
    "french": ["french", "francais", "frances", "franzosisch", "francese", "francophone",
               "французский", "法语", "法語"],
    "portuguese": ["portuguese", "portugues", "portugiesisch", "portugais", "portoghese",
                   "португальский", "葡萄牙语"],
    "italian": ["italian", "italiano", "italienisch", "italien", "italiana",
                "итальянский", "意大利语", "意大利語"],
    "russian": ["russian", "ruso", "russisch", "russe", "russo", "русский", "俄语",
                "俄語", "русскоязычное"],
    "chinese": ["chinese", "chino", "chinesisch", "chinois", "cinese", "中文", "汉语",
                "漢語", "普通话", "mandarin", "cantonese", "китайский", "廣東話", "粤语",
                "國語"],
    "japanese": ["japanese", "japones", "japanisch", "japonais", "giapponese", "日本語",
                 "日语", "日本语", "японский"],
    "korean": ["korean", "coreano", "koreanisch", "coreen", "한국어", "韩语", "韓語",
               "корейский"],
    "arabic": ["arabic", "arabe", "arabisch", "arabo", "العربية", "عربي", "阿拉伯语",
               "арабский"],
    "greek": ["greek", "griego", "griechisch", "grec", "greco", "ελληνικά", "ελληνικα",
              "греческий"],
    "dutch": ["dutch", "neerlandes", "holandes", "nederlands", "niederlandisch",
              "neerlandais", "olandese", "vlaams", "flemish"],
    "polish": ["polish", "polaco", "polnisch", "polonais", "polacco", "polski", "польский"],
    "turkish": ["turkish", "turco", "turkisch", "turc", "turkce", "турецкий"],
    "hindi": ["hindi", "हिंदी", "हिन्दी"],
    "ukrainian": ["ukrainian", "ucraniano", "ukrainisch", "українська", "украинский"],
    "romanian": ["romanian", "rumano", "rumanisch", "romana", "румынский"],
    "swedish": ["swedish", "sueco", "schwedisch", "svenska"],
    "norwegian": ["norwegian", "noruego", "norwegisch", "norsk"],
    "danish": ["danish", "danes", "danisch", "dansk"],
    "finnish": ["finnish", "finlandes", "finnisch", "suomi"],
    "czech": ["czech", "checo", "tschechisch", "cestina"],
    "hungarian": ["hungarian", "hungaro", "ungarisch", "magyar"],
    "hebrew": ["hebrew", "hebreo", "hebraisch", "עברית"],
    "persian": ["persian", "farsi", "persa", "persisch", "فارسی"],
    "indonesian": ["indonesian", "indonesio", "bahasa indonesia"],
    "thai": ["thai", "tailandes", "ภาษาไทย"],
    "vietnamese": ["vietnamese", "vietnamita", "tieng viet"],
    "catalan": ["catalan", "catala"],
    "galician": ["galician", "gallego", "galego"],
    "basque": ["basque", "vasco", "euskara"],
}

# Region words and non-English country names that are geography, not music.
# Country and state names that occur in the stations' own `country` and
# `state` fields are picked up automatically from the data.
GEO_WORDS = [
    "europe", "europa", "европа", "欧洲", "africa", "afrique", "afrika", "африка",
    "asia", "asien", "asie", "азия", "亚洲", "oceania", "oceanie", "australasia",
    "north america", "norteamerica", "nordamerika", "amerique du nord",
    "south america", "sudamerica", "suramerica", "sudamerika", "central america",
    "centroamerica", "latin america", "latinoamerica", "amerique latine", "lateinamerika",
    "america", "americas", "caribe", "caraibes", "karibik", "middle east",
    "medio oriente", "moyen orient", "naher osten", "scandinavia", "escandinavia",
    "skandinavien", "nordic", "balkans", "balcanes", "mediterranean", "mediterraneo",
    "iberia", "benelux", "dach", "maghreb", "sahel",
    "mexico", "espana", "deutschland", "osterreich", "schweiz", "suisse", "svizzera",
    "italia", "brasil", "brasilien", "peru", "perú", "republica dominicana",
    "puerto rico", "costa rica", "panama", "guatemala", "honduras", "el salvador",
    "nicaragua", "россия", "украина", "беларусь", "中国", "日本", "한국", "ελλαδα",
    "turkiye", "polska", "nederland", "belgie", "belgique", "sverige", "norge",
    "danmark", "eire", "usa", "uk",
    "mx", "mex", "cdmx", "mexico city", "ciudad de mexico", "valle de mexico", "sureste",
]

# Radio networks and brands. Not genres, but useful for "find station X" queries.
BRANDS = [
    "nrj", "mvs", "mvs radio", "radiopolis", "radiorama", "grupo acir", "acir", "exa",
    "exa fm", "ponte exa", "la estacion exacta", "la estacion naranja", "cherie fm",
    "iheart", "iheart radio", "sipout ai", "la hora nacional",
]


# =========================================================================== #
# Second batch: added after running the first version on the real catalogue's
# list of 2,700 tags (tags used by 3+ stations). Kept in one block so it is easy
# to extend: add a synonym to the right list, re-run normalize_tags.py, compare.
# =========================================================================== #

def _w(text: str) -> list[str]:
    """'a|b|c' -> ['a', 'b', 'c'] (keeps the long lists below readable)."""
    return [x.strip() for x in text.split("|") if x.strip()]


def _merge(target: dict, extra: dict) -> None:
    for key, values in extra.items():
        bucket = target.setdefault(key, [])
        bucket.extend(v for v in values if v not in bucket)


# "ai" moves from generic to the ai-generated format below.
GENERIC_TAGS = [t for t in GENERIC_TAGS if t not in {"ai"}]

GENERIC_WORDS |= set(_w(
    "hits|hit|city|only|programming|programs|programas|shows|commercial|national|nacional"))

# Words that do not count against a phrase when it is split into parts.
STOPWORDS = set(_w(
    "of|de|del|la|el|los|las|en|y|e|and|the|da|do|dos|das|der|die|und|et|le|les|du|des|for|to|"
    "in|on|a|an|i|o|ou|or|with|con|sin|para|por|al|un|una|by|at|from|is|s|from|más|mas|de la"))

GENERIC_TAGS += _w(
    "multicultural|multilingual|diversity|exclusively|other|undefined|test|"
    "new format rebranding|curated|digital|mobile|pc|direct|fun|today|current|modern|"
    "generalist|programas grabados|grabados|grabadas|envivo|decades|"
    "la mejor|lo mejor|only the golden classics|non stop|nonstop|music only|"
    "only music|non commercial music|free radio station|favorite|favourite|"
    "radio station|stations|network|networks|channel|canal|studio|live playlist|playlist|"
    "playlists|best music|best hits|super|ultra|max|maxima|plus|fm center|"
    "radio show|season|seasons|vol|new format|rebranding|name|unknown|none|nothing|general music")

# --- technical tags: frequencies, bitrates, codecs, stream formats ------------
TECH_TAGS = _w(
    "https|http|m3u8|m3u|pls|hls|flac|lossless|dab|dab+|hd radio|hdradio|ogg|opus|"
    "wma|mono|iptv|livestream|live stream|liveradio|stream|browserfriendly|metadata|tts|"
    "high quality audio|high quality|hq|hd audio|ssl|icecast|shoutcast|radionomy|streaming radio|"
    "web stream|audio stream|html5|player")

# --- features a station says about itself (not genres) ------------------------
FEATURES = {
    "ad-free": _w(
        "no ads|sans pub|sanspub|sans publicite|commercial free|commercial-free|adfree|ad free|"
        "ad-free|no commercials|no advertising|sin publicidad|sem publicidade|werbefrei|"
        "keine werbung|pas de pub|no adverts|ohne werbung|reklamfri"),
    "non-commercial": _w(
        "non commercial|non-commercial|noncommercial|non profit|non-profit|nonprofit|"
        "not for profit|not-for-profit|listener supported|listener-supported|"
        "nicht kommerzielles lokalradio|nichtkommerzielles lokalradio|noncomm|"
        "sin fines de lucro|sem fins lucrativos|donation supported"),
}

# --- mood / activity: useful for vibe-style queries ---------------------------
MOODS = {
    "workout": _w("workout|running|run|fitness|gym|training|cardio|exercise|motivational|"
                  "motivation|spinning"),
    "focus": _w("study|focus|work|working|concentration|music for study|deep work|reading|"
                "homework|productivity|studying"),
    "driving": _w("driving|road|roadtrip|road trip|night drive|drive|highway|car"),
    "upbeat": _w("upbeat|happy|happy music|feel good|energetic|energy|positive energie|"
                 "positive energy|uplifting|good vibes|sunshine|joyful|cheerful|fresh"),
    "beach": _w("beach|beach bar|beach club|beachclub|pool beach bar|sunset|poolside|summer|"
                "tropical vibes|balearic"),
    "night": _w("night|nightlife|late night|midnight|after dark|dreamy"),
    "romance": _w("date night|candlelight|intimate"),
}

BRANDS += _w(
    "multimedios|multimedios radio|globalmedia|la mejor aqui nomas|la mejor fm|w radio|los40|"
    "los 40|star group|rogers media|mediaset|sveriges radio|mitteldeutscher rundfunk|mdr|"
    "mvs noticias|caracol radio|radio disney|radio formula|radio formula primera cadena|"
    "radio formula segunda cadena|luznetwork|capital media|valanci media group|stereo uno|imer|"
    "instituto mexicano de la radio|radio psr|radio sa|p4|vox|vox fm|uniradio|egofm|reyfm|"
    "arroba fm|@fm|te conecta|kiss fm|kiss|star radio|cadena rasa|indes radios|la poderosa|"
    "la lupe|la comadre|la ke buena|la z|la q|la octava|la caliente|la ranchera|la mexicana|"
    "la tremenda|la sabrosita|la patrona|la invasora|la mas picuda|el exametro|el viejon|"
    "el fonografo|magic fm|retro fm|mix fm|vive fm|boom fm|soy fm|love fm|fm rainbow|fm globo|"
    "jovem pan|rtl|cbc|abc|pri|apm|gbh|pacifica|ncs|ncs radio|promodj|prisa radio|"
    "radio france|srg ssr|rtp|antena 1|cope|rne|iheart|stingray network|bauer radio|"
    "global radio|mdr sputnik|mdr schlagerwelt|meine schlagerwelt|ndr hd|ndr fernsehen|"
    "norddeutscher rundfunk|nordmagazin|hallo niedersachsen|hamburg journal|"
    "schleswig holstein magazin|mdr thuringen|mdr sachsen anhalt|radio sa|radio nucleo|"
    "radio lobo|radio crystal|radio united|radio felicidad|radio centro|radio ranchito|"
    "radio universal|radio cadena enciso|radio resultados|vibra radio|exa|"
    "frecuencia ultimate|nachklang fm|dpark|vot|turkiye nin sesi|"
    "sipout|sipout ai|moi merino|egofm|vox love station|vox radio hits|los 40 principales|"
    "xeu|walm|rsl|rdp|mgt|ntr|nrw|cdc|fda|who|esquina 32|ponte exa|studio exa|rock n exa|"
    "grd multimedia|gps media|jb multimedia|nrm comunicaciones|ntr medios de comunicacion|"
    "alica medios|tribuna comunicacion|mg comunicacion|nucleo comunicacion del sureste|"
    "corporacion bajio comunicaciones|organizacion radiofonica tamaulipeca|"
    "grupo audiorama comunicaciones")

GEO_WORDS += _w(
    "jalisco|veracruz|sinaloa|sonora|chihuahua|baja california|baja california sur|nuevo leon|"
    "coahuila|guanajuato|puebla|michoacan|san luis potosi|tamaulipas|estado de mexico|guerrero|"
    "aguascalientes|nayarit|zacatecas|yucatan|tabasco|campeche|chiapas|oaxaca|quintana roo|"
    "morelos|hidalgo|durango|queretaro|colima|tlaxcala|monterrey|guadalajara|tijuana|mexicali|"
    "ciudad juarez|los mochis|culiacan|hermosillo|mazatlan|tampico|leon|merida|morelia|tepic|"
    "torreon|xalapa|poza rica|piedras negras|ensenada|puerto vallarta|acapulco|boca del rio|"
    "ciudad obregon|ciudad victoria|ciudad del carmen|gdl|mty|slp|cdmx|mexico city|"
    "ciudad de mexico|ciudad mexico|valle de mexico|sureste|bajio|el paso|los angeles|san diego|"
    "nogales|chetumal|villahermosa|fresnillo|saltillo|monclova|gomez palacio|irapuato|celaya|"
    "cuernavaca|toluca|pachuca|tapachula|orizaba|tuxtla gutierrez|tuxtla|comitan|zamora|apodaca|"
    "metepec|ameca|autlan|manzanillo|tehuacan|atlixco|coatzacoalcos|tantoyuca|tuxpan|navojoa|"
    "guasave|guamuchil|delicias|parral|hidalgo del parral|reynosa|mcallen|calexico|eagle pass|"
    "ciudad acuna|agua prieta|san luis rio colorado|cancun|playa del carmen|los cabos|"
    "san jose del cabo|bahia de banderas|tlalmanalco|perote|calvillo|chilpancingo|"
    "ciudad guzman|ciudad valles|apatzingan|fortin de las flores|rosarito|guadalupe|victoria|"
    "texas|california|florida|new york|new york city|chicago|boston|denver|seattle|las vegas|"
    "sacramento|pittsburgh|minneapolis|boise|miami|austin|nashville|baltimore|arizona|kentucky|"
    "fayetteville|bowling green|waynesboro|pensacola|dubois|london|londres|england|inglaterra|"
    "united kingdom|reino unido|great britain|scotland|wales|ireland|france|canada|toronto|"
    "calgary|halifax|quebec|australia|sydney|melbourne|brisbane|auckland|new zealand|germany|"
    "bayern|sachsen|sachsen anhalt|thuringen|thueringen|niedersachsen|hamburg|"
    "mecklenburg vorpommern|schleswig holstein|nurnberg|dresden|leipzig|halle|halle saale|"
    "magdeburg|cologne|koln|burgenlandkreis|silesia|galicia|galiza|madeira|mallorca|ibiza|"
    "sicilia|lazio|napoli|torino|catania|roma|almeria|viseu|foz do iguacu|parana|rosario|"
    "cordoba|buenos aires|la pampa|general pico|pehuajo|resistencia chaco|bogota|caracas|"
    "guayaquil|san pedro sula|phnom penh|ibadan|ankara|simferopol|nizhniy novgorod|krym|alsace|"
    "auvergne|occitanie|dordogne|gers|reunion|antilles|region caribe|pacific|west coast|"
    "argentina|brasil|brazil|colombia|chile|peru|ecuador|venezuela|bolivia|uruguay|paraguay|"
    "cuba|spain|espana|portugal|italy|italia|austria|switzerland|netherlands|belgium|poland|"
    "russia|ukraine|belarus|romania|moldova|bulgaria|serbia|croatia|bosnia|bosna|macedonia|"
    "albania|greece|turkey|turkiye|cyprus|north cyprus|kktc|israel|egypt|morocco|tunisia|"
    "algeria|nigeria|ghana|cameroon|south africa|kenya|ethiopia|iraq|iran|saudi|kuwait|bahrain|"
    "uae|india|south india|tamilnadu|pakistan|bangladesh|sri lanka|nepal|indonesia|thailand|"
    "vietnam|cambodia|philippines|malaysia|singapore|china|guangdong|shenzhen|japan|korea|"
    "taiwan|hong kong|estonia|latvia|lithuania|finland|sweden|norway|denmark|iceland|"
    "kazakhstan|armenia|georgia|azerbaijan|uzbekistan|jamaica|haiti|trinidad|bahamas|"
    "united states|america|northern ireland|catalunya|catalonia|euskadi|andalucia|"
    "west|east|north|south")

MULTI.update({
    "pop clasico": ["genre:pop", "genre:oldies"],
    "classic pop": ["genre:pop", "genre:oldies"],
    "world news": ["format:news"],
    "international news": ["format:news"],
    "electro swing": ["genre:electronic", "genre:jazz"],
    "bossa": ["genre:jazz", "genre:brazilian"],
    "bossanova": ["genre:jazz", "genre:brazilian"],
    "garage punk": ["genre:rock"],
    "garage rock": ["genre:rock"],
})

DECADE_WORDS.update({
    "sixties": "1960s", "seventies": "1970s", "eighties": "1980s", "nineties": "1990s",
    "fifties": "1950s", "noughties": "2000s", "gen x": "1990s", "20th century": "1900s",
})

_merge(LANGUAGES, {
    "german": _w("deutsche|deutscher|deutsches|deutschsprachig"),
    "dutch": _w("hollands|nederlandse|nederlandstalig"),
    "portuguese": _w("portuguesa|portugues|portuguesas"),
    "russian": _w("русская|русские|русское"),
})

_merge(GENRES, {
    "pop": _w(
        "soft pop|alternative pop|adult pop|vocal pop|hyperpop|sophisti pop|electropop|electro pop|"
        "deutschpop|austropop|latino pop|euro hits|singlecharts|partycharts|radiocharts|top100|"
        "hit music|hit radio|contemporary hit radio|todays hits|today s hits|summer hits|"
        "summer tunes|ndw|madonna|ed sheeran|популярная|популярное|pop punk|spanish hits|"
        "russian hits|ретро хиты|top music|muzica usoara|muzica usoara romaneasca|"
        "tragoudia|pop espanol|pop folk"),
    "rock": _w(
        "alt rock|alt-rock|stoner rock|pub rock|krautrock|kraut rock|surf rock|surf music|surf|"
        "punkrock|hardrock|psychedelic|psychedelia|prog|progressive|post punk|post grunge|"
        "postgrunge|album rock|active rock|mainstream rock|modern rock|melodic rock|"
        "instrumental rock|slow rock|glam rock|art rock|southern rock|gothic rock|garage punk|"
        "queen|rolling stones|linkin park|deutschrock|deutsch rock|rock nacional|rock latino|"
        "rock classics|rock hits|rock music|dance rock|electronic rock|college rock|new rock|"
        "jamband|jam band|grindcore|zabavna rock"),
    "alternative": _w(
        "gothic|goth|darkwave|dark wave|cold wave|minimal wave|industrial|ebm|futurepop|"
        "indie dance|indie electronic|indie music|independent artists|independent radio|"
        "underground|underground music|alternative classics|ozgun muzik|dream pop|shoegaze|"
        "experimental rock|art pop"),
    "metal": _w(
        "classic metal|glam metal|hair metal|progressive metal|alternative metal|sludge|stoner|"
        "stoner metal|doom|thrash|trash metal|deathcore|metallica|iron maiden|heavy rock|"
        "heavy-metal|wacken|wacken open air|black metal|death metal|symphonic metal"),
    "jazz": _w(
        "classic jazz|piano jazz|post bop|soft jazz|smoothjazz|smoothjazz com|jazz funk|"
        "jazzfunk|jazz lounge|fusion|ragtime|big bands|big band|jazz piano|jazz vocal|"
        "free jazz|hard bop|cool jazz|nu jazz|nu-jazz|jazz standards|standards"),
    "classical": _w(
        "classical piano|classical guitar|classical baroque|modern classical|modern composition|"
        "light orchestral|traditional opera|choral|choir|classique|solo piano|strings|violin|"
        "medieval|mittelalter|gregorian|chant|bach|beethoven|mozart|vivaldi|chopin|classical california|"
        "boston symphony orchestra|orchestra|symphony|new age piano|piano music|"
        "musica clasica|clasica romantica|romantic classical|electroacoustic|contemporary composition"),
    "electronic": _w(
        "bass|jungle|garage|ukg|uk garage|speed garage|2step|breaks|hard dance|gabber|frenchcore|"
        "makina|happy hardcore|uptempo hardcore|hands up|handsup|hard trance|techstep|neurofunk|"
        "liquid|liquid funk|liquid dnb|future bass|future funk|chillstep|psybient|psychill|"
        "chiptune|chiptunes|8bit|8 bit|bitpop|demoscene|retrowave|vaporwave|darksynth|synth|"
        "synths|cyberpunk|moombahton|glitch|elektro|eletronic|eletronica|hypertechno|big room|"
        "bigroom|dubtechno|dub techno|microhouse|rominimal|jackin house|techhouse|deephouse|"
        "afrohouse|afro house|melodic house|chill house|organic house|funky house|soulful house|"
        "bass house|latin house|house music|house|chillsynth|futuresynth|spacesynth|eurobeat|"
        "trance|progressive trance|uplifting trance|vocal trance|melodic trance|"
        "goa trance|psytrance|melodic techno|dark techno|hard techno|deep techno|electro techno|"
        "ambient techno|acid|drum n bass|d n b|dub step|raw hardstyle|hardstyle|"
        "all of edm and all of music|edm festival|burning man"),
    "dance": _w(
        "rave|raves|clubbing|houseparty|house party|partymix|party mix|party hits|club hits|"
        "club dance|club house|dj mix|dj mixes|djs|dj sets|dj remix|dj radio|deejay|deejay remix|"
        "remix|remixes|remixed|mashup|mashups|mixes|mixtape|mixtapes|partybreaks|"
        "ibiza club|dance classics|nightclub|disco funk|discomusic|disco music|italo|"
        "italo dance|italodance|dancefloor|90s dance|70s disco|hot mix|mix show|live dj"),
    "hip hop": _w(
        "phonk|freestyle|deutschrap|german rap|rap us|rap hiphop|hip-hop|gangsta|boom bap|"
        "classic hip hop|old school hip hop|underground hip hop|christian hip hop|trap soul|"
        "chilled trap"),
    "r&b/soul": _w(
        "rb|p funk|p-funk|boogie|funky|groove|grooves|soulful|classic soul|modern soul|"
        "smooth soul|retro r b|rnb classics|r b soul|r b music|rhythm blues|blue eyed soul|"
        "urban contemporary|mainstream urban"),
    "country": _w(
        "red dirt|cowboy|new country|classic country|traditional country|modern country|"
        "contemporary country|country pop|alternative country|texas country|country music|"
        "outlaw|nashville sound"),
    "folk": _w(
        "acoustic|accoustic|acoustic folk|alt folk|neofolk|bard|trova|nueva trova|breton|gaelic|"
        "narodna|narodna muzika|izvorna|domaca|muzica populara|populara|polka|zydeco|cajun|"
        "halk muzigi|turk halk muzigi|turku|laiko|laika|dimotika|rebetiko|rebetico|"
        "cretan|greek traditional|world folk|folk classics|occasional folk classics|"
        "volkstumlich|blasmusik|trad folk|traditional music|traditional folk|ballermann"),
    "latin": _w(
        "latinoamericana|musica latinoamericana|radios latinoamericanas|"
        "banda tradicional|banda nortena|sierreno|nortena|gruperas|grupera|corridos tumbados|"
        "cumbia ecuatoriana|cumbia peruana|peruvian cumbia|cumbias|chicha|chicha ecuatoriana|"
        "cuarteto|regueton|reggeton|regaeton|reggaeton|dembow|salsas|salsa colombiana|"
        "latin salsa|classic salsa|boleros mexicanos|fiesta mexicana|tecnomerengue|"
        "musica ecuatoriana|musica andina|chamame|bailable|musica chilena|tropical music|"
        "musica tropical|musica mexicana|mexican regional|corridos|musica de mariachi|"
        "radio ranchera|rancheras|reggae en espanol|latin urban|latin hits"),
    "brazilian": _w(
        "sertanejo raiz|sertaneja|forro|campeira|gaucha|gauchesca|gaudeira|nativista|caipira|"
        "moda de viola|brega|pagode|samba pagode|musica popular brasileira|brazilian pop|"
        "brazilian rock|brazilian music"),
    "reggae": _w("reggea|reagge|roots reggae|dub reggae|dub|rocksteady|ragga|dancehall|reggae gospel"),
    "world": _w(
        "manele|manele vechi|etno|etnic|ethno|arabesk|tarab|rai|kwaito|highlife|hiplife|konpa|"
        "kompa|zouk|soca|dangdut|koplo|campursari|afrofusion|afro pop|afropop|colinde|"
        "world hits|world beats|worldbeat|world middle east|indigenous music|african music|"
        "caribbean music|tamil songs|tamil music|tamil hits|tamil cinema music|kurdish songs|"
        "fado|kizomba|"
        "balkan|balkan music|turbo folk|etno"),
    "asian pop": _w("opm|pinoy|anime openings|anime radio|vocaloid|city pop|citypop|j pop|"
                    "jrock|krock|thai pop|v pop"),
    "instrumental": _w("instrumental music|solo guitar|drums"),
    "oldies": _w(
        "throwbacks|throwback|flashback|flash back|remember|timeless|legends|goldies|gold|golden|"
        "old hits|oldschool|old school|golden music|all time classics|all time-classics|"
        "old age|heritage|vintage radio|vintage music|retro music|retro hits|"
        "classic radio|classic hits|adult standards|pop classics|clasico|musica del recuerdo|"
        "regional del recuerdo|gruperas del recuerdo|nostalgic"),
    "chanson": _w(
        "chanson|chansons|chanson francaise|chansons francaises|french chansons|"
        "rire et chansons|variete francaise|chanson francophone"),
    "schlager": _w(
        "schlagerwelt|schlagerhits|kultschlager|popschlager|partyschlager|apres ski|apresski|"
        "karneval|karnevalsmusik|musikantenstadl|deutsche schlager|discofox oldies|"
        "volkstumliche musik"),
    "romantic": _w(
        "balada romantica|romantica y femenina|solo musica romantica|amor solo musica romantica|"
        "romantik|liebe|liebeslieder|love|love song|love songs|amor|amor es|romance|lovesongs|"
        "love-songs|vida romantica|romanticas|baladas romanticas|luna de amor|bella musica|"
        "musica romantica|fm musica romantica|slow"),
    "ambient": _w("drone|ambient electronic|ambient lounge|smooth lounge|vocal lounge|lofi beats|"
                  "chill beats|lofi hip hop|chilled|relaxed|ambiental|deep ambient|"
                  "zen ambient|easy music|soft music|beautiful music|calm music|sounds of nature|"
                  "entspannung|healing music|sleep music|spa music|yacht rock"),
    "soundtrack": _w(
        "movie|movies|video games|video game music|videogame music|videogames|videogame|"
        "gamemusic|game music|game|games|retro games|arcade|vgm|tv themes|movie trailers|"
        "movie scores|movie soundtracks|movie music|film score|film scores|musicals|musical|"
        "broadway|showtunes|show tunes|disney music|grand theft auto|fallout|classic movies"),
    "novelty": _w(
        "gachi|gachibass|gachimuchi|gachiremix|гачи|гачи ремикс|гачимучи|meme music|novelty|"
        "parody|covers|каверы|comedy songs"),
    "vocal": _w("a cappella|acappella|vocal|vocals|crooner|crooners|female vocalists|"
                "female vocals|female voices|femalevocals|barbershop|doo-wop|doo wop"),
    "seasonal": _w("carols|christmas songs|christmas rock|christmas music|weihnachtslieder|"
                   "joulumusiikki|jul|last christmas|natal|navidad|noel|holiday music|"
                   "holiday music nov dec|seasonal holiday|x mas|x-mas|carnaval|carnival"),
    "variety": _w("mixed programming|eclectic programming|eclectica|ecletica|eclectic prog|"
                  "variedad|variados|varios|various music|music variety|variety hits|"
                  "all genres|generalista|multi genre|all of music|mixed music|diverse"),
})

_merge(FORMATS, {
    "news": _w(
        "journalism|jornalismo|jornalismo all news|reportage|info|infoformate|infotainment|"
        "haber|haberler|nieuws|wiadomosci|stiri|noticieros|noticia|panorama informativo|"
        "informativo ntr|sondersendungen|special broadcast|news radio|all news|breaking news|"
        "current affairs|actualites|world news"),
    "talk": _w(
        "hablada|habladas|talks|talkback|cross talk|crosstalk|debates|debatten|commentary|"
        "comentarios|comentario|lectures|chat|morning show|morning shows|radio shows|live show|"
        "live shows|разговорный|разговорное|razgovornoe|political|conservative|patriot|"
        "conspiracy|conspiracies|conspiracy theories|nationalism|nationalist|feminist|feminista|"
        "lgbt|lgbtq|gay|propaganda|protest|activism|activismo|mujer|women|opinion|"
        "talk and speech|talk speech"),
    "sports": _w(
        "bundesliga|hockey|baseball|match|matches|league|liga|football commentary|"
        "sports commentary|horse racing|racing|espacio deportivo|deportes y musica|"
        "esportes futebol|champions league|premier league|la liga|serie a"),
    "religion": _w(
        "evangelio|evangelica|religia|crestin|crestin ortodox|ortodox|ortodoxy|orthodoxy|"
        "orthodox church|orthodox christian|christian orthodox|adoracion|adoration|hymns|hymn|"
        "christian hymns|old time hymns|iglesia catolica|catolica|religioso catolico|"
        "catholic religious|catholic radio|catholic talk|mensajes cristianos|gospel evangelica|"
        "audio bible|bible reading|bible teaching|calvary chapel|jewish|jewish community|"
        "judaism|torah|ilahi|devotional|bhakti|mantra|healing|faith|inspirational|"
        "christianity|jesus|cristao|crista|southern gospel|black gospel|urban gospel|"
        "christian worship|christian teaching|christian preaching|christian talk|"
        "praise and worship|praise worship|christian praise worship|pentecostal|prayers|"
        "reciter|reciters|quran radio|raadio quran|sunnah|hadith|tilawat|tafsir|"
        "buddhism|buddhist|hindu|sikh|gurbani|church|iglesia|igreja|chiesa|kirche|"
        "worship music|christian music|christian rock|christian contemporary|ccm"),
    "kids": _w(
        "kinderlieder|kinderradio|kindermusik|childrens music|fairytales|fairy tales|"
        "bedtime stories|disney|disneyland|family|familia|familie|familiar|detskoe|детское|"
        "kinder|kids music|children s music|baby music|lullabies|nursery rhymes"),
    "community": _w(
        "comunitarias|comunitarios|communautaire|low power fm|lpfm|hospital radio|"
        "lokalradio|lokalfernsehen|nicht kommerziell|concesion social|concesion comunitaria|"
        "servicio social|offener kanal|burgerfunk|free radio|radio libre|libre|"
        "associative|radio associative|radios comunitarias|radio comunitaria"),
    "pirate": _w("pirate|piraten|piraat|piratenmuziek|piratenhits|etherpiraten|offshore radio|"
                 "pirate radio|geheimezender|piratenzender|piratenhits|piraten radio"),
    "public": _w(
        "gobierno|government|municipal|local government|gobierno del estado|state radio|"
        "servicio publico|public radio|radio publica|radio publique|concesion publica|"
        "emergency|emergency and public safety|public safety|secretaria de cultura|"
        "voice of turkiye|state broadcaster"),
    "indigenous": _w("indigenous|indigena|indigenas|first nations|native american|aboriginal|"
                     "native|first nation|acadian"),
    "accessibility": _w("blind|blind radio|radio reading service|reading service|"
                        "audio description|low vision"),
    "ai-generated": _w("ai generated|ai-generated|ai music|ai radio|ai|aimusic|"
                       "artificial intelligence|suno|generative|generated|ai generated music|"
                       "udio|ai dj|ai hosted"),
    "culture": _w(
        "poetry|poesia|storytelling|stories|tales|mystery|detective|noir|thriller|horror|"
        "suspense|sci fi|scifi|science fiction|fantasy|crime|sitcom|radio plays|audio drama|"
        "documentation|docs|history|black history|vintage commercials|classic radio drama|"
        "british comedy|vintage comedy|american comedy|"
        "sci-fi|old time radio|otr|philosophy|society|ufo|paranormal|esoteric|"
        "astrology|erotic"),
    "lifestyle": _w(
        "health|salud|sante|gesundheit|wellness|yoga|lifestyle|life|vida|business|"
        "negocios|finance|finanzas|economy|economics|economic|economia|technology|tecnologia|"
        "agriculture|agricultura|tourism|turismo|travel|viajes|environment|medio ambiente|"
        "environnement|nature|public health|science and technology|tech talk|entrepreneur|"
        "entrepreneurship|investing|stocks|real estate|automotive|auto|motorcycle|cars|"
        "cooking|food|gardening|fashion|beauty|parenting|relationships|dating|education talk"),
    "service": _w("traffic news|traffic information|traffic radio broadcast|local traffic weather|"
                  "emergency alerts|noaa weather radio|weather radio|weather forecast|"
                  "road traffic|ham radio|morse code|cw|amateur radio|numbers station"),
    "local": _w("local programming|local music|local radio|radio local|local weather|"
                "radio locale|locale radio|regional news|noticias regionales|regionalmagazin|"
                "regionalstudio|regionalfernsehen|hyperlocal|neighborhood|neighbourhood|"
                "city radio|town radio"),
    "youth": _w("youth|jovem|jugend|young adults|teens|teen|jeunesse|jeunes|youth programming|"
                "youth programs|gen z|millennials|college age"),
    "comedy": _w("comedy radio|stand up comedy|prank calls|prank|satire radio|funny"),
})

# Fixes after reviewing phrase()/fuzzy false positives
GENERIC_TAGS += _w("popular music|musica popular|música popular|popular culture music")
FORMATS.setdefault("talk", []).extend(_w("progressive talk|conservative talk|political talk"))

# Fuzzy false positives seen on the real catalogue
GENERIC_TAGS += _w("popular|brass|trash|electric|cover")
