"use strict";

const loginForm = document.getElementById("login-form");
const endpointInput = document.getElementById("project-endpoint");
const endpointError = document.getElementById("endpoint-error");
const microsoftLoginButton = document.getElementById(
    "microsoft-login-button"
);
const loginNotice = document.getElementById("login-notice");

function validateProjectEndpoint(value) {
    const trimmedValue = value.trim();

    if (!trimmedValue) {
        return {
            valid: false,
            message: "Enter an Azure Foundry project endpoint."
        };
    }

    let endpoint;

    try {
        endpoint = new URL(trimmedValue);
    } catch (error) {
        return {
            valid: false,
            message: "Enter a valid HTTPS URL."
        };
    }

    if (endpoint.protocol !== "https:") {
        return {
            valid: false,
            message: "The endpoint must use HTTPS."
        };
    }

    if (!endpoint.hostname.endsWith(".services.ai.azure.com")) {
        return {
            valid: false,
            message:
                "The endpoint must use an approved " +
                "services.ai.azure.com host."
        };
    }

    if (!endpoint.pathname.startsWith("/api/projects/")) {
        return {
            valid: false,
            message:
                "The endpoint path must start with /api/projects/."
        };
    }

    if (
        endpoint.username ||
        endpoint.password ||
        endpoint.search ||
        endpoint.hash
    ) {
        return {
            valid: false,
            message:
                "Credentials, query parameters, and fragments " +
                "are not allowed."
        };
    }

    const projectName = endpoint.pathname
        .slice("/api/projects/".length)
        .replaceAll("/", "")
        .trim();

    if (!projectName) {
        return {
            valid: false,
            message: "The endpoint must contain a project name."
        };
    }

    return {
        valid: true,
        normalizedEndpoint:
            endpoint.origin +
            endpoint.pathname.replace(/\/+$/, "")
    };
}

function showEndpointError(message) {
    endpointInput.setAttribute("aria-invalid", "true");
    endpointError.textContent = message;
}

function clearEndpointError() {
    endpointInput.removeAttribute("aria-invalid");
    endpointError.textContent = "";
}

endpointInput.addEventListener("input", function handleInput() {
    clearEndpointError();

    loginNotice.className = "login-notice";
    loginNotice.textContent =
        "Microsoft Entra authentication will be connected " +
        "in the next implementation stage.";
});

loginForm.addEventListener("submit", function handleSubmit(event) {
    event.preventDefault();

    const result = validateProjectEndpoint(endpointInput.value);

    if (!result.valid) {
        showEndpointError(result.message);
        endpointInput.focus();
        return;
    }

    clearEndpointError();

    loginNotice.className =
        "login-notice login-notice--success";

    loginNotice.textContent =
        "Endpoint format is valid. " +
        "Opening the Version 2 workspace preview.";

    window.setTimeout(function openWorkspace() {
        window.location.assign("/workspace");
    }, 550);
});

microsoftLoginButton.addEventListener(
    "click",
    function handleMicrosoftLogin() {
        loginNotice.className =
            "login-notice login-notice--warning";

        loginNotice.textContent =
            "Microsoft Entra sign-in is not connected yet. " +
            "This button will be enabled in Sprint 2.2.";
    }
);
