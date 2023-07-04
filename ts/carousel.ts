import { select } from './helpers';

export const carouselScript = () => {
    // Hero carousel indicators
    const indicators = select('#hero-carousel-indicators');

    const items = select('#heroCarousel .carousel-item', true);

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
