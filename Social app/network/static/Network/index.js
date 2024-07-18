// Function to toggle the counter between 0 and 1
function toggleCounter(postId, displayId) {
    // Construct a unique key for each post
    const counterKey = `counter_${postId}`;

    // Initialize counter in localStorage if not present
    if (!localStorage.getItem(counterKey)) {
        localStorage.setItem(counterKey, 0);
    }

    let counter = parseInt(localStorage.getItem(counterKey));
    counter = counter === 0 ? 1 : 0;
    
    // Update the counter display
    document.getElementById(displayId).innerHTML = counter;

    // Update the counter value in localStorage
    localStorage.setItem(counterKey, counter);
}

// Set initial values for counters
document.addEventListener('DOMContentLoaded', function () {
    const likeButtons = document.querySelectorAll('.like-button');
    likeButtons.forEach((button) => {
        const postId = button.dataset.postId;
        const displayId = `like-counter_${postId}`;

        const counterKey = `counter_${postId}`;
        const initialCounterValue = parseInt(localStorage.getItem(counterKey)) || 0;

        document.getElementById(displayId).innerHTML = initialCounterValue;

        button.addEventListener('click', function () {
            toggleCounter(postId, displayId);
        });
    });
});