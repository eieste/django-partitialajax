export default {
    configs: {
        dataAttributePrefix: "partitial",
    },
    options: {
        url: "",
        element: null,
        onlyChildReplace: true,
        interval: -1,
        allowedElements: "all",
        textEventCallback: "console.info",
        restrictRemoteConfiguration: true,
        configFromElement: true,
        directLoad: true
    },
    remote: {
        reRegister: true,
        timeout: false,
    }
}