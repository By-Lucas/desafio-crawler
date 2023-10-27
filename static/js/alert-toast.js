let toastTimer; // Variável para armazenar o temporizador

function showToast(status, message) {
    // Cancela qualquer temporizador existente
    clearTimeout(toastTimer);

    // Seleciona o elemento toast-body
    const toastBody = document.querySelector('#toast-body');
    
    // Define a cor do toast com base no status
    const bgClass = status === 'success' ? 'bg-success' : 'bg-danger';
    
    // Define o conteúdo do toast
    toastBody.innerHTML = message;
    
    // Seleciona o elemento toast e adiciona as classes necessárias
    const toast = document.querySelector('#toast');
    toast.classList.add('show', bgClass);
    
    // Configura um novo temporizador para fechar o toast após 5 segundos
    toastTimer = setTimeout(() => {
        closeToast();
    }, 6000);
}

function closeToast() {
    // Seleciona o elemento toast
    const toast = document.querySelector('#toast');
    
    // Remove a classe 'show' para ocultar o toast
    toast.classList.remove('show');
}
