import {getCookie, jsconsole} from "./contrib";
import settings from "./setting";
import {elementBinding, extractConfigFromElement} from "./bindings";


var csrftoken = getCookie("csrftoken");
const partitial_ajax_list = [];

function withDefault(defaultDict, data){
    let opt = Object.assign({}, defaultDict);
    return Object.assign(opt, data);
}


/** Class representing a point. */
export default class PartitialAjax {

    /**
     * @typedef {Object} PartitialAjax
     * @param options dict with configuration options for each seperate Partitial. See: :ref:`partitial-ajax-options`
     * @param event dict with function bindings for hooks. See :ref:`partitial-ajax-events`
     */
    constructor(options, event) {
        let self = this;
        self.intervalFlag = undefined;
        self.event = event || {};

        // Add this Partitial to constant list
        partitial_ajax_list.push({
            element: options.trigger_element || options.element,
            partitialAjax: self
        });

        // Test if options is only a Element
        // (the remaining configuration will be loaed from this element)
        if(options instanceof Element){
            self.options = {
                "element": options
            };
        }else{
            // if options is the options object merge userconfiguration with defaults
            self.options = withDefault(settings.options, options);
        }

        // if allowed use element to get configuration
        if(self.options.configFromElement){
            let elem = self.options.trigger_element || self.options.element;
            self.options = withDefault(self.options, extractConfigFromElement(elem))
        }

        // Trigger directly a initial request to fill this partitial
        if(self.options.directLoad){
            self.getFromRemote();
        }

        // If interval is configured setup the refresh interval (if interval is smaller than 100 the config will be ignored
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
        // Trigger afterSetup event
        self.callEvent("afterSetup", self);
    }

    /**
     * Find a Partitial by the given element argument (used paritial_ajax_list to find it)
     * @return {boolean|PartitialAjax} Return the PartitialAjax object if found or return false
     */
    static getPartitialFromElement(element){
        let result = false;
        partitial_ajax_list.forEach(function(item){
            if(item.element === element){
                result = item.partitialAjax;
            }
        });
        return result;
    }

    delete(){
        let self = this;
        const index = partitial_ajax_list.indexOf(self);
        if (index > -1) {
            partitial_ajax_list.splice(index, 1);
        }
    }

    /**
     * Run autoconfiguration; This method find all elements with data-partitial configuration attributes and setups partitils by the given attributes
     */
    static initialize(){
        elementBinding();
    }

    /**
     * Load Partitial from remote Source
     */
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
                self.callEvent("onRemoteError", {"response": response});
            }
        }).then(function(response) {
            return response.json();
        }).then(function(data) {
            self.callEvent("onRemoteData");

            // If allowed by settings allow remote configuration
            if(!self.options.restrictRemoteConfiguration){
                self.handleOptions(data);
            }

            // Handle Text Informations
            if(data.hasOwnProperty("text")){
                self.handleTextData(data);
            }

            // Handle Partitial Information
            if(data.hasOwnProperty("content")){
                self.handlePartitialData(data);
            }
            self.callEvent("onHandeldRemoteData", {"remoteData": data});

        }).catch(function(ex) {
            self.callEvent("onResponseError", {"exception": ex});
        });
    }

    /**
     * Reconfigure current ParitialAjax object with the remote Option information
     * @param data Parsed remote json Response
     */
    handleOptions(data){

        if("option" in data){
            self.remoteOption = Object.assign(data.option, settings.remote);
        }
        // ToDo Update Behavior of current PartitialAjax
    }

    /**
     *
     * Handle Partitial Data
     * @param data Parsed remote json Response
     */
    handlePartitialData(data){
        let self = this;
        // Itterate over each content selecotr
        Object.keys(data.content).forEach(function(selector){
            let content = data.content[selector];
            let parent_element = null;
            // If PartitialAjax options element is the same as remote selector; replace content directly
            if(self.options.element == document.querySelectorAll(selector)[0]){
                self._replaceContent(self.options.element, content);
                return;
            }else if(self.options.onlyChildReplace) {
                // if "onlyChildReplace" is activated, make sure that all selectors are a child element of the PartitialAjax element
                parent_element = self.options.element;
            }else{
                // Allow to replace each element with the same selector
                parent_element = document;
            }

            let parts = parent_element.querySelectorAll(selector);
            parts.forEach(function(key){
                self._replaceContent(key, content);
            });
        });
    }

    /**
     * Private Method; Replace content by given element
     * @param element Element which content should be replaced
     * @param content New content for element
     * @private
     */
    _replaceContent(element, content){
        let self = this;
        // Check if selector which should be replaced is allowed by allowedElements option
        let allowed_elements_selector_list = document.querySelectorAll(self.options.allowedElements.split(","));
        let allowed_elements_list = [];

        //If allowedElement Options is set replace only valid elements
        allowed_elements_selector_list.forEach(function(key){
            let element_list = document.querySelectorAll(allowed_elements_selector_list[key]);
            allowed_elements_list = [...allowed_elements_list, ...element_list]

        });

        allowed_elements_list.forEach(function(key){
            let elem = allowed_elements_list[key];

            if(elem == element){
                let result = self.callEvent("onReplaceContent", {"element": element, "content": content});
                if(result == undefined){
                    element.innerHTML = content;
                }else{
                    result.element.innerHTML = result.content;
                }
            }
        });

        // allow each defined element
        if(self.options.allowedElements == "all"){
            let result = self.callEvent("onReplaceContent", {"element": element, "content": content});

            if(result == undefined){
                element.innerHTML = content;
            }else{
                result.element.innerHTML = result.content;
            }
        }
    }

    /**
     * Trigger textEventCallback method for each transmited text key:value pair
     * @param data Remote json Response Data
     */

    handleTextData(data){
        // Handle Text Only Information
        Object.keys(data.text).forEach(function(key){
            let method = eval(self.options.textEventCallback);
            method(key, data.text[key]);
            //eval(self.options.textEventCallback+"('"+key+"','"+data.text[key]+"')")
        });
    }

    /**
     * Register/Overwrite a new Hook on a created PartitialAjax Object
     * @param eventname Name ov event/hook See: :ref:`partitial-ajax-events`
     * @param callback Function which should be triggerd
     */
    register(eventname, callback){
        let self = this;
        self.event[eventname] = callback;
    }

    /**
     * executing the stored funktino when the hook is reached
     * @param eventname
     * @param data argument that is passed into the hook method
     */
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
