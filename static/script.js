document.querySelectorAll('.bg-danger').forEach((button) => button.addEventListener('click', (event) => {
    const id = event.target.parentElement.parentElement.parentElement.innerText
    console.log(id)
    if (id === "") return
    fetch('/deleteuser', {
        headers: {
            "Content-Type": "application/json",
        },
        method: 'post',
        body: JSON.stringify({ username: id }),
    }).then(e => {
        console.log(e)
        if (window.history.replaceState) {
            window.history.replaceState(null, null, window.location.href);
        }
        location.reload()
    }).catch(e => {
        console.log(e)
    })
}))

function delete_vendor(property_name, vendor_name) {
    if (string_id === "") return
    fetch(`/deleteuser/${property_name}/${vendor_name}`, {
        headers: {
            "Content-Type": "application/json",
        },
        method: 'delete',
    }).then(e => {
        console.log(e)
    }).catch(e => {
        console.log(e)
    })
}