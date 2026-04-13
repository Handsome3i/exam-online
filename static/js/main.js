document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.option-item').forEach(function(item) {
        item.addEventListener('click', function(e) {
            if (e.target.tagName === 'INPUT') return;
            const input = item.querySelector('input[type="radio"], input[type="checkbox"]');
            if (!input) return;

            if (input.type === 'radio') {
                const name = input.name;
                document.querySelectorAll('.option-item input[name="' + name + '"]').forEach(function(r) {
                    r.closest('.option-item').classList.remove('selected');
                });
                input.checked = true;
                item.classList.add('selected');
            } else {
                input.checked = !input.checked;
                item.classList.toggle('selected', input.checked);
            }
        });
    });

    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.querySelector('.sidebar');
    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('open');
        });
    }
});

function initTimer(seconds, displayEl, formEl) {
    let remaining = seconds;

    function update() {
        const m = Math.floor(remaining / 60);
        const s = remaining % 60;
        displayEl.textContent = String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0');
        if (remaining <= 300) {
            displayEl.classList.add('warning');
        }
        if (remaining <= 0) {
            clearInterval(timer);
            formEl.submit();
            return;
        }
        remaining--;
    }

    update();
    const timer = setInterval(update, 1000);
}
