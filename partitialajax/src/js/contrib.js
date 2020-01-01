/**
 * Get Information from given cookie (used for csrf)
 * @param name cookieName
 * @returns {null}
 */
export function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Unsued console infom method
 * @param level Level: (all console.* levels)
 * @param info Text message
 */
export function jsconsole(level, info) {
    switch (level.toLowerCase()) {
        case "debug":
        case "log":
            Object.apply(console.log, arguments);
            //console.log(info);
        break;
    }
}

/**
 * Converts camelCase to kebab-case
 * @param string camelCase String
 * @returns {string} converted kebab-case string
 */
export function camelToKebab(string) {
    return string.replace(/([a-z0-9]|(?=[A-Z]))([A-Z])/g, '$1-$2').toLowerCase();
}

/**
 * Converts kebab-case to camelCase string
 * @param string kebab-case-string
 * @returns {String|void|*} new converted camelCaseString
 */
export function kebabToCamel(string){
    return string.replace(/-([a-z])/g, function (g) { return g[1].toUpperCase(); });
}