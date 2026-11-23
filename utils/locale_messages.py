"""Complete messages for workbook instructions, reports and upload feedback."""
MESSAGES = {
"mcq": "གདམ་ཁ་ཅན་གྱི་དྲི་བ",
"Multiple choice": "གདམ་ཁ་ཅན་གྱི་དྲི་བ",
"Answer key": "དྲི་བའི་ལན",
"Maximum scores": "སྐུགས་ཚད་མཐོ་ཤོས",
"Written response": "བྲིས་ལན", "Written / Essay": "བྲིས་ལན་དང་རྩོམ་ཡིག",
"Test Distribution": "སྐུགས་ཀྱི་ཁྱབ་ཚུལ།", "Test distribution": "སྐུགས་ཀྱི་ཁྱབ་ཚུལ།",
"Item Analysis Report": "དྲི་བ་དབྱེ་ཞིབ་ཀྱི་སྙན་ཞུ།",
"Class results": "སློབ་སྡེའི་གྲུབ་འབྲས།",
"Class assessment report": "སློབ་སྡེའི་དབྱེ་ཞིབ་སྙན་ཞུ།",
"Item": "དྲི་བ", "Question": "དྲི་བ", "Key": "དྲི་བའི་ལན",
"Discrim.": "ཁྱད་འབྱེད་ཚད",
"Decision": "གྲོས་ཐག", "Reason": "རྒྱུ་མཚན",
"Functional distractors": "ནུས་ཅན་ལན་འཛོལ་གདམ་ཁ",
"Non-functional distractors": "ནུས་མེད་ལན་འཛོལ་གདམ་ཁ",
"Distractors (FD / NFD)": "ནུས་ཅན་དང་ནུས་མེད་ལན་འཛོལ་གདམ་ཁ",
"Distractors by question": "དྲི་བ་རེ་རེའི་ལན་འཛོལ་གདམ་ཁ",
"FD": "ནུས་ཅན", "NFD": "ནུས་མེད", "None": "མེད",
"DE (%)": "ལན་འཛོལ་གདམ་ཁའི་ནུས་ཚད་ (%)",
"DE = distractor efficiency.": "ལན་འཛོལ་གདམ་ཁའི་ནུས་ཚད་འདི་བརྒྱ་ཆའི་ཐོག་སྟོན་ཡོད།",
"Each option shows its selection count and percentage of all students. An incorrect option selected by at least 5% of students is functional. Below 5%, it is a non-functional distractor (NFD).":
"གདམ་ཁ་རེ་ལུ་ གདམ་མི་སློབ་ཕྲུག་གི་གྱངས་ཁ་དང་བརྒྱ་ཆ་སྟོན་ཡོད། ལན་འཛོལ་བའི་གདམ་ཁ་འདི་ སློབ་ཕྲུག་ 5% ཡང་ན་དེ་ལས་མངམ་གིས་གདམ་པ་ཅིན་ནུས་ཅན་དང་ 5% ལས་ཉུངམ་གིས་གདམ་པ་ཅིན་ནུས་མེད་ཨིན།",
"MCQ assessment template": "གདམ་ཁ་ཅན་གྱི་དྲི་བ་དབྱེ་ཞིབ་དཔེ་གཞི",
"True or False assessment template": "བདེན་རྫུན་དབྱེ་ཞིབ་དཔེ་གཞི",
"Fill in the Blanks assessment template": "ས་སྟོང་བསུབ་ནིའི་དབྱེ་ཞིབ་དཔེ་གཞི",
"Matching assessment template": "ཆ་སྒྲིག་ནིའི་དབྱེ་ཞིབ་དཔེ་གཞི",
"Written / Long Answer assessment template": "བྲིས་ལན་དང་ལན་རིངམ་དབྱེ་ཞིབ་དཔེ་གཞི",
"Test distribution template": "སྐུགས་ཀྱི་ཁྱབ་ཚུལ་དཔེ་གཞི",
"Total Score = MCQ + all sections. Use the full test score for each student.":
"བསྡོམས་སྐུགས་ནང་གདམ་ཁ་ཅན་གྱི་དྲི་བ་དང་སྡེ་ཚན་གཞན་ཆ་མཉམ་གྱི་སྐུགས་བསྡོམས་དགོ།",
"Enter each student’s name and overall test score. The overall score determines the upper and lower groups.":
"སློབ་ཕྲུག་རེའི་མིང་དང་བསྡོམས་སྐུགས་བཙུགས། བསྡོམས་སྐུགས་ཀྱིས་སྡེ་ཚན་མཐོ་ཤོས་དང་དམའ་ཤོས་གཏན་འབེབས་འབདཝ་ཨིན།",
"Fill the gold KEY row above the headers with A, B, C or D. Leave its Total Score blank.":
"མགོ་ཡིག་གི་ལྟག་ལུ་ གསེར་མདོག་ཅན་གྱི་དྲི་བའི་ལན་གྲལ་ཐིག་ནང་ ཀ་ ཁ་ ག་ ཡང་ན་ ང་ བཙུགས། གྲལ་ཐིག་འདིའི་བསྡོམས་སྐུགས་ས་སྟོང་བཞག",
"Fill the gold KEY row with True or False (T/F also accepted).":
"གསེར་མདོག་ཅན་གྱི་དྲི་བའི་ལན་གྲལ་ཐིག་ནང་ བདེན་ ཡང་ན་ རྫུན་ བཙུགས།",
"Fill the gold KEY row with accepted answers, separated by | (e.g. Paro | Paro Dzong).":
"གསེར་མདོག་ཅན་གྱི་དྲི་བའི་ལན་གྲལ་ཐིག་ནང་ ཆ་འཇོག་འབད་མི་ལན་ཚུ་ | གིས་ཕྱེ་སྟེ་བཙུགས། དཔེར་ན་ སྤ་རོ་ | སྤ་རོ་རྫོང་།",
"Fill the gold KEY row with the correct matching letter or number for each question.":
"གསེར་མདོག་ཅན་གྱི་དྲི་བའི་ལན་གྲལ་ཐིག་ནང་ དྲི་བ་རེའི་ཆ་འགྲིག་མི་ཡི་གུ་ཡང་ན་ཨང་བཙུགས།",
"Fill the gold MAX row with the maximum score for each question.":
"གསེར་མདོག་ཅན་གྱི་སྐུགས་ཚད་གྲལ་ཐིག་ནང་ དྲི་བ་རེའི་སྐུགས་ཚད་མཐོ་ཤོས་བཙུགས།",
"Enter student details and responses below the headers. Blank responses score zero.":
"མགོ་ཡིག་གི་འོག་ལུ་སློབ་ཕྲུག་གི་གནས་ཚུལ་དང་ལན་བཙུགས། ལན་ས་སྟོང་ལུ་སྐུགས་ཀླད་ཀོར་ཨིན།",
"Enter student details and responses below. Blank responses score zero.":
"འོག་ལུ་སློབ་ཕྲུག་གི་གནས་ཚུལ་དང་ལན་བཙུགས། ལན་ས་སྟོང་ལུ་སྐུགས་ཀླད་ཀོར་ཨིན།",
"Enter the marks awarded for each question. Blank item marks count as zero.":
"དྲི་བ་རེ་ལས་ཐོབ་མི་སྐུགས་བཙུགས། སྐུགས་ས་སྟོང་ལུ་ཀླད་ཀོར་སྦེ་བརྩིཝ་ཨིན།",
"Add student rows as needed. Add Q-number columns or delete unused question columns.":
"དགོས་མཁོ་དང་འཁྲིལ་སློབ་ཕྲུག་གི་གྲལ་ཐིག་དང་དྲི་བའི་ཀེར་ཐིག་ཁ་སྐོང་རྐྱབས། མ་དགོ་པའི་དྲི་བའི་ཀེར་ཐིག་བཏོན་གཏང་།",
"Replace the example scores below with your class scores.": "འོག་གི་དཔེ་ཚད་སྐུགས་ཀྱི་ཚབ་ལུ་ཁྱོད་རའི་སློབ་སྡེའི་སྐུགས་བཙུགས།",
"Enter a student name and overall test score on every row.": "གྲལ་ཐིག་རེ་རེའི་ནང་ སློབ་ཕྲུག་གི་མིང་དང་བསྡོམས་སྐུགས་བཙུགས།",
"Blue: student IDs. Teal: total scores. Add rows as needed.": "ཧོནམ་ནང་སློབ་ཕྲུག་ཨང་དང་ ཧོན་ལྗང་ནང་བསྡོམས་སྐུགས་བཙུགས། དགོས་མཁོ་དང་འཁྲིལ་གྲལ་ཐིག་ཁ་སྐོང་རྐྱབས།",
"Fix the problems above and upload the file again.": "གོང་གི་དཀའ་ངལ་ཚུ་བཅོས་ཏེ་ ཡིག་སྣོད་ལོག་ཡར་བཙུགས་འབད།",
"Every item needs an answer in the key.": "དྲི་བ་རེ་རེ་ལུ་ལན་ཐོ་ནང་ལན་བཀོད་དགོ།",
"The analysis could not be completed. Please check your file and answer key against the Data Format Guide.":
"དབྱེ་ཞིབ་མཇུག་བསྡུ་མ་ཚུགས། ཡིག་སྣོད་དང་ལན་ཐོ་འདི་གནས་སྡུད་བཀོད་ཐངས་ཀྱི་ལམ་སྟོན་དང་བསྡུར་གནང་།",
"The analysis could not be completed. Check your file against the Data Format Guide.":
"དབྱེ་ཞིབ་མཇུག་བསྡུ་མ་ཚུགས། ཡིག་སྣོད་འདི་གནས་སྡུད་བཀོད་ཐངས་ཀྱི་ལམ་སྟོན་དང་བསྡུར་གནང་།",
"Analysing…": "དབྱེ་ཞིབ་འབད་དོ།",
"Checking workbook and analysing responses…": "ལས་དེབ་ཞིབ་དཔྱད་དང་ལན་དབྱེ་ཞིབ་འབད་དོ།",
"One completed MCQ workbook, up to 10 MB.": "བཀང་ཚར་མི་གདམ་ཁ་ཅན་གྱི་དྲི་བའི་ལས་དེབ་གཅིག་ མེ་ག་བའིཊ་ 10 ཚུན།",
"Fewer than 30 students: treat item decisions as indicative.": "སློབ་ཕྲུག་ 30 ལས་ཉུང་པ་ཅིན་ གྲོས་འདེབས་ཚུ་སྔོན་དཔག་སྦེ་བལྟ་གནང་།",
"With fewer than 10 scores, interpret the distribution shape cautiously.": "སྐུགས་ 10 ལས་ཉུང་པ་ཅིན་ ཁྱབ་ཚུལ་གྱི་དབྱིབས་ལས་གྲོས་ཐག་གཅདཔ་ད་དྲན་པ་བཏོན་གནང་།",
"Choose BEFORE looking at the data. Use two-sided unless you have a strong reason for a direction.":
"གནས་སྡུད་མ་བལྟ་བའི་ཧེ་མ་གདམ་ཁ་རྐྱབས། ཕྱོགས་གཅིག་ལུ་རྒྱུ་མཚན་གསལ་ཏོག་ཏོ་མེད་པ་ཅིན་ཕྱོགས་གཉིས་གདམ་ཁ་རྐྱབས།",
"t-test": "ཊི་བརྟག་དཔྱད", "z-test": "ཛེཌ་བརྟག་དཔྱད",
"Null hypothesis": "གཞི་བཞག་ཚོད་དཔག",
"H₀ (null)": "གཞི་བཞག་ཚོད་དཔག",
"H₁ (alternative)": "གདམ་ཁའི་ཚོད་དཔག",
"Measure": "ཚད་འཇལ", "Result": "གྲུབ་འབྲས",
"Significance level": "གལ་གནད་ཚད",
"Known population standard deviation": "ཤེས་ཡོད་པའི་སྡེ་ཚན་ཡོངས་ཀྱི་ཚད་ལྡན་ཁ་བྲལ",
"Reject H0": "གཞི་བཞག་ཚོད་དཔག་ཆ་མེད་གཏང་།",
"Fail to reject H0": "གཞི་བཞག་ཚོད་དཔག་ཆ་མེད་གཏང་ནིའི་ཁུངས་སྐྱེལ་ལངམ་མེད།",
"At least 2 scores are needed.": "ཉུང་མཐའ་སྐུགས་ 2 དགོ།",
"At least 1 score is needed.": "ཉུང་མཐའ་སྐུགས་ 1 དགོ།",
"All scores are identical; the test cannot be computed.": "སྐུགས་ཆ་མཉམ་འདྲ་མཉམ་ཨིནམ་ལས་བརྟག་དཔྱད་རྩིས་བཏོན་མི་བཏུབ།",
"Population σ must be a positive number.": "སྡེ་ཚན་ཡོངས་ཀྱི་ཚད་ལྡན་ཁ་བྲལ་འདི་ 0 ལས་མཐོ་དགོ།",
"No file was uploaded.": "ཡིག་སྣོད་ཡར་བཙུགས་མ་འབད་བས།",
"The file is empty.": "ཡིག་སྣོད་ས་སྟོང་ཨིན་པས།",
"The file contains no data.": "ཡིག་སྣོད་ནང་གནས་སྡུད་མེད།",
"The file has no data.": "ཡིག་སྣོད་ནང་གནས་སྡུད་མེད།",
"The file contains headers but no student rows.": "མགོ་ཡིག་ཡོད་རུང་སློབ་ཕྲུག་གི་གྲལ་ཐིག་མེད།",
"Unsupported file type. Please upload a .csv or .xlsx file.": "ཡིག་སྣོད་འདི་ལག་ལེན་འཐབ་མི་བཏུབ། .csv ཡང་ན་ .xlsx ཡར་བཙུགས་འབད་གནང་།",
"The file could not be read. Check that it is a valid, unprotected .csv or .xlsx file and matches the Data Format Guide.":
"ཡིག་སྣོད་ལྷག་མ་ཚུགས། གསང་ཨང་མེད་པའི་ .csv ཡང་ན་ .xlsx ཨིན་ན་དང་ གནས་སྡུད་བཀོད་ཐངས་དང་འཁྲིལ་ཡོད་ག་བལྟ་གནང་།",
"Upload a non-empty .xlsx workbook smaller than 10 MB.": "གནས་སྡུད་ཡོད་པའི་ .xlsx ལས་དེབ་ མེ་ག་བའིཊ་ 10 ལས་ཆུང་མི་ཡར་བཙུགས་འབད།",
"The MCQ sheet is empty. Download and fill in the template.": "གདམ་ཁ་ཅན་གྱི་དྲི་བའི་ཤོག་ཁྲམ་ས་སྟོང་ཨིན་པས། དཔེ་གཞི་ཕབ་ལེན་འབད་དེ་བཀང་གནང་།",
"Keep exactly one header row beginning with Student ID.": "སློབ་ཕྲུག་ཨང་གིས་འགོ་བཙུགས་མི་མགོ་ཡིག་གྲལ་ཐིག་གཅིག་བཞག",
"The first three columns must be Student ID, Name, and Total Score.": "ཀེར་ཐིག་དང་པ་གསུམ་འདི་ སློབ་ཕྲུག་ཨང་ མིང་ དང་བསྡོམས་སྐུགས་འོང་དགོ།",
"Use question headers Q1, Q2, Q3, … after Total Score.": "བསྡོམས་སྐུགས་ཀྱི་ཤུལ་ལས་ དྲི་བ་དང་པ་ དྲི་བ་གཉིས་པ་ དྲི་བ་གསུམ་པ་ ལ་སོགས་པའི་མགོ་ཡིག་བཙུགས།",
"Question headers must be unique.": "དྲི་བའི་མགོ་ཡིག་བསྐྱར་ཟློས་མེདཔ་འོང་དགོ།",
"Include exactly one answer-key row with KEY in the Student ID column.": "སློབ་ཕྲུག་ཨང་ཀེར་ཐིག་ནང་ དྲི་བའི་ལན་ཟེར་བཀོད་པའི་ལན་ཐོ་གྲལ་ཐིག་གཅིག་བཞག",
"Every answer-key cell must contain A, B, C, or D.": "ལན་ཐོའི་ནང་ ཀ་ ཁ་ ག་ ཡང་ན་ ང་ བཙུགས།",
"Enter at least two students below the column headers.": "མགོ་ཡིག་གི་འོག་ལུ་སློབ་ཕྲུག་ཉུང་མཐའ་ 2 ཀྱི་གནས་སྡུད་བཙུགས།",
"Every student row needs a Student ID and Name.": "སློབ་ཕྲུག་རེ་ལུ་ཨང་དང་མིང་དགོ།",
"Student IDs must be unique. Check for duplicate student rows.": "སློབ་ཕྲུག་ཨང་བསྐྱར་ཟློས་མེདཔ་འོང་དགོ། གྲལ་ཐིག་ལོག་བཙུགས་ཡོད་ག་ཞིབ་དཔྱད་འབད།",
"Every student needs a non-negative numeric Total Score (MCQ + all sections).": "སློབ་ཕྲུག་རེ་ལུ་སྡེ་ཚན་ཆ་མཉམ་གྱི་བསྡོམས་སྐུགས་ 0 ཡང་ན་དེ་ལས་མཐོ་མི་ཨང་གྲངས་བཙུགས།",
"Student responses must be A, B, C, D, or blank for an omitted answer.": "སློབ་ཕྲུག་གི་ལན་ཀ་ ཁ་ ག་ ང་ ཡང་ན་ལན་མ་བྲིས་པ་ཅིན་ས་སྟོང་བཞག",
"Could not read the workbook. Use the .xlsx template and keep the sheet named MCQ.": "ལས་དེབ་ལྷག་མ་ཚུགས། .xlsx དཔེ་གཞི་ལག་ལེན་འཐབ་སྟེ་ ཤོག་ཁྲམ་གྱི་མིང་གདམ་ཁ་ཅན་གྱི་དྲི་བ་སྦེ་བཞག",
"Only .xlsx workbooks are accepted.": ".xlsx ལས་དེབ་ཡར་བཙུགས་འབད།",
"At least two columns are needed: StudentID and one item column (see the Data Format Guide).": "སློབ་ཕྲུག་ཨང་དང་དྲི་བ་གཅིག་གི་ཀེར་ཐིག་ཚུད་དེ་ ཉུང་མཐའ་ཀེར་ཐིག་ 2 དགོ།",
"Include at least one item column, such as Q1.": "དྲི་བ་དང་པ་བཟུམ་གྱི་དྲི་བའི་ཀེར་ཐིག་ཉུང་མཐའ་གཅིག་བཙུགས།",
"At least 2 students are required to calculate discrimination.": "ཁྱད་འབྱེད་ཚད་རྩིས་བཏོན་ནི་ལུ་སློབ་ཕྲུག་ཉུང་མཐའ་ 2 དགོ།",
"Negative scores found. Scores must be 0 or greater.": "མེད་གྲངས་ཀྱི་སྐུགས་འདུག སྐུགས་འདི་ 0 ཡང་ན་དེ་ལས་མཐོ་དགོ།",
"Missing item marks are scored as 0 and reported per item.": "སྐུགས་ས་སྟོང་འདི་ 0 སྦེ་བརྩི་སྟེ་དྲི་བ་རེ་རེའི་སྙན་ཞུ་ནང་སྟོནམ་ཨིན།",
"Blank responses are scored as incorrect.": "ལན་ས་སྟོང་འདི་ལན་འཛོལ་བ་སྦེ་བརྩིཝ་ཨིན།",
"Some entries have no column header. Add a header for every item.": "གནས་སྡུད་ལ་ལུ་ལུ་མགོ་ཡིག་མེད་པས། དྲི་བ་རེ་རེ་ལུ་མགོ་ཡིག་བཙུགས།",
"Difficulty or discrimination could not be computed (too little data or no variation).": "གནས་སྡུད་མ་ལང་པ་ཡང་ན་ཁྱད་པར་མེདཔ་ལས་ དཀའ་ཚད་ཡང་ན་ཁྱད་འབྱེད་ཚད་རྩིས་བཏོན་མ་ཚུགས།",
}

PATTERNS = {
r"Student (\d+)": "སློབ་ཕྲུག་ {0}",
r"Include one (.+) column with an entry for each student\.": "སློབ་ཕྲུག་རེའི་གནས་སྡུད་བཙུགས་སའི་ {0} ཀེར་ཐིག་གཅིག་བཞག",
r"The first column must be 'StudentID' \(found '(.+)'\)\.": "ཀེར་ཐིག་དང་པའི་མིང་ {0} གི་ཚབ་ལུ་ སློབ་ཕྲུག་ཨང་བཙུགས།",
r"Duplicate item column names: (.+)\.": "དྲི་བའི་མགོ་ཡིག་བསྐྱར་ཟློས་འདུག་ {0}",
r"Duplicate StudentID values: (.+)": "སློབ་ཕྲུག་ཨང་བསྐྱར་ཟློས་འདུག་ {0}",
r"Include exactly one (KEY|MAX) row\.": "{0} གྲལ་ཐིག་གཅིག་བཞག",
r"Missing an answer-key row with StudentID = KEY\.": "སློབ་ཕྲུག་ཨང་ཀེར་ཐིག་ནང་ དྲི་བའི་ལན་ཟེར་བཀོད་པའི་ལན་ཐོ་གྲལ་ཐིག་བཙུགས།",
r"Missing a row with StudentID = MAX giving each item's maximum score\.": "སློབ་ཕྲུག་ཨང་ཀེར་ཐིག་ནང་ སྐུགས་ཚད་ཟེར་བཀོད་པའི་གྲལ་ཐིག་བཙུགས།",
r"(\d+) student row\(s\) have no StudentID\.": "སློབ་ཕྲུག་གི་གྲལ་ཐིག་ {0} ལུ་ཨང་མེད།",
r"Only (\d+) students: results are very unstable\. Use ≥ 30 students if possible\.": "སློབ་ཕྲུག་ {0} ལས་བརྟེན་མི་གྲུབ་འབྲས་འགྱུར་བ་འགྱོ་སྲིད། འབད་ཚུགས་པ་ཅིན་ 30 ཡང་ན་དེ་ལས་མངམ་བཙུགས།",
r"(\d+) students: below the recommended minimum of 30 for stable item statistics\.": "སློབ་ཕྲུག་ {0} འདི་ གྲུབ་འབྲས་བརྟན་ཏོག་ཏོ་དོན་ལུ་བསླབ་བྱ་བྱིན་མི་ 30 ལས་ཉུངམ་ཨིན།",
r"(\d+) empty cell\(s\) \(([\d.]+)%\)\. (.+)": "ས་སྟོང་ {0} ({1}%) འདུག {2}",
r"Item\(s\) with no responses at all: (.+)\.": "ལན་གཅིག་ཡང་མེད་པའི་དྲི་བ་ཚུ་ {0}",
r"No answer key given for: (.+)\.": "དྲི་བ་འདི་ཚུ་ལུ་ལན་ཐོ་མེད་ {0}",
r"Item '(.+)': the MAX score must be a number greater than 0\.": "{0} གི་སྐུགས་ཚད་འདི་ 0 ལས་མཐོ་བའི་ཨང་གྲངས་འོང་དགོ།",
r"Answer key for (.+) must be True/False \(or T/F\)\.": "{0} གི་ལན་ཐོ་ནང་ བདེན་ཡང་ན་རྫུན་བཙུགས།",
r"(\d+) response\(s\) are not True/False/T/F; they are scored as incorrect\.": "ལན་ {0} འདི་བདེན་རྫུན་གྱི་ལན་མེནམ་ལས་འཛོལ་བ་སྦེ་བརྩིཝ་ཨིན།",
r"Item '(.+)': accepted answer list is empty\.": "{0} གི་ཆ་འཇོག་འབད་མི་ལན་ཐོ་ས་སྟོང་ཨིན་པས།",
r"(\d+) score\(s\) are not numbers \(use digits, e\.g\. 7\.5\)\.": "སྐུགས་ {0} འདི་ཨང་གྲངས་མེན་པས། དཔེར་ན་ 7.5 བཟུམ་གྱི་ཨང་གྲངས་བཙུགས།",
r"Scores above the maximum for: (.+)\.": "སྐུགས་ཚད་མཐོ་ཤོས་ལས་ལྷག་མི་དྲི་བ་ཚུ་ {0}",
r"The file is larger than (\d+) MB\. Please upload a smaller file\.": "ཡིག་སྣོད་འདི་མེ་ག་བའིཊ་ {0} ལས་སྦོམ་འདུག ཆུང་ཀུ་ཅིག་ཡར་བཙུགས་འབད།",
r"(.+) – (?:combined )?Excel template": "{0} · ལས་དེབ་དཔེ་གཞི",
r"(.+) – sample data": "{0} · དཔེ་ཚད་གནས་སྡུད",
r"([\d.]+)% (?:CI|two-sided confidence interval) for the mean": "ཆ་སྙོམས་ཀྱི་ {0}% ཡིད་ཆེས་བར་མཚམས",
r"Population mean (.+)": "སྡེ་ཚན་ཡོངས་ཀྱི་ཆ་སྙོམས་ {0}",
r"Sample: n = (\d+) \(<30\)\. The t-test relies on approximately normal data for small samples\.": "དཔེ་ཚད་ཀྱི་གྱངས་ཁ་ {0} ཨིན། དཔེ་ཚད་ཆུང་ཀུ་ལུ་ཊི་བརྟག་དཔྱད་འབད་ནི་ལུ་ གནས་སྡུད་སྤྱིར་བཏང་ཁྱབ་ཚུལ་དང་ཉེ་བ་འོང་དགོ།",
r"n = (\d+) \(<30\): normality of the population is required for a valid z-test\.": "དཔེ་ཚད་གྱངས་ཁ་ {0} ཨིན། ཛེཌ་བརྟག་དཔྱད་ལུ་སྡེ་ཚན་ཡོངས་སྤྱིར་བཏང་ཁྱབ་ཚུལ་འོང་དགོ།",
r"Sample: Shapiro-Wilk suggests non-normality \(p = ([\d.]+)\)\. Interpret with caution(.*)": "ཁྱབ་ཚུལ་ཞིབ་དཔྱད་ཀྱིས་སྤྱིར་བཏང་ཁྱབ་ཚུལ་མེན་པའི་རྟགས་སྟོན་ཡོད། (p = {0}) གྲུབ་འབྲས་ལུ་དྲན་པ་བཏོན་གནང་།",
}


MESSAGES.update({
"One-sample t-test": "དཔེ་ཚད་གཅིག་གི་ཊི་བརྟག་དཔྱད",
"One-sample z-test": "དཔེ་ཚད་གཅིག་གི་ཛེཌ་བརྟག་དཔྱད",
"Karma Dorji": "ཀརྨ་རྡོ་རྗེ།",
"MCQ score (correct answers)": "གདམ་ཁ་ཅན་གྱི་དྲི་བའི་སྐུགས",
"Mean MCQ score": "གདམ་ཁ་ཅན་གྱི་དྲི་བའི་ཆ་སྙོམས་སྐུགས",
"p-value": "p གནས་གོང",
"Statistic": "གྲངས་རྩིས", "Value": "གནས་གོང",
"Number Correct": "ལན་ངོ་མ་གྱངས་ཁ", "Number Incorrect": "ལན་འཛོལ་བ་གྱངས་ཁ",
"Max Score": "སྐུགས་ཚད་མཐོ་ཤོས", "Mean Score": "ཆ་སྙོམས་སྐུགས",
"Difficulty (p = mean/max)": "དཀའ་ཚད་ (p)",
"Item-Total r": "དྲི་བ་དང་སྐུགས་བསྡོམས་འབྲེལ་ཚད་ (r)",
"Missing Scores": "སྐུགས་ས་སྟོང་གྱངས་ཁ",
"Too easy": "འཇམ་དྲགསཔ", "Too difficult": "དཀའ་དྲགསཔ",
"Poor": "ཞན་པ", "Fair": "འབྲིང་", "Good": "ལེགས་ཤོམ", "Ideal": "འོས་འབབ་ལྡན་པ",
"Negative": "མེད་གྲངས", "Not available": "མི་འཇུག",
"n": "གྱངས་ཁ", "N": "གྱངས་ཁ", "Population mean": "སྡེ་ཚན་ཡོངས་ཀྱི་ཆ་སྙོམས",
"differs from": "དང་ཁྱད་པར་ཡོད་",
})

MESSAGES.update({
"Very Difficult": "དཀའ་དྲགསཔ", "Too Easy": "འཇམ་དྲགསཔ",
"Excellent": "ལེགས་ཤོམ་མཐའ་དག", "Acceptable": "འོས་འབབ་ལྡན་པ",
"Minimum score": "སྐུགས་དམའ་ཤོས", "Maximum score": "སྐུགས་མཐོ་ཤོས",
"A z-test is appropriate only when the population standard deviation is KNOWN (e.g. from a standardised test), or the samples are very large and σ is well estimated. If σ is estimated from a small class, use a t-test instead.":
"ཛེཌ་བརྟག་དཔྱད་འདི་ སྡེ་ཚན་ཡོངས་ཀྱི་ཚད་ལྡན་ཁ་བྲལ་ཤེས་ཡོད་པའི་སྐབས་འཇུགཔ་ཨིན། སློབ་སྡེ་ཆུང་ཀུའི་སྐུགས་ལས་ཚོད་དཔག་འབད་བ་ཅིན་ ཊི་བརྟག་དཔྱད་གདམ་གནང་།",
"score": "སྐུགས", "Students are ranked by their overall test score for the upper and lower 27% groups.":
"སྡེ་ཚན་མཐོ་ཤོས་དང་དམའ་ཤོས་ 27% རེ་གདམ་ནི་ལུ་ སློབ་ཕྲུག་ཚུ་ཆོས་རྒྱུགས་ཡོངས་ཀྱི་བསྡོམས་སྐུགས་དང་འཁྲིལ་གོ་རིམ་བསྒྲིགས་ཡོད།",
})
PATTERNS.update({
r"(\d+) students · Mean overall score ([\d.]+)\. Each bar shows the number of students\.":
"སློབ་ཕྲུག་ {0} · བསྡོམས་སྐུགས་ཀྱི་ཆ་སྙོམས་ {1} ཨིན། ཀེར་ཐིག་རེ་གིས་སློབ་ཕྲུག་གྱངས་ཁ་སྟོནམ་ཨིན།",
r"The result is statistically significant at (?:α|alpha) = ([\d.]+): there is evidence that (.+)\.":
"གལ་གནད་ཚད་ {0} ལུ་གྲངས་རྩིས་ཀྱི་གལ་གནད་ཡོད་པའི་གྲུབ་འབྲས་ཐོན་ཡོད། {1} ཟེར་བའི་ཁུངས་སྐྱེལ་འདུག",
r"The result is not statistically significant at (?:α|alpha) = ([\d.]+): there is not enough evidence that (.+)\. This does not prove the null hypothesis true\.":
"གལ་གནད་ཚད་ {0} ལུ་གྲངས་རྩིས་ཀྱི་གལ་གནད་ཅན་གྱི་གྲུབ་འབྲས་མ་ཐོན། {1} ཟེར་བའི་ཁུངས་སྐྱེལ་ལངམ་མེད། འདི་གིས་གཞི་བཞག་ཚོད་དཔག་བདེན་པ་ཨིན་ཟེར་མི་སྟོན།",
r"the mean differs from (.+)": "ཆ་སྙོམས་འདི་ {0} དང་ཁྱད་པར་ཡོད",
r"the mean is greater than (.+)": "ཆ་སྙོམས་འདི་ {0} ལས་མཐོ",
r"the mean is less than (.+)": "ཆ་སྙོམས་འདི་ {0} ལས་དམའ",
})


PATTERNS[r"differs from (.+)"] = "དང་ཁྱད་པར་ཡོད་ {0}"


MESSAGES.update({
"StudentID": "སློབ་ཕྲུག་ཨང",
"Enter a name for every student in the Name column.": "སློབ་ཕྲུག་རེའི་མིང་འདི་མིང་ཀེར་ཐིག་ནང་བཙུགས།",
"Enter a numeric overall Total Score for every student.": "སློབ་ཕྲུག་རེའི་བསྡོམས་སྐུགས་ཨང་གྲངས་ཐོག་བཙུགས།",
"All descriptive statistics": "འགྲེལ་བཤད་གྲངས་རྩིས་ཆ་མཉམ",
"Lower quartile (Q1)": "བཞི་ཆ་དང་པའི་ཚད",
"Upper quartile (Q3)": "བཞི་ཆ་གསུམ་པའི་ཚད",
})

MESSAGES.update({
"no_distractor_options": "དྲི་བའི་དབྱེ་བ་འདི་ལུ་ལན་འཛོལ་བའི་གདམ་ཁ་ནུས་ཚད་རྩིས་མི་བཏོན།",
"English": "ཨིང་ལིཤ",
"Lower whisker": "འོག་གི་མཐའ་ཚད", "Upper whisker": "ལྟག་གི་མཐའ་ཚད",
})
