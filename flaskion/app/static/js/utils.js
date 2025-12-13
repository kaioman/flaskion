
export class HttpClient {

    static async post(url, payload) {
        try {
            const response = await fetch(url, {
                method : "POST",
                headers: { "Content-Type":  "application/json" },
                body: JSON.stringify(payload)
            });
            
            if (!response.ok) {
                throw new Error("Server Error: " + response.status);
            }

            return await response.json();
        } catch (error) {
            throw error;
        }
    }

    static async get(url) {
        const response = await fetch(url, { method: "GET" });
        
        if (!response.ok) {
            throw new Error("Server Error: " + response.status);
        }
        return await response.json();
    }
}
