function deleteNote(noteId) {
    console.log('NoteId:', noteId);
    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({ noteId: noteId }),
    }).then((_res)=> {
        window.location.href = "/";
        console.log('Note deleted!');
    })
}

function deleteGroup(groupId) {
    console.log('GroupId:', groupId);
    fetch("/delete-group", {
        method: "POST",
        body: JSON.stringify({ groupId: groupId }),
    }).then((_res)=> {
        window.location.href = "/group";
        console.log('Group deleted!');
    })
}

function deleteProduct(productId) {
    console.log('ProductId:', productId);
    fetch("/delete-product", {
        method: "POST",
        body: JSON.stringify({ productId: productId }),
    }).then((_res)=> {
        window.location.href = "/product";
        console.log('Product deleted!');
    })
}


const groupSelect = document.querySelector('#group');
const submitBtn = document.querySelector('#add_product');

  // Disable the submit button if no option is selected
  function toggleSubmitBtn() {
    if (groupSelect.value === 'Choose...') {
      submitBtn.disabled = true;
    } else {
      submitBtn.disabled = false;
    }
  }

  // Call the toggleSubmitBtn function when the page is loaded
  toggleSubmitBtn();

  // Call the toggleSubmitBtn function when the select value is changed
  groupSelect.addEventListener('change', toggleSubmitBtn);
