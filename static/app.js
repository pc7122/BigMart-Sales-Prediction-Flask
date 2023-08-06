function onPageLoad() {
    console.log("document loaded");
    const url = "/get-outlets";

    $.post(url, function (data, status) {
        if (data) {
            console.log(data.outlets);
            let outlets = data.outlets;
            $('#outlets').empty();
            $('#outlets').append(new Option("Choose", "", true));
            for (let i in outlets) {
                let opt = new Option(outlets[i], i);
                $('#outlets').append(opt);
            }
            $('#outlets option').first().attr('disabled', 'disabled');
        }
    });
}

window.onload = onPageLoad;