PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS examinations (
  examination_id INTEGER PRIMARY KEY,
  year INTEGER NOT NULL UNIQUE,
  organizing_institute TEXT,
  history_evidence_source_id INTEGER
);

CREATE TABLE IF NOT EXISTS sources (
  source_id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  url TEXT NOT NULL,
  organization TEXT,
  source_class TEXT NOT NULL,
  examination_year INTEGER,
  retrieved_at TEXT,
  local_path TEXT,
  sha256 TEXT,
  file_size_bytes INTEGER,
  page_count INTEGER,
  authenticity_status TEXT NOT NULL DEFAULT 'UNVERIFIED',
  inspection_status TEXT NOT NULL DEFAULT 'PENDING',
  notes TEXT
);

CREATE TABLE IF NOT EXISTS papers (
  paper_id TEXT PRIMARY KEY,
  examination_id INTEGER NOT NULL REFERENCES examinations(examination_id),
  paper_code TEXT NOT NULL CHECK (paper_code = 'CS'),
  paper_name TEXT,
  session_label TEXT NOT NULL DEFAULT 'UNKNOWN',
  set_label TEXT NOT NULL DEFAULT 'UNKNOWN',
  paper_source_id TEXT REFERENCES sources(source_id),
  official_key_source_id TEXT REFERENCES sources(source_id),
  paper_status TEXT NOT NULL DEFAULT 'NOT_ESTABLISHED',
  expected_question_count INTEGER,
  extracted_question_count INTEGER NOT NULL DEFAULT 0,
  UNIQUE(examination_id, paper_code, session_label, set_label)
);

CREATE TABLE IF NOT EXISTS sessions (
  session_id TEXT PRIMARY KEY,
  paper_id TEXT NOT NULL REFERENCES papers(paper_id) ON DELETE CASCADE,
  session_label TEXT NOT NULL,
  start_time TEXT,
  UNIQUE(paper_id, session_label)
);

CREATE TABLE IF NOT EXISTS subjects (
  subject_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS topics (
  topic_id INTEGER PRIMARY KEY,
  subject_id INTEGER NOT NULL REFERENCES subjects(subject_id),
  name TEXT NOT NULL,
  UNIQUE(subject_id, name)
);

CREATE TABLE IF NOT EXISTS subtopics (
  subtopic_id INTEGER PRIMARY KEY,
  topic_id INTEGER NOT NULL REFERENCES topics(topic_id),
  name TEXT NOT NULL,
  UNIQUE(topic_id, name)
);

CREATE TABLE IF NOT EXISTS concepts (
  concept_id INTEGER PRIMARY KEY,
  subtopic_id INTEGER REFERENCES subtopics(subtopic_id),
  name TEXT NOT NULL,
  description TEXT
);

CREATE TABLE IF NOT EXISTS questions (
  question_id TEXT PRIMARY KEY,
  paper_id TEXT NOT NULL REFERENCES papers(paper_id),
  session_id TEXT REFERENCES sessions(session_id),
  question_number TEXT NOT NULL,
  page_number INTEGER,
  original_question_text TEXT NOT NULL,
  normalized_question_text TEXT,
  question_type TEXT NOT NULL DEFAULT 'UNKNOWN'
    CHECK(question_type IN ('MCQ','MSQ','NAT','UNKNOWN')),
  marks REAL,
  negative_marks REAL,
  official_answer TEXT,
  independently_derived_answer TEXT,
  answer_status TEXT NOT NULL DEFAULT 'PENDING',
  subject_id INTEGER REFERENCES subjects(subject_id),
  topic_id INTEGER REFERENCES topics(topic_id),
  subtopic_id INTEGER REFERENCES subtopics(subtopic_id),
  concept_id INTEGER REFERENCES concepts(concept_id),
  difficulty TEXT NOT NULL DEFAULT 'UNASSESSED'
    CHECK(difficulty IN ('EASY','MEDIUM','HARD','UNASSESSED')),
  diagram_reference TEXT,
  extraction_method TEXT,
  confidence_score REAL,
  verification_level INTEGER NOT NULL DEFAULT 2
    CHECK(verification_level BETWEEN 0 AND 5),
  verification_status TEXT NOT NULL DEFAULT 'PENDING',
  UNIQUE(paper_id, session_id, question_number)
);

CREATE TABLE IF NOT EXISTS question_options (
  option_id INTEGER PRIMARY KEY,
  question_id TEXT NOT NULL REFERENCES questions(question_id) ON DELETE CASCADE,
  option_label TEXT NOT NULL,
  option_text TEXT NOT NULL,
  official_correct INTEGER CHECK(official_correct IN (0,1)),
  UNIQUE(question_id, option_label)
);

CREATE TABLE IF NOT EXISTS answer_keys (
  answer_key_id TEXT PRIMARY KEY,
  paper_id TEXT NOT NULL REFERENCES papers(paper_id),
  source_id TEXT REFERENCES sources(source_id),
  key_version TEXT NOT NULL DEFAULT 'UNKNOWN',
  published_at TEXT,
  status TEXT NOT NULL DEFAULT 'UNVERIFIED'
);

CREATE TABLE IF NOT EXISTS solutions (
  solution_id TEXT PRIMARY KEY,
  question_id TEXT NOT NULL REFERENCES questions(question_id) ON DELETE CASCADE,
  solution_text TEXT NOT NULL,
  concept_explanation TEXT,
  step_by_step TEXT,
  alternative_method TEXT,
  incorrect_option_explanations TEXT,
  common_mistakes TEXT,
  solution_type TEXT NOT NULL DEFAULT 'INDEPENDENT',
  verification_status TEXT NOT NULL DEFAULT 'PENDING'
);

CREATE TABLE IF NOT EXISTS question_source_mapping (
  question_id TEXT NOT NULL REFERENCES questions(question_id) ON DELETE CASCADE,
  source_id TEXT NOT NULL REFERENCES sources(source_id),
  evidence_type TEXT NOT NULL,
  page_number INTEGER,
  notes TEXT,
  PRIMARY KEY(question_id, source_id, evidence_type)
);

CREATE TABLE IF NOT EXISTS syllabus_versions (
  syllabus_version_id TEXT PRIMARY KEY,
  version_label TEXT NOT NULL,
  effective_from_year INTEGER,
  effective_to_year INTEGER,
  source_id TEXT REFERENCES sources(source_id),
  notes TEXT
);

CREATE TABLE IF NOT EXISTS syllabus_topics (
  syllabus_topic_id TEXT PRIMARY KEY,
  syllabus_version_id TEXT NOT NULL REFERENCES syllabus_versions(syllabus_version_id),
  subject_id INTEGER REFERENCES subjects(subject_id),
  topic_id INTEGER REFERENCES topics(topic_id),
  official_topic_name TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'INCLUDED'
);

CREATE TABLE IF NOT EXISTS question_syllabus_mapping (
  question_id TEXT NOT NULL REFERENCES questions(question_id) ON DELETE CASCADE,
  syllabus_version_id TEXT NOT NULL REFERENCES syllabus_versions(syllabus_version_id),
  syllabus_topic_id TEXT REFERENCES syllabus_topics(syllabus_topic_id),
  mapping_status TEXT NOT NULL DEFAULT 'PENDING',
  rationale TEXT,
  PRIMARY KEY(question_id, syllabus_version_id)
);

CREATE TABLE IF NOT EXISTS similarity_groups (
  group_id TEXT PRIMARY KEY,
  group_label TEXT NOT NULL,
  similarity_method TEXT,
  evidence TEXT
);

CREATE TABLE IF NOT EXISTS similarity_members (
  group_id TEXT NOT NULL REFERENCES similarity_groups(group_id),
  question_id TEXT NOT NULL REFERENCES questions(question_id),
  similarity_score REAL,
  PRIMARY KEY(group_id, question_id)
);

CREATE TABLE IF NOT EXISTS verification_logs (
  log_id INTEGER PRIMARY KEY,
  question_id TEXT REFERENCES questions(question_id),
  paper_id TEXT REFERENCES papers(paper_id),
  verification_level INTEGER NOT NULL,
  result TEXT NOT NULL,
  verifier TEXT,
  evidence_source_id TEXT REFERENCES sources(source_id),
  notes TEXT,
  verified_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS extraction_batches (
  batch_id TEXT PRIMARY KEY,
  paper_id TEXT REFERENCES papers(paper_id),
  batch_label TEXT NOT NULL,
  started_at TEXT,
  completed_at TEXT,
  status TEXT NOT NULL DEFAULT 'PLANNED',
  questions_extracted INTEGER NOT NULL DEFAULT 0,
  errors_count INTEGER NOT NULL DEFAULT 0,
  log_path TEXT
);

CREATE TABLE IF NOT EXISTS paper_availability (
  year INTEGER PRIMARY KEY,
  cs_paper_status TEXT NOT NULL DEFAULT 'NOT_ESTABLISHED',
  evidence_source_id TEXT REFERENCES sources(source_id),
  sessions_found INTEGER NOT NULL DEFAULT 0,
  notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_papers_exam ON papers(examination_id);
CREATE INDEX IF NOT EXISTS idx_questions_paper ON questions(paper_id);
CREATE INDEX IF NOT EXISTS idx_questions_type ON questions(question_type);
CREATE INDEX IF NOT EXISTS idx_questions_subject ON questions(subject_id);
CREATE INDEX IF NOT EXISTS idx_questions_topic ON questions(topic_id);
CREATE INDEX IF NOT EXISTS idx_sources_year ON sources(examination_year);
