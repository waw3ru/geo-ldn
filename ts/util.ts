export const me = 'you';

export const selectElement = (el: string, all = false) => {
    el = el.trim();
    if (all) {
        return document.querySelectorAll(el);
    } else {
        return document.querySelector(el);
    }
};

export const onEvent = (
    type: string,
    el: string,
    listener: EventListenerOrEventListenerObject,
    all = false
) => {
    let selectEl = selectElement(el, all);
    if (!selectEl) return;

    if (all) {
        (selectEl as NodeListOf<Element>).forEach(e =>
            e.addEventListener(type, listener)
        );
    } else {
        (selectEl as Element).addEventListener(type, listener);
    }
};

export const handleScrollEffect = (
    el: Document,
    listener: EventListenerOrEventListenerObject
) => {
    el.addEventListener('scroll', listener);
};

export const toggleCSS = (el$: string, className: string) => {
    const el = selectElement(el$) as Element;

    if (!el) return;

    if (window.scrollY > 100) {
        el.classList.add(className);
    } else {
        el.classList.remove(className);
    }
};
