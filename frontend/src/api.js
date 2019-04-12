const API_DOMAIN = "http://localhost:8000";

export function api_autocomplete() {
    return fetch(API_DOMAIN + "/api/display/autocomplete?token=public").then(res => res.json());
}

export function api_live(code) {
    return fetch(API_DOMAIN + "/live/" + encodeURIComponent(code)).then(res => res.json());
}

export function api_review_data(type, code) {
    return fetch(API_DOMAIN + "/api/display/" + encodeURIComponent(type) + "/" + encodeURIComponent(code) + "?token=public").then(res => res.json());
}
