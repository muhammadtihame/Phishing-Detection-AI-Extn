// A portion of your background.js file
async function detectPhishing(url) {
    try {
        const response = await fetch("http://localhost:5000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: url })
        });
        
        const data = await response.json();
        
        if (data.is_phishing) {
            return { redirectUrl: chrome.runtime.getURL("warning.html") };
        }
    } catch (error) {
        console.error("API call failed:", error);
    }
    
    return { cancel: false };
}