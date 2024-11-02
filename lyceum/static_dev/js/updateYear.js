document.addEventListener('DOMContentLoaded', function() {
    const currentYearElement = document.getElementById('current-year');
    const serverTimeString = currentYearElement.getAttribute('data-server-time');
    const serverDate = new Date(serverTimeString);
    const localDate = new Date();

    const MILLISECONDS_IN_ONE_DAY = 24 * 60 * 60 * 1000;

    if (Math.abs(localDate - serverDate) < MILLISECONDS_IN_ONE_DAY) {
        currentYearElement.innerText = `© ${localDate.getFullYear()} Мой сайт. Все права защищены.`;
    }
});
