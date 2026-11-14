PRAGMA foreign_keys = ON;

-- All-paper schema. Never key a question by year + question number alone.
CREATE TABLE IF NOT EXISTS paper_codes (
  paper_code TEXT PRIMARY KEY, paper_name TEXT NOT NULL,
  first_official_listing_year INTEGER, last_official_listing_year INTEGER,
  introduction_status TEXT NOT NULL DEFAULT 'UNVERIFIED',
  official_reference_source_id TEXT, notes TEXT
);
CREATE TABLE IF NOT EXISTS examinations (
  year INTEGER PRIMARY KEY CHECK(year BETWEEN 1983 AND 2027),
  organizing_institute TEXT, official_history_source_id TEXT,
  historical_status TEXT NOT NULL DEFAULT 'NOT_RESEARCHED', notes TEXT
);
CREATE TABLE IF NOT EXISTS source_documents (
  source_id TEXT PRIMARY KEY, title TEXT NOT NULL, source_url TEXT NOT NULL,
  organization TEXT,
  source_class TEXT NOT NULL CHECK(source_class IN ('OFFICIAL','INSTITUTIONAL','THIRD_PARTY','COMMUNITY','USER_SUPPLIED')),
  document_type TEXT NOT NULL DEFAULT 'UNKNOWN', examination_year INTEGER,
  paper_code TEXT, session_label TEXT, set_label TEXT, retrieved_at TEXT,
  local_path TEXT, sha256 TEXT, file_size_bytes INTEGER, page_count INTEGER,
  authenticity_status TEXT NOT NULL DEFAULT 'UNVERIFIED',
  inspection_status TEXT NOT NULL DEFAULT 'PENDING', licence_or_reuse_notes TEXT, notes TEXT,
  FOREIGN KEY(examination_year) REFERENCES examinations(year),
  FOREIGN KEY(paper_code) REFERENCES paper_codes(paper_code)
);
CREATE TABLE IF NOT EXISTS exam_paper_offerings (
  offering_id TEXT PRIMARY KEY, year INTEGER NOT NULL REFERENCES examinations(year),
  paper_code TEXT NOT NULL REFERENCES paper_codes(paper_code),
  offering_status TEXT NOT NULL DEFAULT 'NOT_RESEARCHED', session_count INTEGER,
  source_id TEXT REFERENCES source_documents(source_id), evidence_notes TEXT,
  UNIQUE(year,paper_code)
);
CREATE TABLE IF NOT EXISTS paper_sessions (
  session_id TEXT PRIMARY KEY, offering_id TEXT NOT NULL REFERENCES exam_paper_offerings(offering_id),
  session_label TEXT NOT NULL, session_date TEXT, start_time TEXT, end_time TEXT,
  source_id TEXT REFERENCES source_documents(source_id), UNIQUE(offering_id,session_label)
);
CREATE TABLE IF NOT EXISTS paper_sets (
  paper_id TEXT PRIMARY KEY, session_id TEXT NOT NULL REFERENCES paper_sessions(session_id),
  set_label TEXT NOT NULL DEFAULT 'MASTER', paper_source_id TEXT REFERENCES source_documents(source_id),
  answer_key_source_id TEXT REFERENCES source_documents(source_id),
  paper_status TEXT NOT NULL DEFAULT 'NOT_VERIFIED', expected_question_count INTEGER,
  extracted_question_count INTEGER NOT NULL DEFAULT 0, UNIQUE(session_id,set_label)
);
CREATE TABLE IF NOT EXISTS paper_sections (
  section_id TEXT PRIMARY KEY, paper_id TEXT NOT NULL REFERENCES paper_sets(paper_id),
  section_code TEXT, section_name TEXT NOT NULL, section_kind TEXT NOT NULL DEFAULT 'COMPULSORY',
  selectable_group TEXT, selection_min INTEGER, selection_max INTEGER, marks_total REAL, notes TEXT
);
CREATE TABLE IF NOT EXISTS subjects (
  subject_id INTEGER PRIMARY KEY, paper_code TEXT NOT NULL REFERENCES paper_codes(paper_code),
  subject_name TEXT NOT NULL, UNIQUE(paper_code,subject_name)
);
CREATE TABLE IF NOT EXISTS topics (
  topic_id INTEGER PRIMARY KEY, subject_id INTEGER NOT NULL REFERENCES subjects(subject_id),
  topic_name TEXT NOT NULL, UNIQUE(subject_id,topic_name)
);
CREATE TABLE IF NOT EXISTS subtopics (
  subtopic_id INTEGER PRIMARY KEY, topic_id INTEGER NOT NULL REFERENCES topics(topic_id),
  subtopic_name TEXT NOT NULL, UNIQUE(topic_id,subtopic_name)
);
CREATE TABLE IF NOT EXISTS concepts (
  concept_id INTEGER PRIMARY KEY, subtopic_id INTEGER REFERENCES subtopics(subtopic_id),
  concept_name TEXT NOT NULL, description TEXT
);
CREATE TABLE IF NOT EXISTS questions (
  question_id TEXT PRIMARY KEY, paper_id TEXT NOT NULL REFERENCES paper_sets(paper_id),
  section_id TEXT REFERENCES paper_sections(section_id), question_number TEXT NOT NULL,
  question_group TEXT, source_page_start INTEGER, source_page_end INTEGER,
  original_question_text TEXT NOT NULL, normalized_question_text TEXT,
  question_type TEXT NOT NULL DEFAULT 'UNKNOWN' CHECK(question_type IN ('MCQ','MSQ','NAT','OTHER','UNKNOWN')),
  question_format TEXT, marks REAL, negative_marks REAL, official_answer_text TEXT,
  independently_derived_answer TEXT, answer_status TEXT NOT NULL DEFAULT 'PENDING',
  subject_id INTEGER REFERENCES subjects(subject_id), topic_id INTEGER REFERENCES topics(topic_id),
  subtopic_id INTEGER REFERENCES subtopics(subtopic_id), concept_id INTEGER REFERENCES concepts(concept_id),
  difficulty TEXT NOT NULL DEFAULT 'UNASSESSED' CHECK(difficulty IN ('EASY','MEDIUM','HARD','UNASSESSED')),
  extraction_method TEXT, extraction_confidence REAL, verification_status TEXT NOT NULL DEFAULT 'PENDING',
  verified_by TEXT, verified_at TEXT, UNIQUE(paper_id,question_number)
);
CREATE TABLE IF NOT EXISTS question_options (
  option_id INTEGER PRIMARY KEY, question_id TEXT NOT NULL REFERENCES questions(question_id) ON DELETE CASCADE,
  option_label TEXT NOT NULL, option_text TEXT NOT NULL,
  is_officially_correct INTEGER CHECK(is_officially_correct IN (0,1)), UNIQUE(question_id,option_label)
);
CREATE TABLE IF NOT EXISTS question_assets (
  asset_id TEXT PRIMARY KEY, question_id TEXT NOT NULL REFERENCES questions(question_id) ON DELETE CASCADE,
  asset_type TEXT NOT NULL CHECK(asset_type IN ('DIAGRAM','TABLE','IMAGE','EQUATION','OTHER')),
  source_page INTEGER, local_path TEXT, alt_text TEXT, crop_coordinates TEXT, sha256 TEXT,
  verification_status TEXT NOT NULL DEFAULT 'PENDING'
);
CREATE TABLE IF NOT EXISTS answer_key_items (
  key_item_id TEXT PRIMARY KEY, paper_id TEXT NOT NULL REFERENCES paper_sets(paper_id),
  question_number TEXT NOT NULL, answer_value TEXT, answer_range_min REAL, answer_range_max REAL,
  disposition TEXT, key_version TEXT NOT NULL DEFAULT 'UNKNOWN',
  source_id TEXT REFERENCES source_documents(source_id), verification_status TEXT NOT NULL DEFAULT 'PENDING',
  UNIQUE(paper_id,question_number,key_version)
);
CREATE TABLE IF NOT EXISTS solutions (
  solution_id TEXT PRIMARY KEY, question_id TEXT NOT NULL REFERENCES questions(question_id) ON DELETE CASCADE,
  solution_kind TEXT NOT NULL DEFAULT 'INDEPENDENT', concept_explanation TEXT, prerequisites TEXT,
  step_by_step_solution TEXT NOT NULL, calculation_details TEXT, correct_answer_explanation TEXT,
  incorrect_option_explanations TEXT, shortcut_or_alternative TEXT, common_mistakes TEXT,
  official_solution_source_id TEXT REFERENCES source_documents(source_id),
  verification_status TEXT NOT NULL DEFAULT 'PENDING'
);
CREATE TABLE IF NOT EXISTS syllabus_versions (
  syllabus_version_id TEXT PRIMARY KEY, paper_code TEXT NOT NULL REFERENCES paper_codes(paper_code),
  version_label TEXT NOT NULL, effective_from_year INTEGER, effective_to_year INTEGER,
  source_id TEXT REFERENCES source_documents(source_id), notes TEXT
);
CREATE TABLE IF NOT EXISTS syllabus_topics (
  syllabus_topic_id TEXT PRIMARY KEY,
  syllabus_version_id TEXT NOT NULL REFERENCES syllabus_versions(syllabus_version_id),
  parent_topic_id TEXT, official_topic_name TEXT NOT NULL, topic_level INTEGER NOT NULL DEFAULT 1, notes TEXT
);
CREATE TABLE IF NOT EXISTS question_syllabus_mapping (
  question_id TEXT NOT NULL REFERENCES questions(question_id) ON DELETE CASCADE,
  syllabus_version_id TEXT NOT NULL REFERENCES syllabus_versions(syllabus_version_id),
  syllabus_topic_id TEXT NOT NULL REFERENCES syllabus_topics(syllabus_topic_id),
  mapping_status TEXT NOT NULL DEFAULT 'PENDING', rationale TEXT,
  PRIMARY KEY(question_id,syllabus_version_id,syllabus_topic_id)
);
CREATE TABLE IF NOT EXISTS similarity_groups (
  similarity_group_id TEXT PRIMARY KEY, label TEXT NOT NULL, similarity_basis TEXT, reviewer_notes TEXT
);
CREATE TABLE IF NOT EXISTS similarity_members (
  similarity_group_id TEXT NOT NULL REFERENCES similarity_groups(similarity_group_id),
  question_id TEXT NOT NULL REFERENCES questions(question_id), similarity_score REAL,
  PRIMARY KEY(similarity_group_id,question_id)
);
CREATE TABLE IF NOT EXISTS verification_events (
  event_id INTEGER PRIMARY KEY, paper_id TEXT REFERENCES paper_sets(paper_id),
  question_id TEXT REFERENCES questions(question_id), source_id TEXT REFERENCES source_documents(source_id),
  verification_stage TEXT NOT NULL, result TEXT NOT NULL, reviewer TEXT, notes TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS extraction_batches (
  batch_id TEXT PRIMARY KEY, paper_id TEXT REFERENCES paper_sets(paper_id), batch_name TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'PLANNED', started_at TEXT, completed_at TEXT,
  questions_extracted INTEGER NOT NULL DEFAULT 0, questions_verified INTEGER NOT NULL DEFAULT 0,
  errors_count INTEGER NOT NULL DEFAULT 0, report_path TEXT
);
CREATE INDEX IF NOT EXISTS idx_offerings_year_code ON exam_paper_offerings(year,paper_code);
CREATE INDEX IF NOT EXISTS idx_sessions_offering ON paper_sessions(offering_id);
CREATE INDEX IF NOT EXISTS idx_papers_session ON paper_sets(session_id);
CREATE INDEX IF NOT EXISTS idx_questions_paper ON questions(paper_id);
CREATE INDEX IF NOT EXISTS idx_questions_subject ON questions(subject_id);
CREATE INDEX IF NOT EXISTS idx_questions_topic ON questions(topic_id);
CREATE INDEX IF NOT EXISTS idx_questions_type ON questions(question_type);
CREATE INDEX IF NOT EXISTS idx_sources_year_code ON source_documents(examination_year,paper_code);
