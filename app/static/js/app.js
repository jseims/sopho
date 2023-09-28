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
            html += '<li class="span2"> <div class="thumbnail" onclick="app.model.load_book(' + book.id + ', 1)"> <img src="';
            html += book.image_url;
            html += '" alt=""> <h5>';
            html += book.title;
            html += '</h5> <p></p>'
            html += book.author;
            html += '</p> </div> </li>'
        }
        app.view.$book_list.html(html);
    },

    book_selected : function() {
        var html = "";
        html += "<p>" + app.model.current_book.title;

        html += '<div class="tabbable"> <ul class="nav nav-tabs">';
        for(var i = 0; i < app.model.prompts.length; i++) {
            if (i+1 == app.model.current_prompt_id) {
                html += '<li class="active">';
            } else {
                html += '<li>';
            }
            
            html += '<a href="#' + i + '" data-toggle="tab" onclick="app.model.load_book(' + app.model.current_book.id + ', ' + app.model.prompts[i].id + ')">' + app.model.prompts[i].label + '</a></li>';
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
                list = app.model.response_list;
                content_html = "";
                if (app.model.prompts[i].name == "test") {
                    content_html = app.view.create_test_content(list);
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

    create_test_content : function(list) {
        return "<p>Test!</p>";
    },

    create_list_content : function(list) {
        var html = '';

        for(var i = 0; i < list.length; i++) {
            html += '<div class="response-point" onclick="app.model.load_subresponse(' + i + ', 0)">';
            html += list[i];
            html += '</div>'
            html += '<div id="point_' + i + '"></div>';
        }
        return html;
    },

    display_subresponse : function() {
        // remove old 
        var old_name = "#point_" + app.model.old_position
        var new_name = "#point_" + app.model.current_position
        var old_element = $(old_name);
        var new_element = $(new_name);

        old_element.html("");

        var html = '';
        html += '<div class="tabbable"> <ul class="nav nav-tabs">';
        for(var i = 0; i < app.model.sub_prompts.length; i++) {
            if (app.model.sub_prompts[i].id == app.model.current_parent_prompt_id) {
                html += '<li class="active">';
            } else {
                html += '<li>';
            }
            
            html += '<a href="#' + i + '" data-toggle="tab" onclick="app.model.load_subresponse(' + app.model.current_position + ', ' + i + ')">' + app.model.sub_prompts[i].label + '</a></li>';
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
                html += app.model.subresponse_text;
            }
            html += '</p></div>';
        }
        html += '</div></div>';

        new_element.html(html);
    }

};

app.model = {
    books : [],
    current_book : null,
    prompts : [],
    current_prompt_id : 1,
    current_parent_prompt_id : 1,
    old_position : 0,
    current_position : 0,
    response_list : [],
    sub_prompts : [],
    subresponse_text : "",

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
            app.log(json);
            app.model.current_book = app.find_in_list(app.model.books, "id", book_id);
            app.model.prompts = json.prompt_list;
            app.model.response_list = json.response_list;
            app.model.current_prompt_id = prompt_id
            app.view.book_selected();
        });
    },

    load_subresponse : function (position, parent_index) {
        app.log("load_subresponse position " + position + " parent_index " + parent_index)
        $.getJSON(this.get_subresponse_url + "?book_id=" + app.model.current_book.id + "&prompt_id=" + app.model.current_prompt_id + "&position=" + position + "&parent_index=" + parent_index, function(json) {
            app.log(json);
            app.model.sub_prompts = json.prompt_list;
            app.model.subresponse_text = json.response_list;
            app.model.old_position = app.model.current_position;
            app.model.current_position = position;
            app.model.current_parent_prompt_id = json.active_prompt_id;
            app.view.display_subresponse();
        });
    }


};

app.view.init();
app.model.get_books();
