import $ from "jquery";


function load_parameter(elem, name, defaultvalue="", decode=false){
    let val = $(elem).data(prefix+""+name);
    if(val){
        if(decode){
            return atob(val);
        }else{
            return val;
        }
    }else{
        return defaultvalue;
    }
}



$(default_class).each(function(){
    let elem = $(this);
    let partitial = new AjaxPartitial(elem);
    partitial.init();
    $(elem).data("partitial", partitial);
});

