let audio = new Audio();
audio.src = "https://www.soundjay.com/button/beep-07.wav";
audio.volume = 0.5;

function activateLeftLaneChange() {
    hideAll();
    document.getElementById("aPillarLeft").style.display = "flex";
    document.getElementById("bPillarLeft").style.display = "flex";
    document.getElementById("rearView").style.display = "block";
    playAlert("Caution, a motorcycle is approaching on the left!");
}

function activateRightLaneChange() {
    hideAll();
    document.getElementById("aPillarRight").style.display = "flex";
    document.getElementById("bPillarRight").style.display = "flex";
    document.getElementById("rearView").style.display = "block";
    playAlert("Caution, a car is approaching on the right!");
}

function showParkingView() {
    hideAll();
    document.getElementById("birdView").style.display = "block";
}

function resetView() {
    document.getElementById("aPillarLeft").style.display = "flex";
    document.getElementById("aPillarRight").style.display = "flex";
    document.getElementById("bPillarLeft").style.display = "flex";
    document.getElementById("bPillarRight").style.display = "flex";
    document.getElementById("rearView").style.display = "none";
    document.getElementById("birdView").style.display = "none";
}

function hideAll() {
    document.getElementById("aPillarLeft").style.display = "none";
    document.getElementById("aPillarRight").style.display = "none";
    document.getElementById("bPillarLeft").style.display = "none";
    document.getElementById("bPillarRight").style.display = "none";
    document.getElementById("rearView").style.display = "none";
    document.getElementById("birdView").style.display = "none";
}

function playAlert(message="Caution, a vehicle is approaching!") {
    alert(message);
    audio.play();
}

function changeVolume(direction) {
    if (direction === 'up' && audio.volume < 1) audio.volume += 0.1;
    if (direction === 'down' && audio.volume > 0) audio.volume -= 0.1;
    alert("Current Volume: " + Math.round(audio.volume * 100) + "%");
}

function customizeAlert() {
    let newSound = prompt("Enter a custom sound URL:", audio.src);
    if (newSound) {
        audio.src = newSound;
        alert("Alert sound updated!");
    }
}