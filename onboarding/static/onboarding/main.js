document.addEventListener("DOMContentLoaded", () => {
  // Get all "navbar-burger" elements
  const navbarBurgers = document.querySelectorAll(".navbar-burger");

  // Check if there are any navbar burgers
  if (navbarBurgers.length > 0) {
    // Add a click event on each of them
    navbarBurgers.forEach((navbarBurger) => {
      navbarBurger.addEventListener("click", () => {
        // Get the target from the "data-target" attribute
        const target = navbarBurger.dataset.target;
        const targetElement = document.getElementById(target);

        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        navbarBurger.classList.toggle("is-active");
        targetElement.classList.toggle("is-active");
      });
    });
  }

  // Animate hero title and buttons
  gsap.from("#hero-title", { duration: 1, y: -100, opacity: 0 });
  gsap.from("#cta-buttons", {
    duration: 1,
    y: 100,
    opacity: 0,
    delay: 0.5,
  });

  // Animate features section on scroll
  gsap.from("#features-title", {
    duration: 1,
    opacity: 0,
    scrollTrigger: "#features-title",
  });
  gsap.from(".features-section .card", {
    duration: 1,
    opacity: 0,
    y: 100,
    stagger: 0.2,
    scrollTrigger: {
      trigger: ".features-section",
      start: "top center",
    },
  });

  // Animate How It Works section on scroll
  gsap.from("#how-it-works-title", {
    duration: 1,
    opacity: 0,
    scrollTrigger: "#how-it-works-title",
  });
  gsap.from(".how-it-works .column", {
    duration: 1,
    opacity: 0,
    y: 100,
    stagger: 0.2,
    scrollTrigger: {
      trigger: ".how-it-works",
      start: "top center",
    },
  });

  // Animate CTA section on scroll
  gsap.from("#cta-title", {
    duration: 1,
    opacity: 0,
    y: 50,
    scrollTrigger: "#cta-title",
  });

  function getCurrentYear(element) {
    const currentYear = new Date().getFullYear();
    element.textContent = currentYear;
  }

  getCurrentYear(document.getElementById("current-year"));
});

function toggleAccordion(header) {
  const button = header.querySelector("button.toggle-accordion");
  const messageBody = header.nextElementSibling;
  const icon = button.querySelector(".icon");

  // Toggle the message body visibility
  if (
    messageBody.style.display === "none" ||
    messageBody.style.display === ""
  ) {
    messageBody.style.display = "block"; // Show the message body
    button.classList.add("active"); // Rotate the arrow icon
  } else {
    messageBody.style.display = "none"; // Hide the message body
    button.classList.remove("active"); // Reset the arrow icon
  }
}
