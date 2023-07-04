import { select } from './helpers';
import { carouselScript } from './carousel';
import { navbarScript } from './navbar';

(function () {
    // Toggle .header-scrolled class to #header when page is scrolled
    const selectHeader = select('#header');

    if (selectHeader) {
        const headerScrolled = () => {
            if (window.scrollY > 50) {
                selectHeader.classList.add('header-scrolled');
            } else {
                selectHeader.classList.remove('header-scrolled');
            }
        };

        window.addEventListener('load', headerScrolled);
        window.addEventListener('scroll', headerScrolled);
    }

    // Back to top button
    const backtotop = select('.back-to-top');

    if (backtotop) {
        const toggleBacktotop = () => {
            if (window.scrollY > 100) {
                backtotop.classList.add('active');
            } else {
                backtotop.classList.remove('active');
            }
        };

        window.addEventListener('load', toggleBacktotop);
        window.addEventListener('scroll', toggleBacktotop);
    }

    navbarScript();

    carouselScript();
})();
