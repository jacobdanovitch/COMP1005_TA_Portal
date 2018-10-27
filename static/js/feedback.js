var copyFeedback = function () {
    const feedback = document.getElementById("feedback");
    const copyButton = document.getElementById("copyButton");

    copyButton.onclick = function () {
        var textArea = document.createElement('textarea');

        textArea.setAttribute('style', 'width:1px;border:0;opacity:0;');
        textArea.setAttribute('readonly', '');

        document.body.appendChild(textArea);

        textArea.value = feedback.innerHTML;
        textArea.select();

        const success = document.execCommand('copy');
        document.body.removeChild(textArea);

        if (success) {
            copyButton.innerText = "Copied!";
            copyButton.classList.add("positive");
        }
        else {
            copyButton.classList.add("negative");
            alert('Something went wrong!');
        }
    };
};

window.addEventListener("load", copyFeedback);