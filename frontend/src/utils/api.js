// src/utils/api.js

const baseURL = "http://localhost:5000/api";

const api = {
  async request(endpoint, options = {}) {
    const path = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
    const url = `${baseURL.replace(/\/$/, "")}${path}`;

    const token = localStorage.getItem("access_token");

    const headers = {
      ...options.headers,
    };

    // Only set Content-Type for JSON requests
    if (!(options.body instanceof FormData)) {
      headers["Content-Type"] = "application/json";
    }

    if (token) {
      headers["Authentication-Token"] = token;
    }

    const config = {
      ...options,
      headers,
    };

    try {
      const response = await fetch(url, config);

      if (response.status === 401) {
        alert("Please login first");
        throw new Error("Unauthorized");
      }

      if (!response.ok) {
        let bodyText = "";

        try {
          bodyText = await response.text();
        } catch (e) {}

        const err = new Error(
          bodyText
            ? `${response.status} - ${bodyText}`
            : `HTTP Error ${response.status}`
        );

        err.status = response.status;
        throw err;
      }

      if (response.status === 204) return null;

      const text = await response.text();

      if (!text) return null;

      try {
        return JSON.parse(text);
      } catch {
        return text;
      }
    } catch (err) {
      return Promise.reject(err);
    }
  },

  get(endpoint, options = {}) {
    return this.request(endpoint, {
      ...options,
      method: "GET",
    });
  },

  post(endpoint, data, options = {}) {
    return this.request(endpoint, {
      ...options,
      method: "POST",
      body: data instanceof FormData ? data : JSON.stringify(data),
    });
  },

  put(endpoint, data, options = {}) {
    return this.request(endpoint, {
      ...options,
      method: "PUT",
      body: data instanceof FormData ? data : JSON.stringify(data),
    });
  },

  patch(endpoint, data, options = {}) {
    return this.request(endpoint, {
      ...options,
      method: "PATCH",
      body: data instanceof FormData ? data : JSON.stringify(data),
    });
  },

  delete(endpoint, options = {}) {
    return this.request(endpoint, {
      ...options,
      method: "DELETE",
    });
  },
};

export default api;