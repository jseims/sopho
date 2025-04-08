USE SOPHO;

DELETE FROM llm_config;

INSERT INTO llm_config (email, model, prompt) VALUES 
  ("moderator", "gpt4o", "you are awesome");

