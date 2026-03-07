/*
DesiGrowth Frontend Script

Features
1. Campaign form submission
2. AI loading animation
3. Backend API request
4. Store campaign result
5. Preview page rendering
*/

document.addEventListener("DOMContentLoaded", function () {

/* =========================
CREATE LOADING OVERLAY
========================= */

function showLoading() {

const loadingDiv = document.createElement("div")

loadingDiv.id = "loadingOverlay"

loadingDiv.innerHTML = `
<div class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">

<div class="bg-white p-8 rounded-xl shadow-lg text-center max-w-sm">

<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>

<h2 class="text-lg font-semibold mb-2">
Generating AI Campaign...
</h2>

<p class="text-gray-500 text-sm">
Please wait while we create your marketing content.
</p>

</div>

</div>
`

document.body.appendChild(loadingDiv)

}


/* =========================
FORM SUBMISSION
========================= */

const form = document.getElementById("campaignForm")

if (form) {

form.addEventListener("submit", async function(e){

e.preventDefault()

showLoading()

const business = document.getElementById("business").value
const product = document.getElementById("product").value
const offer = document.getElementById("offer").value
const festival = document.getElementById("festival").value
const location = document.getElementById("location").value


try {

const response = await fetch("https://desigrowth-2.onrender.com/generate-campaign", {

method: "POST",

headers:{
"Content-Type":"application/json"
},

body: JSON.stringify({
business,
product,
offer,
festival,
location
})

})

const data = await response.json()

localStorage.setItem("campaignData", JSON.stringify(data))

window.location.href = "preview.html"

}

catch(error){

console.error("Campaign generation error:", error)

alert("Failed to generate campaign.")

}

})

}


/* =========================
PREVIEW PAGE
========================= */

if (window.location.pathname.includes("preview.html")) {

const stored = localStorage.getItem("campaignData")

if (stored){

const data = JSON.parse(stored)

const caption = document.getElementById("caption")
const hashtags = document.getElementById("hashtags")
const poster = document.getElementById("poster")
const downloadBtn = document.getElementById("downloadBtn")

const previewCaption = document.getElementById("previewCaption")
const previewPoster = document.getElementById("previewPoster")
const previewTags = document.getElementById("previewTags")

if (caption) caption.innerText = data.caption
if (hashtags) hashtags.innerText = data.hashtags

if (poster) {
  poster.src = data.poster

  // Poster reveal animation
  poster.onload = () => {
    poster.classList.remove("opacity-0", "scale-90")
    poster.classList.add("opacity-100", "scale-100")
  }
}

if (previewPoster) {
  previewPoster.src = data.poster
  previewPoster.classList.add("transition-all","duration-700","opacity-0")

  previewPoster.onload = () => {
    previewPoster.classList.remove("opacity-0")
    previewPoster.classList.add("opacity-100")
  }
}
if (previewCaption) previewCaption.innerText = data.caption
if (previewTags) previewTags.innerText = data.hashtags


if (downloadBtn){

downloadBtn.addEventListener("click", function(){

const link = document.createElement("a")

link.href = data.poster

link.download = "desigrowth-poster.png"

link.click()

})

}

}

}

})