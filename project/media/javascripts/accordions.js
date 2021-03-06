oer.accordion = {};

oer.accordion.init = function($accordion) {

  $accordion.data("animated", false);

  var $headers = $accordion.find(".accordion-header");

  function open_section($header) {
    if ($accordion.data("animated")) {
      return;
    }
    if ($header.data("expanded")) {
      return;
    }
    $headers.each(function() {
      var $this = $(this);
      if ($this.data("expanded")) {
        $this.data("expanded", false);
        $this.data("$handler").removeClass("expanded");
        $this.data("$body").slideUp(200);
      }
    });
    $header.data("expanded", true);
    $header.data("$handler").addClass("expanded");
    $accordion.data("animated", true);
    $header.data("$body").slideDown(200, function() {
      $accordion.data("animated", false);
    });
  }

  $headers.each(function() {
    var $header = $(this);
    var $handler = $header.find("a");
    $header.data("expanded", false);
    $header.data("$handler", $handler);
    $header.data("$body", $header.next(".accordion-body"));
    $handler.mouseover(function() {
      open_section($header);
    });
    $handler.click(function(e) {
      var $this = $(this);
      if ($this.attr("href") === "#") {
        e.preventDefault();
        open_section($header);
      }
    });
  });
};
