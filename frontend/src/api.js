const API_DOMAIN = "http://localhost:8000";
const API_TOKEN = "public";

export function api_autocomplete() {
    return fetch(API_DOMAIN + "/api/display/autocomplete?token=" + API_TOKEN).then(res => res.json());
}

export function api_live(code) {
    return fetch(API_DOMAIN + "/live/" + encodeURIComponent(code)).then(res => res.json());
}

export function api_review_data(type, code) {
    return fetch(API_DOMAIN + "/api/display/" + encodeURIComponent(type) + "/" + encodeURIComponent(code) + "?token=" + API_TOKEN).then(res => res.json());
}

export function api_contact(name) {
    return fetch("https://api.pennlabs.org/directory/search?name=" + encodeURIComponent(name)).then(res => res.json()).then((res) => {
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
    return fetch(API_DOMAIN + "/api/display/history/" + encodeURIComponent(course) + "/" + encodeURIComponent(instructor) + "?token=" + API_TOKEN).then(res => res.json());
}
