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
    fetch(`/deletevendor/${property_name}/${vendor_name}`, {
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

function request_invoice(property_name, vendor_name) {
    fetch(`/sendinvoice/${property_name}/${vendor_name}}`, {
        headers: {
            "Content-Type": "application/json",
        },
        method: 'get',
    }).then(e => {
        console.log(e)
        window.location.href = `/`;
    }).catch(e => {
        console.log(e)
    })
}

function edit_vendor(property_name, vendor_name) {
    window.location.href = `/editvendor/${property_name}/${vendor_name}`;
}