const solarSystem = document.querySelector('.solar-system');
const modal = document.getElementById('planet-info-modal');
const planetName = document.getElementById('planet-name');
const planetInfo = document.getElementById('planet-info');
const closeButton = document.querySelector('.close-btn');

// Planet data
const planetData = {
    Mercury: "Mercury is the closest planet to the Sun and has a very thin atmosphere. It's known for its extreme temperature fluctuations.",
    Earth: "Earth is the third planet from the Sun and the only known planet to support life. It has a diverse environment and a single moon.",
    Mars: "Mars, often referred to as the 'Red Planet', has a thin atmosphere and is known for its large volcanoes and canyons.",
    Jupiter: "Jupiter is the largest planet in the solar system, famous for its Great Red Spot, a giant storm. It has a thick atmosphere and many moons."
};

// Add event listener to track mouse movement
document.addEventListener('mousemove', (e) => {
    const width = window.innerWidth;
    const height = window.innerHeight;

    // Calculate mouse position relative to the center of the window
    const mouseX = e.clientX - width / 2;
    const mouseY = e.clientY - height / 2;

    // Set maximum tilt angles
    const maxTiltX = 10;
    const maxTiltY = 10;

    // Calculate tilt values based on mouse position
    const tiltX = (mouseY / height) * maxTiltX;
    const tiltY = (mouseX / width) * maxTiltY;

    // Apply the tilt transform to the solar system
    solarSystem.style.transform = `rotateX(${-tiltX}deg) rotateY(${tiltY}deg)`;
});

// Add click event to planets
document.querySelectorAll('.planet').forEach(planet => {
    planet.addEventListener('click', (e) => {
        const selectedPlanet = e.currentTarget.parentElement.getAttribute('data-planet');
        planetName.textContent = selectedPlanet;
        planetInfo.textContent = planetData[selectedPlanet];
        modal.style.display = "block"; // Show modal
    });
});

// When the user clicks on <span> (x), close the modal
closeButton.onclick = function() {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
