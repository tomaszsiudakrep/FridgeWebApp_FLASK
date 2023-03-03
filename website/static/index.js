function deleteNote(noteId) {
    console.log('Test', noteId);
    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({ noteId: noteId }),
    }).then((_res)=> {
        window.location.href = "/";
    })
    console.log('TEST');
}

