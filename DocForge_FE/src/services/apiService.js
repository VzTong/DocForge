import router from "@/route.js";
import config from "../configs/config.js";

function getApiUrl(endpoint) {
    if (endpoint.startsWith("/")) {
        endpoint = endpoint.substring(1);
    }
    return `${config.API_URL_PY_SERVICE}${endpoint}`;
}

const apiService = {
    async get(endpoint) {
        const resp = await fetch(getApiUrl(endpoint),{
            headers:{
                "Content-Type": "application/json",
                "Authorization": `Bearer ${sessionStorage.getItem("accessToken")}`
            }
        })
        if(resp.status === 401){
            window.location.href = '/dang-nhap'
            return;
        }
        const data = await resp.json()
        return data
    },
    async post(endpoint, data) {
        const resp = await fetch(getApiUrl(endpoint), {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${sessionStorage.getItem("accessToken")}`
            },
            body: JSON.stringify(data)
        })
        const result = await resp.json()
        return result
    },
    async put(endpoint, data) {
        const resp = await fetch(getApiUrl(endpoint), {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${sessionStorage.getItem("accessToken")}`
            },
            body: JSON.stringify(data)
        })
        const result = await resp.json()
        return result
    },
    async delete(endpoint) {
        const resp = await fetch(getApiUrl(endpoint),{
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${sessionStorage.getItem("accessToken")}`
            },
        })
        const data = await resp.json()
        return data
    },
}

export default apiService;