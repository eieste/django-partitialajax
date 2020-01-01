import {getCookie, jsconsole} from "./contrib";
import settings from "./setting";
import {elementBinding, extractConfigFromElement} from "./bindings";


var csrftoken = getCookie("csrftoken");
const partitial_ajax_list = [];

function withDefault(defaultDict, data){
    let opt = Object.assign({}, defaultDict);
    return Object.assign(opt, data);
}


export default class PartitialAjax {
    /**
     * Foobar
    */
    constructor(options, event) {
        let self = this;
        self.intervalFlag = undefined;
        self.event = event || {};

        let search_info = {
            element: options.trigger_element || options.element,
            partitialAjax: self
        };
        partitial_ajax_list.push(search_info);

        if(options instanceof Element){
            self.options = {
                "element": options
            };
        }else{
            self.options = withDefault(settings.options, options);
        }


        // if allowed use element to get configuration
        if(self.options.configFromElement){
            let elem = self.options.trigger_element || self.options.element;
            self.options = withDefault(self.options, extractConfigFromElement(elem))
        }

        if(self.options.directLoad){
            self.getFromRemote();
        }

        try{
            let interval = parseInt(self.options.interval);
            if(interval > 100){
                self.intervalFlag = window.setInterval(function(){
                    self.getFromRemote()
                }, interval);
            }
        }catch(e){
            jsconsole("DEBUG", e);
        }

        self.callEvent("afterSetup", self);
    }

    static getPartitialFromElement(element){
        let result = false;
        partitial_ajax_list.forEach(function(item){
            if(item.element === element){
                result = item.partitialAjax;
            }
        });
        return result;
    }

    static initialize(){
        elementBinding();
    }

    getFromRemote(){
        let self = this;

        fetch(self.options.url+"?is-ajax", {
            method: 'GET',
            mode: 'cors',
            redirect: 'follow',
            headers: new Headers({ 'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': csrftoken})
        }).then(function(response){
            if (response.status >= 200 && response.status < 300) {
                return response
            } else {
                var error = new Error(response.statusText);
                error.response = response;
                throw error
            }
        }).then(function(response) {
            return response.json();
        }).then(function(data) {
            self.callEvent("onRemoteData");
            if(!self.options.restrictRemoteConfiguration){
                self.handleOptions(data);
            }
            if(data.hasOwnProperty("text")){
                self.handleTextData(data);
            }

            if(data.hasOwnProperty("content")){
                self.handlePartitialData(data);
            }
            self.callEvent("onHandeldRemoteData", {"remoteData": data});

        }).catch(function(ex) {
            console.log('parsing failed', ex)
        });
    }

    handleOptions(data){

        self.remoteOption = Object.assign(data.option, settings.remote);


    }

    handlePartitialData(data){
        let self = this;
        Object.keys(data.content).forEach(function(selector){
            let content = data.content[selector];

            if(self.options.element == document.querySelectorAll(selector)[0]){
                self._replaceContent(self.options.element, content);
            }else if(self.options.onlyChildReplace) {

                let parts = self.options.element.querySelectorAll(selector);
                for(let i = 0; i < parts.length; i++){
                    self._replaceContent(parts[i], content);
                }
            }else{
                let parts = document.querySelectorAll(selector);
                for(let i = 0; i < parts.length; i++){
                    self._replaceContent(parts[i], content);
                }
            }
        });
    }

    _replaceContent(element, content){
        let self = this;
        let allowed_elements_selector_list = document.querySelectorAll(self.options.allowedElements.split(","));
        let allowed_elements_list = [];

        for(let i = 0; i <= allowed_elements_selector_list.length; i++){
            let element_list = document.querySelectorAll(allowed_elements_selector_list[i]);
            allowed_elements_list = [...allowed_elements_list, ...element_list]
        }

        for(let i = 0; i <= allowed_elements_list.length;i++){
            let elem = allowed_elements_list[i];

            if(elem == element){
                let result = self.callEvent("onReplaceContent", {"element": element, "content": content});
                if(result == undefined){
                    element.innerHTML = content;
                }else{
                    result.element.innerHTML = result.content;
                }
            }
        }

        if(self.options.allowedElements == "all"){
            let result = self.callEvent("onReplaceContent", {"element": element, "content": content});

            if(result == undefined){
                element.innerHTML = content;
            }else{
                result.element.innerHTML = result.content;
            }
        }
    }

    handleTextData(data){
        // Handle Text Only Information
        Object.keys(data.text).forEach(function(key){
            let method = eval(self.options.textEventCallback);
            method(key, data.text[key]);
            //eval(self.options.textEventCallback+"('"+key+"','"+data.text[key]+"')")
        });
    }

    register(eventname, callback){
        let self = this;
        self.event[eventname] = callback;
    }

    callEvent(eventname, data){
        let self = this;
        Object.keys(self.event).forEach(function(key){
            if(eventname == key){
                let method = self.event[key];
                data["partitial_ajax"] = self;
                return method(data);
            }
        });
    }

}
