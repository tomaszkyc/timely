import {
    addClass,
    addEventHandler,
    elementExists,
    getElementValue,
    removeClass,
    removeElement,
    setElementValue,
    toggleClass
} from "./tools";
import {Cite, CountdownResult} from "./models";
import {Filter, getCountdownResultsService} from "./countdown-results-service";
import {APICiteService} from "./cite-service";

$(async function () {
    // invoke functions after page is loaded
    initCountDownData();
    renderCountdownResultList();
    fetchLatestCountdownResults();

    // setting event handlers
    setEventHandlers();

});

function setEventHandlers() {
    addEventHandler('time-range', 'input', timeCounterOnInput);
    addEventHandler('countdown-button', 'click', timeCounterButtonOnClick);
    addEventHandler('remove-countdown-results-modal-submit', 'click', removeCountdownResults);
}

// variables
var countdown: NodeJS.Timeout | null = null;
var countdownResult: CountdownResult;
const START_THE_COUNTDOWN_LABEL = 'Start the countdown!';
const STOP_THE_COUNTDOWN_LABEL = "Give up!";
const SECOND = 1, MINUTE = 60 * SECOND;
const SECOND_IN_MS = SECOND * 1000, MINUTE_IN_MS = 60 * SECOND_IN_MS;
const COUNTDOWN_RESULT_LOCAL_STORAGE_KEY = 'countdownResults';
const COUNTDOWN_CITE_TEXT_ID = 'countdown-cite-text';
var countdownCiteIntervalObject: NodeJS.Timeout | null = null;
const countdownResultService = getCountdownResultsService();
const citeService = new APICiteService();


function initCountDownData() {
    setElementValue('min-dozens', 6);
    setElementValue('min-unity', 0);
    setElementValue('sec-dozens', 0);
    setElementValue('sec-unity', 0);
}

function timeCounterOnInput(event: Event) {
    if (event) {
        let target = event.target as HTMLInputElement;
        const newNumberOfMinutes = Number.parseInt(target.value);

        const minDozens = parseInt(String(newNumberOfMinutes / 10));
        const minUnity = parseInt(String(newNumberOfMinutes % 10));

        setElementValue('min-dozens', minDozens);
        setElementValue('min-unity', minUnity);
    }
}


async function timeCounterButtonOnClick() {
    const button = document.getElementById('countdown-button');
    const timeRange = document.getElementById('time-range') as HTMLInputElement;

    if (shouldStartCountdown() && button && timeRange) {
        startCountdown();
        countdownResult = new CountdownResult(new Date(), null, false);

        button.innerText = STOP_THE_COUNTDOWN_LABEL;
        timeRange.disabled = true;
        toggleClass('countdown-container', 'countdown-container-expanded');
        addClass('countdown-button', 'custom-btn-warning');
        setTimeout(function () {
            toggleClass('countdown-progressbar-wrapper', 'd-none');
            toggleClass('countdown-cite', 'd-none');
        }, 200);
        startCountdownCiteRefreshing();
    } else {
        stopCountdown();
        countdownResult.finishDate = new Date();


        addCountdownResultToList(countdownResult);
        countdownResultService
            .then(service => service.add(countdownResult))
            .then(() => renderCountdownResultList());

        if (button) {
            button.innerText = START_THE_COUNTDOWN_LABEL;
        }

        timeRange.disabled = false;
        resetToActualTimerangeValue();
        resetProgressBar();

        toggleClass('countdown-container', 'countdown-container-expanded');
        removeClass('countdown-button', 'custom-btn-warning');
        toggleClass('countdown-cite', 'd-none');
        setTimeout(function () {
            toggleClass('countdown-progressbar-wrapper', 'd-none');
        }, 200);
        stopCountdownCiteRefreshing();
    }


}

function updateProgressBar() {
    let totalNumberOfSeconds = getRangeValueInSeconds();
    let actualNumberOfSeconds = getActualTimeCounterValue();

    let progress = 100 - Math.floor((actualNumberOfSeconds * 100) / totalNumberOfSeconds);
    let progressWidthToSet = `${progress}%`;

    const progressBar = document.getElementById('progress-bar');

    if (progress > 10 && progressBar) {
        progressBar.style.width = progressWidthToSet;
    }
    if (progressBar) {
        progressBar.innerText = progressWidthToSet;
    }
}

function resetProgressBar() {
    const progressBar = document.getElementById('progress-bar');
    if (progressBar) {
        progressBar.style.width = '10%';
        progressBar.innerText = '0%';
    }
}

function getRangeValueInSeconds() {
    const timeRange = document.getElementById('time-range') as HTMLInputElement;
    let numberOfMinutes = Number.parseInt(timeRange.value);
    return numberOfMinutes * 60;
}


function resetToActualTimerangeValue() {
    const timeRange = document.getElementById('time-range') as HTMLInputElement;
    const numberOfMinutes = Number.parseInt(timeRange.value);

    let minDozens = Math.floor(numberOfMinutes / 10);
    let minUnity = numberOfMinutes - minDozens * 10;

    setElementValue('min-dozens', minDozens);
    setElementValue('min-unity', minUnity);
    setElementValue('sec-dozens', 0);
    setElementValue('sec-unity', 0);
}

function shouldStartCountdown() {
    const button: HTMLElement | null = document.getElementById('countdown-button');
    if (button) {
        return button.innerText == START_THE_COUNTDOWN_LABEL;
    }
    return false;
}

function startCountdown() {
    makeCountdownStep();
    countdown = setInterval(function () {
        makeCountdownStep();
        updateProgressBar();
    }, 1000);
}

function stopCountdown() {
    if (countdown) {
        clearInterval(countdown);
    }
    countdown = null;
}

function getActualTimeCounterValue() {
    let minDozens = parseInt(getElementValue('min-dozens'));
    let minUnity = parseInt(getElementValue('min-unity'));
    let secDozens = parseInt(getElementValue('sec-dozens'));
    let secUnity = parseInt(getElementValue('sec-unity'));

    let sumOfSeconds = minDozens * 10 * MINUTE
        + minUnity * MINUTE
        + secDozens * 10 * SECOND
        + secUnity * SECOND;
    return sumOfSeconds;
}

/**
 * Makes a 1 second change in countdown.
 */
function makeCountdownStep() {

    let sumOfSeconds = getActualTimeCounterValue();

    if (sumOfSeconds == 0) {
        stopCountdown();
        countdownResult.success = true;
        timeCounterButtonOnClick();
        return;
    }

    sumOfSeconds -= 1; //divide actual one sec

    let mins = Math.floor(sumOfSeconds / MINUTE);
    let minDozens = Math.floor(mins / 10);
    let minUnity = mins - minDozens * 10;

    let seconds = sumOfSeconds - mins * MINUTE;
    let secDozens = Math.floor(seconds / 10);
    let secUnity = seconds - secDozens * 10;

    setElementValue('min-dozens', minDozens);
    setElementValue('min-unity', minUnity);
    setElementValue('sec-dozens', secDozens);
    setElementValue('sec-unity', secUnity);
}

function addCountdownResultToList(countdownResult: CountdownResult) {
    let list = document.getElementById('countdown-results-wrapper');
    if (list) {
        list.children[2].after(countdownResult.asHTMLElement());
    }
}

async function renderCountdownResultList() {
    countdownResultService.then(service => {
        service.getAll(new Filter('all', null, null), 1, 10)
            .then(results => {
                if (results.notEmpty()) {
                    removeClass('countdown-results-wrapper', 'd-none');
                    removeClass('countdown-results', 'm-0');
                } else {
                    addClass('countdown-results-wrapper', 'd-none');
                    addClass('countdown-results', 'm-0');
                }
            })
            .catch(error => {
                addClass('countdown-results-wrapper', 'd-none');
                addClass('countdown-results', 'm-0');
            });
    });
}

async function fetchLatestCountdownResults() {
    countdownResultService.then(service => {
        service.getAll(new Filter('all', null, null), 1, 10)
            .then(results => {
                if (results.notEmpty()) {
                    removeClass('countdown-results-wrapper', 'd-none');
                    // @ts-ignore
                    results.data.reverse().forEach(result => addCountdownResultToList(result))
                } else {
                    addClass('countdown-results-wrapper', 'd-none');
                }
            })
    });
}

async function removeCountdownResults() {
    //hide the container from main page
    addClass('countdown-results-wrapper', 'd-none');
    addClass('countdown-results', 'm-0');

    countdownResultService
        .then(service => service.removeAll());

    //delete data from DOM
    let results = document.getElementsByClassName('countdown-result');
    while (results[0]) {
        let parentNode = results[0].parentNode;
        if (parentNode) {
            parentNode.removeChild(results[0]);
        }
    }
}


function addCountdownCite(citeText = '', shouldRemoveFirst = false) {
    if (shouldRemoveFirst) {
        removeElement(COUNTDOWN_CITE_TEXT_ID);
    }
    let cite = new Cite(citeText, COUNTDOWN_CITE_TEXT_ID);
    const parentElement = document.getElementById('countdown-cite');
    if (parentElement) {
        parentElement.appendChild(cite.asHTMLElement());
    }
}


async function handleCountdownCite() {
    //hide text
    addClass(COUNTDOWN_CITE_TEXT_ID, 'd-none');
    citeService.get().then(data => {

        if (elementExists(COUNTDOWN_CITE_TEXT_ID)) {
            addCountdownCite(data.text, true)
        } else {
            addCountdownCite(data.text, false);
        }
        //at the end show text
        removeClass(COUNTDOWN_CITE_TEXT_ID, 'd-none');
    });
}

async function startCountdownCiteRefreshing() {
    handleCountdownCite();
    countdownCiteIntervalObject = setInterval(
        handleCountdownCite,
        MINUTE_IN_MS
    );
}

function stopCountdownCiteRefreshing() {
    if (countdownCiteIntervalObject) {
        clearInterval(countdownCiteIntervalObject);
    }
}