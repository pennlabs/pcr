const API_DOMAIN = "https://penncoursereview.com";
const PUBLIC_API_TOKEN = "public";
var API_TOKEN = "shibboleth";

function api_fetch(url) {
    return new Promise((resolve, reject) => {
        fetch(url).then(res => res.json()).then((res) => {
            if (res.error === "Invalid token.") {
                if (window.auth) {
                    window.auth.forceReauth().then(() => resolve(api_fetch(url)));
                }
            }
            resolve(res);
        }).catch((e) => reject(e));
    });
}

export function set_auth_token(token) {
    API_TOKEN = token;
}

export function redirect_for_auth() {
    window.location.href = API_DOMAIN + "/api/display/token?token=shibboleth&redirect=" + encodeURIComponent(window.location.href);
}

export function api_autocomplete() {
    return api_fetch(API_DOMAIN + "/api/display/autocomplete?token=" + encodeURIComponent(PUBLIC_API_TOKEN));
}

export function api_live(code) {
    return api_fetch(API_DOMAIN + "/live/" + encodeURIComponent(code));
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
