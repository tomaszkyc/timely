import {createUUID} from "./tools";

export function pad(number: number, size: number): string {
    let s = String(number);
    while (s.length < (size || 2)) {
        s = "0" + s;
    }
    return s;
}

function formatDate(date: Date): string {
    let year = date.getFullYear();
    let month = pad(date.getMonth() + 1, 2);
    let dayOfMonth = pad(date.getDate(), 2);
    let hour = pad(date.getHours(), 2);
    let minute = pad(date.getMinutes(), 2);
    let second = pad(date.getSeconds(), 2);
    return `${year}-${month}-${dayOfMonth} ${hour}:${minute}:${second}`;
}


interface HTMLElementCreator {
    asHTMLElement(): HTMLElement;
}


export class CountdownResult implements HTMLElementCreator {
    startDate: Date;
    finishDate: Date | null;
    success: boolean;

    constructor(startDate: Date, finishDate: Date | null, success: boolean) {
        this.startDate = startDate;
        this.finishDate = finishDate;
        this.success = success;
    }

    public getTotalSeconds(): number {
        if (this.finishDate == null) {
            this.finishDate = new Date();
        }
        return Math.round((this.finishDate.getTime() - this.startDate.getTime()) / 1000);
    }

    public formatTotalTime(): string {
        let totalSeconds = this.getTotalSeconds();
        let minutes = Math.floor(totalSeconds / 60);
        let seconds = totalSeconds - minutes * 60;
        let formattedTime: string;
        if (minutes != 0) {
            formattedTime = `${minutes} min ${seconds} s`;
        } else {
            formattedTime = `${seconds}s`;
        }
        return formattedTime;
    }

    public asHTMLElement(): HTMLElement {
        //create element
        let element = document.createElement('div');
        element.classList.add('countdown-result')

        //adding icon
        let icon = document.createElement('i');
        if (this.success) {
            icon.classList.add('fas', 'fa-check-circle', 'fa-2x');
            icon.classList.add('countdown-result-icon-success');
        } else {
            icon.classList.add('fas', 'fa-stop-circle', 'fa-2x');
            icon.classList.add('countdown-result-icon-failure');
        }
        element.appendChild(icon);

        //adding results details
        let details = document.createElement('div');
        details.classList.add('countdown-result-details');
        details.appendChild(document.createTextNode(`Start date: ${formatDate(this.startDate)}`));
        if (this.finishDate) {
            details.appendChild(document.createElement('br'));
            details.appendChild(document.createTextNode(`End date: ${formatDate(this.finishDate)}`));
        }
        details.appendChild(document.createElement('br'));
        details.appendChild(document.createTextNode(`You were focused ${this.formatTotalTime()}`));
        element.appendChild(details);

        //return element
        return element;
    }

}

export class Cite implements HTMLElementCreator {
    text: string;
    id: string;

    constructor(text: string = '', id: string = '') {
        this.text = text;
        this.id = id;
    }

    public asHTMLElement(): HTMLElement {
        let cite = document.createElement('cite');
        cite.id = this.id;
        cite.appendChild(document.createTextNode(this.text));
        return cite;
    }
}

export class Spinner implements HTMLElementCreator {
    classes: string[];
    spinnerId: string;
    previousButtonText: string = '';
    buttonId: string | null = null;

    constructor(classes: string[] = []) {
        this.classes = classes;
        this.spinnerId = createUUID();
    }

    public asHTMLElement(): HTMLElement {
        //creating new spinner span
        let spinner = document.createElement('span');
        spinner.id = this.spinnerId;

        //adding styles
        spinner.classList.add(...this.classes);

        //adding attributes
        spinner.setAttribute('role', 'status');
        spinner.setAttribute('aria-hidden', 'true');

        return spinner;
    }

    addSpinnerToButton(buttonId: string, newText: string): void {
        this.buttonId = buttonId;
        const element = document.getElementById(this.buttonId);
        if (element) {
            //get actual element text
            this.previousButtonText = element.innerText;
            element.innerText = newText;
            element.appendChild(this.asHTMLElement());
        }
    }

    removeSpinnerFromButton(): void {
        if (!this.buttonId) {
            throw new Error('Given spinner is not used anywhere so it cannot be deleted.');
        }
        const element = document.getElementById(this.buttonId);
        if (element && element.hasChildNodes()) {
            //set previous button text
            element.innerText = this.previousButtonText;

            //remove spinner
            for(let idx = 0; idx < element.children.length; idx++) {
                let childElement = element.children[idx];
                if (childElement.id == this.spinnerId) {
                    element.removeChild(childElement);
                    break;
                }
            }
        }
    }
}

export class PaginationBar implements HTMLElementCreator {
    numberOfElements: number;
    pageSize: number;
    currentPageNumber: number | undefined;
    onClickCallback: any;
    numberOfPages: number;

    constructor(numberOfElements: number, pageSize: number, currentPageNumber?: number,
                onClickCallback?: any) {
        this.numberOfElements = numberOfElements;
        this.pageSize = pageSize;
        this.currentPageNumber = currentPageNumber;
        this.onClickCallback = onClickCallback;
        this.numberOfPages = Math.ceil(this.numberOfElements / this.pageSize);
    }

    asHTMLElement(): HTMLElement {

        let nav = document.createElement('nav');
        nav.id = 'pagination-nav';
        nav.classList.add('pagination-nav');

        let listOfPaginationElements = document.createElement('ul');
        listOfPaginationElements.classList.add('pagination', 'justify-content-center');


        if (this.numberOfPages > 0) {

            //create 'previous' element
            let previousPaginationElement = this.createPreviousPaginationElement();
            listOfPaginationElements.appendChild(previousPaginationElement);

            for (let idx = 0; idx < this.numberOfPages; idx++) {

                let isActiveItem = (idx + 1) == this.currentPageNumber;

                let paginationElement = this.createPaginationElement(String(idx + 1), false, isActiveItem);
                listOfPaginationElements.appendChild(paginationElement);
            }

            //create 'next' element
            let nextPaginationElement = this.createNextPaginationElement();
            listOfPaginationElements.appendChild(nextPaginationElement);
        }

        nav.appendChild(listOfPaginationElements);
        return nav;
    }

    createPaginationElement(text: string, disabled: boolean, active: boolean): HTMLElement {
        let listItem = document.createElement('li');
        listItem.classList.add('page-item', 'user-select-none', 'pagination-nav-element');
        if (disabled) {
            listItem.classList.add('disabled');
        }
        if (active) {
            listItem.classList.add('active');
        }

        let link = document.createElement('a');
        link.classList.add('page-link')
        link.href = '#';
        link.innerText = text;

        listItem.appendChild(link);

        //events
        listItem.addEventListener('click', this.onClickCallback);


        return listItem;
    }

    createPreviousPaginationElement(): HTMLElement {
        let previousPaginationElement = undefined;
        if (this.currentPageNumber && this.currentPageNumber > this.numberOfPages) {
            previousPaginationElement = this.createPaginationElement('Previous', false, false);
        } else {
            previousPaginationElement = this.createPaginationElement('Previous', true, false);
        }
        return previousPaginationElement;
    }

    createNextPaginationElement(): HTMLElement {
        let paginationElement = undefined;
        if (this.currentPageNumber && this.currentPageNumber < this.numberOfPages) {
            paginationElement = this.createPaginationElement('Next', false, false);
        } else {
            paginationElement = this.createPaginationElement('Next', true, false);
        }
        return paginationElement;
    }

    static setActivePage(elementId: string, pageNumber: number): void {
        const element = document.getElementById(elementId);
        if (!element) {
            return;
        }
        let paginationElements = element.querySelectorAll(".page-item");


        for (let i = 0; i < paginationElements.length; i++) {
            let paginationElement = paginationElements[i];
            //first remove active class
            paginationElement.classList.remove('active');

            //if a element text matches the page number - mark as active
            let currentPaginationElementValue = (paginationElement.firstElementChild as HTMLInputElement).textContent;
            if (String(pageNumber) == currentPaginationElementValue) {
                paginationElement.classList.add('active');

                //we also need to cover enabling / disabling the 'previous' / 'next' buttons
                let previousElement = paginationElements[i - 1];
                let previousElementValue = previousElement.textContent;
                if (previousElementValue != 'Previous') {
                    this.enablePaginationElement(elementId, 'Previous');
                } else {
                    this.disablePaginationElement(elementId, 'Previous');
                }

                let nextElement = paginationElements[i + 1];
                let nextElementValue = nextElement.textContent;
                if (nextElementValue != 'Next') {
                    this.enablePaginationElement(elementId, 'Next');
                } else {
                    this.disablePaginationElement(elementId, 'Next');
                }
            }
        }
    }

    static getActivePage(elementId: string): number | null {
        const element = document.getElementById(elementId);
        if (!element) {
            return null;
        }
        let paginationElements = element.querySelectorAll(".page-item");

        let activePage = null;

        for (let i = 0; i < paginationElements.length; i++) {
            let element1 = paginationElements[i];

            if (element1.classList.contains('active')) {
                let currentElementPageValue = (element1.firstElementChild as HTMLInputElement).textContent;
                if (currentElementPageValue) {
                    activePage = Number.parseInt(currentElementPageValue);
                    break;
                }
            }
        }
        return activePage;
    }

    static enablePaginationElement(elementId: string, paginationElementValue: string | number) {
        if (typeof paginationElementValue === "number") {
            paginationElementValue = String(paginationElementValue)
        }
        const element = document.getElementById(elementId);
        if (!element) {
            return null;
        }
        let paginationElements = element.querySelectorAll(".page-item");
        for (let i = 0; i < paginationElements.length; i++) {
            let element1 = paginationElements[i];
            let value = element1.textContent;
            if (element1.classList.contains('disabled') && value && value == paginationElementValue) {
                element1.classList.remove('disabled');
                break;
            }
        }
    }

    static disablePaginationElement(elementId: string, paginationElementValue: string | number) {
        if (typeof paginationElementValue === "number") {
            paginationElementValue = String(paginationElementValue)
        }
        const element = document.getElementById(elementId);
        if (!element) {
            return null;
        }
        let paginationElements = element.querySelectorAll(".page-item");
        for (let i = 0; i < paginationElements.length; i++) {
            let element1 = paginationElements[i];
            let value = element1.textContent;
            if (value && value == paginationElementValue) {
                element1.classList.add('disabled');
                break;
            }
        }
    }

    static getNumberOfPages(elementId: string): number {
        const element = document.getElementById(elementId);
        if (!element) {
            return 0;
        }
        let paginationElements = element.querySelectorAll(".page-item");
        //subtract 2 because these are 'previous' and
        //'next' elements
        //Also we using max if there will be 0 it will return 0
        //if there will be more elements it will return correct number
        return Math.max(0, paginationElements.length - 2);
    }
}