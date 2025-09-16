// Get CSRF token from meta tag
function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

function deleteNote(noteId) {
    if (confirm('Are you sure you want to delete this note?')) {
        fetch("/delete-note", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({ noteId: noteId }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
            } else {
                location.reload();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while deleting the note.');
        });
    }
}

function toggleFavorite(noteId) {
    fetch(`/toggle-favorite/${noteId}`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while updating the note.');
    });
}