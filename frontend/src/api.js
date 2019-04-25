const API_DOMAIN = "https://penncoursereview.com";
const PUBLIC_API_TOKEN = "public";
var API_TOKEN = "shibboleth";
var authRetryCount = 0;

function api_fetch(url) {
    return fetch(url).then(res => res.json()).then((res) => {
        if (res.error === "Invalid token.") {
            if (window.auth && authRetryCount < 5) {
                authRetryCount += 2;
                window.auth.forceReauth();
            }
        }
        else {
            authRetryCount -= 1;
        }
        return res;
    });
}

export function set_auth_token(token) {
    API_TOKEN = token;
}

export function get_auth_origin() {
    return API_DOMAIN;
}

export function get_auth_url() {
    return API_DOMAIN + "/api/display/token?token=shibboleth&host=" + encodeURIComponent(window.location.href);
}

export function api_autocomplete() {
    return api_fetch(API_DOMAIN + "/api/display/autocomplete?token=" + PUBLIC_API_TOKEN);
}

export function api_live(code) {
    return api_fetch(API_DOMAIN + "/live/" + encodeURIComponent(code));
}

export function api_review_data(type, code) {
    return api_fetch(API_DOMAIN + "/api/display/" + encodeURIComponent(type) + "/" + encodeURIComponent(code) + "?token=" + API_TOKEN);
}

export function api_contact(name) {
    return api_fetch("https://api.pennlabs.org/directory/search?name=" + encodeURIComponent(name)).then((res) => {
        if (res.result_data.length !== 1) {
            return null;
        }
        else {
            return {
                email: res.result_data[0].list_email,
                organization: res.result_data[0].list_organization,
                title: res.result_data[0].list_title_or_major
            };
        }
    });
}

export function api_history(course, instructor) {
    return api_fetch(API_DOMAIN + "/api/display/history/" + encodeURIComponent(course) + "/" + encodeURIComponent(instructor) + "?token=" + API_TOKEN);
}
