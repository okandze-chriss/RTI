let btn = document.getElementById('nbox-close')

btn.addEventListener('click', ()=>{
    let container = document.querySelector('.nbox-container');
    container.style.display = 'none';
})
window.onload = ()=>{
    document.querySelector('.nbox-container').animate(
    [
        { transform: 'translateX(600px)' },
        { transform: 'translateX(0px)' },
    ],
     {
        duration: 1000,
      }
    );
}