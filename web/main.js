// Linker function to util's ValidateURL function
function ValidateURL() {

    // Obtainng VideoURL and Error Message Output fields from DOM
    let videoURL = document.getElementById("videoURLInput").value
    let output = document.getElementById("errorMessage")
    let fileName = document.getElementById("fileDataInput")

    // Calling to Python utils function
    eel.ValidateURL(videoURL)(function(response) {

        // Storing video resolutions
        let resolution = response.videoData.resolutions

        // Ouputing the returned response message into Error Message field
        output.innerText = response.errorMessage 
        fileName.value = response.videoData.fileName
    })
}

// Download video function
function DownloadVideo(resolution) {

    console.log("Function has fired")

    // Request user to select the download Path
    eel.selectFolder()

    // Get fileName and errorMessage fields
    let fileName = document.getElementById("fileDataInput").value
    let errorMessage = document.getElementById("errorMessage")

    eel.DownloadVideo(resolution, fileName)(function(response) {
        errorMessage.innerText = response
    })
}
