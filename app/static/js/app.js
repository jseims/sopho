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

app.mobile = navigator.userAgent.match(/(iPhone|iPod|iPad|Android|BlackBerry)/) != null;

app.model = {
    books : [],

    // load books
    book_url : "get_books",

    get_books : function() {
        app.log(this.book_url);            
        $.getJSON(this.book_url, function(json) {
            app.log(json);
        });
    }
}


app.model.get_books();