const API_DOMAIN = window.location.protocol + "//" + window.location.host;
const PUBLIC_API_TOKEN = "public";
var API_TOKEN = "platform";

function api_fetch(url) {
    return fetch(url).then(res => res.json());
}

export function redirect_for_auth() {
    window.location.href = API_DOMAIN + "/accounts/login/?next=" + encodeURIComponent(window.location.href);
}

export function get_logout_url() {
    return API_DOMAIN + "/accounts/logout/?next=" + encodeURIComponent(window.location.origin + "/logout");
}

export function redirect_for_logout() {
    window.location.href = get_logout_url();
}

export function api_autocomplete() {
    return api_fetch(API_DOMAIN + "/api/display/autocomplete?token=" + encodeURIComponent(PUBLIC_API_TOKEN));
}

export function api_is_authenticated(func) {
    api_fetch(API_DOMAIN + "/api/display/auth?token=" + encodeURIComponent(PUBLIC_API_TOKEN)).then((data) => {
        func(data.authed);
    });
}

export function api_live(code) {
    return api_fetch(API_DOMAIN + "/api/display/live/" + encodeURIComponent(code) + "?token=" + encodeURIComponent(PUBLIC_API_TOKEN));
}

export function api_live_instructor(name) {
    return api_fetch("https://api.pennlabs.org/registrar/search/instructor?q=" + encodeURIComponent(name));
}

export function api_review_data(type, code) {
    return api_fetch(API_DOMAIN + "/api/display/" + encodeURIComponent(type) + "/" + encodeURIComponent(code) + "?token=" + encodeURIComponent(API_TOKEN));
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
    return api_fetch(API_DOMAIN + "/api/display/history/" + encodeURIComponent(course) + "/" + encodeURIComponent(instructor) + "?token=" + encodeURIComponent(API_TOKEN));
}
