document.addEventListener('DOMContentLoaded', function() {
    const itemTypeField = document.querySelector('#id_item_type');
    const serverPcFields = ['#id_server_pc', '#id_username', '#id_password'];
    const staffFields = ['#id_last_name', '#id_first_name', '#id_position'];
    const usefulPhoneFields = ['#id_description', '#id_contact_phone'];
    const phoneCodeFields = ['#id_phone_code', '#id_phone_function'];

    function hideAllFields() {
        [...serverPcFields, ...staffFields, ...usefulPhoneFields, ...phoneCodeFields].forEach(function(field) {
            document.querySelector(field).closest('.form-row').style.display = 'none';
        });
    }

    function showFields(fields) {
        fields.forEach(function(field) {
            document.querySelector(field).closest('.form-row').style.display = '';
        });
    }

    function handleFieldVisibility() {
        const value = itemTypeField.value;
        hideAllFields();
        if (value === 'computers' || value === 'pyrseia' || value === 'applications') {
            showFields(serverPcFields);
        } else if (value === 'staff') {
            showFields(staffFields);
        } else if (value === 'useful_phones') {
            showFields(usefulPhoneFields);
        } else if (value === 'phone_codes') {
            showFields(phoneCodeFields);
        }
    }

    itemTypeField.addEventListener('change', handleFieldVisibility);
    handleFieldVisibility(); // Να τρέχει κατά την αρχική φόρτωση
});
