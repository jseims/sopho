USE SOPHO;

DELETE FROM book;

INSERT INTO `book` VALUES 
  (1, 'https://www.amazon.com/Rational-Optimist-How-Prosperity-Evolves/dp/006145205X', 
    "https://m.media-amazon.com/images/I/51uuXs3tzlL._SY466_.jpg",
    "The Rational Optimist: How Prosperity Evolves",
    "Matt Ridley", "non-fiction"),
  (2, 'https://www.amazon.com/Skin-Game-Hidden-Asymmetries-Daily/dp/0425284646', 
    "https://m.media-amazon.com/images/I/71tG+8MoHgL._SY466_.jpg",
    "Skin in the Game: Hidden Asymmetries in Daily Life (Incerto)",
    "Nassim Nicholas Taleb", "non-fiction"),
  (3, 'https://www.amazon.com/Steve-Jobs-Walter-Isaacson/dp/1451648537', 
    "https://m.media-amazon.com/images/I/61d7gLTQ4bL._SY466_.jpg",
    "Steve Jobs",
    "Walter Isaacson", "non-fiction"),
  (4, 'https://www.amazon.com/The-Three-Body-Problem-audiobook/dp/B00P00QPPY', 
    "https://m.media-amazon.com/images/I/51pHYR3yHaL.jpg",
    "The Three-Body Problem",
    "Cixin Liu", "fiction");


DELETE FROM prompt;

JSON object which enumerates a set of 5 child objects.                       
                        Each child object has a property named "q" and a property named "a".
                        For each child object assign to the property named "q" a question which has its answer in the article 
                        and to the property named "a" a short answer to this question.
                        The resulting JSON object should be in this format: [{"q":"string","a":"string"}].\n\n
                        The article:\n
                        ${textToUse}\n\n
                        The JSON object:\n\n`;


create a valid JSON array of objects for translating baby speak into English following this format:

[{"baby": "sound the baby makes",
"volumeDb": "how loud is the sound, decibels as a floating-point number",
"timeMin": "how long the sound is made, minutes with 2 decimal places",
"meaning": "what the baby might be trying to communicate",
"confidencePct": "certainty of meaning, percent as an integer,
"response": "what sound the parent should reply with"}]

The JSON object:
`.trim()                        

Respond with a valid JSON array that lists these paragraphs as ['paragraph 1'], ['paragraph 2'], ['paragraph 3']

Respond with <response>[{'question' : 'text of the question','A)':'text of question A','B)':'text of question B','C)':'text of question C','D)':'text of question D','answer':'correct asnwer (A-D)'},'explanation':'a few sentences to explain why the correct answer is correct']</response>
Respond with a valid JSON array that lists these questions as [{'question' : 'text of the question','A)':'text of question A','B)':'text of question B','C)':'text of question C','D)':'text of question D','answer':'correct asnwer (A-D)'},'explanation':'a few sentences to explain why the correct answer is correct']


INSERT INTO `prompt` VALUES 
  (1, NULL, 1, 1, 1, 'unknown_category', 
  "You are a detail-oriented professor with complete and accurate information about books.  You are talking to a college student eager to understand books.  Your answers will explain to the best of your abilities and be truthful.  You will always respond in json format.  If you don't know the answer to a question, respond with {'error' : 'I do not know'}", 
  "Summarize the book %s by %s.  If the book has multiple chapters that reflect how the content naturally organizes, please create a summary for each chapter with a paragraph of text that explains the key points of that chapter.  If the book is not naturally organized into chapters then summarize into 5-10 paragraphs, each one explaining a portion of the book's content. Respond with a valid JSON array that lists these paragraphs as ['paragraph 1'], ['paragraph 2'], ['paragraph 3']",
  "summary", "Summary"),
  (2, NULL, 1, 1, 2, 'unknown_category', 
  "You are a detail-oriented professor with complete and accurate information about books.  You are talking to a college student eager to understand books.  Your answers will explain to the best of your abilities and be truthful.  You will always respond in json format.  If you don't know the answer to a question, respond with {'error' : 'I do not know'}", 
  "What are some specific examples discussed in the book %s by %s?  Try to come up with about 10 examples that illustrate the thesis of the book and write a detailed paragraph for each example. Respond with a valid JSON array that lists these paragraphs as ['paragraph 1'], ['paragraph 2'], ['paragraph 3']",
  "examples", "Examples"),
  (3, NULL, 1, 1, 3, 'unknown_category', 
  "You are a detail-oriented professor with complete and accurate information about books.  You are talking to a college student eager to understand a particular book as well as work by other writers that explore related concepts.  Your answers will explain to the best of your abilities and be truthful.  You will always respond in json format.  If you don't know the answer to a question, respond with {'error' : 'I do not know'}", 
  "What do other writers have to say about the content of the book %s by %s?  In particular, please write 5-10 paragraphs that give detailed explanations of these thoughts.  These paragraphs should span the range of common arguments from others, both in support and in opposition to the book (and various different oppositional arguments, and provide sources).  Respond with a valid JSON array that lists these paragraphs as ['paragraph 1'], ['paragraph 2'], ['paragraph 3']",
  "discussion", "Discussion"),
  (4, NULL, 1, 1, 4, 'unknown_category', 
  "You are a detail-oriented professor with complete and accurate information about books.  You are talking to a college student eager to understand books and wants to be tested on their knowledge.  Your will ask questions that are relevant to the conten of the book, show detailed knowledge and be truthful.  You will always respond in json format.  If you don't know the answer to a question, respond with {'error' : 'I do not know'}", 
  "Can you provide 10-20 multiple choice questions to test knowledge of the book %s by %s?  Respond with a valid JSON array that lists these questions as [{'question' : 'text of the question','A)':'text of question A','B)':'text of question B','C)':'text of question C','D)':'text of question D','answer':'correct asnwer (A-D)'},'explanation':'a few sentences to explain why the correct answer is correct']",
  "test", "Test Me"),
  (5, 1, 1, 2, 1, 'unknown_category', 
  "You are a detail-oriented professor with complete and accurate information about books.  You are talking to a college student eager to understand books.  Your answers will explain to the best of your abilities and be truthful.  You will go deep into details.  You will always respond in json format.  If you don't know the answer to a question, respond with {'error' : 'I do not know'}", 
  "The book %s by %s talks has a section about %s.  Please explain what the author meant in that section by summarizing into 5-10 paragraphs, each one explaining a portion of the section. Respond with a valid JSON array that lists these paragraphs as ['paragraph 1'], ['paragraph 2'], ['paragraph 3']",
  "summary", "Summary"),
  (6, 1, 1, 2, 2, 'unknown_category', 
  "You are a detail-oriented professor with complete and accurate information about books.  You are talking to a college student eager to understand books.  Your answers will explain to the best of your abilities and be truthful.  You will go deep into details.  You will always respond in json format.  If you don't know the answer to a question, respond with {'error' : 'I do not know'}", 
  "What are some specific examples discussed in the book %s by %s specifically to the section about %s?  Try to come up with about 10 examples that illustrate the arguments of this section and write a detailed paragraph for each example. Respond with a valid JSON array that lists these paragraphs as ['paragraph 1'], ['paragraph 2'], ['paragraph 3']",
  "examples", "Examples"),
  (7, 1, 1, 2, 3, 'unknown_category', 
  "You are a detail-oriented professor with complete and accurate information about books.  You are talking to a college student eager to understand books.  Your answers will explain to the best of your abilities and be truthful.  You will go deep into details.  You will always respond in json format.  If you don't know the answer to a question, respond with {'error' : 'I do not know'}", 
  "What do other writers have to say about the content of the book %s by %s, specifically to the section about %s?  In particular, please write 5-10 paragraphs that give detailed explanations of these thoughts.  These paragraphs should span the range of common arguments from others, both in support and in opposition to the section (and various different oppositional arguments, and provide sources).  Respond with a valid JSON array that lists these paragraphs as ['paragraph 1'], ['paragraph 2'], ['paragraph 3']",
  "discussion", "Discussion"),
  (8, 1, 1, 2, 4, 'unknown_category', 
  "You are a detail-oriented professor with complete and accurate information about books.  You are talking to a college student eager to understand books.  Your answers will explain to the best of your abilities and be truthful.  You will go deep into details.  You will always respond in json format.  If you don't know the answer to a question, respond with {'error' : 'I do not know'}", 
  "Can you provide 10-20 multiple choice questions to test knowledge of the book %s by %s, specifically to the section about %s?  Respond with a valid JSON array that lists these questions as [{'question' : 'text of the question','A)':'text of question A','B)':'text of question B','C)':'text of question C','D)':'text of question D','answer':'correct asnwer (A-D)'},'explanation':'a few sentences to explain why the correct answer is correct']",
  "test", "Test Me"),
  (9, 2, 1, 2, 1, 'unknown_category', 
  "You are a detail-oriented professor with complete and accurate information about books.  You are talking to a college student eager to understand books.  Your answers will explain to the best of your abilities and be truthful.  You will go deep into details.  You will always respond in json format.  If you don't know the answer to a question, respond with {'error' : 'I do not know'}", 
  "The following is an example from the book %s by %s: %s.  Please explain what the author means by this example by summarizing into 5-10 paragraphs, each one explaining a portion of the example. Respond with a valid JSON array that lists these paragraphs as ['paragraph 1'], ['paragraph 2'], ['paragraph 3']",
  "summary", "Summary"),
  (10, 2, 1, 2, 2, 'unknown_category', 
  "You are a detail-oriented professor with complete and accurate information about books.  You are talking to a college student eager to understand books.  Your answers will explain to the best of your abilities and be truthful.  You will go deep into details.  You will always respond in json format.  If you don't know the answer to a question, respond with {'error' : 'I do not know'}", 
  "The following is an example from the book %s by %s: %s.  Try to come up with about 10 further examples that illustrate the author's example and write a detailed paragraph for each example. Respond with a valid JSON array that lists these paragraphs as ['paragraph 1'], ['paragraph 2'], ['paragraph 3']",
  "examples", "Examples"),
  (11, 2, 1, 2, 3, 'unknown_category', 
  "You are a detail-oriented professor with complete and accurate information about books.  You are talking to a college student eager to understand books.  Your answers will explain to the best of your abilities and be truthful.  You will go deep into details.  You will always respond in json format.  If you don't know the answer to a question, respond with {'error' : 'I do not know'}", 
  "The following is an example from the book %s by %s: %s. What do other writers have to say about the meaning and validity of that example?  In particular, please write 5-10 paragraphs that give detailed explanations of these thoughts.  These paragraphs should span the range of common arguments from others, both in support and in opposition to the example (and various different oppositional arguments, and provide sources).  Respond with a valid JSON array that lists these paragraphs as ['paragraph 1'], ['paragraph 2'], ['paragraph 3']",
  "discussion", "Discussion"),
  (12, 2, 1, 2, 4, 'unknown_category', 
  "You are a detail-oriented professor with complete and accurate information about books.  You are talking to a college student eager to understand books.  Your answers will explain to the best of your abilities and be truthful.  You will go deep into details.  You will always respond in json format.  If you don't know the answer to a question, respond with {'error' : 'I do not know'}", 
  "Can you provide 10-20 multiple choice questions to test knowledge of the book %s by %s, specifically related to the example %s?  Respond with a valid JSON array that lists these questions as [{'question' : 'text of the question','A)':'text of question A','B)':'text of question B','C)':'text of question C','D)':'text of question D','answer':'correct asnwer (A-D)'},'explanation':'a few sentences to explain why the correct answer is correct']",
  "test", "Test Me"),
  (13, 3, 1, 2, 1, 'unknown_category', 
  "You are a detail-oriented professor with complete and accurate information about books.  You are talking to a college student eager to understand books.  Your answers will explain to the best of your abilities and be truthful.  You will go deep into details.  You will always respond in json format.  If you don't know the answer to a question, respond with {'error' : 'I do not know'}", 
  "The following is a discussion about the book %s by %s: %s.  Please this explain this discussion by summarizing into 5-10 paragraphs, each one explaining a portion of the discussion. Respond with a valid JSON array that lists these paragraphs as ['paragraph 1'], ['paragraph 2'], ['paragraph 3']",
  "summary", "Summary"),
  (14, 3, 1, 2, 2, 'unknown_category', 
  "You are a detail-oriented professor with complete and accurate information about books.  You are talking to a college student eager to understand books.  Your answers will explain to the best of your abilities and be truthful.  You will go deep into details.  You will always respond in json format.  If you don't know the answer to a question, respond with {'error' : 'I do not know'}", 
  "The following is a discussion about the book %s by %s: %s.  Try to come up with about 10 further examples that illustrate the arguments of the discussion and write a detailed paragraph for each example. Respond with a valid JSON array that lists these paragraphs as ['paragraph 1'], ['paragraph 2'], ['paragraph 3']",
  "examples", "Examples"),
  (15, 3, 1, 2, 3, 'unknown_category', 
  "You are a detail-oriented professor with complete and accurate information about books.  You are talking to a college student eager to understand books.  Your answers will explain to the best of your abilities and be truthful.  You will go deep into details.  You will always respond in json format.  If you don't know the answer to a question, respond with {'error' : 'I do not know'}", 
  "Can you provide 10-20 multiple choice questions to test knowledge of discussion about the book %s by %s: %s?  Respond with a valid JSON array that lists these questions as [{'question' : 'text of the question','A)':'text of question A','B)':'text of question B','C)':'text of question C','D)':'text of question D','answer':'correct asnwer (A-D)'},'explanation':'a few sentences to explain why the correct answer is correct']",
  "test", "Test Me"),
  (16, 4, 1, 2, 1, 'unknown_category', 
  "You are a detail-oriented professor with complete and accurate information about books.  You are talking to a college student eager to understand books.  Your answers will explain to the best of your abilities and be truthful.  You will go deep into details.  You will always respond in json format.  If you don't know the answer to a question, respond with {'error' : 'I do not know'}", 
  "In the book %s by %s, one question is %s and the answer is %s.  Please the context from the book around this question and answer by summarizing into 5-10 paragraphs, each one explaining a portion of this context. Respond with a valid JSON array that lists these paragraphs as ['paragraph 1'], ['paragraph 2'], ['paragraph 3']",
  "summary", "Summary"),
  (17, 4, 1, 2, 2, 'unknown_category', 
  "You are a detail-oriented professor with complete and accurate information about books.  You are talking to a college student eager to understand books.  Your answers will explain to the best of your abilities and be truthful.  You will go deep into details.  You will always respond in json format.  If you don't know the answer to a question, respond with {'error' : 'I do not know'}", 
  "In the book %s by %s, one question is %s and the answer is %s. What do other writers have to say about this question and answer, both in the context of the book as well as the wider world?  In particular, please write 5-10 paragraphs that give detailed explanations of these thoughts.  These paragraphs should span the range of common arguments from others, both in support and in opposition to the answer (and various different oppositional arguments, and provide sources).  Respond with a valid JSON array that lists these paragraphs as ['paragraph 1'], ['paragraph 2'], ['paragraph 3']",
  "discussion", "Discussion");


