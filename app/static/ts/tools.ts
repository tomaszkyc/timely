import {pad} from "./models";

export function elementExists(elementId: string) {
    return document.getElementById(elementId) != null;
}

export function removeElement(elementId: string) {
    const element: HTMLElement | null = document.getElementById(elementId);
    if (element) {
        let parentNode = element.parentNode;
        if (parentNode) {
            parentNode.removeChild(element);
        }
    }
}

export function removeAllElementChildren(elementId: string) {
    const element = document.getElementById(elementId);
    if (element) {
        while (element.hasChildNodes()) {
            // @ts-ignore
            element.removeChild(element.firstChild);
        }
    }
}

export function toggleClass(elementId: string, ...classNames: string[]) {
    const element = document.getElementById(elementId);
    if (element) {
        classNames.forEach(className => element.classList.toggle(className));
    }
}

export function addClass(elementId: string, ...classNames: string[]) {
    const element = document.getElementById(elementId);
    if (element) {
        element.classList.add(...classNames);
    }
}

export function removeClass(elementId: string, ...classNames: string[]) {
    const element = document.getElementById(elementId);
    if (element) {
        element.classList.remove(...classNames);
    }
}


export function setElementValue(elementId: string, value: any) {
    const element = document.getElementById(elementId) as HTMLInputElement;
    if (element) {
        element.value = value;
    }
}

export function getElementValue(elementId: string): string {
    const element = document.getElementById(elementId) as HTMLInputElement;
    return element.value;
}

export function getElementText(elementId: string): string | null {
    const element = document.getElementById(elementId) as HTMLInputElement;
    return element.textContent;
}

export function addEventHandler(elementId: string, eventType: string, callback: any): void {
    const element = document.getElementById(elementId);
    if (element) {
        element.addEventListener(eventType, callback);
    }
}

export function disableElement(elementId: string): void {
    const element = document.getElementById(elementId) as HTMLInputElement;
    element.disabled = true;
}

export function enableElement(elementId: string): void {
    const element = document.getElementById(elementId) as HTMLInputElement;
    element.disabled = false;
}

export async function isUserAuthenticated(): Promise<any> {
    let isUserAuthenticated = $.ajax({
        url: 'api/user/authenticated',
        type: 'GET'
    });
    return isUserAuthenticated;
}

export function canConnectToAPI(): boolean {
    let canConnect = false;
    $.ajax({
        url: 'api/status',
        type: 'GET',
        async: false,
        success: data => canConnect = true
    });
    return canConnect;
}

export function formatDateAsStandardString(date: Date): string {
    let year = date.getFullYear();
    let month = pad(date.getMonth() + 1, 2);
    let dayOfMonth = pad(date.getDate(), 2);
    return `${year}-${month}-${dayOfMonth}`;
}

export function subtractFromDate(date: Date, days: number): Date {
    let numberOfMiliseconds = days * 24 * 60 * 60 * 1000;
    return new Date(date.getTime() - numberOfMiliseconds)
}

export function getNoDataDialog(): HTMLElement {
    const element = document.createElement('p');
    element.appendChild(document.createTextNode('There is no data matching your filter criteria.'));
    return element;
}

//source: https://www.w3resource.com/javascript-exercises/javascript-math-exercise-23.php
export function createUUID(): string {
    var dt = new Date().getTime();
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = (dt + Math.random() * 16) % 16 | 0;
        dt = Math.floor(dt / 16);
        return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
    return uuid;
}

export async function showToast(toast: any, timeout?: number) {
    if (!timeout) {
        timeout = 2000;
    }
    setTimeout(() => toast.show(), timeout);
}

export async function hideToast(toast: any, timeout?: number) {
    if (!timeout) {
        timeout = 2000;
    }
    setTimeout(() => toast.hide(), timeout);
}