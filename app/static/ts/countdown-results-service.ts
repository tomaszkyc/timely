import {CountdownResult} from "./models";
import {getElementValue, isUserAuthenticated} from "./tools";

const COUNTDOWN_RESULT_LOCAL_STORAGE_KEY = 'countdownResults';

export class Filter {
    countdownStatus: string;
    startDate: Date | null;
    finishDate: Date | null;

    constructor(countdownStatus: string, startDate: Date | null, finishDate: Date | null) {
        this.countdownStatus = countdownStatus;
        this.startDate = startDate;
        this.finishDate = finishDate;
    }

    static getFilterFromHTML(): Filter {
        let countdownStatus = getElementValue('filter-countdown-status');
        let startDate = new Date(getElementValue('filter-countdown-date-from'));
        let finishDate = new Date(getElementValue('filter-countdown-date-to'));

        //set default values for start date and finish date
        if (startDate) {
            startDate.setHours(0, 0, 0, 0);
        }
        if (finishDate) {
            finishDate.setHours(23, 59, 59, 999);
        }
        return new Filter(countdownStatus, startDate, finishDate);
    }

}


export class Response<T> {
    totalNumber: number | undefined;
    data: T[] | undefined;

    constructor(totalNumber?: number, data?: T[]) {
        this.totalNumber = totalNumber;
        this.data = data;
    }

    notEmpty(): boolean {
        return !!(this.data && this.data.length > 0);
    }

    empty(): boolean {
        return !this.notEmpty();
    }
}

export enum SortByOrder {
    ASC = "ASC",
    DESC = "DESC"
}

export class SortBy {
    propertyName: string;
    order: SortByOrder;

    constructor(propertyName: string, order: SortByOrder) {
        this.propertyName = propertyName;
        this.order = order;
    }
}

export class Sorter {

    static sort(data: any[], sorters: SortBy[]) {
        sorters.forEach(sorter => {
            data.sort((a, b) => {
                if (sorter.order == SortByOrder.ASC) {
                    return (a[sorter.propertyName] > b[sorter.propertyName]) ? 1 : -1;
                } else {
                    return (a[sorter.propertyName] > b[sorter.propertyName]) ? -1 : 1;
                }
            });
        });
    }

}


export interface CountdownResultsService {
    getAll(filter: Filter, page?: number, pageSize?: number, sorters?: SortBy[]): Promise<Response<CountdownResult>>;

    add(countdownResult: CountdownResult): Promise<boolean>;

    addAll(countdownResults: CountdownResult[]): Promise<boolean>;

    removeAll(): Promise<boolean>;
}


//add a factory pattern for the services

export async function getCountdownResultsService(): Promise<CountdownResultsService> {

    //check for connection with backend
    let userAuthenticated = await isUserAuthenticated();
    console.log(`userAuthenticated: ${userAuthenticated}`);
    if (userAuthenticated) {
        return new Promise((resolve) => {
            resolve(new RemoteCountdownResultsService());
        });
    } else {
        return new Promise((resolve) => {
            resolve(new LocalCountdownResultsService())
        });
    }
}


export class RemoteCountdownResultsService implements CountdownResultsService {
    async getAll(filter: Filter, page?: number, pageSize?: number, sorters?: SortBy[]): Promise<Response<CountdownResult>> {
        //for tests only
        if (!sorters) {
            sorters = [new SortBy('finishDate', SortByOrder.DESC)]
        }
        return $.ajax({
            type: 'GET',
            url: 'api/countdown-result',
            data: {
                data: JSON.stringify({
                        filter: filter,
                        page: page,
                        pageSize: pageSize,
                        sorters: sorters
                    }
                )
            }
        }).then(result => {
            let totalNumber = result['totalNumber'];
            result = (result.data as any[]).map(e => {
                return new CountdownResult(new Date(e['startDate']), new Date(e['finishDate']), e['success'])
            });
            let response = new Response<CountdownResult>(totalNumber, result);
            return new Promise((resolve) => resolve(response))
        });
    }

    async add(countdownResult: CountdownResult): Promise<boolean> {
        return $.ajax({
            type: 'POST',
            url: 'api/countdown-result',
            data: {
                data: JSON.stringify([countdownResult])
            }
        }).then(() => {
            return new Promise((resolve) => resolve(true))
        }).catch(() => {
            return new Promise((resolve, reject) => reject(false))
        });
    }

    async removeAll(): Promise<boolean> {
        return $.ajax({
            type: 'DELETE',
            url: 'api/countdown-result',
        }).then(() => {
            return new Promise((resolve) => resolve(true))
        }).catch(() => {
            return new Promise((resolve, reject) => reject(false))
        });
    }

    addAll(countdownResults: CountdownResult[]): Promise<boolean> {
        // @ts-ignore
        return $.ajax({
            type: 'POST',
            url: 'api/countdown-result',
            data: {
                data: JSON.stringify(countdownResults)
            }
        }).then( () => {
            return new Promise(resolve => resolve(true))
        }).catch((err) => {
            console.error(err);
            return new Promise((resolve, reject) => reject(true))
        });
    }
}

export class LocalCountdownResultsService implements CountdownResultsService {
    async removeAll(): Promise<boolean> {
        // delete data from local storage
        localStorage.clear();
        return new Promise((resolve) => resolve(true));
    }

    async getAll(filter: Filter, page?: number, pageSize?: number, sorters?: SortBy[]): Promise<Response<CountdownResult>> {
        let response = new Response<CountdownResult>();
        let countdownResults: CountdownResult[] = [];
        let localStorageValueSerialized: string | null = localStorage.getItem(COUNTDOWN_RESULT_LOCAL_STORAGE_KEY);
        if (localStorageValueSerialized) {
            let results: any[] = JSON.parse(localStorageValueSerialized);
            for (let i = 0; i < results.length; i++) {
                let result = results[i];
                let countDownResult = new CountdownResult(new Date(result['startDate']),
                    new Date(result['finishDate']),
                    result['success']);
                countdownResults.push(countDownResult);
            }
        }

        //set response total length
        response.totalNumber = countdownResults.length;

        countdownResults = countdownResults.filter(x => {
            if (filter.countdownStatus == 'all') {
                return true
            } else if (filter.countdownStatus == 'success') {
                return x.success
            } else if (filter.countdownStatus == 'failure') {
                return !x.success
            }
        }).filter(x => {
            if (filter.startDate != null) {
                return x.startDate >= filter.startDate;
            }
            return true;
        }).filter(x => {
            if (filter.finishDate != null && x.finishDate) {
                return x.finishDate <= filter.finishDate;
            }
            return true;
        });

        //sort data before pagination
        LocalCountdownResultsService.sortData(countdownResults, sorters);

        //if there is need a pagination
        if (page != null && pageSize != null) {
            let startIndex = (page - 1) * pageSize;
            let endIndex = page * pageSize;
            countdownResults = countdownResults.slice(startIndex, endIndex)
        }


        response.data = countdownResults;
        return response;
    }

    private static sortData(data: CountdownResult[], sorters?: SortBy[]): void {
        // if there is no sorters - lets sort by end date DESC
        if (!sorters) {
            sorters = [];
            sorters.push(new SortBy('finishDate', SortByOrder.DESC))
        }
        Sorter.sort(data, sorters);
    }

    async add(countdownResult: CountdownResult): Promise<boolean> {
        let localStorageValueSerialized: string | null = localStorage.getItem(COUNTDOWN_RESULT_LOCAL_STORAGE_KEY);
        let results: CountdownResult[] = [];

        if (localStorageValueSerialized) {
            results = JSON.parse(localStorageValueSerialized);

            results.push(countdownResult);
            localStorage.setItem(COUNTDOWN_RESULT_LOCAL_STORAGE_KEY, JSON.stringify(results));
        } else {
            results.push(countdownResult);
            localStorage.setItem(COUNTDOWN_RESULT_LOCAL_STORAGE_KEY, JSON.stringify(results));
        }
        return true;
    }

    addAll(countdownResults: CountdownResult[]): Promise<boolean> {
        return Promise.resolve(false);
    }

}