// Linker function to util's ValidateURL function
function ValidateURL() {

    // Obtainng VideoURL and Error Message Output fields from DOM
    let videoURL = document.getElementById("videoURLInput").value
    let output = document.getElementById("errorMessage")

    // Calling to Python utils function
    eel.ValidateURL(videoURL)(function(response) {
        // Ouputing the returned response message into Error Message field
        console.log(response)

        let data = response.videoData
        console.log("Video data: ", data)

        output.innerText = response.errorMessage 
    })
}