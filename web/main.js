// Linker function to util's ValidateURL function
function ValidateURL() {

    // Obtainng VideoURL and Error Message Output fields from DOM
    let videoURL = document.getElementById("videoURLInput").value
    let output = document.getElementById("errorMessage")
    let fileName = document.getElementById("fileDataInput")

    // Activate Loading Spinner and set Text
    document.getElementById("LoadingSpinner").style.display = "block"
    document.getElementById("LoadingText").innerText = "Verifying URL ...."

    // Calling to Python utils ValidateURL function
    eel.ValidateURL(videoURL)(function(response) {

        // Change videoURL input field colour based on response's error message
        if (response.errorMessage === "") {
            document.getElementById("videoURLInput").style.borderColor = "green"
        }else {
            document.getElementById("videoURLInput").style.borderColor = "red"
        }

        // Deactivaet Loading Spinner and reset text
        document.getElementById("LoadingSpinner").style.display = "none"
        document.getElementById("LoadingText").innerText = ""

        // Ouputing the returned response messages 
        output.innerText = response.errorMessage 
        fileName.value = response.fileName
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

    // Activate Loading Spinner and set Text
    document.getElementById("LoadingSpinner").style.display = "block"
    document.getElementById("LoadingText").innerText = "Downloading video ..."

    eel.DownloadVideo(resolution, fileName)(function(response) {
        errorMessage.innerText = "Video is downloaded!"

        // Deactivaet Loading Spinner and reset text
        document.getElementById("LoadingSpinner").style.display = "none"
        document.getElementById("LoadingText").innerText = ""
    })
}
