use sopho;

DROP TABLE IF EXISTS book;
CREATE TABLE book (
  id bigint unsigned NOT NULL,
  amazon_url varchar(1024) NOT NULL,
  image_url varchar(1024) NOT NULL,
  title varchar(1024) NOT NULL,
  author varchar(256) DEFAULT NULL,
  category varchar(256) DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS prompt;
CREATE TABLE prompt (
  id bigint unsigned NOT NULL,
  prompt_set int unsigned NOT NULL,
  level int unsigned NOT NULL,
  position int unsigned NOT NULL,
  category varchar(256) DEFAULT NULL,
  system_text varchar(8096) NOT NULL,
  prompt_text varchar(8096) NOT NULL,
  name varchar(256) NOT NULL,
  label varchar(256) NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS prompt_response;
CREATE TABLE prompt_response (
  id bigint unsigned NOT NULL,
  book_id bigint unsigned NOT NULL,
  prompt_id bigint unsigned NOT NULL,
  created_on int unsigned NOT NULL,
  prompt_hash varchar(256) NOT NULL,
  prompt_text TEXT NOT NULL,
  response_text TEXT NOT NULL,
  llm varchar(256) DEFAULT NULL,
  compute_time int unsigned NOT NULL DEFAULT 0,
  prompt_tokens int unsigned NOT NULL DEFAULT 0,
  response_tokens int unsigned NOT NULL DEFAULT 0,
  error int unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  UNIQUE KEY promt_constraint (prompt_hash)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
