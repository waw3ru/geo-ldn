import { toggleCSS, handleScrollEffect, onEvent, selectElement } from './util';

const handleCarousel = () => {
    const indicators = selectElement('#hero-carousel-indicators') as Element;
    const items = selectElement(
        '#heroCarousel .carousel-item',
        true
    ) as NodeListOf<Element>;

    items.forEach((item, index) => {
        if (index === 0) {
            indicators.innerHTML +=
                `<li data-bs-target='#heroCarousel' data-bs-slide-to='${index}' class='active'></li>`.trim();
        } else {
            indicators.innerHTML +=
                `<li data-bs-target='#heroCarousel' data-bs-slide-to='${index}'></li>`.trim();
        }
    });
};

const main = () => {
    // toggle header
    window.addEventListener('load', () => toggleCSS('#header', 'header-scrolled'));
    handleScrollEffect(document, () => toggleCSS('#header', 'header-scrolled'));

    // toggle back-to-top
    window.addEventListener('load', () => toggleCSS('.back-to-top', 'active'));
    handleScrollEffect(document, () => toggleCSS('.back-to-top', '.back-to-top'));

    // on mobile scroll
    onEvent('click', '.mobile-nav-toggle', function (e) {
        const el = selectElement('#navbar') as Element;

        el.classList.toggle('navbar-mobile');

        // @ts-expect-error
        this.classList.toggle('bi-list');
        // @ts-expect-error
        this.classList.toggle('bi-x');
    });

    // mobile nav when active
    onEvent(
        'click',
        '.navbar .dropdown > a',
        function (e) {
            const el = selectElement('#navbar') as Element;

            if (el.classList.contains('navbar-mobile')) {
                e.preventDefault();

                // @ts-expect-error
                this.nextElementSibling.classList.toggle('dropdown-active');
            }
        },
        true
    );

    handleCarousel();
};

window.addEventListener('DOMContentLoaded', main);
