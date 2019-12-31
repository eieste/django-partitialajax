import settings from "./setting";
import { camelToKebab, kebabToCamel } from "./contrib";
import PartitialAjax from "./PartitialAjax";

export function extractConfigFromElement(element){

    let opt = {};
    Object.keys(settings.options).forEach(function (key) {
        let kebab = camelToKebab(key);
        let new_val = element.getAttribute("data-"+ (settings.configs.dataAttributePrefix ? settings.configs.dataAttributePrefix+"-" : "")+kebab);

        if(new_val){
            opt[key] = new_val
        }
    });
    return opt;
}

export function elementBinding(element){
    let element_list = [];

    let selector_list = [];
    let partitial_attr_prefix = "[data-toggle=modal][data-target][data-"+settings.configs.dataAttributePrefix+"-";

    Object.keys(settings.options).forEach(function (key) {
        selector_list.push(partitial_attr_prefix+camelToKebab(key)+"]")
    });

    let parent = document;
    if(element !== undefined){
        parent = element;
    }

    element_list = Array.from(parent.querySelectorAll(selector_list.join(", ")+", [data-"+ (settings.configs.dataAttributePrefix ? settings.configs.dataAttributePrefix+"-" : "")+"activate=true]"));
    element_list.forEach(function(elem){
        let opt = extractConfigFromElement(elem);
        opt["element"] = elem;

        if(elem.hasAttribute("data-toggle") && elem.hasAttribute("data-target")){
            opt["element"] = document.querySelector(elem.getAttribute("data-target"));
            opt["trigger_element"] = elem;
            opt["directLoad"] = false;
            let part = new PartitialAjax(opt);

            elem.addEventListener("click", function(){
                part.getFromRemote();
            });
        }else{
            new PartitialAjax(opt);
        }

    });
}