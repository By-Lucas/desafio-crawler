

function showToast(status, message) {
    // Seleciona o elemento toast-body
    const toastBody = document.querySelector('#toast-body');
    
    // Define a cor do toast com base no status
    const bgClass = status === 'success' ? 'bg-success' : 'bg-danger';
    
    // Define o conteúdo do toast
    toastBody.innerHTML = message;
    
    // Seleciona o elemento toast e adiciona as classes necessárias
    const toast = document.querySelector('#toast');
    toast.classList.add('show', bgClass);
    
    // Exibe o toast por 5 segundos e em seguida o fecha
    setTimeout(() => {
        toast.classList.remove('show', bgClass);
    }, 5000);
}


function closeToast() {
    // Seleciona o elemento toast-body
    const toastBody = document.querySelector('#toast-body');
    
    // Seleciona o elemento toast e adiciona as classes necessárias
    const toast = document.querySelector('#toast');
    
    toast.hide()
}
    // Exibe o toast por 3 segundos e em seguida o fecha

// ;(function () {
//     const toastElement = document.getElementById("toast")
//     const toastBody = document.getElementById("toast-body")
//     const toast = new bootstrap.Toast(toastElement, {delay: 5000})

//     htmx.on("showMessage", (e) => {
//         const message = e.detail.message
//         const bgClass = e.detail.bgClass

//         toastBody.innerText = e.detail.value
//         toastElement.classList.remove('bg-danger', 'bg-success')
//         toastElement.classList.add('bg-' + bgClass)
//         toastBody.innerText = message
//         toast.show()
//     })
// })()