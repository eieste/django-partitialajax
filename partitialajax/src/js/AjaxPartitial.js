import $ from "jquery";

let prefix = "partitial-";
let default_class = ".ajaxpartitial-container";

let defaults = {
    ajax: {
        reregister: true
    }
};


function load_parameter(elem, name, defaultvalue="", decode=false){
    /**
     * Load Parameters
     * @type {jQuery}
     */
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

class AjaxPartitial{
    /**
     * Manage all AjaxPartitials
     * @param elem jQuery Element of Partitial Area
     */

    constructor(elem) {
        let self = this;
        self.info = {
            elements: {
                self: $(elem),
                reload: $(elem).data(prefix+"reload")
            },
            parameters: {
                url: load_parameter(elem, "url", ""),
                selectorstring: load_parameter(elem, "selectorstring", "", true),
                allowed_elements: $.map(load_parameter(elem, "allowed-elements", "").split(","), $.trim)
            }
        };
    }

    /**
     * General Global Initialize of all Partitials
     */
    static init(){
        $(default_class).each(function(){
            let elem = $(this);
            let partitial = new AjaxPartitial(elem);
            partitial.init();
            $(elem).data("partitial", partitial);
        });
    }

    /**
     * Initialize of one Specific Partitial (Called from constructor)
     */
    init(){
        let self = this;
        if(self.info.elements.reload){
            self.registerReloadButton();
        }
    };

    /**
     * If reload button is defined; Initialize Click events here
     */
    registerReloadButton(){
        let self = this;
        $(self.info.elements.reload).on("click", function(){
            $.getJSON(self.info.parameters.url, function (data) {
                $.each(data.content, function(selector, template){
                    if(selector in self.info.parameters.allowed_elements || "all" in self.info.parameters.allowed_elements){
                        $(selector).html(data.content[selectorstring]);
                    }else if(selector === self.info.parameters.selectorstring){
                        $(self.info.elements.self).html(data.content[self.info.parameters.selectorstring]);
                    }
                });
                let options = $.extend({}, defaults.ajax, data.options);
                console.log(options);
                if(options.reregister){
                    self.registerReloadButton();
                }
            });
        });
    };



}

export default AjaxPartitial;