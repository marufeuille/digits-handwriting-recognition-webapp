window.onload = () => {

    const send = () => {
        method = $('[name=method]').val();
        console.log(method)
        var canvas = document.getElementsByTagName("canvas")[0];
        data = canvas.toDataURL("image/png")
        var fData = new FormData();
        fData.append('img', data);
        fData.append('method', method)
        $.ajax({
            url: "http://localhost:8080/predict", 
            type: "POST",
            data: fData,
            processData: false,
            contentType: false,
            success: (res, dataType) => {
                $("#result").text(res)
            }
        })
    }
    
    const clear =  () => {
        var canvas = document.getElementsByTagName("canvas")[0];
        ctx = canvas.getContext("2d")
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    }
    
    var imageBoard = new DrawingBoard.Board('main-board', {
        controls: false,
        color: '#000',
        size: 30,
        webStorage: false
    });
    imageBoard.ev.bind('board:stopDrawing', (ev) => {
        send()
    })
    $('[name=method]').change((ev) => {
        send()
    });
    $("#clear").click((ev) => {
        clear()
    })
}