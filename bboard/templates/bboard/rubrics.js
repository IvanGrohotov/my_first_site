var domain = 'http://localhost:8000/bboard/'

window.onload = function() {
    var list = document.getElementById('list');

    var rubricListLoader = new XMLHttpRequest()
    var rubricUpdater = new XMLHttpRequest()
    rubricUpdater.onreadystatechange = function() {
        if (rubricUpdater.readyState == 4) {
            if ((rubricUpdater.status == 200) || (rubricUpdater.status==201)) {
                rubricListLoad();
                rubricForm.reset();
                id.value = '';       
            }else{
                window.alert(rubricUpdater.statusText);
            }
        }
    }

    var rubricForm = document.getElementById('rubric_form');
    rubricForm.addEventListener('submit', function (evt){
        evt.preventDefault();
        var vid = id.value;
        if (vid) {
            var url = 'api/rubrics/' + vid +'/';
            var method = 'POST';
        } else {
            var url = 'api/rubrics/';
            var method = 'POST';
        }
        data = JSON.stringify({id: vid, name: name.value, order: order.value});
        rubricUpdater.open(method, domain + url, true);
        rubricUpdater.setRequestHeader('Content-Type', 'aplications/json');
        rubricUpdater.send(data);
    })
    function rubricListLoad() {
        rubricUpdater.open('GET', domain + 'api/rubrics/', true);
        rubricUpdater.send();
    }

    rubricListLoad();
}