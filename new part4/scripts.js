(function () {
  "use strict";

  // Mock data so pages render without a backend
  const AppData = {
    places: [
      {
        id: "p1",
        name: "Cozy Loft",
        price_per_night: 120,
        host: "Alice",
        description: "A sunny loft in the city center, close to cafes and museums.",
        amenities: ["Wi‑Fi", "Kitchen", "Air conditioning"],
        reviews: [
          { user: "Bob", rating: 5, comment: "Fantastic stay, very clean!" },
          { user: "Cara", rating: 4, comment: "Great location and comfy bed." }
        ]
      },
      {
        id: "p2",
        name: "Beach Bungalow",
        price_per_night: 180,
        host: "Diego",
        description: "Steps from the beach. Hear the waves and enjoy sunsets.",
        amenities: ["Wi‑Fi", "Free parking", "Washer"],
        reviews: []
      }
    ]
  };

  // Auth helpers (client-side only, demo)
  function isLoggedIn() {
    return Boolean(localStorage.getItem("token"));
  }
  function currentUser() {
    return localStorage.getItem("user") || "";
  }
  function setAuthUI() {
    const link = document.getElementById("login-link");
    if (!link) return;
    if (isLoggedIn()) {
      link.textContent = "Logout";
      link.href = "#";
      link.addEventListener("click", function (e) {
        e.preventDefault();
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        location.reload();
      }, { once: true });
    } else {
      link.textContent = "Login";
      link.href = "login.html";
    }
  }

  // Index page: render list of places
  function renderPlaces() {
    const container = document.getElementById("places-list");
    if (!container) return;
    container.innerHTML = "";
    AppData.places.forEach((p) => {
      const card = document.createElement("article");
      card.className = "place-card";
      card.innerHTML = `
        <h3>${escapeHtml(p.name)}</h3>
        <p class="muted">$${Number(p.price_per_night).toFixed(0)} per night</p>
        <a class="details-button" href="place.html?id=${encodeURIComponent(p.id)}">View Details</a>
      `;
      container.appendChild(card);
    });
  }

  // Place details page
  function renderPlaceDetails() {
    const details = document.getElementById("place-details");
    if (!details) return;

    const params = new URLSearchParams(location.search);
    const id = params.get("id");
    const place = AppData.places.find((p) => p.id === id) || AppData.places[0];

    const title = document.getElementById("place-title");
    const info = document.getElementById("place-info");
    const amenitiesList = document.getElementById("amenities-list");
    const reviewsList = document.getElementById("reviews-list");
    const addBtn = document.getElementById("add-review-button");
    const loginPrompt = document.getElementById("login-prompt");

    title.textContent = place.name;
    info.innerHTML = `
      <p><strong>Host:</strong> ${escapeHtml(place.host)}</p>
      <p><strong>Price:</strong> $${Number(place.price_per_night).toFixed(0)} per night</p>
      <p><strong>Description:</strong> ${escapeHtml(place.description)}</p>
    `;

    amenitiesList.innerHTML = "";
    place.amenities.forEach((a) => {
      const li = document.createElement("li");
      li.textContent = a;
      amenitiesList.appendChild(li);
    });

    reviewsList.innerHTML = "";
    if (place.reviews.length === 0) {
      const p = document.createElement("p");
      p.className = "muted";
      p.textContent = "No reviews yet.";
      reviewsList.appendChild(p);
    } else {
      place.reviews.forEach((r) => {
        const div = document.createElement("div");
        div.className = "review-card";
        div.innerHTML = `
          <p><strong>${escapeHtml(r.user)}</strong> — Rating: ${Number(r.rating)}/5</p>
          <p>${escapeHtml(r.comment)}</p>
        `;
        reviewsList.appendChild(div);
      });
    }

    if (isLoggedIn()) {
      addBtn.hidden = false;
      addBtn.href = `add_review.html?id=${encodeURIComponent(place.id)}`;
      loginPrompt.hidden = true;
    } else {
      addBtn.hidden = true;
      loginPrompt.hidden = false;
    }
  }

  // Login page
  function wireLoginForm() {
    const form = document.getElementById("login-form");
    if (!form) return;
    const error = document.getElementById("login-error");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      const email = (document.getElementById("email").value || "").trim();
      const password = (document.getElementById("password").value || "").trim();
      if (email.length && password.length) {
        // Demo: accept any non-empty credentials
        localStorage.setItem("token", "demo-token");
        localStorage.setItem("user", email);
        const params = new URLSearchParams(location.search);
        const redirect = params.get("redirect");
        location.href = redirect || "index.html";
      } else {
        error.hidden = false;
      }
    });
  }

  // Add Review page
  function wireAddReviewForm() {
    const form = document.getElementById("add-review-form");
    const guardMsg = document.getElementById("auth-guard-msg");
    if (!form) return;

    if (!isLoggedIn()) {
      guardMsg.hidden = false;
      // Redirect to login with return
      const returnTo = `add_review.html${location.search || ""}`;
      setTimeout(() => {
        location.href = `login.html?redirect=${encodeURIComponent(returnTo)}`;
      }, 1200);
      return;
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      const params = new URLSearchParams(location.search);
      const id = params.get("id") || "p1";
      const rating = Number(document.getElementById("rating").value);
      const comment = (document.getElementById("comment").value || "").trim();
      if (!rating || !comment) return;

      const place = AppData.places.find((p) => p.id === id) || AppData.places[0];
      place.reviews.push({
        user: currentUser() || "You",
        rating,
        comment
      });

      // Navigate back to details to see the new review (session-only)
      location.href = `place.html?id=${encodeURIComponent(id)}`;
    });
  }

  function escapeHtml(str) {
    return String(str)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  // Init on load
  document.addEventListener("DOMContentLoaded", function () {
    setAuthUI();
    renderPlaces();
    renderPlaceDetails();
    wireLoginForm();
    wireAddReviewForm();
  });
})();