new Vue({
    el: '#password-checker',
    data: {
        password: '',
        confirmPassword: ''
    },
    computed: {
        passwordsDontMatch() {
            return this.password && this.confirmPassword && this.password !== this.confirmPassword;
        }
    },
    methods: {
        checkPasswords() {
            if (!this.passwordsDontMatch) {
                this.submitForm();
            }
        },
        submitForm() {
            document.querySelector('#password-checker form').submit();
        }
    }
});