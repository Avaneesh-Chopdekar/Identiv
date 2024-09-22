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
});
