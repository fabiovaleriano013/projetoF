
console.log('Modal.js loaded');
class Modal {
    constructor(modalId, title, contentId, triggerId=null) {
        this.modalId = modalId;
        this.title = title;
        this.contentId = contentId;
        this.triggerId = triggerId; // id do botao que vai ativar o modal

        // VARIÁVEIS:
        // modal: é o id que a div modal irá ter, é um nome qualquer que o programador desejar.
        // title: é o título que a modal irá ter.
        // contentId: é o id da div que possui o conteúdo que ficará no modal.
        // botao: é o id do botão que irá abrir a modal.
    }

    createModal() {
        let modal = document.createElement('div');
        modal.id = this.modalId;
        modal.className = "modal";
        modal.style.display = 'none';

        let modalContent = document.createElement('div');
        modalContent.className = "modal-content";

        let modalHeader = document.createElement('div');
        modalHeader.className = "modal-header p-0 d-flex justify-content-center align-items-center text-align-left";

        let modalTitle = document.createElement('h1');
        modalTitle.className = "modal-title fs-5 pb-2";
        modalTitle.textContent = this.title;

        let closeBtn = document.createElement('span');
        closeBtn.className = "close";
        closeBtn.innerHTML = "&times;";
        closeBtn.onclick = () => this.closeModal();

        modalHeader.appendChild(modalTitle);
        modalHeader.appendChild(closeBtn);

        let modalBody = document.createElement('div');
        modalBody.className = "modal-body d-flex flex-column align-items-center justify-content-evenly";

        let contentElement = document.getElementById(this.contentId);
        modalBody.appendChild(contentElement);
        contentElement.style.display = 'flex';


        modalContent.appendChild(modalHeader);
        modalContent.appendChild(modalBody);
        modal.appendChild(modalContent);

        document.body.querySelector('main').appendChild(modal);

        if (this.triggerId) { 
            let triggerElement = document.getElementById(this.triggerId);
            triggerElement.onclick = () => this.openModal();
        }
    }

    openModal() {
        let modal = document.getElementById(this.modalId);
        modal.style.display = 'flex';

        window.onclick = function (event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }
    }

    closeModal() {
        let modal = document.getElementById(this.modalId);
        modal.style.display = 'none';
    }
}
