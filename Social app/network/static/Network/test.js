// Initialize counters in localStorage if not present
if (!localStorage.getItem('counter1')) {
  localStorage.setItem('counter1', 0);
}

document.addEventListener('DOMContentLoaded', function () {
  // Initialize counters for each post in localStorage if not present
  document.querySelectorAll('.like-counter').forEach(function (counterDisplay) {
      const postId = counterDisplay.getAttribute('data-counterid');
      if (!localStorage.getItem(`counter1_${postId}`)) {
          localStorage.setItem(`counter1_${postId}`, 0);
      }

      // Set initial values for like counters
      counterDisplay.innerHTML = localStorage.getItem(`counter1_${postId}`) || 0;
  });

  // Add click event handlers to the like buttons
  document.querySelectorAll('.like-button').forEach(function (button) {
      button.onclick = function () {
          const postId = this.getAttribute('data-postid');
          const isLiked = this.getAttribute('data-liked') === 'true';

          // Update the like status visually
          const counterDisplay = document.querySelector(`[data-counterid="${postId}"]`);
          let counter = parseInt(localStorage.getItem(`counter1_${postId}`)) || 0;

          if (isLiked) {
              counter--;
              this.setAttribute('data-liked', 'false');
          } else {
              counter++;
              this.setAttribute('data-liked', 'true');
          }

          counterDisplay.innerHTML = counter;
          localStorage.setItem(`counter1_${postId}`, counter);

          // Send AJAX request to add/remove like
          const url = isLiked ? `/remove_like/${postId}/` : `/add_like/${postId}/`;
          fetch(url, {
                method: "POST",
                headers: {"X-CSRFToken": getCookie("csrftoken")},
          })
          .then(response => {
              if (!response.ok) {
                  throw new Error(`HTTP error! Status: ${response.status}`);
              }
              return response.json();
          })
          .then(result => {
              console.log(result.message); // Log the server response
  
             // Update the WhoYouLiked list based on the server response
             const likedPosts = result.whoYouLiked || [];
             updateWhoYouLiked(likedPosts);
          })
          .catch(error => console.error('Error:', error));
      };
  });

  // Set initial values for like counters
  document.querySelectorAll('.like-counter').forEach(function (counterDisplay) {
      const postId = counterDisplay.getAttribute('data-counterid');
      counterDisplay.innerHTML = localStorage.getItem(`counter1_${postId}`) || 0;
  });
});

// Function to get CSRF token from cookies
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

// Function to update the WhoYouLiked list in the HTML
function updateWhoYouLiked(likedPosts) {
  document.querySelectorAll('.like-button').forEach(function (button) {
      const postId = button.getAttribute('data-postid');
      button.setAttribute('data-liked', likedPosts.includes(postId) ? 'true' : 'false');
  });
}
