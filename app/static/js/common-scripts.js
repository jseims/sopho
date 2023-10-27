
(function($){
	$(function(){



        // Phone nav click function

        $('.navbar-toggler').click(function () {
            $("body").toggleClass("navShown");
            $(".nav-wrap").fadeToggle()
        });


        $(".header-search-icon").on("click", function() {
            $(".header-search").toggleClass("searchShown");
        });
          
		
	})// End ready function.
   
})(jQuery)



