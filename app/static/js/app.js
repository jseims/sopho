var app = app || {};

app.events = {
    PAGE_LOADED : "page_loaded",
    MODEL_CHANGED : "model_changed",
    DATA_LOADED : "data_loaded",
};

app.log = function(msg) {
    if (window.console && console.log) {
        console.log(msg);
    }
};

app.find_in_list = function(list, matchField, matchVal) {
    if (list) {
        for(var i = 0; i < list.length; i++) {
            var val = list[i][matchField];
            if (val === matchVal) {
                return list[i];
            }
        }
    }
};

app.shuffle = function(array) {
    let currentIndex = array.length,  randomIndex;
  
    // While there remain elements to shuffle.
    while (currentIndex > 0) {
  
      // Pick a remaining element.
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex--;
  
      // And swap it with the current element.
      [array[currentIndex], array[randomIndex]] = [
        array[randomIndex], array[currentIndex]];
    }
  
    return array;
};
  


app.mobile = navigator.userAgent.match(/(iPhone|iPod|iPad|Android|BlackBerry)/) != null;

app.view = {
    $book_list : null,
    $book_content : null,
    
    // call a list of initialization functions
    // and initialize quicklist view (always present)
    init : function (viewList) {
        app.view.$book_list = $("#book_list");
        app.view.$book_content = $("#book_content");
    },


    display_books : function() {
        var html = "";

        app.log("books!");
        app.log(app.model.books);
        for(var i = 0; i < app.model.books.length; i++) {

            book = app.model.books[i];

            html += '<a href="/book?id=' + book.id + '" class="card rounded-3">'
            html += '<div class="image-wrapper">';

            html += '<img src="' + book.image_url + '" alt="book thumnail" width=160 height=233>';
            html += '</div> <div class="card-body">';
            html += '<h5 class="card-title">' + book.title + '</h5>';
            html += '<p class="card-text">'+ book.author + '</p>';
            html += '</div> </a>'


        }
        app.view.$book_list.html(html);
    },

    book_selected : function() {
        var html = "";

        html += '<section class="hero-wrap">';
        html += '<div class="rounded-5 bg-style hero-inner" style="background-image: url(/template/static/img/faq-hero-bg.jpg);">';
        html += '<div class="container-xl"> <div class="row align-items-center"> <div class="col-12 col-md-4 ps-0 pe-0 pe-lg-4 hero-thumb">';
        html += '<figure> <img src="' + app.model.current_book.image_url + '" alt="hero-thumb" class="w-100"> </figure> </div>';
        html += '<div class="col-12 col-md-8 text-center text-md-start ms-auto me-auto mt-3 mt-md-0 ps-0 pe-0 hero-text">';
        html += '<h2>' + app.model.current_book.title + '</h2>';
        html += '<h4 class="d-block mt-3 mt-md-4 pb-3 fw-medium">' + app.model.current_book.author + '</h4>';
        html += '<div class="d-block d-md-inline-flex btn-group mt-3 mt-md-5">';
        html += '<a href="' + app.model.current_book.amazon_url + '" class="me-3 rounded border-0 btn btn-primary btn-ex-md">Amazon Link</a>';
        html += '<a href="/test_me?book_id=' + app.model.current_book.id + '&response_piece_id=-1" class="d-block mt-3 mt-md-0 rounded border-0 btn btn-secondary btn-sm">Test Me</a>'
        html += '</div> </div> </div> </div> </div> </section>'

        html += '<div>';
        for(var i = 0; i < app.model.prompt_response_list.length; i++) {
            var list = app.model.prompt_response_list;
            var content_html = app.view.create_list_content(list[i].response_list);
            html += content_html;
        }
        html += '</div>';

        app.view.$book_content.html(html);
    },

  
    display_test : function(choice) {
        var html = "";

        html += '<section class="hero-wrap">  <div class="rounded-5 bg-style hero-inner"> <div class="container-xl">';
        html += '<div class="row align-items-center"> <div class="col-12 col-md-2 ps-4 hero-thumb"> <figure class="rounded-4">';
        html += '<img src="' + app.model.current_book.image_url + '" width=184px height=240px alt="hero-thumb" class="w-100">';
        html += '</figure> </div> <div class="col-12 col-md-10 hero-text">';
        html += '<a href=/book?id=' + app.model.current_book.id + ' class="d-flex ms-0 ms-md-4 align-items-center back-link">';
        html += '<img src="/template/static/svgs/back-arrow.svg" alt="">';
        html += '<span class="ps-4 fw-semibold">Back to ' + app.model.current_book.title + '</span>';
        html += '</a> </div> </div> </div> </section>';

        $("#back_breadcrumb").html(html);

        if (app.model.question_number > 0) {
            var last_question = JSON5.parse(app.model.question_list[app.model.question_number-1].text);
            var answer = last_question.answer;
            var right_wrong = "<span style='color:green'>Correct!</span>";
            if (answer != choice) {
                right_wrong = "<span style='color:red'>Wrong!</span>"
                app.model.test_questions_wrong++;
            } else {
                app.model.test_questions_right++;
            }
            $("#right_wrong").html(right_wrong);

            // set score
            var score = 5 * app.model.test_questions_right - 10 * app.model.test_questions_wrong;
            score = Math.max(score, 0);
            score = Math.min(score, 100)
            if (score == 0) {
                app.model.test_questions_wrong = 0;
                app.model.test_questions_right = 0;
            }
            if (score == 100) {
                app.model.test_questions_wrong = 0;
                app.model.test_questions_right = 20;
            }
            if (score < 20) {
                $("#award_img").hide(html);
            } else {
                $("#award_img").show(html);
            }

            html = "<span>" + score + "</span>/100";
            $("#test_score").html(html);

            html = '<a href="/text_search?id=' + app.model.question_list[app.model.question_number-1].id + '">' + last_question.explanation + '</a>';            
            $("#explanation").html(html);
        } else {
            $("#award_img").hide(html);
        }

        var question = JSON5.parse(app.model.question_list[app.model.question_number].text);
        $("#question_text").html(question.question);

        html = '<form action="#" method="post">';

        html += '<div class="ps-0 form-check"><input class="form-check-input" type="checkbox" value="" id="Checked-1">';
        html += '<label class="w-100 form-check-label" for="Checked-1" onclick="app.view.display_test(\'A)\')">' + question["A)"] + '</label>';
        html += '<span class="d-flex align-items-center justify-content-center position-absolute top-50 translate-middle-y bg-white rounded-circle check-mark">A</span></div>'

        html += '<div class="ps-0 form-check"><input class="form-check-input" type="checkbox" value="" id="Checked-1">';
        html += '<label class="w-100 form-check-label" for="Checked-1" onclick="app.view.display_test(\'B)\')">' + question["B)"] + '</label>';
        html += '<span class="d-flex align-items-center justify-content-center position-absolute top-50 translate-middle-y bg-white rounded-circle check-mark">B</span></div>'

        html += '<div class="ps-0 form-check"><input class="form-check-input" type="checkbox" value="" id="Checked-1">';
        html += '<label class="w-100 form-check-label" for="Checked-1" onclick="app.view.display_test(\'C)\')">' + question["C)"] + '</label>';
        html += '<span class="d-flex align-items-center justify-content-center position-absolute top-50 translate-middle-y bg-white rounded-circle check-mark">C</span></div>'

        html += '<div class="ps-0 form-check"><input class="form-check-input" type="checkbox" value="" id="Checked-1">';
        html += '<label class="w-100 form-check-label" for="Checked-1" onclick="app.view.display_test(\'D)\')">' + question["D)"] + '</label>';
        html += '<span class="d-flex align-items-center justify-content-center position-absolute top-50 translate-middle-y bg-white rounded-circle check-mark">D</span></div>'

        html += "</form>";

        $("#answer_text").html(html);

        if (app.model.question_number < app.model.question_list.length - 1) {
            app.model.question_number++;
        } else {
            app.model.question_number = 0;
        }
    },

    create_list_content : function(list) {
        var html = '';

        html += '<section class="faq-content"> <div class="container-xl"> <div class="row"><div class="p-0 accordion" id="accordionExample">';

        for(var i = 0; i < list.length; i++) {
            html += '<div class="accordion-item mt-4 border-0"> <h2 class="accordion-header">';
            html += '<button class="accordion-button collapsed" type="button" onclick="app.model.load_subresponse(\'' + list[i]['id'] +  '\', ' + i + ')" ';
            html += 'data-bs-toggle="collapse" data-bs-target="#collapse_' + i + '" aria-expanded="false" aria-controls="collapse_' + i + '">'
            html += list[i].text;
            html += '</button></h2>'
            html += '<div id="collapse_' + i + '" class="accordion-collapse collapse" data-bs-parent="#accordionExample"></div></div>'
        }

        html += '</div></div></div></section>'

        return html;
    },

    create_sublist_content : function(list, parent_position) {
        var html = '';

        for(var i = 0; i < list.length; i++) {
            html += '<div class="accordion-item mt-4 border-0"> <h2 class="accordion-header">';
            html += '<button class="accordion-button collapsed" onclick="app.model.load_subsubresponse(\'' + list[i]['id'] +  '\', ' + i + ')" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapse_' + i +'" aria-expanded="false" aria-controls="flush-collapse_' + i + '">';
            html += list[i].text;
            html += '</button> </h2> <div id="flush-collapse_' + i + '" class="accordion-collapse collapse" data-bs-parent="#collapse_' + parent_position + '"></div></div>'
        }
        return html;
    },

    create_subsublist_content : function(prompt, list) {
        var html = '';

        html += '<div class="accordion-row">'
        html += '<h3 class="mb-0 text-white">' + prompt.label + "</h3>";
        html += '</div>'

        for(var i = 0; i < list.length; i++) {
            html += '<div class="accordion-row">';
            if (prompt.name == "discussion") {
                html += '<p>' + list[i].text + '</p>';
            } else {
                html += '<a href="/text_search?id=' + list[i].id + '">' + list[i].text + '</a>';            
            }
            html += '</div>'
        }
        return html;
    },


    
    display_subresponse : function() {
        // remove old 
        var old_name = "#collapse_" + app.model.old_position;
        var new_name = "#collapse_" + app.model.current_position;
        var old_element = $(old_name);
        var new_element = $(new_name);

        app.log("old_element length " + old_element.length);

        old_element.html("");

        var html = '';
        html += '<div class="accordion-body"> <div class="mt-1 accordion-inner">';
        html += '<a href="/test_me?book_id=' + app.model.current_book.id + '&response_piece_id=' + app.model.response_piece_id + '" class="border-0 btn btn-gradient btn-xl">Test Me on this section</a>';
        html += '<div class="accordion accordion-flush" id="accordionFlushExample">'
    
        for(var i = 0; i < app.model.subprompt_response_list.length; i++) {
            var list = app.model.subprompt_response_list;
            var content_html = app.view.create_sublist_content(list[i].response_list, app.model.current_position);
            html += content_html;
        }

        html += '</div></div></div>';

        new_element.html(html);
    },


    display_subsubresponse : function() {
        var old_name = "#flush-collapse_" + app.model.old_subposition;
        var new_name = "#flush-collapse_" + app.model.current_subposition;
        var old_element = $(old_name);
        var new_element = $(new_name);

        old_element.html("");

        var html = '';
        html += '<div class="accordion-body"> <div class="accordion-inner">';
        html += '<a href="/test_me?book_id=' + app.model.current_book.id + '&response_piece_id=' + app.model.response_piece_id + '" class="border-0 btn btn-gradient btn-xl">Test Me on this section</a>'
        html += '<div class="accordion-wrap">'

        html += '<div class="tab-content">';

        for(var i = 0; i < app.model.subsubprompt_response_list.length; i++) {
            var list = app.model.subsubprompt_response_list;
            var prompt = list[i].prompt;
            var content_html = app.view.create_subsublist_content(prompt, list[i].response_list);
            html += content_html;
        }

        html += '</div></div></div>';

        new_element.html(html);
        new_element.removeClass("collapse");
    },    

    display_book_matches : function() {
        $("#response_piece_text").html(app.model.match_text);
        $("#response_piece_search_position").html('Showing simliar match ' + (app.model.cur_match+1) + ' out of ' + app.model.matches.length);
        $("#book_page_text").html('Page ' + app.model.cur_page + ' out of ' + app.model.max_page);

        // create back breadcrumb
        var html = "";

        html += '<div class="col-12 col-md-2 ps-4 hero-thumb"> <figure class="rounded-4">';
        html += '<img src="' + app.model.image_url + '" width=184px height=240px alt="hero-thumb" class="w-100">';
        html += '</figure> </div> <div class="col-12 col-md-10 hero-text">';
        html += '<a href=/book?id=' + app.model.content_info.book_id + ' class="d-flex ms-0 ms-md-4 align-items-center back-link">';
        html += '<img src="/template/static/svgs/back-arrow.svg" alt="">';
        html += '<span class="ps-4 fw-semibold">Back to ' + app.model.title + '</span>';
        html += '</a> </div>'

        $("#back_breadcrumb").html(html);

        // content to display
        var content = "";
        for(var i = 0; i < app.model.text_list.length; i++) {
            var text_obj = app.model.text_list[i];
            if (text_obj.id == app.model.content_info.id) {
                content += '<p class="select_book_text">'
            } else {
                content += '<p>'
            }
            content += text_obj.text;
        }
        $("#book_text").html(content);

        // set next / back search and page buttons
        $('#back_search_btn').removeAttr('onclick');
        $('#back_search_btn').attr('onClick', 'app.model.set_match_index(' + (app.model.cur_match - 1) + ');');
        $('#next_search_btn').removeAttr('onclick');
        $('#next_search_btn').attr('onClick', 'app.model.set_match_index(' + (app.model.cur_match + 1) + ');');
        
        $('#back_page_btn').removeAttr('onclick');
        $('#back_page_btn').attr('onClick', 'app.model.load_page(' + app.model.content_info.book_id + ', ' + (app.model.cur_page - 1) + ');');
        $('#next_page_btn').removeAttr('onclick');
        $('#next_page_btn').attr('onClick', 'app.model.load_page(' + app.model.content_info.book_id + ', ' + (app.model.cur_page + 1) + ');');
    },

    contact_us : function() {
        var email = $('#contact_us_email').val();
        app.log(email);
        var msg = $('#contact_us_msg').val();
        app.log(msg);

        app.model.contact_us(email, msg);

        var html = "<p>Thank you for your message, we will review shortly</p>";
        $("#contact_us_form").html(html);
    }

};

app.model = {
    books : [],
    current_book : null,
    prompts : [],
    current_prompt_id : 1,
    current_parent_prompt_id : -1,
    old_position : 0,
    current_position : 0,
    old_subposition : 0,
    current_subposition : 0,
    response_list : [],
    sub_prompts : [],
    subresponse_list : [],
    test_questions_right : 0,
    test_questions_wrong: 0,

    // load books
    get_books_url : "get_books",
    get_book_content_url : "get_book_content",
    get_subresponse_url : "get_subresponse",
    get_subsubresponse_url : "get_subresponse",
    load_book_matches_url : "load_book_matches",
    load_match_index_url : "load_match_index",
    load_page_url : "load_page",
    get_test_questions_url : "get_test_questions",
    contact_us_url : "contact_us",

    get_books : function() {
        app.log(this.get_books_url);            
        $.getJSON(this.get_books_url, function(json) {
            app.log(json);
            app.model.books = json;
            app.view.display_books();
        });
    },

    load_book : function (book_id) {
        $.getJSON(this.get_book_content_url + "?book_id=" + book_id, function(json) {
            app.log("loaded book for id " + book_id);
            app.log(json);
            app.model.current_book = json.book_info;
            app.model.prompt_response_list = json.prompt_response_list;
            app.view.book_selected();
        });
    },

    // position is how far down the list of content got clicked
    load_subresponse : function (response_piece_id, position) {        
        app.log("load_subresponse response_piece_id " + response_piece_id + " book_id " + app.model.current_book.id);
        $.getJSON(this.get_subresponse_url + "?response_piece_id=" + response_piece_id, function(json) {
            app.log(json);
            app.model.subprompt_response_list = json.subprompt_response_list;
            app.model.old_position = app.model.current_position;
            app.model.current_position = position;
            app.model.response_piece_id = response_piece_id;
            app.view.display_subresponse();
        });
    },

    // position is how far down the list of content got clicked
    load_subsubresponse : function (response_piece_id, position) {        
        app.log("load_subsubresponse response_piece_id " + response_piece_id + " book_id " + app.model.current_book.id);
        $.getJSON(this.get_subsubresponse_url + "?response_piece_id=" + response_piece_id, function(json) {
            app.log(json);
            app.model.subsubprompt_response_list = json.subprompt_response_list;
            app.model.old_subposition = app.model.current_position;
            app.model.current_subposition = position;
            app.model.response_piece_id = response_piece_id;
            app.view.display_subsubresponse();
        });
    },
    
    load_book_matches : function(response_piece_id) {
        app.log("load_text_search id " + response_piece_id)
        $.getJSON(this.load_book_matches_url + "?id=" + response_piece_id, function(json) {
            app.log(json);
            app.model.match_text = json.match_text;
            app.model.content_info = json.content_info;
            app.model.title = json.title;
            app.model.image_url = json.image_url;
            app.model.text_list = json.text_list;
            app.model.matches = json.matches;
            app.model.max_page = json.max_page;
            app.model.cur_page = app.model.content_info.page
            app.model.cur_match = 0
            app.view.display_book_matches();
        });
    },

    set_match_index : function(match_index) {
        app.log("set_search_index id " + match_index)
        if (match_index >= 0 && match_index < app.model.matches.length) {
            $.getJSON(this.load_match_index_url + "?id=" + app.model.matches[match_index], function(json) {
                app.log(json);
                app.model.content_info = json.content_info;
                app.model.text_list = json.text_list;
                app.model.cur_page = app.model.content_info.page
                app.model.cur_match = match_index
                app.view.display_book_matches();
            })
        }
    },

    load_page : function(book_id, page) {
        app.log("load_page book id " + book_id + " page " + page)
        if (page > 0 && page <= app.model.max_page) {
            $.getJSON(this.load_page_url + "?book_id=" + book_id + "&page=" + page, function(json) {
                app.log(json);
                app.model.text_list = json.text_list;
                app.model.cur_page = page
                app.view.display_book_matches();
            })
        }
    },

    load_book_test_questions : function(book_id, response_piece_id) {
        app.log("load_book_test_questions book id " + book_id + " response_piece_id" + response_piece_id)
        $.getJSON(this.get_test_questions_url + "?book_id=" + book_id + "&response_piece_id=" + response_piece_id, function(json) {
            app.log(json);
            app.model.question_list = app.shuffle(json.question_list);
            app.model.current_book = json.book_info;
            app.model.question_number = 0;
            app.view.display_test(null);
        })
    },

    contact_us : function(email, msg) {
        var data = {
            email : email,
            msg : msg
        };

        app.log(data);
        app.log(JSON.stringify(data))
        $.ajax({
            url: this.contact_us_url,
            type: "POST",
            contentType:"application/json; charset=utf-8",
            data: JSON.stringify(data),
            dataType: "json",
        });
    }


};

app.view.init();
