interface IOAuth {
    ENABLED: boolean,
    CLIENT_ID: string,
    STRATEGY: string,
};

export const OAUTH_GITHUB: IOAuth = {
    ENABLED: true,
    CLIENT_ID: "54e24d68a1ecc051a70a",
    STRATEGY: "GITHUB",
};

export const API_URL: string = "http://localhost:5000/api"
//example: "http://localhost:5000/api" or "https://example-domain.com/api"

export const GOOGLE_ANALYTICS_ID: string = "UA-12345678-1";