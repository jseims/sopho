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

INSERT INTO `prompt` VALUES 
  (1, 1, 1, 1, 'unknown_category', 
  "You are a detail-oriented professor with complete and accurate information about books.  You are talking to a college student eager to understand books.  Your answers will explain to the best of your abilities and be truthful.  You will always respond in json format.  If you don't know the answer to a question, respond if <response>I don't know</response>", 
  "Summarize the book %s by %s?  If the book has multiple chapters that reflect how the content naturally organizes, please create a summary for each chapter with a paragraph of text that explains the key points of that chapter.  If the book is not naturally organized into chapters then summarize into 5-10 paragraphs, each one explaining a portion of the book's content. List these paragraphs in the response as <response>[<point>xxx</point><point>xxx</point>]</response>",
  "summary", "Summary"),
  (2, 1, 1, 2, 'unknown_category', 
  "You are a detail-oriented professor with complete and accurate information about books.  You are talking to a college student eager to understand books.  Your answers will explain to the best of your abilities and be truthful.  You will always respond in json format.  If you don't know the answer to a question, respond if <response>I don't know</response>", 
  "What are some specific examples discussed in the book %s by %s?  Try to come up with about 10 examples that illustrate the thesis of the book and write a detailed paragraph for each example. List these paragraphs in the response as <response>[<point>xxx</point><point>xxx</point>]</response>",
  "examples", "Examples"),
  (3, 1, 1, 3, 'unknown_category', 
  "You are a detail-oriented professor with complete and accurate information about books.  You are talking to a college student eager to understand a particular book as well as work by other writers that explore related concepts.  Your answers will explain to the best of your abilities and be truthful.  You will always respond in json format.  If you don't know the answer to a question, respond if <response>I don't know</response>", 
  "What do other writers have to say about the content of the book %s by %s?  In particular, please write 5-10 paragraphs that give detailed explanations of these thoughts.  These paragraphs should span the range of arguments from others, both in support and in opposition to the book (and various different oppositional arguments)  Also, for each paragraph, give a number on a scale of 1 to 10 that reflects how controversial the argument is (where 1 is highly accepted by mainstream thinkers and 10 is extremely controversial). List these paragraphs in the response as <response>[<point>{'text':'what others have to say','controversy_scale':'1 to 10 scale'}</point>]</response>",
  "discussion", "Discussion"),
  (4, 1, 1, 4, 'unknown_category', 
  "You are a detail-oriented professor with complete and accurate information about books.  You are talking to a college student eager to understand books and wants to be tested on their knowledge.  Your will ask questions that are relevant to the conten of the book, show detailed knowledge and be truthful.  You will always respond in json format.  If you don't know the answer to a question, respond if <response>I don't know</response>", 
  "Can you provide 10-20 multiple choice questions to test knowledge of the book %s by %s?  Respond with <response>[{'question' : 'text of the question','A)':'text of question A','B)':'text of question B','C)':'text of question C','D)':'text of question D','answer':'correct asnwer (A-D)'},'explanation':'a paragraph to explain why the correct answer is correct']</response>",
  "test", "Test Me");

