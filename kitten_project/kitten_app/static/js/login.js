$(document).ready(function () {
    $('#loginForm').on('submit', function (event) {
        event.preventDefault();
        $.ajax({
            url: $(this).attr('action'),
            method: 'POST',
            data: $(this).serialize(),
            success: function (response) {
                // Показываем сообщение об успешном входе
                showModal("Вы успешно вошли в систему!");
            },
            error: function (xhr, status, error) {
                // Показываем сообщение об ошибке входа
                showModal("Ошибка входа. Проверьте данные и попробуйте снова.");
            }
        });
    });

    function showModal(message) {
        $('#modalMessage').text(message);
        $('#modal').fadeIn();
    }

    $('#modalClose').on('click', function () {
        $('#modal').fadeOut();
    });
});
