/**
 * Utility functions.
 */
AUMed.Util = {
    template: function(template, data) {
        template = $.trim(template);
        return template.replace(/%(\w*)%/g, function (m, key) {
            return data.hasOwnProperty(key) ? data[key] : "";
        });
    },
    api: function(params) {
        $.ajax({
            url: window.location.origin + "/api/" + params.url,
            type: params.type ? params.type : "GET",
            data: params.data ? JSON.stringify(params.data) : "",
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: params.callback,
            error: function(jqXHR, text, error) {
                params.callback({
                    error: text + " " + error,
                });
                console.log(text + " " + error);
            },
        });
    },
    isDoctor: function() {
        return localStorage.getItem("user_type") == "doctor"
    },
    toggleUserType: function() {
        if (localStorage.getItem('user_type') == "doctor") {
            localStorage.setItem('user_type', "patient");
            
        } else {
            localStorage.setItem('user_type', "doctor");
        }
        location.reload();
    },
    capitalize: function(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    },
    getFormattedDate(date) {
        return date.getMonth()+1 + "/" + date.getDate() + "/" + date.getFullYear();
    }
};