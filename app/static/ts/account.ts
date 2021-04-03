import {Spinner} from "./models";
import {addEventHandler, disableElement, enableElement, getElementText, setElementValue} from "./tools";

$(function () {

    addDeleteAccountModalHandler();


    // setting event handlers
    addEventHandler('account-details-form', 'submit', formSubmit);
    addEventHandler(REMOVE_ACCOUNT_EMAIL_INPUT_ID, 'input', verifyEmailsMatch)

});

const FORM_SUBMIT_BTN_ID = 'form-submit-btn';
const REMOVE_ACCOUNT_EMAIL_INPUT_ID = 'remove-account-email';
const REMOVE_ACCOUNT_MODAL_BTN = 'remove-account-modal-submit';
const REMOVE_ACCOUNT_MODAL_ID = 'remove-account-modal';


function formSubmit() {
    let spinner = new Spinner(['spinner-border', 'spinner-border-sm']);
    spinner.addSpinnerToButton(FORM_SUBMIT_BTN_ID, 'Updating ');
}

function verifyEmailsMatch(event: Event) {
    let currentUserEmail = getElementText('current-user-email');
    let givenEmail = (event.target as HTMLInputElement).value;

    if (currentUserEmail && givenEmail
        && currentUserEmail === givenEmail) {
        enableElement(REMOVE_ACCOUNT_MODAL_BTN)
    } else {
        disableElement(REMOVE_ACCOUNT_MODAL_BTN);
    }
}

function addDeleteAccountModalHandler() {
    let deleteAccountModal = document.getElementById(REMOVE_ACCOUNT_MODAL_ID);
    if (deleteAccountModal) {
        deleteAccountModal.addEventListener('show.bs.modal', function (event) {
            setElementValue(REMOVE_ACCOUNT_EMAIL_INPUT_ID, '');
        });
    }

}