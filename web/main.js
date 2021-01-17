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

// Download video function
function DownloadVideo(resolution) {

    console.log("Function has fired")

    // let videoURL = document.getElementById("videoURLInput").value
    let videoURL = "https://www.youtube.com/watch?v=FIB33xnTq0E"
    // let fileName = document.getElementById("filename").value
    let fileName = "outputwooo"
    // let outputPath = document.getElementById("downloadLocationPath").innerText
    let outputPath = "C:/Users/charl/Desktop"

    eel.DownloadVideo(videoURL, resolution, fileName, outputPath)(function(response) {
        console.log(resolution)

        document.getElementById("downloadLocationPath").innerText = response 
    })
}