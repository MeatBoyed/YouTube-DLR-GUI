// Linker function to util's ValidateURL function
function ValidateURL() {

    // Obtainng VideoURL and Error Message Output fields from DOM
    let videoURL = document.getElementById("videoURLInput").value
    let output = document.getElementById("errorMessage")

    // Calling to Python utils function
    eel.ValidateURL(videoURL)(function(res) {
        // Ouputing the returned response message into Error Message field
        output.innerText = res 
    })
}