"""Static content of the AISS Framework (AI Implementation Framework for Nigerian Secondary Schools)."""

TIERS = {
    0: {"name": "Tier 0 - Paper", "short": "Paper & cards (no electricity)",
        "sees": "Paper and physical objects", "does": "Label data, follow rules, build simple manual tables",
        "proves": "Paper portfolio", "setup": 165_000, "running": 165_000, "students": 40},
    1: {"name": "Tier 1 - Shared screen", "short": "One shared teacher screen",
        "sees": "A shared screen", "does": "Watch predictions, observe errors, take a turn",
        "proves": "Paper portfolio with error notes", "setup": 511_000, "running": 241_000, "students": 60},
    2: {"name": "Tier 2 - Offline computers", "short": "Offline school computers",
        "sees": "Offline school computer", "does": "Train basic offline models, count test errors",
        "proves": "Saved offline models and performance records", "setup": 5_031_000, "running": 831_000, "students": 150},
    3: {"name": "Tier 3 - Online lab", "short": "Online school computers",
        "sees": "Online school computer", "does": "Build local projects with real data",
        "proves": "Completed project, presentation and contest results", "setup": 5_331_000, "running": 1_131_000, "students": 200},
}

# (id, question, [(label, points), ...])
AUDIT_ITEMS = [
    (1, "Regular electricity supply (grid, solar or generator)?", [("Yes", 3), ("Sometimes", 1), ("No", 0)]),
    (2, "Secure room with working outlets?", [("Yes", 2), ("No", 0)]),
    (3, "Working computers or tablets for students?", [("10 or more", 3), ("1 to 9", 2), ("None", 0)]),
    (4, "Teacher smartphone available for lessons?", [("Yes", 1), ("No", 0)]),
    (5, "Regular internet connection?", [("Yes", 2), ("Sometimes", 1), ("No", 0)]),
    (6, "Designated AI lead teacher with allocated time?", [("Yes", 3), ("Partial", 1), ("No", 0)]),
    (7, "Designated deputy lead teacher?", [("Yes", 1), ("No", 0)]),
    (8, "Secured funding for Years 2 and 3?", [("Yes", 2), ("No", 0)]),
    (9, "Assigned technician for repairs?", [("Yes", 2), ("No", 0)]),
    (10, "No history of broken or abandoned donated technology?", [("Yes", 1), ("No", 0)]),
]
MAX_AUDIT_SCORE = 20

TIER_ACTIONS = {
    0: ["Run the Week 1 unplugged lesson now; it needs no power or budget.",
        "Direct first spending to reliable power (e.g. solar), not computers.",
        "Appoint a lead AI teacher and a deputy with timetabled hours.",
        "Hold club sessions in school hours so girls and other learners are not excluded."],
    1: ["Use one teacher device and a shared screen for demonstrations; keep paper work for every student.",
        "Secure the device and a charging routine before adding anything else.",
        "Appoint a lead teacher and deputy; train them first.",
        "Plan funding for Years 2 and 3 before buying more equipment."],
    2: ["Install offline tools on the school computers and test them before term starts.",
        "Name a technician and set a repair routine.",
        "Keep paper portfolios alongside saved models so evidence is portable.",
        "Document funding for Years 2 and 3."],
    3: ["Use projects with real, self-collected local data.",
        "Obtain parental consent before any online tool is used (see the Portfolio & Consent page).",
        "Act as a hub: share lessons and training with neighbouring schools.",
        "Prepare a step-down plan in case power or internet fails."],
}

CURRICULUM = [
    {"Weeks": "1-2", "Core topic": "What is AI?",
     "Paper activity (Tier 0-1)": "Classify school tools as fixed-rule or learning tools.",
     "Digital activity (Tier 2-3)": "Demonstrate an AI tool online or on a phone."},
    {"Weeks": "3-4", "Core topic": "Data and labelling",
     "Paper activity (Tier 0-1)": "Collect class data and sort printed picture cards.",
     "Digital activity (Tier 2-3)": "Enter data and label images in a software tool."},
    {"Weeks": "5-7", "Core topic": "Training and testing",
     "Paper activity (Tier 0-1)": "Build a paper rule table and test errors on cards.",
     "Digital activity (Tier 2-3)": "Train a model on a PC or tablet and test accuracy."},
    {"Weeks": "8-9", "Core topic": "Bias and errors",
     "Paper activity (Tier 0-1)": "Discuss biased card samples and correct wrong text outputs.",
     "Digital activity (Tier 2-3)": "Test real AI outputs for errors using local examples."},
    {"Weeks": "10-11", "Core topic": "Ethics and integrity",
     "Paper activity (Tier 0-1)": "Role-play privacy rights and draft classroom AI rules.",
     "Digital activity (Tier 2-3)": "Examine online privacy policies and cite AI tools."},
    {"Weeks": "12", "Core topic": "Final project",
     "Paper activity (Tier 0-1)": "Present a poster solution for a local problem.",
     "Digital activity (Tier 2-3)": "Present a digital model demonstration."},
]

STAGES = [
    ("1. Curious", "JSS 1", "Learns the basics; finds everyday uses of AI in Nigeria."),
    ("2. Careful", "JSS 2-3", "Tries an AI tool with guidance; practises honest habits."),
    ("3. Critical", "SS 1", "Spots wrong answers; understands bias and data ownership."),
    ("4. Creative", "SS 2", "Builds a simple AI model and finds its mistakes."),
    ("5. Connected", "SS 3", "Completes a real project on a local issue; plans next steps."),
]

RUBRIC = {
    "Local problem": ["Copied from a textbook.", "Relevant local issue.", "Clear local problem with community impact."],
    "Data quality": ["Incomplete or made up.", "Collected by the student.", "Carefully collected and labelled, with notes."],
    "Testing and errors": ["No testing done.", "Tested and errors counted.", "Tested, errors counted and explained."],
    "Fairness and ethics": ["Not addressed.", "Acknowledges potential bias.", "Explains who is affected and proposes fixes."],
    "Honesty and integrity": ["Unclear AI usage.", "States where AI was used.", "Clearly credits AI help versus own work."],
}

PORTFOLIO_ITEMS = ["Labelled data sample", "Paper rule table", "Error log",
                   "Fairness note", "Signed AI-use declaration", "Project poster or demo description"]

EQUITY = [
    ("Female students", "After-school conflicts with chores and travel.", "Hold clubs during school hours or breaks; send direct invitations."),
    ("Struggling readers", "Heavy text materials create frustration.", "Use card sorting, drawings and visual group discussion."),
    ("Non-English speakers", "English-only terms are hard to grasp.", "Introduce concepts in local languages first, then link to English."),
    ("Low-income learners", "Cannot afford mobile data for home tasks.", "Do all work in class, offline; assign no online homework."),
]

REFERENCES = [
    "Bell, T., Alexander, J., Freeman, I., & Grimley, M. (2009). Computer Science Unplugged: School students doing real computing without computers. The New Zealand Journal of Applied Computing and Information Technology, 13(1), 20-29.",
    "Black, P., & Wiliam, D. (1998). Assessment and classroom learning. Assessment in Education: Principles, Policy & Practice, 5(1), 7-74.",
    "Buolamwini, J., & Gebru, T. (2018). Gender shades: Intersectional accuracy disparities in commercial gender classification. Proceedings of Machine Learning Research, 81, 77-91.",
    "Casal-Otero, L., et al. (2023). AI literacy in K-12: A systematic literature review. International Journal of STEM Education, 10, Article 29.",
    "Federal Republic of Nigeria. (2023). Nigeria Data Protection Act, 2023.",
    "Ji, Z., et al. (2023). Survey of hallucination in natural language generation. ACM Computing Surveys, 55(12), Article 248.",
    "Long, D., & Magerko, B. (2020). What is AI literacy? Competencies and design considerations. CHI 2020. https://doi.org/10.1145/3313831.3376727",
    "Mishra, P., & Koehler, M. J. (2006). Technological pedagogical content knowledge. Teachers College Record, 108(6), 1017-1054.",
    "Ng, D. T. K., et al. (2021). Conceptualizing AI literacy: An exploratory review. Computers and Education: Artificial Intelligence, 2, 100041.",
    "Papert, S. (1980). Mindstorms: Children, computers, and powerful ideas. Basic Books.",
    "Touretzky, D., et al. (2019). Envisioning AI for K-12: What should every child know about AI? AAAI-19, 33(1), 9795-9799.",
    "Toyama, K. (2015). Geek heresy: Rescuing social change from the cult of technology. PublicAffairs.",
    "UNESCO. (2023). Guidance for generative AI in education and research.",
    "UNESCO. (2024a). AI competency framework for teachers.",
    "UNESCO. (2024b). AI competency framework for students.",
]
