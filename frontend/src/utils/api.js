const API_DOMAIN = `${window.location.protocol}//${window.location.host}`
const PUBLIC_API_TOKEN = 'public'
const API_TOKEN = 'platform'

function apiFetch(url) {
  return fetch(url).then(res => res.json())
}

export function redirectForAuth() {
  window.location.href = `${API_DOMAIN}/accounts/login/?next=${encodeURIComponent(
    window.location.href
  )}`
}

export function getLogoutUrl() {
  return `${API_DOMAIN}/accounts/logout/?next=${encodeURIComponent(
    `${window.location.origin}/logout`
  )}`
}

export function apiAutocomplete() {
  return apiFetch(
    `${API_DOMAIN}/api/display/autocomplete?token=${encodeURIComponent(
      PUBLIC_API_TOKEN
    )}`
  )
}

export function apiIsAuthenticated(func) {
  apiFetch(
    `${API_DOMAIN}/api/display/auth?token=${encodeURIComponent(
      PUBLIC_API_TOKEN
    )}`
  ).then(data => {
    if (typeof data.authed === 'undefined') {
      window.Raven.captureMessage(`Auth check error: ${JSON.stringify(data)}`, {
        level: 'error',
      })
    }
    func(data.authed)
  })
}

export function apiLive(code) {
  return apiFetch(
    `${API_DOMAIN}/api/display/live/${encodeURIComponent(
      code
    )}?token=${encodeURIComponent(PUBLIC_API_TOKEN)}`
  )
}

export function apiLiveInstructor(name) {
  return apiFetch(
    `https://api.pennlabs.org/registrar/search/instructor?q=${encodeURIComponent(
      name
    )}`
  )
}

export function apiReviewData(type, code) {
  return apiFetch(
    `${API_DOMAIN}/api/display/${encodeURIComponent(type)}/${encodeURIComponent(
      code
    )}?token=${encodeURIComponent(API_TOKEN)}`
  )
}

export function apiContact(name) {
  return apiFetch(
    `https://api.pennlabs.org/directory/search?name=${encodeURIComponent(name)}`
  ).then(res => {
    if (res.result_data.length !== 1) {
      return null
    }

    return {
      email: res.result_data[0].list_email,
      organization: res.result_data[0].list_organization,
      title: res.result_data[0].list_title_or_major,
    }
  })
}

export function apiHistory(course, instructor) {
  return apiFetch(
    `${API_DOMAIN}/api/display/history/${encodeURIComponent(
      course
    )}/${encodeURIComponent(instructor)}?token=${encodeURIComponent(API_TOKEN)}`
  )
}
