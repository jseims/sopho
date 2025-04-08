use sopho;

create database sopho; 
CREATE USER 'ubuntu'@'localhost' IDENTIFIED BY '123qwe';
GRANT ALL PRIVILEGES ON * . * TO 'ubuntu'@'localhost';
FLUSH PRIVILEGES;


DROP TABLE IF EXISTS job;
CREATE TABLE job (
  id INT AUTO_INCREMENT PRIMARY KEY,
  msg_id bigint unsigned NOT NULL,
  msg_type ENUM('email') DEFAULT 'email',
  status ENUM('waiting', 'done', 'error') DEFAULT 'waiting',
  error_msg varchar(8192) DEFAULT NULL,
  llm_config bigint unsigned DEFAULT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  KEY status_key (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS email;
CREATE TABLE email (
  id INT AUTO_INCREMENT PRIMARY KEY,
  email_from varchar(1024) NOT NULL,
  email_to varchar(2048) NOT NULL,
  email_cc varchar(2048) NOT NULL,
  email_text TEXT NOT NULL,
  subject varchar(2048) NOT NULL,
  spam_score FLOAT NOT NULL,
  date varchar(1024) NOT NULL,
  in_reply_to varchar(1024) NOT NULL,
  message_id varchar(1024) NOT NULL,
  email_references varchar(4096) DEFAULT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

