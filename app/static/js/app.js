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
            html += '<li class="span2"> <a href="/book?id=' + book.id + '"> <div class="thumbnail"> <img src="';
            html += book.image_url;
            html += '" alt=""> <h5>';
            html += book.title;
            html += '</h5> <p></p>'
            html += book.author;
            html += '</p> </div> </a> </li>'
        }
        app.view.$book_list.html(html);
    },

    book_selected : function() {
        var html = "";
        html += '<div class="row">';
        html += '<span class="span3"> <img src="' + app.model.current_book.image_url + '"> </span>';
        html += '<span class="span9"> <h1>' + app.model.current_book.title + '</h1>'; 
        html += '<p>By ' + app.model.current_book.author;
        html += '<p><a class="btn btn-primary" href="' + app.model.current_book.amazon_url + '">Amazon Link</a>';
        html += '</span>';
        html += "</div>"

        html += '<div class="tabbable"> <ul class="nav nav-tabs">';
        for(var i = 0; i < app.model.prompts.length; i++) {
            if (i+1 == app.model.current_prompt_id) {
                html += '<li class="active">';
            } else {
                html += '<li>';
            }
            
            html += '<a data-toggle="tab" onclick="app.model.load_book(' + app.model.current_book.id + ', ' + app.model.prompts[i].id + ')">' + app.model.prompts[i].label + '</a></li>';
        }

        html += '</ul> <div class="tab-content">';

        for(var i = 0; i < app.model.prompts.length; i++) {
            html += '<div class="tab-pane';
            if (i+1 == app.model.current_prompt_id) {
                html += ' active';
            }
            html += '" id="' + i + '">';
            html += '<p id="tab1-' + app.model.prompts[i].name + '">';
            
            if (i+1 == app.model.current_prompt_id) {
                var list = app.model.response_list;
                content_html = "";
                if (app.model.prompts[i].name == "test") {
                    content_html = app.view.create_test_content(list, 1);
                } else {
                    content_html = app.view.create_list_content(list);
                }
                html += content_html;
            }
            html += '</p></div>';
        }
        html += '</div></div>';

        app.view.$book_content.html(html);
    },

    test_click : function(num, answer, level) {
        var list = [];
        if (level == 1) {
            list = app.model.response_list;
        } else if (level == 2) {
            list = app.model.subresponse_list;
        }
        var item =  JSON5.parse(list[num].text);
        var answer_map = {"A)" : 0, "B)" : 1, "C)" : 2, "D)" : 3};
        var click_index = answer_map[answer]
        var correct_index = answer_map[item['answer']]
        var answer_element = $("#test_answer_" + num);
        var click_btn_element = $("#test_btn_" + click_index + "_" + num);
        var correct_btn_element = $("#test_btn_" + correct_index + "_" + num);

        // remove all red button
        for (var i = 0; i < 4; i++) {
            var btn = $("#test_btn_" + i + "_" + num);
            btn.removeClass("btn-danger");
        }

        var answer_html = ""
        if (click_index == correct_index) {
            answer_html += "<p>Correct!";
            click_btn_element.addClass("btn-success")
        } else {
            answer_html += "<p>Wrong!";
            click_btn_element.addClass("btn-danger")
            correct_btn_element.addClass("btn-success")
        }

        if (level == 1) {
            answer_html += '<div class="response-point" onclick="app.model.load_subresponse(' + num + ', 0)">';
            answer_html += item['explanation'];
            answer_html += '</div>'
            answer_html += '<div id="point_' + num + '"></div>';
        } else {
            answer_html += "<p>" + item['explanation'];
        }
        answer_element.html(answer_html);
    },

    create_test_content : function(list, level) {
        var html = "";

        //debugger;

        for(var i = 0; i < list.length; i++) {
            var item =  JSON5.parse(list[i].text);
            html += "<h3>" + (i+1) + ": " + item.question + "</h3>";
            html += "<button id='test_btn_0_" + i + "' class='btn' style='padding: 10px; margin: 10px;' onclick=\"app.view.test_click(" + i + ", 'A)', " + level + ")\">" + item["A)"] + "</button>";
            html += "<button id='test_btn_1_" + i + "' class='btn' style='padding: 10px; margin: 10px;' onclick=\"app.view.test_click(" + i + ", 'B)', " + level + ")\">" + item["B)"] + "</button>";
            html += "<button id='test_btn_2_" + i + "' class='btn' style='padding: 10px; margin: 10px;' onclick=\"app.view.test_click(" + i + ", 'C)', " + level + ")\">" + item["C)"] + "</button>";
            html += "<button id='test_btn_3_" + i + "' class='btn' style='padding: 10px; margin: 10px;' onclick=\"app.view.test_click(" + i + ", 'D)', " + level + ")\">" + item["D)"] + "</button>";
            html += "<div id='test_answer_" + i + "'></div>"
        }
        return html;
    },

    create_list_content : function(list) {
        var html = '';

        for(var i = 0; i < list.length; i++) {
            html += '<div class="response-point" onclick="app.model.load_subresponse(' + i + ', 0)">';
            html += list[i].text;
            html += '</div>'
            html += '<div id="point_' + i + '"></div>';
        }
        return html;
    },

    create_sublist_content : function(list) {
        var html = '';

        for(var i = 0; i < list.length; i++) {
            html += '<div class="response-sub-point">';
            html += '<a href="/text_search?id=' + list[i].id + '">' + list[i].text + '</a>';
            html += '</div>'
            html += '<div id="sub_point_' + i + '"></div>';
        }
        return html;
    },

    display_subresponse : function() {
        // remove old 
        var old_name = "#point_" + app.model.old_position
        var new_name = "#point_" + app.model.current_position
        var old_element = $(old_name);
        var new_element = $(new_name);

        app.log("old_element length " + old_element.length);

        old_element.html("");

        var html = '';
        html += '<div class="tabbable"> <ul class="nav nav-tabs">';
        for(var i = 0; i < app.model.sub_prompts.length; i++) {
            if (app.model.sub_prompts[i].id == app.model.current_parent_prompt_id) {
                html += '<li class="active">';
            } else {
                html += '<li>';
            }
            
            html += '<a data-toggle="tab" onclick="app.model.load_subresponse(' + app.model.current_position + ', ' + i + ')">' + app.model.sub_prompts[i].label + '</a></li>';
        }

        html += '</ul> <div class="tab-content">';

        for(var i = 0; i < app.model.sub_prompts.length; i++) {
            html += '<div class="tab-pane';
            if (app.model.sub_prompts[i].id == app.model.current_parent_prompt_id) {
                html += ' active';
            }
            html += '" id="' + i + '">';
            html += '<p id="sub-tab1-' + app.model.sub_prompts[i].name + '">';
            
            if (app.model.sub_prompts[i].id == app.model.current_parent_prompt_id) {
                var list = app.model.subresponse_list;
                var content_html = "";
                if (app.model.sub_prompts[i].name == "test") {
                    content_html = '<div class="response-sub-point">';
                    content_html += app.view.create_test_content(list, 2);
                    content_html += "</div>"
                } else {
                    content_html = app.view.create_sublist_content(list);
                }
                html += content_html;
            }
            html += '</p></div>';
        }
        html += '</div></div>';

        new_element.html(html);
        app.log("new_element length " + new_element.length);
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
    response_list : [],
    sub_prompts : [],
    subresponse_list : [],

    // load books
    get_books_url : "get_books",
    get_book_content_url : "get_book_content",
    get_subresponse_url : "get_subresponse",

    get_books : function() {
        app.log(this.get_books_url);            
        $.getJSON(this.get_books_url, function(json) {
            app.log(json);
            app.model.books = json;
            app.view.display_books();
        });
    },

    load_book : function (book_id, prompt_id) {
        $.getJSON(this.get_book_content_url + "?book_id=" + book_id + "&prompt_id=" + prompt_id, function(json) {
            app.log("loaded book for id " + book_id);
            app.log(json);
            app.model.current_book = app.find_in_list(app.model.books, "id", book_id);
            app.model.prompts = json.prompt_list;
            app.model.sub_prompts = json.subprompt_list;
            app.model.response_list = json.response_list;
            app.model.subresponse_list = json.subresponse_list;
            app.model.current_prompt_id = prompt_id
            app.view.book_selected();
        });
    },

    // position is how far down the list of content got clicked
    // parent_index is which subprompt is open by default in the result
    load_subresponse : function (position, parent_index) {        
        app.log("load_subresponse position " + position + " parent_index " + parent_index)
        $.getJSON(this.get_subresponse_url + "?book_id=" + app.model.current_book.id + "&prompt_id=" + app.model.current_prompt_id + "&position=" + position + "&parent_index=" + parent_index, function(json) {
            app.log(json);
            app.model.sub_prompts = json.prompt_list;
            app.model.subresponse_list = json.response_list;
            app.model.old_position = app.model.current_position;
            app.model.current_position = position;
            app.model.current_parent_prompt_id = json.active_prompt_id;
            app.view.display_subresponse();
        });
    },

    load_text_search : function(response_piece_id) {

        
    }

};

app.view.init();
app.model.get_books();
