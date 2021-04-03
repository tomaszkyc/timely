import {addEventHandler} from "./tools";
import {Spinner} from "./models";

$(function () {
    // setting event handlers
    addEventHandler('password-reset-form', 'submit', formSubmit);
});

const FORM_SUBMIT_BTN_ID = 'form-submit-btn';

function formSubmit() {
    let spinner = new Spinner(['spinner-border', 'spinner-border-sm']);
    spinner.addSpinnerToButton(FORM_SUBMIT_BTN_ID, 'Please wait ');
}