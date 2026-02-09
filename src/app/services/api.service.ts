import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class ApiService {

  private apiKey = 'GnxfSTv97r1ahChs079le4C3NgEfrpDFaWG1X6zG';

  constructor(private http: HttpClient) {}

  getUser(user: string) {
    const headers = new HttpHeaders({
      'x-api-key': this.apiKey
    });

    const params = new HttpParams().set('user', user);


    return this.http.get('/api/getUser', { headers, params });
  }
}