var cubeShare = {
    title: '',
    width: 600,
    height: 400,

    init: function() {
        var share = document.querySelectorAll('.share-btn');
        for(var i = 0, l = share.length; i < l; i++) {
            var url = share[i].getAttribute('data-url') || location.href,
                title = share[i].getAttribute('data-title') || '',
                desc = share[i].getAttribute('data-desc') || '',
                img = share[i].getAttribute('data-img') || '',
                el = share[i].querySelectorAll('a');

            for(var a = 0, al = el.length; a < al; a++) {
                var id = el[a].getAttribute('data-id');
                if(id)
                    this.addEventListener(el[a], 'click', {id: id, url: url, title: title, desc: desc, img: img});
            }
        }
    },

    addEventListener: function(el, eventName, opt) {

        var _this = this, handler = function() {
            _this.share(opt.id, opt.url, opt.title, opt.desc, opt.img);
        };

        if(el.addEventListener) {
            el.addEventListener(eventName, handler);
        } else {
            el.attachEvent('on' + eventName, function() {
                handler.call(el);
            });
        }
    },

    share: function(id, url, title, desc, img) {
        url = encodeURIComponent(url);
        desc = encodeURIComponent(desc);
        title = encodeURIComponent(title);
        img = encodeURIComponent(img);

        switch(id) {
            case 'fb':
                this.popupCenter('https://www.facebook.com/sharer/sharer.php?u=' + url, this.title, this.width, this.height);
                break;

            case 'vk':
                this.popupCenter('https://vk.com/share.php?' +
                            'url=' + url +
                            '&title=' + title +
                            '&description=' + desc +
                            '&image=' + img,
                    this.title, this.width, this.height);
                break;

            case 'tw':
                var text = title || desc || '';
                if(title.length > 0 && desc.length > 0)
                    text = title + ' - ' + desc;
                if(text.length > 0)
                    text = '&text=' + text;

                this.popupCenter('https://twitter.com/intent/tweet?url=' + url + text, this.title, this.width, this.height);
                break;

            case 'gp':
                this.popupCenter('https://plus.google.com/share?url=' + url, this.title, this.width, this.height);
                break;

            case 'in':
                this.popupCenter('https://www.linkedin.com/shareArticle?mini=true&url=' + url, this.title, this.width, this.height);
                break;

            case 'mail':
                var text = title || desc || '';
                if(title.length > 0 && desc.length > 0)
                    text = title + ' - ' + desc;
                if(text.length > 0)
                    text = text + ' / ';
                if(title.length > 0)
                    title = title + ' / ';

                var mail = 'mailto:?Subject=' + title + this.title + '&body=' + text + url;
                this.newTab(mail);
                break;

            default:
                break;
        };
    },

    newTab: function(url) {
        var win = window.open(url, '_blank');
        win.focus();
    },

    popupCenter: function(url, title, w, h) {
        var dualScreenLeft = window.screenLeft !== undefined ? window.screenLeft : screen.left;
        var dualScreenTop = window.screenTop !== undefined ? window.screenTop : screen.top;

        var width = window.innerWidth ? window.innerWidth : document.documentElement.clientWidth ? document.documentElement.clientWidth : screen.width;
        var height = window.innerHeight ? window.innerHeight : document.documentElement.clientHeight ? document.documentElement.clientHeight : screen.height;

        var left = ((width / 2) - (w / 2)) + dualScreenLeft;
        var top = ((height / 3) - (h / 3)) + dualScreenTop;

        var newWindow = window.open(url, title, 'scrollbars=yes, width=' + w + ', height=' + h + ', top=' + top + ', left=' + left);

        if (window.focus) {
            newWindow.focus();
        }
    }
};

cubeShare.init();