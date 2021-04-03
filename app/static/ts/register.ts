import {Spinner} from "./models";
import {addEventHandler} from "./tools";

$(function () {


    // setting event handlers
    addEventHandler('register-form', 'submit', formSubmit);


});

const FORM_SUBMIT_BTN_ID = 'form-submit-btn';

function formSubmit() {
    let spinner = new Spinner(['spinner-border', 'spinner-border-sm']);
    spinner.addSpinnerToButton(FORM_SUBMIT_BTN_ID, 'Please wait ');
}