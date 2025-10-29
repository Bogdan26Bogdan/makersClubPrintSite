const button = document.getElementById("generateButton");
const responseContainer = document.getElementById("responseContainer");

button.addEventListener("click", async () => {
    try {
        const response = await fetch("/generate-magic-value");
        value = await response.text();
        responseContainer.textContent = value;
    } catch (error) {
        console.error("Error fetching magic value:", error);
        responseContainer.textContent = "Error fetching magic value";
    }
});
