

export interface CiteService {
    get(): Promise<string>;
}

export class APICiteService implements CiteService {
    async get(): Promise<any> {
        let cite = $.ajax({
            url: '/api/cite',
            type: 'GET'
        });
        return cite;
    }

}