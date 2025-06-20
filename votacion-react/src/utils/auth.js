import * as jwtDecode from "jwt-decode";

export function saveToken(token) {
  localStorage.setItem("jwt_token", token);
}

export function getToken() {
  return localStorage.getItem("jwt_token");
}

export function removeToken() {
  localStorage.removeItem("jwt_token");
}

export function getUser() {
  const token = getToken();
  if (!token) return null;
  try {

    return jwtDecode.default ? jwtDecode.default(token) : jwtDecode(token);
  } catch {
    return null;
  }
}
