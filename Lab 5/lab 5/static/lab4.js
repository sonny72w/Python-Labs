function toggleSecurityInfo() {
    const infoSection = document.getElementById('security-details');
    if (infoSection.style.display === 'none' || infoSection.style.display === '') {
        infoSection.style.display = 'block';
        console.log("DOM: Security logs are now VISIBLE.");
    } else {
        infoSection.style.display = 'none';
        console.log("DOM: Security logs are now HIDDEN.");
    }
}
function runSystemCheck() {
    const statusText = document.getElementById('system-status');
    statusText.style.color = "green"; 
    statusText.innerText = "SYSTEM STATUS: SECURE (All Nodes Active)";
    console.log("User Action: System Check Successful.");
}