import axios from "axios";

/* ======================================
   AXIOS INSTANCE
====================================== */

const API = axios.create({
  baseURL: "http://localhost:8000/api",
  headers: {
    "Content-Type": "application/json",
  },
});

/* ======================================
   AUTO ATTACH JWT
====================================== */

API.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");

  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

/* ======================================
   AUTH APIs
====================================== */

/* -------- REGISTER -------- */

export const registerUser = async (
  email: string,
  password: string,
  organization_name: string
) => {
  const response = await API.post("/users/register", {
    email,
    password,
    organization_name,
  });

  return response.data;
};

/* -------- LOGIN (IMPORTANT FIX) -------- */

export const loginUser = async (email: string, password: string) => {
  const formData = new URLSearchParams();
  formData.append("username", email); // OAuth2 uses "username"
  formData.append("password", password);

  const response = await axios.post(
    "http://localhost:8000/api/users/login",
    formData,
    {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    }
  );

  // Save JWT
  localStorage.setItem("access_token", response.data.access_token);

  return response.data;
};

/* -------- LOGOUT -------- */

export const logoutUser = () => {
  localStorage.removeItem("access_token");
};

export default API;
