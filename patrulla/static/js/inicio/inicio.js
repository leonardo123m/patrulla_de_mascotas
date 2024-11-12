var tl = gsap.timeline({
    scrollTrigger: {
        trigger: ".misyvi",
        start: "0% 80%",  // Ajusta el inicio del trigger para que la animación comience más suavemente
        end: "100% 10%",  // Aumenta el rango de desplazamiento
        scrub: 1.5,       // Agrega un scrub más lento para mayor suavidad
    }
});

tl.to("#imag", {
    top: "135%",
    left: "12%",
    rotate: "30deg",
    ease: "power1.out", 
}, 'imag');

tl.to("#imag", {
    top: "225%",
    left: "5%",
    rotate: "30deg",
    ease: "power1.out",
}, 'otraEtapa');

tl.to("#imag", {
    top: "230%",
    left: "-52%",
    rotate: "0deg",
    ease: "power1.out",
}, 'otraEtapa2');

tl.to("#imag", {
    top: "270%",
    left: "-40%",
    rotate: "-30deg",
    ease: "power3.out",
}, 'otraEtapa3');

tl.to("#imag", {
    top: "310%",
    left: "-40%",
    rotate: "0deg",
    ease: "power1.out",
    
}, 'otraEtapa4');



let nextButton = document.getElementById('next');
let prevButton = document.getElementById('prev');
let backButton = document.getElementById('back');
let seemoreButton = document.querySelectorAll('.seemore');
let carousel = document.querySelector('.carousel');
let listHTML = document.querySelector('.carousel .list');

nextButton.onclick = function() {
    showSlider('next');
}
prevButton.onclick = function() {
    showSlider('prev');
}
let unAcceptClick;
const showSlider = (type) => {
    nextButton.style.pointerEvents = 'none';
    prevButton.style.pointerEvents = 'none';

    carousel.classList.remove('prev', 'next');
    let items = document.querySelectorAll('.carousel .list .item');
    if(type === 'next') {
        listHTML.appendChild(items[0]);
        carousel.classList.add('next');
    }
    else{
        let positionLast = items.length -1;
        listHTML.prepend(items[positionLast]);
        carousel.classList.add('prev');
    }
    clearTimeout(unAcceptClick);
    unAcceptClick = setTimeout(() => {
        nextButton.style.pointerEvents = 'auto';
        prevButton.style.pointerEvents = 'auto';
    }, 2000);
}

seemoreButton.forEach(button => {
    button.onclick = function(){
        carousel.classList.add('showDetail');
    }
})
backButton.onclick = function() {
    carousel.classList.remove('showDetail');
}