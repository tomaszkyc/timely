import {
    Filter,
    getCountdownResultsService,
    LocalCountdownResultsService,
    RemoteCountdownResultsService
} from "./countdown-results-service";
import {
    addClass,
    addEventHandler,
    disableElement,
    enableElement,
    formatDateAsStandardString,
    getNoDataDialog,
    hideToast,
    removeAllElementChildren,
    removeClass,
    setElementValue,
    subtractFromDate
} from "./tools";
import {CountdownResult, PaginationBar, Spinner} from "./models";


$(async function () {
    initFilterForm();
    await fetchInitialData();
    setEventHandlers();
});

const countdownResultService = getCountdownResultsService();

function setEventHandlers() {
    addEventHandler('remove-countdown-results-modal-submit', 'click', removeCountdownResults);
    addEventHandler('filter-countdown-btn', 'click', clickFilterButtonHandler);
    addEventHandler('sync-countdown-results-btn', 'click', syncCountdownResultsButtonHandler);
}

async function syncCountdownResultsButtonHandler() {

    let localCountdownResultsService = new LocalCountdownResultsService();
    localCountdownResultsService.getAll(new Filter('all', null, null), 1, 10000000).then(response => {
        if (response.notEmpty() && response.data) {
            // @ts-ignore
            let startSyncToast = new bootstrap.Toast(document.getElementById('sync-countdown-results-toast'), {delay: 10000000});
            startSyncToast.show();
            let results = response.data;
            let remoteCountdownResultsService = new RemoteCountdownResultsService();
            remoteCountdownResultsService.addAll(results).then(() => {
                // @ts-ignore
                let toast = new bootstrap.Toast(document.getElementById('sync-countdown-results-toast-success'), {delay: 10000});
                toast.show();

                //hide other toast
                hideToast(startSyncToast);
            }).catch(() => {
                // @ts-ignore
                let toast = new bootstrap.Toast(document.getElementById('sync-countdown-results-toast-failure'), {delay: 10000});
                toast.show();
                //hide other toast
                hideToast(startSyncToast);
            });
        } else {
            // @ts-ignore
            let toast = new bootstrap.Toast(document.getElementById('sync-countdown-results-toast-no-data-to-sync'), {delay: 10000});
            toast.show();

        }
    }).catch(err => {
        console.error(err);
    });

    await syncFromServerToLocalStorage();
}

async function syncFromServerToLocalStorage() {
    let localCountdownResultsService = new LocalCountdownResultsService();
    let remoteCountdownResultsService = new RemoteCountdownResultsService();

    //fetch data from API
    return remoteCountdownResultsService.getAll(new Filter('all', null, null), 1, 10).then(response => {
        if (response.notEmpty()) {
            //delete data from local storage
            localCountdownResultsService.removeAll().then(() => {
                // @ts-ignore
                return localCountdownResultsService.addAll(response.data)
            })
        } else {
            return new Promise((resolve, reject) => reject(false))
        }
    });

}

async function removeCountdownResults() {
    countdownResultService.then(service => {
        service.removeAll().then(() => {
            removeAllElementChildren('countdown-results');
            removeAllElementChildren('countdown-results-pagination');

            fetchInitialData();
        })
    })
}

function clickPaginationElementHandler(event: Event): void {
    const element = event.target as HTMLElement;
    const currentPage = PaginationBar.getActivePage('pagination-nav');
    const numberOfPages = PaginationBar.getNumberOfPages('pagination-nav');
    if (element && currentPage) {
        let elementValue = element.textContent;
        if (!elementValue) {
            return;
        }

        if (elementValue == 'Previous') {
            elementValue = String(currentPage - 1);
        } else if (elementValue == 'Next') {
            elementValue = String(currentPage + 1);
        }


        let selectedPage = parseInt(elementValue);
        // if clicked element is a number
        // and it's not the current page
        if (selectedPage != currentPage
            && selectedPage >= 1
            && selectedPage <= numberOfPages) {

            //create filter
            let filter = Filter.getFilterFromHTML();

            //query results
            countdownResultService.then(service => {
                service.getAll(filter, selectedPage, 10).then(response => {
                    //clear actual ones
                    removeAllElementChildren('countdown-results');

                    //add new ones
                    if (response.notEmpty()) {
                        // @ts-ignore
                        response.data.forEach(element => addCountdownResultToList(element));

                        //change active page
                        PaginationBar.setActivePage('pagination-nav', selectedPage);
                    } else {
                        let noDataDialog = getNoDataDialog();
                        let divWithPagination = document.getElementById('countdown-results-pagination');
                        if (divWithPagination) {
                            divWithPagination.appendChild(noDataDialog);
                        }
                    }
                }).catch(() => {
                    //clear actual ones
                    removeAllElementChildren('countdown-results');
                    let noDataDialog = getNoDataDialog();
                    let divWithPagination = document.getElementById('countdown-results-pagination');
                    if (divWithPagination) {
                        divWithPagination.appendChild(noDataDialog);
                    }
                });
            })

        }
    }
}

async function fetchInitialData() {
    countdownResultService.then(service => {
        service.getAll(new Filter('all', null, null), 1, 10)
            .then(results => {
                if (results.notEmpty()) {
                    renderCountdownResultList(true);
                    // @ts-ignore
                    results.data.forEach(result => addCountdownResultToList(result));

                    //enable button to remove activities
                    enableElement('remove-countdown-results-btn');
                }

                if (results.notEmpty()) {
                    //render pagination bar
                    // @ts-ignore
                    let paginationBar = new PaginationBar(results.totalNumber,
                        10, 1, clickPaginationElementHandler);

                    let divWithPagination = document.getElementById('countdown-results-pagination');
                    if (divWithPagination) {
                        divWithPagination.appendChild(paginationBar.asHTMLElement());
                    }
                }

                if (results.empty()) {
                    let noDataDialog = getNoDataDialog();
                    let divWithPagination = document.getElementById('countdown-results-pagination');
                    if (divWithPagination) {
                        divWithPagination.appendChild(noDataDialog);
                    }
                    //disable button to remove activities
                    disableElement('remove-countdown-results-btn');
                }
            });
    });
}

function renderCountdownResultList(visible: boolean) {
    if (visible) {
        removeClass('countdown-results', 'd-none');
    } else {
        addClass('countdown-results', 'd-none');
    }
}

function addCountdownResultToList(countdownResult: CountdownResult) {
    let list = document.getElementById('countdown-results');
    if (list) {
        list.appendChild(countdownResult.asHTMLElement());
    }
}

function initFilterForm() {
    let now = new Date();
    now.setHours(23, 59, 59);
    let dateFrom = subtractFromDate(now, 30);
    setElementValue('filter-countdown-date-from', formatDateAsStandardString(dateFrom));
    setElementValue('filter-countdown-date-to', formatDateAsStandardString(now));
}

async function clickFilterButtonHandler(event: Event) {
    //add spinner
    let spinner = new Spinner(['spinner-border', 'spinner-border-sm']);
    let target = event.target as HTMLElement;
    if (target) {
        spinner.addSpinnerToButton(target.id, 'Please wait ');
    }

    let filter = Filter.getFilterFromHTML();

    countdownResultService.then(service => {
        service.getAll(filter, 1, 10).then(
            results => {

                if (results.notEmpty()) {
                    removeAllElementChildren('countdown-results');
                    renderCountdownResultList(true);
                    // @ts-ignore
                    results.data.forEach(result => addCountdownResultToList(result));

                    //enable button to remove activities
                    enableElement('remove-countdown-results-btn');
                } else {
                    renderCountdownResultList(true);
                    removeAllElementChildren('countdown-results');

                    //disable button to remove activities
                    disableElement('remove-countdown-results-btn');
                }

                //remove pagination bar
                removeAllElementChildren('countdown-results-pagination');

                if (results.notEmpty()) {
                    //render pagination bar
                    // @ts-ignore
                    let paginationBar = new PaginationBar(results.totalNumber,
                        10, 1, clickPaginationElementHandler);


                    let divWithPagination = document.getElementById('countdown-results-pagination');
                    if (divWithPagination) {
                        divWithPagination.appendChild(paginationBar.asHTMLElement());
                    }
                } else {
                    let noDataDialog = getNoDataDialog();
                    let divWithPagination = document.getElementById('countdown-results-pagination');
                    if (divWithPagination) {
                        divWithPagination.appendChild(noDataDialog);
                    }
                }

                //remove spinner
                spinner.removeSpinnerFromButton();
            }
        ).catch(() => {
            //remove spinner
            spinner.removeSpinnerFromButton();
        })
    });
    //remove spinner
    spinner.removeSpinnerFromButton();
}
