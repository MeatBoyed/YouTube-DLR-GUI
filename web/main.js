// Linker function to util's ValidateURL function
function ValidateURL() {

    // Obtainng VideoURL and Error Message Output fields from DOM
    let videoURL = document.getElementById("videoURLInput").value
    let output = document.getElementById("errorMessage")
    let fileName = document.getElementById("fileName")

    // Calling to Python utils function
    eel.ValidateURL(videoURL)(function(response) {

        // Storing video resolutions
        let resolution = response.videoData.resolutions
        console.log(resolution)

        

        // Ouputing the returned response message into Error Message field
        output.innerText = response.errorMessage 
        fileName.value = response.videoData.fileName
    })
}

function GetDownloadLocation() {
    let downloadPath = document.getElementById("downloadLocationPath")

    eel.selectFolder()(function(response) {
        downloadPath.innerText = response
    });
}