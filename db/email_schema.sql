use sopho;

create database sopho; 
CREATE USER 'ubuntu'@'localhost' IDENTIFIED BY '123qwe';
GRANT ALL PRIVILEGES ON * . * TO 'ubuntu'@'localhost';
FLUSH PRIVILEGES;


DROP TABLE IF EXISTS job;
CREATE TABLE job (
  id bigint unsigned NOT NULL PRIMARY KEY,
  msg_id bigint unsigned NOT NULL,
  msg_type ENUM('email') DEFAULT 'email',
  status ENUM('waiting', 'done', 'error') DEFAULT 'waiting',
  error_msg TEXT DEFAULT NULL,
  llm_config bigint unsigned DEFAULT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  KEY status_key (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS email;
CREATE TABLE email (
  id bigint unsigned NOT NULL PRIMARY KEY,
  email_from varchar(1024) NOT NULL,
  email_to varchar(2048) DEFAULT NULL,
  email_cc varchar(2048) DEFAULT NULL,
  email_text TEXT DEFAULT NULL,
  subject varchar(1024) DEFAULT NULL,
  spam_score FLOAT NOT NULL,
  date varchar(256) DEFAULT NULL,
  in_reply_to varchar(1024) DEFAULT NULL,
  message_id varchar(1024) DEFAULT NULL,
  email_references TEXT DEFAULT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS llm_config;
CREATE TABLE llm_config (
  id bigint unsigned NOT NULL PRIMARY KEY,
  email varchar(1024) NOT NULL,
  model varchar(1024) NOT NULL,
  prompt TEXT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

