/*
DesiGrowth Frontend Script
Handles:

1. Form submission
2. Sending campaign data to backend
3. Receiving generated campaign
4. Redirecting to preview page
5. Displaying results
   */

document.addEventListener("DOMContentLoaded", function () {

/* ================================
CAMPAIGN FORM SUBMISSION
=================================*/

const form = document.getElementById("campaignForm");

if (form) {

```
form.addEventListener("submit", async function (e) {

  e.preventDefault();

  const businessName = document.getElementById("business").value;
  const productName = document.getElementById("product").value;
  const offer = document.getElementById("offer").value;
  const festival = document.getElementById("festival").value;
  const location = document.getElementById("location").value;

  try {

    const response = await fetch("/generate-campaign", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        business: businessName,
        product: productName,
        offer: offer,
        festival: festival,
        location: location
      })
    });

    const data = await response.json();

    /* Save response for preview page */

    localStorage.setItem(
      "campaignData",
      JSON.stringify(data)
    );

    /* Redirect to preview page */

    window.location.href = "preview.html";

  } catch (error) {

    console.error("Error generating campaign:", error);
    alert("Failed to generate campaign. Please try again.");

  }

});
```

}

/* ================================
LOAD PREVIEW DATA
=================================*/

if (window.location.pathname.includes("preview.html")) {

```
const storedData = localStorage.getItem("campaignData");

if (storedData) {

  const data = JSON.parse(storedData);

  const caption = document.getElementById("caption");
  const hashtags = document.getElementById("hashtags");
  const poster = document.getElementById("poster");
  const downloadBtn = document.getElementById("downloadBtn");

  if (caption) caption.innerText = data.caption || "";
  if (hashtags) hashtags.innerText = data.hashtags || "";

  if (poster && data.poster_url) {
    poster.src = data.poster_url;
  }

  if (downloadBtn && data.poster_url) {

    downloadBtn.addEventListener("click", function () {

      const link = document.createElement("a");
      link.href = data.poster_url;
      link.download = "desigrowth-poster.png";
      link.click();

    });

  }

}
```

}

});

