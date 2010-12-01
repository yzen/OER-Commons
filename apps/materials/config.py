COURSE_TYPE = u'course'
LIBRARY_TYPE = u'library'
OERMATTER_TYPE = u'matter'
BLOG_POST_TYPE = u'blog_post'

content_types_dict = {
    COURSE_TYPE:{'title':u'Course Related Materials', 'title_plural':u'Course Related Materials'},
    LIBRARY_TYPE:{'title':u'Library or Collection', 'title_plural':u'Libraries and Collections'},
    OERMATTER_TYPE:{'title':u'OER Community Item', 'title_plural':u'OER Community Items'},
    BLOG_POST_TYPE:{'title':u'Blog Post', 'title_plural':u'Blog Posts'},
}

SUGGESTED_KEYWORDS = [
    u"Accounting" ,
    u"Agriculture" ,
    u"Anthropology" ,
    u"Archaeology" ,
    u"Architecture" ,
    u"Art History" ,
    u"Astronomy" ,
    u"Biology" ,
    u"Business Law" ,
    u"Chemistry" ,
    u"Cinema" ,
    u"Communication Studies" ,
    u"Computer Sciences" ,
    u"Criminal Justice" ,
    u"Dance" ,
    u"Digital Media" ,
    u"E-Commerce" ,
    u"Economics" ,
    u"Education" ,
    u"Engineering" ,
    u"Environmental" ,
    u"Finance" ,
    u"Fine Arts" ,
    u"Gender Studies" ,
    u"Geography" ,
    u"Geology" ,
    u"Health Policy" ,
    u"Health Sciences" ,
    u"History" ,
    u"Information Technology" ,
    u"International Business" ,
    u"Language and Literature" ,
    u"Law" ,
    u"Library and Information Studies" ,
    u"Linguistics" ,
    u"Management" ,
    u"Marketing" ,
    u"Mathematics" ,
    u"Music" ,
    u"Nanotechnology" ,
    u"Philosophy" ,
    u"Photography" ,
    u"Physics" ,
    u"Political Science" ,
    u"Psychiatry" ,
    u"Psychology" ,
    u"Religion" ,
    u"Rhetoric" ,
    u"Sociology" ,
    u"Statistics and Probability" ,
    u"Theatre" ,
    u"World Languages" ,
    u"Writing" ,
]

items_vocabularies = {
    'languages': [
        (u'Abkhazian', u'ab') ,
        (u'Afar', u'aa') ,
        (u'Afrikaans', u'af') ,
        (u'Albanian', u'sq') ,
        (u'Amharic', u'am') ,
        (u'Arabic', u'ar') ,
        (u'Armenian', u'hy') ,
        (u'Assamese', u'as') ,
        (u'Aymara', u'ay') ,
        (u'Azerbaijani', u'az') ,
        (u'Bashkir', u'ba') ,
        (u'Basque', u'eu') ,
        (u'Bengali', u'bn') ,
        (u'Bhutani', u'dz') ,
        (u'Bihari', u'bh') ,
        (u'Bislama', u'bi') ,
        (u'Breton', u'br') ,
        (u'Bulgarian', u'bg') ,
        (u'Burmese', u'my') ,
        (u'Byelorussian (Belarussian)', u'be') ,
        (u'Cambodian', u'km') ,
        (u'Catalan', u'ca') ,
        (u'Chinese', u'zh') ,
        (u'Cornish', u'kw') ,
        (u'Corsican', u'co') ,
        (u'Croatian', u'hr') ,
        (u'Czech', u'cs') ,
        (u'Danish', u'da') ,
        (u'Dutch', u'nl') ,
        (u'English', u'en') ,
        (u'Esperanto', u'eo') ,
        (u'Estonian', u'et') ,
        (u'Faroese', u'fo') ,
        (u'Fiji', u'fj') ,
        (u'Finnish', u'fi') ,
        (u'French', u'fr') ,
        (u'Frisian', u'fy') ,
        (u'Galician', u'gl') ,
        (u'Georgian', u'ka') ,
        (u'German', u'de') ,
        (u'Greek', u'el') ,
        (u'Greenlandic', u'kl') ,
        (u'Guarani', u'gn') ,
        (u'Gujarati', u'gu') ,
        (u'Haitian', u'ht') ,
        (u'Hausa', u'ha') ,
        (u'Hebrew', u'he') ,
        (u'Hindi', u'hi') ,
        (u'Hungarian', u'hu') ,
        (u'Icelandic', u'is') ,
        (u'Indonesian', u'id') ,
        (u'Interlingua', u'ia') ,
        (u'Interlingue', u'ie') ,
        (u'Inuktitut', u'iu') ,
        (u'Inupiak', u'ik') ,
        (u'Irish (Irish Gaelic)', u'ga') ,
        (u'Italian', u'it') ,
        (u'Japanese', u'ja') ,
        (u'Javanese', u'jw') ,
        (u'Kannada', u'kn') ,
        (u'Kashmiri', u'ks') ,
        (u'Kazakh', u'kk') ,
        (u'Kirghiz', u'ky') ,
        (u'Kirundi', u'rn') ,
        (u'Kiyarwanda', u'rw') ,
        (u'Korean', u'ko') ,
        (u'Kurdish', u'ku') ,
        (u'Laotian', u'lo') ,
        (u'Latin', u'la') ,
        (u'Latvian Lettish', u'lv') ,
        (u'Lingala', u'ln') ,
        (u'Lithuanian', u'lt') ,
        (u'Luxemburgish', u'lb') ,
        (u'Macedonian', u'mk') ,
        (u'Malagasy', u'mg') ,
        (u'Malay', u'ms') ,
        (u'Malayalam', u'ml') ,
        (u'Maltese', u'mt') ,
        (u'Manx Gaelic', u'gv') ,
        (u'Maori', u'mi') ,
        (u'Marathi', u'mr') ,
        (u'Moldavian', u'mo') ,
        (u'Mongolian', u'mn') ,
        (u'Nauru', u'na') ,
        (u'Nepali', u'ne') ,
        (u'Northern S\xe1mi', u'se') ,
        (u'Norwegian', u'no') ,
        (u'Occitan', u'oc') ,
        (u'Oriya', u'or') ,
        (u'Oromo', u'om') ,
        (u'Pashto', u'ps') ,
        (u'Persian', u'fa') ,
        (u'Polish', u'pl') ,
        (u'Portuguese', u'pt') ,
        (u'Punjabi', u'pa') ,
        (u'Quechua', u'qu') ,
        (u'Rhaeto-Romance', u'rm') ,
        (u'Romanian', u'ro') ,
        (u'Russian', u'ru') ,
        (u'Samoan', u'sm') ,
        (u'Sangho', u'sg') ,
        (u'Sanskrit', u'sa') ,
        (u'Scots Gaelic (Scottish Gaelic)', u'gd') ,
        (u'Serbian', u'sr') ,
        (u'Serbo-Croatian', u'sh') ,
        (u'Sesotho', u'st') ,
        (u'Setswana', u'tn') ,
        (u'Shona', u'sn') ,
        (u'Sindhi', u'sd') ,
        (u'Singhalese', u'si') ,
        (u'Siswati', u'ss') ,
        (u'Slovak', u'sk') ,
        (u'Slovenian', u'sl') ,
        (u'Somali', u'so') ,
        (u'Spanish', u'es') ,
        (u'Sudanese', u'su') ,
        (u'Swahili', u'sw') ,
        (u'Swedish', u'sv') ,
        (u'Tagalog', u'tl') ,
        (u'Tajik', u'tg') ,
        (u'Tamil', u'ta') ,
        (u'Tatar', u'tt') ,
        (u'Telugu', u'te') ,
        (u'Thai', u'th') ,
        (u'Tibetan', u'bo') ,
        (u'Tigrinya', u'ti') ,
        (u'Tonga', u'to') ,
        (u'Tsonga', u'ts') ,
        (u'Turkish', u'tr') ,
        (u'Turkmen', u'tk') ,
        (u'Twi', u'tw') ,
        (u'Uigur', u'ug') ,
        (u'Ukrainian', u'uk') ,
        (u'Urdu', u'ur') ,
        (u'Uzbek', u'uz') ,
        (u'Vietnamese', u'vi') ,
        (u'Volap\xfck', u'vo') ,
        (u'Welsh', u'cy') ,
        (u'Wolof', u'wo') ,
        (u'Xhosa', u'xh') ,
        (u'Yiddish', u'yi') ,
        (u'Yorouba', u'yo') ,
        (u'Zhuang', u'za') ,
        (u'Zulu', u'zu') ,
    ],
    'countries': [
        (u"Afghanistan", u"afghanistan"),
        (u"Albania", u"albania"),
        (u"Algeria", u"algeria"),
        (u"American Samoa", u"american-samoa"),
        (u"Andorra", u"andorra"),
        (u"Angola", u"angola"),
        (u"Anguilla", u"anguilla"),
        (u"Antarctica", u"antarctica"),
        (u"Antigua Barbuda", u"antigua-barbuda"),
        (u"Argentina", u"argentina"),
        (u"Armenia", u"armenia"),
        (u"Aruba", u"aruba"),
        (u"Australia", u"australia"),
        (u"Austria", u"austria"),
        (u"Azerbaijan", u"azerbaijan"),
        (u"Bahamas", u"bahamas"),
        (u"Bahrain", u"bahrain"),
        (u"Bangladesh", u"bangladesh"),
        (u"Barbados", u"barbados"),
        (u"Belarus", u"belarus"),
        (u"Belgium", u"belgium"),
        (u"Belize", u"belize"),
        (u"Benin", u"benin"),
        (u"Bermuda", u"bermuda"),
        (u"Bhutan", u"bhutan"),
        (u"Bolivia", u"bolivia"),
        (u"Bosnia Herzegovina", u"bosnia-herzegovina"),
        (u"Botswana", u"botswana"),
        (u"Bouvet Island", u"bouvet-island"),
        (u"Brazil", u"brazil"),
        (u"British Indian Ocean Territory", u"british-indian-ocean-territory"),
        (u"Brunei Darussalam", u"brunei-darussalam"),
        (u"Bulgaria", u"bulgaria"),
        (u"Burkina Faso", u"burkina-faso"),
        (u"Burundi", u"burundi"),
        (u"Cambodia", u"cambodia"),
        (u"Cameroon", u"cameroon"),
        (u"Canada", u"canada"),
        (u"Cape Verde", u"cape-verde"),
        (u"Cayman Islands", u"cayman-islands"),
        (u"Central African Republic", u"central-african-republic"),
        (u"Chad", u"chad"),
        (u"Chile", u"chile"),
        (u"China", u"china"),
        (u"Christmas Island", u"christmas-island"),
        (u"Cocos (Keeling) Islands", u"cocos-keeling-islands"),
        (u"Colombia", u"colombia"),
        (u"Comoros", u"comoros"),
        (u"Congo", u"congo"),
        (u"Congo, Democratic Republic", u"congo-democratic-republic"),
        (u"Cook Islands", u"cook-islands"),
        (u"Costa Rica", u"costa-rica"),
        (u"Cote D'Ivoire", u"cote-d-ivoire"),
        (u"Croatia", u"croatia"),
        (u"Cuba", u"cuba"),
        (u"Cyprus", u"cyprus"),
        (u"Czech Republic", u"czech-republic"),
        (u"Denmark", u"denmark"),
        (u"Djibouti", u"djibouti"),
        (u"Dominica", u"dominica"),
        (u"Dominican Republic", u"dominican-republic"),
        (u"Ecuador", u"ecuador"),
        (u"Egypt", u"egypt"),
        (u"El Salvador", u"el-salvador"),
        (u"Equatorial Guinea", u"equatorial-guinea"),
        (u"Eritrea", u"eritrea"),
        (u"Estonia", u"estonia"),
        (u"Ethiopia", u"ethiopia"),
        (u"Falkland Islands (Malvinas)", u"falkland-islands-malvinas"),
        (u"Faroe Islands", u"faroe-islands"),
        (u"Fiji", u"fiji"),
        (u"Finland", u"finland"),
        (u"France", u"france"),
        (u"French Guiana", u"french-guiana"),
        (u"French Polynesia", u"french-polynesia"),
        (u"French Southern Territories", u"french-southern-territories"),
        (u"Gabon", u"gabon"),
        (u"Gambia", u"gambia"),
        (u"Georgia", u"georgia"),
        (u"Germany", u"germany"),
        (u"Ghana", u"ghana"),
        (u"Gibraltar", u"gibraltar"),
        (u"Greece", u"greece"),
        (u"Greenland", u"greenland"),
        (u"Grenada", u"grenada"),
        (u"Guadeloupe", u"guadeloupe"),
        (u"Guam", u"guam"),
        (u"Guatemala", u"guatemala"),
        (u"Guinea", u"guinea"),
        (u"Guinea-Bissau", u"guinea-bissau"),
        (u"Guyana", u"guyana"),
        (u"Haiti", u"haiti"),
        (u"Heard Island Mcdonald Islands", u"heard-island-mcdonald-islands"),
        (u"Holy See (Vatican City State)", u"holy-see-vatican-city-state"),
        (u"Honduras", u"honduras"),
        (u"Hong Kong", u"hong-kong"),
        (u"Hungary", u"hungary"),
        (u"Iceland", u"iceland"),
        (u"India", u"india"),
        (u"Indonesia", u"indonesia"),
        (u"Iran, Islamic Republic", u"iran-islamic-republic"),
        (u"Iraq", u"iraq"),
        (u"Ireland", u"ireland"),
        (u"Israel", u"israel"),
        (u"Italy", u"italy"),
        (u"Jamaica", u"jamaica"),
        (u"Japan", u"japan"),
        (u"Jordan", u"jordan"),
        (u"Kazakhstan", u"kazakhstan"),
        (u"Kenya", u"kenya"),
        (u"Kiribati", u"kiribati"),
        (u"Korea, Democratic People's Republic", u"korea-democratic-people-s-republic"),
        (u"Korea, Republic", u"korea-republic"),
        (u"Kuwait", u"kuwait"),
        (u"Kyrgyzstan", u"kyrgyzstan"),
        (u"Lao People's Democratic Republic", u"lao-people-s-democratic-republic"),
        (u"Latvia", u"latvia"),
        (u"Lebanon", u"lebanon"),
        (u"Lesotho", u"lesotho"),
        (u"Liberia", u"liberia"),
        (u"Libyan Arab Jamahiriya", u"libyan-arab-jamahiriya"),
        (u"Liechtenstein", u"liechtenstein"),
        (u"Lithuania", u"lithuania"),
        (u"Luxembourg", u"luxembourg"),
        (u"Macao", u"macao"),
        (u"Macedonia, Former Yugoslav Republic", u"macedonia-former-yugoslav-republic"),
        (u"Madagascar", u"madagascar"),
        (u"Malawi", u"malawi"),
        (u"Malaysia", u"malaysia"),
        (u"Maldives", u"maldives"),
        (u"Mali", u"mali"),
        (u"Malta", u"malta"),
        (u"Marshall Islands", u"marshall-islands"),
        (u"Martinique", u"martinique"),
        (u"Mauritania", u"mauritania"),
        (u"Mauritius", u"mauritius"),
        (u"Mayotte", u"mayotte"),
        (u"Mexico", u"mexico"),
        (u"Micronesia, Federated States", u"micronesia-federated-states"),
        (u"Moldova, Republic", u"moldova-republic"),
        (u"Monaco", u"monaco"),
        (u"Mongolia", u"mongolia"),
        (u"Montserrat", u"montserrat"),
        (u"Morocco", u"morocco"),
        (u"Mozambique", u"mozambique"),
        (u"Myanmar", u"myanmar"),
        (u"Namibia", u"namibia"),
        (u"Nauru", u"nauru"),
        (u"Nepal", u"nepal"),
        (u"Netherlands", u"netherlands"),
        (u"Netherlands Antilles", u"netherlands-antilles"),
        (u"New Caledonia", u"new-caledonia"),
        (u"New Zealand", u"new-zealand"),
        (u"Nicaragua", u"nicaragua"),
        (u"Niger", u"niger"),
        (u"Nigeria", u"nigeria"),
        (u"Niue", u"niue"),
        (u"Norfolk Island", u"norfolk-island"),
        (u"Northern Mariana Islands", u"northern-mariana-islands"),
        (u"Norway", u"norway"),
        (u"Oman", u"oman"),
        (u"Pakistan", u"pakistan"),
        (u"Palau", u"palau"),
        (u"Palestinian Territory, Occupied", u"palestinian-territory-occupied"),
        (u"Panama", u"panama"),
        (u"Papua New Guinea", u"papua-new-guinea"),
        (u"Paraguay", u"paraguay"),
        (u"Peru", u"peru"),
        (u"Philippines", u"philippines"),
        (u"Pitcairn", u"pitcairn"),
        (u"Poland", u"poland"),
        (u"Portugal", u"portugal"),
        (u"Puerto Rico", u"puerto-rico"),
        (u"Qatar", u"qatar"),
        (u"Reunion", u"reunion"),
        (u"Romania", u"romania"),
        (u"Russian Federation", u"russian-federation"),
        (u"Rwanda", u"rwanda"),
        (u"Saint Helena", u"saint-helena"),
        (u"Saint Kitts Nevis", u"saint-kitts-nevis"),
        (u"Saint Lucia", u"saint-lucia"),
        (u"Saint Pierre Miquelon", u"saint-pierre-miquelon"),
        (u"Saint Vincent Grenadines", u"saint-vincent-grenadines"),
        (u"Samoa", u"samoa"),
        (u"San Marino", u"san-marino"),
        (u"Sao Tome Principe", u"sao-tome-principe"),
        (u"Saudi Arabia", u"saudi-arabia"),
        (u"Senegal", u"senegal"),
        (u"Serbia Montenegro", u"serbia-montenegro"),
        (u"Seychelles", u"seychelles"),
        (u"Sierra Leone", u"sierra-leone"),
        (u"Singapore", u"singapore"),
        (u"Slovakia", u"slovakia"),
        (u"Slovenia", u"slovenia"),
        (u"Solomon Islands", u"solomon-islands"),
        (u"Somalia", u"somalia"),
        (u"South Africa", u"south-africa"),
        (u"South Georgia South Sandwich Islands", u"south-georgia-south-sandwich-islands"),
        (u"Spain", u"spain"),
        (u"Sri Lanka", u"sri-lanka"),
        (u"Sudan", u"sudan"),
        (u"Suriname", u"suriname"),
        (u"Svalbard Jan Mayen", u"svalbard-jan-mayen"),
        (u"Swaziland", u"swaziland"),
        (u"Sweden", u"sweden"),
        (u"Switzerland", u"switzerland"),
        (u"Syrian Arab Republic", u"syrian-arab-republic"),
        (u"Taiwan, Province China", u"taiwan-province-china"),
        (u"Tajikistan", u"tajikistan"),
        (u"Tanzania, United Republic", u"tanzania-united-republic"),
        (u"Thailand", u"thailand"),
        (u"Timor-Leste", u"timor-leste"),
        (u"Togo", u"togo"),
        (u"Tokelau", u"tokelau"),
        (u"Tonga", u"tonga"),
        (u"Trinidad Tobago", u"trinidad-tobago"),
        (u"Tunisia", u"tunisia"),
        (u"Turkey", u"turkey"),
        (u"Turkmenistan", u"turkmenistan"),
        (u"Turks Caicos Islands", u"turks-caicos-islands"),
        (u"Tuvalu", u"tuvalu"),
        (u"Uganda", u"uganda"),
        (u"Ukraine", u"ukraine"),
        (u"United Arab Emirates", u"united-arab-emirates"),
        (u"United Kingdom", u"united-kingdom"),
        (u"United States", u"united-states"),
        (u"United States Minor Outlying Islands", u"united-states-minor-outlying-islands"),
        (u"Uruguay", u"uruguay"),
        (u"Uzbekistan", u"uzbekistan"),
        (u"Vanuatu", u"vanuatu"),
        (u"Venezuela", u"venezuela"),
        (u"Vietnam", u"vietnam"),
        (u"Virgin Islands, British", u"virgin-islands-british"),
        (u"Virgin Islands, U.S.", u"virgin-islands-u-s"),
        (u"Wallis Futuna", u"wallis-futuna"),
        (u"Western Sahara", u"western-sahara"),
        (u"Yemen", u"yemen"),
        (u"Zambia", u"zambia"),
        (u"Zimbabwe", u"zimbabwe"),
    ],
    'matter_types': [
        (u"News Stories", u"news-stories"),
        (u"Articles and Reports", u"articles-and-reports"),
        (u"Tools and Technology", u"tools-and-technology"),
        (u"Organizations and Associations", u"organizations-and-associations"),
        (u"Conferences and Workshops", u"conferences-and-workshops"),
        (u"Discussion Forums", u"discussion-forums"),
        (u"Blogs and Wikis", u"blogs-and-wikis"),
    ],
    'matter_topics': [
        (u"How and Why of OER", u"how-and-why-of-oer"),
        (u"Teaching and Learning", u"teaching-and-learning"),
        (u"Localization", u"localization"),
        (u"Standards/Certifications", u"standards-certifications"),
        (u"Intellectual Property", u"intellectual-property"),
        (u"Open Source", u"open-source"),
        (u"Technology", u"technology"),
        (u"Research", u"research"),
        (u"Policy", u"policy"),
    ],
    'course_or_module': [
        (u"Full Course", u"full-course"),
        (u"Learning Module", u"learning-module"),
    ],
    'grade_levels': [
        (u"Primary", u"primary"),
        (u"Secondary", u"secondary"),
        (u"Post-secondary", u"post-secondary"),
    ],
    'geographic_relevance': [
        (u"All", u"all"),
        (u"Africa", u"africa"),
        (u"Asia", u"asia"),
        (u"Australia", u"australia"),
        (u"Developing countries", u"developing-countries"),
        (u"Europe", u"europe"),
        (u"Middle East", u"middle-east"),
        (u"North America", u"north-america"),
        (u"South America", u"south-america"),
    ],
    'media_formats': [
        (u"Audio", u"audio"),
        (u"Graphics/Photos", u"graphics-photos"),
        (u"Mobile", u"mobile"),
        (u"Other", u"other"),
        (u"Text/HTML", u"text-html"),
        (u"Downloadable docs", u"downloadable-docs"),
        (u"Video", u"video"),
    ],
    'material_types': [
        (u"Activities and Labs", u"activities-and-labs"),
        (u"Assessments", u"assessments"),
        (u"Audio Lectures", u"audio-lectures"),
        (u"Curriculum Standards", u"curriculum-standards"),
        (u"Discussion Forums", u"discussion-forums"),
        (u"Games", u"games"),
        (u"Homework and Assignments", u"homework-and-assignments"),
        (u"Lecture Notes", u"lecture-notes"),
        (u"Lesson Plans", u"lesson-plans"),
        (u"Readings", u"readings"),
        (u"Simulations", u"simulations"),
        (u"Syllabi", u"syllabi"),
        (u"Teaching and Learning Strategies", u"teaching-and-learning-strategies"),
        (u"Textbooks", u"textbooks"),
        (u"Training Materials", u"training-materials"),
        (u"Video Lectures", u"video-lectures"),
        (u"Other", u"other"),
    ],
    'library_material_types': [
        (u"Primary Source", u"primary-source"),
        (u"Teaching and Learning Strategies", u"teaching-and-learning-strategies"),
        (u"Other", u"other"),
    ],
    'general_subjects': [
        (u"Arts", u"arts"),
        (u"Business", u"business"),
        (u"Humanities", u"humanities"),
        (u"Mathematics and Statistics", u"mathematics-and-statistics"),
        (u"Science and Technology", u"science-and-technology"),
        (u"Social Sciences", u"social-sciences"),
    ],
    'member_role': [
        (u'Instructor', u'instructor'),
        (u'Student', u'student'),
        (u'Self Learner', u'self_affiliated'),
        (u'Researcher', u'researcher'),
        (u'Administrator', u'oer_administrator'),
        (u'Content provider', u'content_provider'),
    ],
    'filter_license_types': [
        (u'CC Attribution', u'cc-by'),
        (u'CC Attribution-Share Alike', u'cc-by-sa'),
        (u'CC Attribution-No Derivative Works', u'cc-by-nd'),
        (u'CC Attribution-Noncommercial', u'cc-by-nc'),
        (u'CC Attribution-Noncommercial-Share Alike', u'cc-by-nc-sa'),
        (u'CC Attribution-Noncommercial-No Derivative Works', u'cc-by-nc-nd'),
        (u'CC Noncommercial-Share Alike', u'cc-nc-sa'),
        (u'Public Domain', u'publicdomain'),
        (u'GNU FDL', u'gnu-fdl'),
     ],
    'cou_buckets': [
        (u'No Strings Attached', u'no-strings-attached'),
        (u'Remix and Share', u'remix-and-share'),
        (u'Share Only', u'share-only'),
        (u'Read the Fine Print', u'read-the-fine-print'),
     ],
    'member_activity_types': [
        (u'Only Items with Ratings', u'rated'),
        (u'Only Items with Reviews', u'reviewed'),
        (u'Only Items with Tags', u'tagged'),
     ],
}

GENERAL_SUBJECT_DESCRIPTIONS = {
  u"arts":u"Art, History, Cinema, Dance, Fine Arts, Music, Photography, Theatre, Visual Arts",
  u"business":u"Accounting, E-Commerce, Economics, Finance, International Business, Management, Marketing",
  u"humanities":u"History, Language and Literature, Library and Information Studies, Linguistics, Philosophy, Religion, Rhetoric, World Languages, Writing, Language Arts, Debate, Grammar, Journalism, Phonics, Reading, Speaking, Spelling, Storytelling, Vocabulary",
  u"mathematics-and-statistics":u"Mathematics, Statistics and Probability, Algebra, Arithmetic, Calculus, Geometry, Measurement, Number theory, Trigonometry",
  u"science-and-technology":u"Agriculture, Architecture, Astronomy, Biology, Chemistry, Computer Sciences, Digital Media, Engineering, Environmental, Geology, Health Policy, Health Sciences, Information Technology, Nanotechnology, Physics, Psychiatry, Physical Education, Sports and Fitness, Life Sciences, Earth Science, Ecology, Meteorology, Oceanography, Paleontology, Pharmacology, Physical Sciences, Space Sciences",
  u"social-sciences":u"Anthropology, Archaeology, Business Law, Communication Studies, Criminal Justice, Education, Gender Studies, Geography, Law, Political Science, Psychology, Sociology, Social Studies, Civics, Current Events, Human Behavior, Human Relations, Social Work, State History, United States History, Urban Studies u",
}

GRADE_LEVEL_DESCRIPTIONS = {
  u"primary":u"includes Pre-K - Grade 6; Elementary; Lower Elementary; Upper Elementary",
  u"secondary":u"includes Grades 7 - 12; High School; Middle School; Jr. High School",
  u"post-secondary":u"includes all Higher Education; College, University, Graduate Levels; Professional Development; Training",
}