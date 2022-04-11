// Dropdown
document.addEventListener('click', (e) => {
    const isDropDownButton = e.target.matches('[data-dropdown-button]')
    if(!isDropDownButton && e.target.closest('[data-dropdown]') != null) return;

    let currentDropdown
    if (isDropDownButton){
        currentDropdown = e.target.closest('[data-dropdown]')
        currentDropdown.classList.toggle('active')
    }
    document.querySelectorAll('[data-dropdown].active').forEach( dropdown => {
        if(dropdown === currentDropdown) return;
        dropdown.classList.remove('active')
    })
})

// Modal
const createBtn = document.querySelector('.activate-btn')
const modalForm = document.querySelector('.modal')
const overlay = document.querySelector('.overlay')
createBtn.addEventListener('click', (() => {
    openModal(modalForm)
}))

overlay.addEventListener('click', (() => {
    const modals = document.querySelectorAll('.modal.active')
    modals.forEach((modal)=> {
        closeModal(modal)
    })
}))

function openModal(modal){
    if (modal == null) return
    modal.classList.add('active')
    overlay.classList.add('active')
}

function closeModal(modal){
    if (modal == null) return
    modal.classList.remove('active')
    overlay.classList.remove('active')
}