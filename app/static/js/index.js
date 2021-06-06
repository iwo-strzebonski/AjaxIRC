Array.range = (start, end) => { return [...Array(end - start).keys()].map(i => i + start) }

$(function() {
    document.getElementById('message').value = ''
    $('#messages').overlayScrollbars({ 
        resize: 'v',
        sizeAutoCapable: true,
        paddingAbsolute: true,
        scrollbars: { clickScrolling : true }
    })

    // eslint-disable-next-line no-var
    var user = window.prompt('Podaj swój nick')

    while (user === null || user.length === 0) {
        user = window.prompt('Podaj swój nick')
    }

    document.getElementById('form').onsubmit = function() {
        let message = document.getElementById('message').value
        if (message === '') return
        let formData = new FormData()
        formData.append('user', user)

        let xhr = new XMLHttpRequest()

        if (message === '/quit') {
            xhr.open('POST', location.href + 'quit')
            location.reload()
        } else if (message.indexOf('/nick') !== -1) {
            formData.append('new', message.substr(message.indexOf(' ') + 1))
            user = message.substr(message.indexOf(' ') + 1)
            xhr.open('POST', location.href + 'nick')
        } else if (message.indexOf('/color') !== -1) {
            formData.append('color', message.substr(message.indexOf(' ') + 1))
            xhr.open('POST', location.href + 'color')
        } else {
            formData.append('message', message)
            xhr.open('POST', location.href + 'send')
        }

        xhr.send(formData)
        document.getElementById('message').value = ''
    }

    var lastMessage = new Date().getTime()

    function addMessage(message) {
        if (message.time > lastMessage) {
            let span = $('<span>')
            let date = $('<span>')
                .append('[' + new Date(message.time).toString().substr(16, 8) + ']')

            let user = $('<span>')
                .append(' &lt;@' + message.user + '&gt; ')
                .css('color', message.color)

            let msg = $('<span>')
                .append(message.message)
            
            msg.emoticonize()

            span.append(date)
            span.append(user)
            span.append(msg)
            $('.os-content').append(span)
            $('.os-content').append($('<br>'))
        }
    }

    function update() {
        $.ajax({
            url: '/data-update',
            success:  function(data) {
                let messages = data.content.split('\n')
                for (let i in messages) if (messages[i] !== '') addMessage(JSON.parse(messages[i]))
                lastMessage = JSON.parse(messages[messages.length - 2]).time
                update()
            },
            timeout: 500000
        })
    }

    update()
})
