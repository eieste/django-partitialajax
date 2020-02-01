/**
 * Default settings
 * @type setting
 */
export default {
    configs: {
        dataAttributePrefix: "partitial",
    },
    options: {
        /**
         * Remote Partitial URL
         */
        url: "",
        /**
         * General Partitial Element
         */
        element: null,
        /**
         * Allow only replace of elements which are a child of options.element (above parameter)
         */
        onlyChildReplace: true,
        /**
         * Automatic Refresh interval
         */
        interval: -1,
        /**
         * Comma seperated list of all selectors which are allowed to replaced
         */
        allowedElements: "all",
        /**
         * Method which should be called for each text key:value pair (usefull for toast.js or other user notification libarys)
         */
        textEventCallback: "console.info",
        /**
         * Ignore Option parameters which are recived from remote Endpoint
         */
        restrictRemoteConfiguration: true,
        /**
         * Ignore data-partitial attributes from main element (parameter above (options.element)
         */
        configFromElement: true,
        /**
         * Load data directly on initialization
         */
        directLoad: true,

        self: ""
    },
    remote: {
        reRegister: true,
        timeout: false,
    }
}