$(document).ready(function() {
    var max_fields      = 8;
    var wrapper         = $(".add-inp");
    var add_button      = $(".add_form_field");
 
    var x = 1;
    $(add_button).click(function(e){
        e.preventDefault();
        if(x < max_fields){
            x++;
            $(wrapper).append('<div><input type="textarea" class="form-control mb-2"name="username" autofocus="" autocapitalize="none" autocomplete="username" required="" id="id_question"><a href="#" class="delete text-dark">Delete</a></div>'); //add input box
        }
  else
  {
  alert('You Reached the limits')
  }
    });
 
    $(wrapper).on("click",".delete", function(e){
        e.preventDefault(); $(this).parent('div').remove(); x--;
    })
});